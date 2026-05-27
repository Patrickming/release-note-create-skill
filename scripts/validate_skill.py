#!/usr/bin/env python3
"""Validate the repository's Cursor skill metadata."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
MAX_DESCRIPTION_LENGTH = 1024
MAX_BODY_LINES = 500


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter.")

    try:
        end_index = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("SKILL.md frontmatter must end with a closing --- line.") from exc

    metadata: dict[str, str] = {}
    for line in lines[1:end_index]:
        if not line.strip():
            continue
        if ":" not in line:
            raise ValueError(f"Invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")

    body = "\n".join(lines[end_index + 1 :])
    return metadata, body


def validate(path: Path) -> list[str]:
    errors: list[str] = []

    if not path.exists():
        return [f"{path} does not exist."]

    text = path.read_text(encoding="utf-8")
    try:
        metadata, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)]

    name = metadata.get("name", "")
    description = metadata.get("description", "")

    if not name:
        errors.append("Missing required frontmatter field: name.")
    elif not NAME_RE.fullmatch(name):
        errors.append("Field 'name' must use lowercase letters, numbers, and hyphens only, max 64 chars.")

    if not description:
        errors.append("Missing required frontmatter field: description.")
    elif len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(f"Field 'description' must be at most {MAX_DESCRIPTION_LENGTH} chars.")

    body_lines = body.splitlines()
    if len(body_lines) > MAX_BODY_LINES:
        errors.append(f"SKILL.md body should stay under {MAX_BODY_LINES} lines; found {len(body_lines)}.")

    if "# " not in body:
        errors.append("SKILL.md should include a top-level heading.")

    return errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("release-note-create/SKILL.md")
    errors = validate(path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {path} is a valid Cursor skill.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
