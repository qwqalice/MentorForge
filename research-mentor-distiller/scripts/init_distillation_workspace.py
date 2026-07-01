#!/usr/bin/env python3
"""Create a clean workspace skeleton for scholar-to-mentor distillation."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        raise ValueError("slug is empty after normalization")
    return value


def touch(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scholar", help="Scholar or lab name, e.g. 'Weidi Xie'")
    parser.add_argument("--root", default=".", type=Path, help="Project root for source_materials and mentor-skills")
    parser.add_argument("--slug", help="Override generated scholar slug")
    args = parser.parse_args()

    slug = slugify(args.slug or args.scholar)
    root = args.root.resolve()

    source_root = root / "source_materials" / slug
    skill_root = root / "mentor-skills" / slug

    for directory in [
        source_root / "web",
        source_root / "papers",
        source_root / "publications",
        source_root / "fulltext",
        source_root / "talks",
        source_root / "notes",
        skill_root / "agents",
        skill_root / "references",
        skill_root / "scripts",
    ]:
        directory.mkdir(parents=True, exist_ok=True)

    touch(
        skill_root / "references" / "evidence-snapshot.md",
        f"# {args.scholar} Evidence Snapshot\n\nStatus: scaffold only.\n",
    )
    touch(
        skill_root / "references" / "publication-index.md",
        f"# {args.scholar} Publication Index\n\nStatus: scaffold only.\n",
    )
    touch(
        skill_root / "references" / "research-taste-profile.md",
        f"# {args.scholar} Research Taste Profile\n\nStatus: scaffold only.\n",
    )
    touch(
        skill_root / "references" / "fulltext-distillation.md",
        f"# {args.scholar} Full-Text Distillation\n\nStatus: scaffold only.\n",
    )
    touch(
        skill_root / "references" / "validation.md",
        f"# {args.scholar} Mentor Skill Validation\n\nStatus: not validated yet.\n",
    )

    print(f"Created source workspace: {source_root}")
    print(f"Created mentor workspace: {skill_root}")


if __name__ == "__main__":
    main()
