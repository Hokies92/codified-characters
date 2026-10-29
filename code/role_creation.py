"""Role Creation: validate narrative role blueprints and export codification-ready profiles.

This module is intentionally upstream of parse_by_scene: it does not call an LLM,
claim to infer motives, or generate executable character rules without review.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0"
REQUIRED_TEXT = (
    "role_id", "name", "universe", "narrative_function", "external_role", "lie"
)
REQUIRED_GROUPS = {
    "ghost": ("event", "interpretation"),
    "want": ("objective", "stakes"),
    "need": ("truth", "observable_change"),
    "arc": ("starting_behavior", "pressure_test", "defining_choice"),
}
GATE_FIELDS = ("id", "trigger", "lie_response", "truth_response", "cost")


def load_blueprint(path: str | Path) -> dict[str, Any]:
    """Read a JSON blueprint; reject non-object roots."""
    with Path(path).open(encoding="utf-8") as file:
        blueprint = json.load(file)
    if not isinstance(blueprint, dict):
        raise ValueError("Blueprint root must be a JSON object")
    return blueprint


def validate_blueprint(role: dict[str, Any]) -> list[str]:
    """Return structural errors. A passing result is NOT proof of character quality."""
    errors: list[str] = []
    if role.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION!r}")
    for field in REQUIRED_TEXT:
        if not isinstance(role.get(field), str) or not role[field].strip():
            errors.append(f"{field} must be nonempty text")
    role_id = role.get("role_id")
    if isinstance(role_id, str) and role_id and not re.fullmatch(r"[a-z][a-z0-9_-]*", role_id):
        errors.append("role_id must be a lowercase slug (a-z, 0-9, _ or -)")
    for group, fields in REQUIRED_GROUPS.items():
        value = role.get(group)
        if not isinstance(value, dict):
            errors.append(f"{group} must be an object")
            continue
        for field in fields:
            if not isinstance(value.get(field), str) or not value[field].strip():
                errors.append(f"{group}.{field} must be nonempty text")
    gates = role.get("decision_gates")
    if not isinstance(gates, list) or not gates:
        errors.append("decision_gates must contain at least one gate")
    else:
        seen: set[str] = set()
        for index, gate in enumerate(gates, 1):
            prefix = f"decision_gates[{index}]"
            if not isinstance(gate, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for field in GATE_FIELDS:
                if not isinstance(gate.get(field), str) or not gate[field].strip():
                    errors.append(f"{prefix}.{field} must be nonempty text")
            identifier = gate.get("id")
            if isinstance(identifier, str):
                if identifier in seen:
                    errors.append(f"{prefix}.id must be unique")
                seen.add(identifier)
            a, b = gate.get("lie_response"), gate.get("truth_response")
            if isinstance(a, str) and isinstance(b, str) and a.strip().casefold() == b.strip().casefold():
                errors.append(f"{prefix} must distinguish Lie- and Truth-driven actions")
    for field in ("relationships", "skills", "constraints"):
        value = role.get(field, [])
        if not isinstance(value, list) or any(not isinstance(s, str) or not s.strip() for s in value):
            errors.append(f"{field} must be a list of nonempty strings")
    if isinstance(role.get("lie"), str) and isinstance(role.get("need"), dict):
        truth = role["need"].get("truth")
        if isinstance(truth, str) and role["lie"].strip().casefold() == truth.strip().casefold():
            errors.append("lie and need.truth must be distinguishable")
    return errors


def render_character_profile(role: dict[str, Any]) -> str:
    """Export into the existing paragraph-oriented character codification workflow."""
    errors = validate_blueprint(role)
    if errors:
        raise ValueError("Invalid blueprint:\n- " + "\n- ".join(errors))

    def lines(items: list[str], empty: str = "Not yet specified.") -> str:
        return "\n\n".join(items) if items else empty

    gates = []
    for gate in role["decision_gates"]:
        gates.append(
            f"Decision gate {gate['id']}: When {gate['trigger']}, and the explicitly "
            f"tracked character arc state is PRE_CHANGE, {role['name']} {gate['lie_response']} "
            f"When the explicitly tracked arc state is TRANSFORMED, "
            f"{role['name']} {gate['truth_response']} "
            f"The tradeoff or cost is: {gate['cost']}"
        )
    skills = ", ".join(role.get("skills", [])) or "Not yet specified."
    return (
        f"# Character Profile: {role['name']}\n\n"
        f"**Character Name:** {role['name']}  \n"
        f"**Source / Universe:** {role['universe']}  \n"
        f"**Role:** {role['external_role']}  \n"
        f"**Narrative Function:** {role['narrative_function']}  \n"
        f"**Blueprint ID:** {role['role_id']}\n\n"
        "## Design Provenance (authoring only; do not feed directly to role-play runtime)\n\n"
        f"**Ghost — event:** {role['ghost']['event']}\n\n"
        f"**Ghost — interpretation:** {role['ghost']['interpretation']}\n\n"
        f"**Lie:** {role['lie']}\n\n"
        f"**Want:** {role['want']['objective']} Stakes: {role['want']['stakes']}\n\n"
        f"**Need — truth:** {role['need']['truth']}\n\n"
        f"**Need — observable change:** {role['need']['observable_change']}\n\n"
        "## Personality\n\n"
        f"At the beginning, {role['name']} {role['arc']['starting_behavior']}\n\n"
        f"The pressure that challenges this behavior is: {role['arc']['pressure_test']}\n\n"
        "## Relationships\n\n"
        f"{lines(role.get('relationships', []))}\n\n"
        "## Abilities / Powers / Skills\n\n"
        f"{skills}\n\n"
        "## Decision Heuristics\n\n"
        f"{lines(gates)}\n\n"
        "## Defining Choice\n\n"
        f"{role['arc']['defining_choice']}\n\n"
        "## Probabilistic / Rare Behaviors\n\n"
        "None specified; do not invent probabilities.\n\n"
        "## Hard Constraints (Never Break)\n\n"
        f"{lines(role.get('constraints', []))}\n\n"
        "## Codification Notes\n\n"
        "Each decision gate must be reviewed and turned into scene-conditioned "
        "parse_by_scene functions using the existing prompts/codification_prompts.md. "
        "The execution environment must supply an explicit PRE_CHANGE or TRANSFORMED "
        "arc state; do not infer transformation solely from a scene. "
        "Unknown scene conditions must be treated explicitly. "
        "The design provenance is for authors, not runtime prompt injection.\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create validated role blueprints for character codification")
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("validate", help="Validate a role blueprint JSON file")
    check.add_argument("blueprint", type=Path)
    export = commands.add_parser("export", help="Export a role blueprint to a codification-ready Markdown profile")
    export.add_argument("blueprint", type=Path)
    export.add_argument("--out", required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        role = load_blueprint(args.blueprint)
        errors = validate_blueprint(role)
        if errors:
            print("Invalid role blueprint:\n- " + "\n- ".join(errors))
            return 1
        if args.command == "validate":
            print(f"Valid role blueprint: {role['role_id']} (structural checks only)")
            return 0
        result = render_character_profile(role)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(result, encoding="utf-8")
        print(f"Exported profile to {args.out}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Role creation failed: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
