"""将 results 目录下的题目按 index 排序并回写。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def _load_json(path: Path) -> Any:
    """读取 JSON 文件。"""
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _dump_json(path: Path, data: Any) -> None:
    """写回 JSON，保持可读格式并在末尾补换行。"""
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _index_sort_key(item: Dict[str, Any]) -> tuple[int, int | str]:
    """排序键：有合法数字 index 的题目优先，非法/缺失 index 放末尾。"""
    value = item.get("index")
    if isinstance(value, bool):
        return (1, str(value))
    if isinstance(value, int):
        return (0, value)
    if isinstance(value, float):
        return (0, int(value))
    if isinstance(value, str):
        try:
            return (0, int(value))
        except ValueError:
            return (1, value)
    return (1, str(value))


def _sort_one_file(path: Path) -> tuple[bool, int]:
    """对单个 JSON 文件执行排序，返回(是否写回, 题目数量)。"""
    data = _load_json(path)
    if not isinstance(data, dict):
        return False, 0

    questions = data.get("questions")
    if not isinstance(questions, list):
        return False, 0

    # 仅处理字典题目，避免因异常数据中断整个批处理。
    dict_questions = [q for q in questions if isinstance(q, dict)]
    if len(dict_questions) != len(questions):
        return False, len(questions)

    sorted_questions = sorted(questions, key=_index_sort_key)
    if sorted_questions == questions:
        return False, len(questions)

    data["questions"] = sorted_questions
    _dump_json(path, data)
    return True, len(questions)


def main() -> int:
    # 以仓库根目录为基准，固定处理 results 目录。
    repo_root = Path(__file__).resolve().parent.parent
    results_dir = repo_root / "results"

    if not results_dir.exists():
        print(f"未找到目录：{results_dir}")
        return 1

    json_files: List[Path] = sorted(results_dir.rglob("*.json"))
    scanned = len(json_files)
    updated = 0
    skipped = 0
    total_questions = 0

    for file_path in json_files:
        try:
            changed, count = _sort_one_file(file_path)
            total_questions += count
            if changed:
                updated += 1
                print(f"已排序并写回：{file_path}")
            else:
                skipped += 1
        except Exception as exc:  # noqa: BLE001
            skipped += 1
            print(f"跳过文件（读取或解析失败）：{file_path}，原因：{exc}")

    print("\n处理完成：")
    print(f"扫描 JSON 文件数：{scanned}")
    print(f"写回文件数：{updated}")
    print(f"跳过文件数：{skipped}")
    print(f"统计到的题目总数：{total_questions}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
