"""Exécuter la recette simulée hors réseau avec la bibliothèque standard Python."""

from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tests.scenarios import scenarios
from tests.contract_checks import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="Écrire le détail JSON des scénarios et contrôles")
    args = parser.parse_args()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    cases = scenarios()
    if args.report:
        source = ROOT / "skills/vinted-prepare-listing"
        report = {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
            "kind": "offline-contract-simulation", "tests_run": result.testsRun,
            "failures": len(result.failures), "errors": len(result.errors), "successful": result.wasSuccessful(),
            "limits": ["Aucun LLM exécuté par le banc", "Aucune image réellement analysée", "Aucun appel Vinted",
                       "Aucune recette Android ou navigateur réel", "La sémantique libre des textes nécessite une recette humaine"],
            "skill_sha256": {p.relative_to(source).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted(source.rglob("*")) if p.is_file()},
            "scenarios": [{"id": c["id"], "title": c["title"], "requirements": c["requirements"],
                           "expected_errors": c["expected_errors"], "observed_errors": sorted(validate(c))} for c in cases],
            "test_failures": [{"test": str(t), "traceback": trace} for t, trace in result.failures + result.errors]
        }
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Rapport : {args.report.resolve()}")
    print(f"{len(cases)} scénarios fictifs ; aucun essai réel exécuté.")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
