"""Vérifier la découverte du skill par le parseur de Codex, sans lancer de modèle.

Interroger uniquement initialize puis skills/list via le protocole stdio local.
Le serveur Codex peut initialiser ses fichiers d'état dans le profil utilisateur.
"""

from pathlib import Path
from queue import Empty, Queue
from threading import Thread
import argparse
import json
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]


def check(cli, *, timeout=25):
    with tempfile.TemporaryFile() as stderr:
        proc = subprocess.Popen([cli, "app-server"], cwd=ROOT, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=stderr)
        replies = Queue()

        def read_lines():
            # Les sélecteurs ne prennent pas en charge les pipes sous Windows.
            try:
                for line in proc.stdout:
                    replies.put(line)
            finally:
                replies.put(None)

        reader = Thread(target=read_lines, daemon=True)
        reader.start()

        def send(payload):
            try:
                proc.stdin.write((json.dumps(payload) + "\n").encode("utf-8"))
                proc.stdin.flush()
            except (BrokenPipeError, OSError) as exc:
                raise RuntimeError("Serveur Codex arrêté avant réponse.") from exc

        def response(ident):
            deadline = time.monotonic() + timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError(f"Découverte locale sans réponse après {timeout:g} secondes.")
                try:
                    line = replies.get(timeout=remaining)
                except Empty as exc:
                    raise TimeoutError(f"Découverte locale sans réponse après {timeout:g} secondes.") from exc
                if line is None:
                    raise RuntimeError("Serveur Codex arrêté avant réponse ; vérifier ses droits d'accès au profil local.")
                try:
                    value = json.loads(line)
                except (ValueError, UnicodeDecodeError):
                    continue
                if not isinstance(value, dict) or value.get("id") != ident:
                    continue
                if "error" in value or not isinstance(value.get("result"), dict):
                    raise RuntimeError(f"Requête de métadonnées {ident} refusée ou invalide.")
                return value["result"]

        try:
            send({"id": 1, "method": "initialize", "params": {
                "clientInfo": {"name": "vinted-skill-local-check", "version": "0.1.0"}}})
            response(1)
            send({"method": "initialized", "params": {}})
            send({"id": 2, "method": "skills/list", "params": {"cwds": [str(ROOT)], "forceReload": True}})
            entries = response(2).get("data", [])
            expected = (ROOT / ".agents/skills/vinted-prepare-listing/SKILL.md").resolve()
            matches = [s for entry in entries for s in entry.get("skills", [])
                       if s.get("name") == "vinted-prepare-listing" and s.get("scope") == "repo" and s.get("path")
                       and Path(s["path"]).resolve() == expected]
            errors = [e for entry in entries for e in entry.get("errors", []) if e.get("path")
                      and Path(e["path"]).resolve().is_relative_to(expected.parent)]
            proof = {"matches": [{k: s.get(k) for k in ["name", "path", "scope", "enabled", "interface"]} for s in matches],
                     "skill_errors": errors}
            if len(matches) != 1 or not matches[0].get("enabled") or errors:
                raise RuntimeError("Skill absent, dupliqué, désactivé ou invalide : " + json.dumps(proof, ensure_ascii=False))
            return proof
        finally:
            if proc.poll() is None:
                proc.terminate()
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=3)
            reader.join(timeout=1)
            proc.stdin.close()
            proc.stdout.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-cli", default=shutil.which("codex"))
    args = parser.parse_args(argv)
    if not args.codex_cli:
        parser.error("Préciser --codex-cli avec le chemin de Codex.")
    if not (ROOT / ".agents/skills/vinted-prepare-listing/SKILL.md").is_file():
        parser.error("Installer d'abord le skill : python tools/install_local.py")
    try:
        proof = check(args.codex_cli)
    except (OSError, RuntimeError, TimeoutError) as exc:
        parser.exit(1, f"Découverte impossible : {exc}\n")
    report_path = ROOT / "livrables/installation-local.json"
    report = json.loads(report_path.read_text(encoding="utf-8")) if report_path.is_file() else {"scope": "local-repository"}
    report["codex_discovery"] = proof
    report["codex_cli_version"] = subprocess.check_output([args.codex_cli, "--version"], text=True,
                                                        encoding="utf-8", stderr=subprocess.DEVNULL, timeout=10).strip()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(proof, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
