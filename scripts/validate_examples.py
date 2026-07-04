from pathlib import Path
import json
import sys

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]

VALIDATION_TARGETS = [
    {
        "name": "Consciousness Structure Record",
        "schema": ROOT / "schemas" / "consciousness-structure-record.schema.json",
        "example": ROOT / "examples" / "consciousness-structure-record.example.yaml",
    }
]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_target(target: dict) -> bool:
    print(f"[validate] {target['name']}")
    print(f"  schema : {target['schema'].relative_to(ROOT)}")
    print(f"  example: {target['example'].relative_to(ROOT)}")

    schema = load_json(target["schema"])
    example = load_yaml(target["example"])

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(example), key=lambda e: list(e.path))

    if errors:
        print(f"[failed] {target['name']}")
        for error in errors:
            path = ".".join(str(p) for p in error.path) or "<root>"
            print(f"  - path: {path}")
            print(f"    message: {error.message}")
        return False

    print(f"[ok] {target['example'].name} is valid")
    return True


def main() -> int:
    all_valid = True

    for target in VALIDATION_TARGETS:
        if not validate_target(target):
            all_valid = False

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
