"""Une méthode de test indépendante par scénario ; tous les résultats sont inspectés."""

import re
import unittest
from tests.contract_checks import validate
from tests.scenarios import scenarios


class SimulatedContractTests(unittest.TestCase):
    pass


def make_test(case):
    def test(self):
        actual = validate(case)
        expected = set(case["expected_errors"])
        if expected:
            self.assertTrue(expected.issubset(actual),
                            f"{case['id']} — {case['title']}\nAttendu : {expected}\nObtenu : {actual}")
        else:
            self.assertEqual(set(), actual, f"{case['id']} — {case['title']}")
    test.__doc__ = case["title"]
    return test


for scenario in scenarios():
    name = "test_" + re.sub(r"\W+", "_", scenario["id"])
    if hasattr(SimulatedContractTests, name):
        raise RuntimeError(f"Identifiant de test dupliqué : {name}")
    setattr(SimulatedContractTests, name, make_test(scenario))
