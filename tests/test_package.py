from pathlib import Path
from tempfile import TemporaryDirectory
import json
import re
import unittest
from unittest.mock import patch

from tests.contract_checks import CONTRACT, ROOT
from tools.install_local import SOURCE, install, matches_source


class PackageTests(unittest.TestCase):
    def test_simple_frontmatter_and_ui_metadata(self):
        # Le frontmatter de ce paquet est volontairement limité à deux scalaires.
        text = (SOURCE / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        pairs = dict(line.split(": ", 1) for line in match.group(1).splitlines())
        self.assertEqual({"name", "description"}, set(pairs))
        self.assertEqual("vinted-prepare-listing", pairs["name"])
        self.assertLessEqual(len(pairs["description"]), 1024)
        self.assertNotIn("[TODO:", text)
        for line in (SOURCE / "agents/openai.yaml").read_text(encoding="utf-8").splitlines()[1:]:
            _, value = line.strip().split(": ", 1)
            self.assertIsInstance(json.loads(value), str)

    def test_reference_links_are_local_and_exist(self):
        for document in SOURCE.rglob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", document.read_text(encoding="utf-8")):
                path = (document.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(path.is_relative_to(SOURCE.resolve()), target)
                self.assertTrue(path.is_file(), target)

    def test_manifest_discovers_exactly_one_skill(self):
        manifest = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("vinted-prepare-listing", manifest["name"])
        self.assertEqual("https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", manifest["$schema"])
        self.assertEqual([SOURCE / "SKILL.md"], list((ROOT / "skills").glob("*/SKILL.md")))
        self.assertNotIn("mcpServers", manifest)
        self.assertNotIn("hooks", manifest.get("extensions", {}).get("com.openai", {}))

    def test_installed_payload_has_no_executable_dependency(self):
        files = {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob("*") if p.is_file()}
        self.assertEqual(files, {
            "SKILL.md", "agents/openai.yaml", "references/item-fields.md", "references/clothing-and-toys.md",
            "references/pricing.md", "references/browser-workflow.md", "references/validation-contract.json"
        })

    def test_contract_excludes_external_mutations(self):
        self.assertTrue(set(CONTRACT["vinted_actions"]).issubset(CONTRACT["allowed_actions"]))
        self.assertFalse({"publish", "boost", "buy", "delete", "send_message", "republish"} & set(CONTRACT["allowed_actions"]))

    def test_local_install_and_idempotent_reinstall(self):
        with TemporaryDirectory() as temp:
            destination = Path(temp) / ".agents/skills/vinted-prepare-listing"
            install(SOURCE, destination)
            install(SOURCE, destination)
            self.assertTrue(matches_source(SOURCE, destination))
            self.assertEqual((SOURCE / "SKILL.md").read_bytes(), (destination / "SKILL.md").read_bytes())
            self.assertTrue((destination / "references/pricing.md").is_file())

    def test_install_preserves_existing_directory(self):
        with TemporaryDirectory() as temp:
            destination = Path(temp) / "existing"
            destination.mkdir()
            marker = destination / "user-content.txt"
            marker.write_text("à conserver", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                install(SOURCE, destination)
            self.assertEqual("à conserver", marker.read_text(encoding="utf-8"))

    def test_install_preserves_foreign_symlink(self):
        with TemporaryDirectory() as temp:
            destination = Path(temp) / "existing"
            try:
                destination.symlink_to(Path(temp) / "absent")
            except OSError as exc:
                self.skipTest(f"Liens symboliques indisponibles : {exc}")
            with self.assertRaises(FileExistsError):
                install(SOURCE, destination)
            self.assertTrue(destination.is_symlink())

    def test_install_rejects_missing_source(self):
        with TemporaryDirectory() as temp:
            with self.assertRaises(ValueError):
                install(Path(temp) / "absent", Path(temp) / "destination")
            self.assertFalse((Path(temp) / "destination").exists())

    def test_copy_install_is_idempotent_and_preserves_modified_files(self):
        with TemporaryDirectory() as temp:
            destination = Path(temp) / "copy"
            install(SOURCE, destination, copy=True)
            install(SOURCE, destination, copy=True)
            self.assertFalse(destination.is_symlink())
            self.assertTrue(matches_source(SOURCE, destination))
            marker = destination / "SKILL.md"
            marker.write_text("modification locale à conserver", encoding="utf-8")
            self.assertFalse(matches_source(SOURCE, destination))
            with self.assertRaises(FileExistsError):
                install(SOURCE, destination, copy=True)
            self.assertEqual("modification locale à conserver", marker.read_text(encoding="utf-8"))

    def test_copy_fallback_when_symlinks_are_unavailable(self):
        with TemporaryDirectory() as temp:
            destination = Path(temp) / "fallback"
            with patch.object(Path, "symlink_to", side_effect=OSError("Symlink unavailable")):
                install(SOURCE, destination)
            self.assertFalse(destination.is_symlink())
            self.assertTrue(matches_source(SOURCE, destination))

    def test_copy_fallback_between_windows_drives(self):
        with TemporaryDirectory() as temp:
            destination = Path(temp) / "other-drive"
            with patch("tools.install_local.os.path.relpath", side_effect=ValueError("Different drives")):
                install(SOURCE, destination)
            self.assertFalse(destination.is_symlink())
            self.assertTrue(matches_source(SOURCE, destination))


if __name__ == "__main__":
    unittest.main()
