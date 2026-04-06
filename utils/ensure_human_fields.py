"""Ensure evidence problems contain human grading fields.

This utility adds the following keys to every dict item under `example` in the
specified JSON file, if missing:

- human_analysis
- human_grading_timestamp
- human_score

If a key already exists (even if empty), it is left unchanged.

Typical usage (in-place):
    python utils/ensure_human_fields.py --input evidence/evidence_problems.json

Dry run (no write):
    python utils/ensure_human_fields.py --input evidence/evidence_problems.json --dry-run

Write to another file:
    python utils/ensure_human_fields.py --input evidence/evidence_problems.json --output evidence/evidence_problems.with_human.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, Iterable, List, Tuple


DEFAULT_FIELDS: Dict[str, Any] = {
    "human_analysis": "",
    "human_grading_timestamp": "",
    "human_score": "",
}


def _load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _dump_json(path: str, data: Any) -> None:
    # Keep formatting stable and readable (repo uses ensure_ascii=False, indent=4)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write("\n")


def _resolve_input_path(input_path: str | None) -> str:
    """Resolve input path with sensible fallbacks.

    Resolution order:
    1) Explicit absolute path, if it exists
    2) Explicit relative path from current working directory
    3) Explicit relative path from repository root (parent of this script)
    4) Default evidence path from repository root
    """

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    default_rel = os.path.join("evidence", "evidence_problems.json")

    candidates: List[str] = []

    if input_path:
        if os.path.isabs(input_path):
            candidates.append(input_path)
        else:
            candidates.append(os.path.abspath(input_path))
            candidates.append(os.path.join(repo_root, input_path))
    else:
        candidates.append(os.path.abspath(default_rel))
        candidates.append(os.path.join(repo_root, default_rel))

    checked: List[str] = []
    for c in candidates:
        norm = os.path.abspath(c)
        if norm in checked:
            continue
        checked.append(norm)
        if os.path.exists(norm):
            return norm

    msg = "Input JSON not found. Tried:\n- " + "\n- ".join(checked)
    raise FileNotFoundError(msg)


def ensure_human_fields(
    data: Any,
    *,
    defaults: Dict[str, Any] | None = None,
    strict: bool = False,
) -> Tuple[Any, int, int, List[str]]:
    """Ensure human grading fields exist.

    Returns: (data, changed_count, skipped_non_dict_count, warnings)
    """

    defaults = dict(DEFAULT_FIELDS if defaults is None else defaults)
    warnings: List[str] = []

    if not isinstance(data, dict):
        raise ValueError("Top-level JSON must be an object/dict")

    examples = data.get("example")
    if not isinstance(examples, list):
        raise ValueError('JSON must contain key "example" as a list')

    changed = 0
    skipped_non_dict = 0

    for i, item in enumerate(examples):
        if not isinstance(item, dict):
            skipped_non_dict += 1
            msg = f"example[{i}] is not an object; skipped"
            if strict:
                raise ValueError(msg)
            warnings.append(msg)
            continue

        item_changed = False
        for k, v in defaults.items():
            if k not in item:
                item[k] = v
                item_changed = True

        if item_changed:
            changed += 1

    return data, changed, skipped_non_dict, warnings


def _parse_args(argv: Iterable[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Add missing human grading fields to evidence problems JSON.")
    p.add_argument(
        "--input",
        "-i",
        default=None,
        help="Input JSON path (default: auto-resolve evidence/evidence_problems.json)",
    )
    p.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output JSON path. If omitted, writes in-place to --input.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not write files; only report how many items would change.",
    )
    p.add_argument(
        "--strict",
        action="store_true",
        help="Fail if example contains non-object items.",
    )
    p.add_argument(
        "--set-now",
        action="store_true",
        help="If set, fill missing human_grading_timestamp with current time.",
    )
    p.add_argument(
        "--timestamp-format",
        default="%Y-%m-%d %H:%M:%S",
        help="Datetime format used with --set-now (default: %Y-%m-%d %H:%M:%S)",
    )
    return p.parse_args(list(argv))


def main(argv: List[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)

    input_path = _resolve_input_path(args.input)
    data = _load_json(input_path)

    defaults = dict(DEFAULT_FIELDS)
    if args.set_now:
        defaults["human_grading_timestamp"] = datetime.now().strftime(args.timestamp_format)

    data, changed, skipped_non_dict, warnings = ensure_human_fields(
        data, defaults=defaults, strict=args.strict
    )

    out_path = input_path if args.output is None else args.output

    if args.dry_run:
        print(f"[dry-run] would update {changed} item(s); skipped non-dict: {skipped_non_dict}; output: {out_path}")
        for w in warnings:
            print(f"WARNING: {w}")
        return 0

    _dump_json(out_path, data)

    print(f"updated {changed} item(s); skipped non-dict: {skipped_non_dict}; wrote: {out_path}")
    for w in warnings:
        print(f"WARNING: {w}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

