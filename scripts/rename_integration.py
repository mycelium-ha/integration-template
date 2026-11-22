#!/usr/bin/env python3
"""Turn the template into your integration in one step.

Renames the `my_integration` package and replaces every template name:

    python3 scripts/rename_integration.py <domain> "<Name>" <repository>

Example:

    python3 scripts/rename_integration.py acme_lamp "Acme Lamp" acme-lamp

Run it once, right after creating the repository from the template, then delete it.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {".py", ".json", ".toml", ".yaml", ".yml", ".md", ".txt", ""}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".mypy_cache", ".ruff_cache", ".pytest_cache"}


def main() -> int:
    """Rename the template."""
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    domain, name, repository = sys.argv[1:]
    if not re.fullmatch(r"[a-z][a-z0-9_]*", domain):
        print(f"Invalid domain {domain!r}: use lowercase letters, digits and underscores")
        return 2

    class_prefix = "".join(part.capitalize() for part in domain.split("_"))
    replacements = [
        ("mycelium-ha/integration-template", f"mycelium-ha/{repository}"),
        ("my-integration", repository),
        ("my_integration", domain),
        ("MyIntegration", class_prefix),
        ("My Integration", name),
    ]

    old_package = ROOT / "custom_components" / "my_integration"
    if not old_package.is_dir():
        print("custom_components/my_integration not found; already renamed?")
        return 1

    this_script = Path(__file__).resolve()
    for path in sorted(ROOT.rglob("*")):
        if (
            not path.is_file()
            or path.resolve() == this_script
            or SKIP_DIRS & set(path.relative_to(ROOT).parts)
            or path.suffix not in TEXT_SUFFIXES
        ):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # binary file such as .coverage
        new_text = text
        for old, new in replacements:
            new_text = new_text.replace(old, new)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")

    old_package.rename(ROOT / "custom_components" / domain)
    print(f"renamed custom_components/my_integration -> custom_components/{domain}")

    # New names change import order and line lengths.
    if shutil.which("ruff"):
        subprocess.run(["ruff", "check", "--fix", "--quiet", str(ROOT)], check=False)
        subprocess.run(["ruff", "format", "--quiet", str(ROOT)], check=False)
    else:
        print("ruff not found: run `ruff check --fix . && ruff format .` after installing it")
    print(f"\nDone. Delete scripts/{this_script.name} and work through the README checklist.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
