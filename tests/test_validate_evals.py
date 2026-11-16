"""Unit tests for the behavioral eval definition validator."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_evals import validate_document  # noqa: E402


class ValidateEvalsTests(unittest.TestCase):
    """Check valid evals and common malformed definitions."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.document = json.loads((ROOT / "tests" / "evals" / "cases.json").read_text(encoding="utf-8"))

    def test_repository_eval_definitions_are_valid(self) -> None:
        self.assertEqual(validate_document(self.document, ROOT), [])

    def test_rejects_unknown_skill_directory(self) -> None:
        document = copy.deepcopy(self.document)
        document["skills"]["missing-skill"] = document["skills"].pop("interview")
        errors = validate_document(document, ROOT)
        self.assertTrue(any("canonical skills/missing-skill/SKILL.md" in error for error in errors))

    def test_rejects_missing_behavior_scenario(self) -> None:
        document = copy.deepcopy(self.document)
        document["skills"]["interview"]["scenarios"].pop()
        errors = validate_document(document, ROOT)
        self.assertTrue(any("expected exactly 3 scenarios" in error for error in errors))

    def test_rejects_incomplete_activation_coverage(self) -> None:
        document = copy.deepcopy(self.document)
        document["skills"]["make-theme"]["activation"]["should_not_activate"].pop()
        errors = validate_document(document, ROOT)
        self.assertTrue(any("should_not_activate: expected exactly 5" in error for error in errors))

    def test_rejects_duplicate_case_id(self) -> None:
        document = copy.deepcopy(self.document)
        scenarios = document["skills"]["panduan-brand"]["scenarios"]
        scenarios[1]["id"] = scenarios[0]["id"]
        errors = validate_document(document, ROOT)
        self.assertTrue(any("duplicate id" in error for error in errors))

    def test_rejects_missing_grading_criteria(self) -> None:
        document = copy.deepcopy(self.document)
        document["skills"]["plans-prototype"]["scenarios"][0]["must"] = []
        errors = validate_document(document, ROOT)
        self.assertTrue(any(".must: non-empty list" in error for error in errors))

    def test_rejects_non_object_root(self) -> None:
        self.assertEqual(validate_document([]), ["root JSON value must be an object"])


if __name__ == "__main__":
    unittest.main()
