"""Régressions sur un clonage neuf et le protocole local, sans compte ni réseau."""

from contextlib import redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import io
import json
import os
import shutil
import subprocess
import sys
import unittest

from tests.contract_checks import ROOT
from tools import verify_discovery


class CleanCheckoutTests(unittest.TestCase):
    def test_install_from_clean_checkout_creates_utf8_report(self):
        with TemporaryDirectory() as temp:
            checkout = Path(temp) / "projet partagé"
            checkout.mkdir()
            for directory in ("tools", "skills"):
                shutil.copytree(ROOT / directory, checkout / directory,
                                ignore=shutil.ignore_patterns("__pycache__"))
            self.assertFalse((checkout / "livrables").exists())
            command = [sys.executable, str(checkout / "tools/install_local.py")]
            options = {"cwd": temp, "capture_output": True, "text": True, "encoding": "utf-8",
                       "env": {**os.environ, "PYTHONIOENCODING": "utf-8"}, "timeout": 10}
            for arguments in (["--copy"], ["--copy"], ["--check"]):
                result = subprocess.run(command + arguments, **options)
                self.assertEqual(0, result.returncode, result.stderr)
            report = json.loads((checkout / "livrables/installation-local.json").read_text(encoding="utf-8"))
            self.assertEqual("copy", report["installation_method"])
            self.assertEqual((checkout / ".agents/skills/vinted-prepare-listing").resolve(), Path(report["path"]).resolve())
            self.assertFalse(report["vinted_live_test_executed"])


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / ".agents/skills/vinted-prepare-listing/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("skill fictif", encoding="utf-8")
        self.processes = []

    def tearDown(self):
        running = [proc for proc in self.processes if proc.poll() is None]
        for proc in running:
            proc.kill()
            proc.wait(timeout=3)
        self.assertFalse(running, "Le contrôle a laissé un processus actif.")

    def entry(self, **overrides):
        return {"name": "vinted-prepare-listing", "path": str(self.skill), "scope": "repo",
                "enabled": True, "interface": {"displayName": "Préparer une annonce"}, **overrides}

    def run_server(self, skills=None, *, errors=None, mode="normal", initialize=None, timeout=3):
        responses = {1: initialize if initialize is not None else {"id": 1, "result": {}},
                     2: {"id": 2, "result": {"data": [{"skills": skills if skills is not None else [self.entry()],
                                                       "errors": errors or []}]}}}
        script = self.root / "fake_server.py"
        script.write_text(
            "import json, sys\n"
            f"responses = {responses!r}\nmode = {mode!r}\n"
            "for line in sys.stdin.buffer:\n"
            "    request = json.loads(line)\n"
            "    if 'id' not in request:\n        continue\n"
            "    if mode == 'eof':\n        sys.exit(0)\n"
            "    if mode == 'silence':\n        continue\n"
            "    sys.stdout.buffer.write(b'not json\\n[]\\n')\n"
            "    sys.stdout.buffer.write((json.dumps(responses[request['id']]) + '\\n').encode('utf-8'))\n"
            "    sys.stdout.buffer.flush()\n", encoding="utf-8")
        real_popen = subprocess.Popen

        def launch(command, **kwargs):
            proc = real_popen([sys.executable, str(script), *command[1:]], **kwargs)
            self.processes.append(proc)
            return proc

        with patch.object(verify_discovery, "ROOT", self.root), \
                patch.object(verify_discovery.subprocess, "Popen", side_effect=launch):
            return verify_discovery.check("fake-codex", timeout=timeout)

    def test_local_skill_with_protocol_noise_is_accepted(self):
        proof = self.run_server()
        self.assertEqual(str(self.skill), proof["matches"][0]["path"])

    def test_same_name_from_another_installation_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "Skill absent"):
            self.run_server([self.entry(path=str(self.root / "other/SKILL.md"))])

    def test_disabled_or_duplicate_local_skill_is_rejected(self):
        for skills in ([self.entry(enabled=False)], [self.entry(), self.entry()], [self.entry(scope="user")]):
            with self.subTest(skills=skills), self.assertRaises(RuntimeError):
                self.run_server(skills)

    def test_local_parse_error_is_rejected(self):
        with self.assertRaises(RuntimeError):
            self.run_server(errors=[{"path": str(self.skill), "message": "frontmatter invalide"}])

    def test_unrelated_parse_error_does_not_invalidate_project_skill(self):
        proof = self.run_server(errors=[{"path": str(self.root / "other/SKILL.md"), "message": "autre skill"}])
        self.assertEqual([], proof["skill_errors"])

    def test_invalid_or_refused_response_is_reported(self):
        for response in ({"id": 1, "result": []}, {"id": 1, "error": {"code": -1}}):
            with self.subTest(response=response), self.assertRaisesRegex(RuntimeError, "refusée ou invalide"):
                self.run_server(initialize=response)

    def test_early_exit_is_reported_and_process_is_reaped(self):
        with self.assertRaisesRegex(RuntimeError, "arrêté avant réponse"):
            self.run_server(mode="eof")

    def test_unresponsive_server_times_out_and_is_reaped(self):
        with self.assertRaises(TimeoutError):
            self.run_server(mode="silence", timeout=0.2)

    def test_discovery_can_recreate_a_missing_report(self):
        proof = {"matches": [self.entry()], "skill_errors": []}
        with patch.object(verify_discovery, "ROOT", self.root), \
                patch.object(verify_discovery, "check", return_value=proof), \
                patch.object(verify_discovery.subprocess, "check_output", return_value="codex test\n"), \
                redirect_stdout(io.StringIO()):
            verify_discovery.main(["--codex-cli", "fake-codex"])
        report = json.loads((self.root / "livrables/installation-local.json").read_text(encoding="utf-8"))
        self.assertEqual(proof, report["codex_discovery"])


if __name__ == "__main__":
    unittest.main()
