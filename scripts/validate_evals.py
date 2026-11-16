#!/usr/bin/env python3
"""Validate the repository's behavioral evaluation definitions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVALS = ROOT / "tests" / "evals" / "cases.json"
REQUIRED_SCENARIO_KINDS = {"happy_path", "edge_case", "adversarial"}


def validate_document(document: Any, root: Path = ROOT) -> list[str]:
    """Return validation errors for an evaluation document.

    Args:
        document: Parsed JSON evaluation document.
        root: Repository root used to resolve canonical skill directories.

    Returns:
        A list of human-readable validation errors. An empty list means valid.
    """
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["root JSON value must be an object"]
    if document.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    skills = document.get("skills")
    if not isinstance(skills, dict) or not skills:
        return errors + ["skills must be a non-empty object"]

    canonical_skills = {
        path.name for path in (root / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    } if (root / "skills").is_dir() else set()
    if set(skills) != canonical_skills:
        missing = sorted(canonical_skills - set(skills))
        unknown = sorted(set(skills) - canonical_skills)
        errors.append(f"skills coverage mismatch: missing={missing}, unknown={unknown}")

    for skill_name, skill_data in skills.items():
        prefix = f"skills.{skill_name}"
        skill_file = root / "skills" / skill_name / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"{prefix}: canonical skills/{skill_name}/SKILL.md does not exist")
        if not isinstance(skill_data, dict):
            errors.append(f"{prefix}: value must be an object")
            continue

        scenarios = skill_data.get("scenarios")
        if not isinstance(scenarios, list) or len(scenarios) != 3:
            errors.append(f"{prefix}.scenarios: expected exactly 3 scenarios")
            scenarios = []

        seen_ids: set[str] = set()
        seen_kinds: set[str] = set()
        for index, scenario in enumerate(scenarios):
            scenario_prefix = f"{prefix}.scenarios[{index}]"
            if not isinstance(scenario, dict):
                errors.append(f"{scenario_prefix}: value must be an object")
                continue
            case_id = scenario.get("id")
            if not isinstance(case_id, str) or not case_id.strip():
                errors.append(f"{scenario_prefix}.id: non-empty string required")
            elif case_id in seen_ids:
                errors.append(f"{scenario_prefix}.id: duplicate id {case_id!r}")
            else:
                seen_ids.add(case_id)
            kind = scenario.get("kind")
            if kind not in REQUIRED_SCENARIO_KINDS:
                errors.append(f"{scenario_prefix}.kind: must be one of {sorted(REQUIRED_SCENARIO_KINDS)}")
            else:
                if kind in seen_kinds:
                    errors.append(f"{scenario_prefix}.kind: duplicate scenario kind {kind!r}")
                seen_kinds.add(kind)
            prompt = scenario.get("prompt")
            if not isinstance(prompt, str) or not prompt.strip():
                errors.append(f"{scenario_prefix}.prompt: non-empty string required")
            for criterion_key in ("must", "must_not"):
                criteria = scenario.get(criterion_key)
                if not isinstance(criteria, list) or not criteria or any(
                    not isinstance(item, str) or not item.strip() for item in criteria
                ):
                    errors.append(f"{scenario_prefix}.{criterion_key}: non-empty list of strings required")
        if seen_kinds != REQUIRED_SCENARIO_KINDS:
            errors.append(f"{prefix}.scenarios: must cover {sorted(REQUIRED_SCENARIO_KINDS)}")

        activation = skill_data.get("activation")
        if not isinstance(activation, dict):
            errors.append(f"{prefix}.activation: object required")
            continue
        activation_prompts: list[str] = []
        for activation_key in ("should_activate", "should_not_activate"):
            prompts = activation.get(activation_key)
            if not isinstance(prompts, list) or len(prompts) != 5 or any(
                not isinstance(item, str) or not item.strip() for item in prompts
            ):
                errors.append(f"{prefix}.activation.{activation_key}: expected exactly 5 non-empty prompts")
            elif isinstance(prompts, list):
                activation_prompts.extend(prompts)
        if len(activation_prompts) != len(set(activation_prompts)):
            errors.append(f"{prefix}.activation: duplicate activation prompt")

    return errors


def main() -> int:
    """Run the eval-definition validator."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, default=DEFAULT_EVALS, help="Path to the eval JSON file")
    args = parser.parse_args()

    try:
        document = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL {args.path}: {exc}", file=sys.stderr)
        return 1

    errors = validate_document(document)
    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1

    skill_count = len(document["skills"])
    scenario_count = sum(len(item["scenarios"]) for item in document["skills"].values())
    trigger_count = sum(
        len(item["activation"]["should_activate"]) + len(item["activation"]["should_not_activate"])
        for item in document["skills"].values()
    )
    print(f"EVAL DEFINITIONS OK: {skill_count} skills, {scenario_count} scenarios, {trigger_count} activation prompts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
