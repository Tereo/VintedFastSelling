"""Installer le skill dans ce projet sans remplacer un skill existant.

Le lien .agents/skills est une installation locale, pas une installation mobile.
Ce script n'installe aucun paquet et ne touche pas à la configuration globale.
"""

from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "skills/vinted-prepare-listing"


def matches_source(source, destination):
    """Reconnaître un lien vers la source ou une copie complète non modifiée."""
    source, destination = Path(source).resolve(), Path(destination)
    if not (source / "SKILL.md").is_file():
        return False
    if destination.is_symlink():
        return destination.resolve() == source
    if not destination.is_dir():
        return False

    def contents(directory):
        entries = list(directory.rglob("*"))
        if any(path.is_symlink() for path in entries):
            return None
        return {path.relative_to(directory): path.read_bytes() for path in entries if path.is_file()}

    expected = contents(source)
    return expected is not None and contents(destination) == expected


def install(source, destination, *, copy=False):
    source, destination = Path(source).resolve(), Path(destination)
    if not (source / "SKILL.md").is_file():
        raise ValueError("Source sans SKILL.md ; installation refusée.")
    if os.path.lexists(destination):
        if matches_source(source, destination):
            return destination
        raise FileExistsError(f"Destination existante conservée : {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    if copy:
        shutil.copytree(source, destination)
    else:
        try:
            destination.symlink_to(os.path.relpath(source, destination.parent.resolve()), target_is_directory=True)
        except OSError:
            # Windows peut refuser les liens sans mode développeur ou privilège.
            # Ne jamais remplacer une destination apparue entre-temps.
            if os.path.lexists(destination):
                raise
            shutil.copytree(source, destination)
    if not matches_source(source, destination):
        raise RuntimeError("Installation non vérifiée.")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Vérifier le lien ou la copie sans écrire")
    mode.add_argument("--copy", action="store_true", help="Installer une copie plutôt qu'un lien symbolique")
    args = parser.parse_args()
    destination = ROOT / ".agents/skills/vinted-prepare-listing"
    if args.check:
        if not matches_source(SOURCE, destination):
            raise SystemExit("Le skill est absent ou différent de la source. Relancer l'installation après vérification de la destination.")
    else:
        install(SOURCE, destination, copy=args.copy)
        report = {
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "scope": "local-repository", "path": str(destination), "source": str(SOURCE),
            "installation_method": "symlink" if destination.is_symlink() else "copy",
            "files_sha256": {str(p.relative_to(SOURCE)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(SOURCE.rglob("*")) if p.is_file()},
            "android_installation_verified": False, "vinted_live_test_executed": False
        }
        report_path = ROOT / "livrables/installation-local.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Installation locale vérifiée : {destination}")


if __name__ == "__main__":
    main()
