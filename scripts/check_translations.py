#!/usr/bin/env python3
"""Check `strings.json` against every locale file in `translations/`.

Finds the integration in `custom_components/` and reports, per locale:
- missing keys (in strings.json, not in the locale)
- orphaned keys (in the locale, not in strings.json)
- placeholder mismatches (`{name}` sets differ from strings.json)

`translations/en.json` is required. Exit code 1 on any finding.
Usage: python3 scripts/check_translations.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = re.compile(r"(?<!\{)\{([a-zA-Z0-9_]+)\}(?!\})")


def flatten(data: Any, prefix: str = "") -> dict[str, str]:
    """Flatten nested translation dicts into dotted keys."""
    if not isinstance(data, dict):
        return {prefix: str(data)}
    out: dict[str, str] = {}
    for key, value in data.items():
        out.update(flatten(value, f"{prefix}.{key}" if prefix else key))
    return out


def load(path: Path) -> dict[str, str]:
    """Load and flatten one JSON file."""
    return flatten(json.loads(path.read_text(encoding="utf-8")))


def check_component(component: Path) -> list[str]:
    """Return all findings for one integration directory."""
    source = load(component / "strings.json")
    locale_files = sorted((component / "translations").glob("*.json"))
    findings: list[str] = []
    if not any(path.stem == "en" for path in locale_files):
        findings.append(f"{component.name}: translations/en.json is missing")

    for path in locale_files:
        data = load(path)
        locale = f"{component.name}/{path.stem}"
        findings += [f"{locale}: missing {key}" for key in sorted(source.keys() - data.keys())]
        findings += [f"{locale}: orphaned {key}" for key in sorted(data.keys() - source.keys())]
        findings += [
            f"{locale}: placeholder mismatch {key}"
            for key in sorted(source.keys() & data.keys())
            if set(PLACEHOLDER.findall(source[key])) != set(PLACEHOLDER.findall(data[key]))
        ]
        print(f"[{locale}] {len(data)} keys")
    return findings


def main() -> int:
    """Check every integration below custom_components/."""
    components = sorted(path.parent for path in ROOT.glob("custom_components/*/strings.json"))
    if not components:
        print("No custom_components/*/strings.json found")
        return 1
    findings = [finding for component in components for finding in check_component(component)]
    for finding in findings:
        print(f"    {finding}")
    print("FAIL" if findings else "OK: all locales in sync with strings.json")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
