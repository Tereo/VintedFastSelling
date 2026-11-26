"""Vérifier les livrables importables, sans compte Claude/ChatGPT ni réseau."""

from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unittest

from tests.contract_checks import ROOT
from tools.build_packages import (
    CLAUDE_ARCHIVE, INSTRUCTIONS, NAME, PLUGIN_ARCHIVE, PUBLISHED_INSTRUCTIONS,
    build_packages, check_sources,
)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "projet partagé"
        self.root.mkdir()
        for directory in ("skills", ".claude-plugin", "tools"):
            shutil.copytree(ROOT / directory, self.root / directory,
                            ignore=shutil.ignore_patterns("__pycache__"))
        for filename in ("plugin.json", "LICENSE"):
            shutil.copy2(ROOT / filename, self.root / filename)
        self.output = Path(self.temp.name) / "paquets"
        self.skill = self.root / f"skills/{NAME}"

    def build(self):
        return build_packages(self.root, self.output)

    def test_claude_import_has_one_root_skill_with_original_resources(self):
        self.build()
        with ZipFile(self.output / CLAUDE_ARCHIVE) as archive:
            expected = {f"{NAME}/{p.relative_to(self.skill).as_posix()}": p.read_bytes()
                        for p in self.skill.rglob("*") if p.is_file()}
            expected[f"{NAME}/LICENSE"] = (self.root / "LICENSE").read_bytes()
            self.assertEqual(set(expected), set(archive.namelist()))
            self.assertIn(f"{NAME}/SKILL.md", archive.namelist())
            for path, content in expected.items():
                self.assertEqual(content, archive.read(path), path)

    def test_plugin_import_contains_both_manifests_and_the_same_skill(self):
        self.build()
        with ZipFile(self.output / PLUGIN_ARCHIVE) as archive:
            self.assertIn("plugin.json", archive.namelist())
            self.assertIn(".claude-plugin/plugin.json", archive.namelist())
            self.assertIn("LICENSE", archive.namelist())
            self.assertGreater(len(archive.read("README.md").decode("utf-8").split()), 40)
            for relative in ("plugin.json", ".claude-plugin/plugin.json"):
                self.assertEqual((self.root / relative).read_bytes(), archive.read(relative))
            for path in self.skill.rglob("*"):
                if path.is_file():
                    self.assertEqual(path.read_bytes(), archive.read(path.relative_to(self.root).as_posix()))

    def test_document_is_self_contained_and_identical_to_the_mobile_export(self):
        self.build()
        content = (self.output / INSTRUCTIONS).read_text(encoding="utf-8")
        self.assertEqual(content, (self.root / PUBLISHED_INSTRUCTIONS).read_text(encoding="utf-8"))
        anchors = re.findall(r'<a id="([^"]+)"></a>', content)
        self.assertEqual(6, len(anchors))
        self.assertEqual(len(anchors), len(set(anchors)))
        targets = re.findall(r"\]\(([^)]+)\)", content)
        self.assertTrue(targets)
        for target in targets:
            self.assertTrue(target.startswith("#"), target)
            self.assertIn(target[1:], anchors)
        contract_text = re.search(r"```json\n(.*?)\n```", content, re.DOTALL).group(1)
        self.assertEqual(json.loads((self.skill / "references/validation-contract.json").read_text(encoding="utf-8")),
                         json.loads(contract_text))

    def test_generation_excludes_unlisted_local_files_and_preserves_sources(self):
        for relative in (".env", "photos/article.jpg", "skills/vinted-prepare-listing/notes-privees.txt"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"donnee locale fictive a exclure")
        before = {p.relative_to(self.skill): p.read_bytes() for p in self.skill.rglob("*") if p.is_file()}
        self.build()
        for name in (CLAUDE_ARCHIVE, PLUGIN_ARCHIVE):
            with ZipFile(self.output / name) as archive:
                for path in archive.namelist():
                    self.assertFalse(PurePosixPath(path).is_absolute())
                    self.assertNotIn("..", PurePosixPath(path).parts)
                    self.assertNotIn(b"donnee locale fictive a exclure", archive.read(path))
        self.assertEqual(before, {p.relative_to(self.skill): p.read_bytes()
                                  for p in self.skill.rglob("*") if p.is_file()})

    def test_archives_and_checksums_are_reproducible(self):
        paths = self.build()
        original = {p.name: p.read_bytes() for p in paths}
        for path in self.skill.rglob("*"):
            if path.is_file():
                os.utime(path, (1000000000, 1000000000))
        self.assertEqual(original, {p.name: p.read_bytes() for p in self.build()})
        for line in original["SHA256SUMS"].decode("utf-8").splitlines():
            checksum, name = line.split("  ", 1)
            self.assertEqual(checksum, hashlib.sha256(original[name]).hexdigest())

    def test_missing_reference_fails_before_creating_outputs(self):
        (self.skill / "references/pricing.md").unlink()
        with self.assertRaisesRegex(ValueError, "requis absent"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_unbundled_reference_cannot_produce_an_incomplete_document(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nLire [autre règle](references/absent.md).\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Référence absente"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_manifest_drift_is_rejected_before_creating_outputs(self):
        path = self.root / ".claude-plugin/plugin.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["version"] = "99.0.0"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "incohérents : version"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_symlink_in_a_required_resource_is_rejected(self):
        path = self.skill / "references/pricing.md"
        path.unlink()
        outside = Path(self.temp.name) / "fichier-local.txt"
        outside.write_text("fichier local fictif", encoding="utf-8")
        try:
            path.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"Liens symboliques indisponibles : {exc}")
        with self.assertRaisesRegex(ValueError, "Lien symbolique refusé"):
            self.build()
        self.assertFalse(self.output.exists())

    def test_stale_mobile_document_is_detected_without_rewriting_it(self):
        self.build()
        check_sources(self.root)
        published = self.root / PUBLISHED_INSTRUCTIONS
        before = published.read_bytes()
        path = self.skill / "references/pricing.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nPrécision de test.\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "périmé"):
            check_sources(self.root)
        self.assertEqual(before, published.read_bytes())

    def test_clean_checkout_cli_builds_and_checks_from_another_directory(self):
        command = [sys.executable, str(self.root / "tools/build_packages.py")]
        options = {"cwd": self.temp.name, "capture_output": True, "text": True, "encoding": "utf-8",
                   "env": {**os.environ, "PYTHONIOENCODING": "utf-8"}, "timeout": 10}
        for arguments in ([], ["--check"]):
            result = subprocess.run(command + arguments, **options)
            self.assertEqual(0, result.returncode, result.stderr)
        self.assertTrue((self.root / "dist" / CLAUDE_ARCHIVE).is_file())
        self.assertTrue((self.root / "dist" / PLUGIN_ARCHIVE).is_file())

    def test_committed_mobile_document_matches_current_sources(self):
        check_sources(ROOT)


if __name__ == "__main__":
    unittest.main()
