"""将 subresults 中的题目按领域和策略追加到 results/deepseek-v3.2。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

# 领域名对齐：兼容历史命名。
FIELD_NAME_MAP: Dict[str, str] = {
    "Commonsense&WorldKnowledge": "Commonsense_and_WorldKnowledge",
    "Commonsense_and_WorldKnowledge": "Commonsense_and_WorldKnowledge",
    "Creative&Open-ended_Questions": "Creative_and_Open-ended_Questions",
    "Creative_and_Open-ended_Questions": "Creative_and_Open-ended_Questions",
    "Data&StatisticalLiteracy": "Data_and_StatisticalLiteracy",
    "Data_and_StatisticalLiteracy": "Data_and_StatisticalLiteracy",
    "Lang_Comp&Produc": "Lang_Comp_and_Produc",
    "Lang_Comp_and_Produc": "Lang_Comp_and_Produc",
    "LogicalReasoning": "Logical_Reasoning",
    "Logical_Reasoning": "Logical_Reasoning",
    "MathematicalReasoning": "Mathematical_Reasoning",
    "Mathematical_Reasoning": "Mathematical_Reasoning",
    "Scientific_Inquiry": "Natural_Science",
    "Natural_Science": "Natural_Science",
    "Socialcultural_Understanding": "Sociocultural_Understanding",
    "Sociocultural_Understanding": "Sociocultural_Understanding",
    "Multimodal_Information": "Multimodal_Information",
}

# 策略目录/文件名对齐：subresults 有 Strategy_5_GKP，results 使用 Strategy_5_KGR。
STRATEGY_FILE_MAP: Dict[str, str] = {
    "Strategy_0_CoT": "Strategy_0_CoT.json",
    "Strategy_1_SC": "Strategy_1_SC.json",
    "Strategy_2_ToT": "Strategy_2_ToT.json",
    "Strategy_3_GoT": "Strategy_3_GoT.json",
    "Strategy_4_Auto-CoT": "Strategy_4_Auto-CoT.json",
    "Strategy_5_GKP": "Strategy_5_KGR.json",
    "Strategy_5_KGR": "Strategy_5_KGR.json",
    "Strategy_6_ART": "Strategy_6_ART.json",
    "Strategy_7_ReAct": "Strategy_7_ReAct.json",
    "Strategy_8_APE": "Strategy_8_APE.json",
    "Strategy_9_RAG": "Strategy_9_RAG.json",
}


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _normalize_field(name: str) -> str:
    return FIELD_NAME_MAP.get(name, name)


def _to_strategy_tag(strategy_filename: str) -> str:
    # 例如 Strategy_0_CoT.json -> _0_CoT
    stem = Path(strategy_filename).stem
    prefix = "Strategy"
    if stem.startswith(prefix):
        return stem[len(prefix) :]
    return f"_{stem}"


def _parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="将 subresults 题目追加到 results/deepseek-v3.2")
    parser.add_argument(
        "--source",
        default=None,
        help="源目录（默认: subresults/deepseek）",
    )
    parser.add_argument(
        "--target",
        default=None,
        help="目标目录（默认: results/deepseek-v3.2）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅统计将要追加的数据，不实际写入",
    )
    return parser.parse_args(list(argv))


def append_subresults_to_results(
    source_root: Path,
    target_root: Path,
    *,
    dry_run: bool = False,
) -> Dict[str, int]:
    """按“领域 + 策略”把 subresults.example 追加到 results.questions。"""
    stats = {
        "strategy_dirs": 0,
        "source_files": 0,
        "target_files_written": 0,
        "questions_appended": 0,
        "skipped": 0,
    }

    if not source_root.exists():
        raise FileNotFoundError(f"未找到源目录: {source_root}")

    strategy_dirs: List[Path] = sorted([p for p in source_root.iterdir() if p.is_dir()])

    for strategy_dir in strategy_dirs:
        strategy_name = strategy_dir.name
        target_strategy_file = STRATEGY_FILE_MAP.get(strategy_name)
        if not target_strategy_file:
            print(f"跳过策略目录（未配置映射）: {strategy_name}")
            stats["skipped"] += 1
            continue

        stats["strategy_dirs"] += 1

        for source_file in sorted(strategy_dir.glob("*.json")):
            stats["source_files"] += 1
            try:
                source_data = _load_json(source_file)
                if not isinstance(source_data, dict):
                    print(f"跳过文件（JSON 顶层不是对象）: {source_file}")
                    stats["skipped"] += 1
                    continue

                examples = source_data.get("example")
                if not isinstance(examples, list):
                    print(f"跳过文件（缺少 example 列表）: {source_file}")
                    stats["skipped"] += 1
                    continue

                field_name = _normalize_field(source_file.stem)
                target_field_dir = target_root / field_name
                target_file = target_field_dir / target_strategy_file

                if target_file.exists():
                    target_data = _load_json(target_file)
                    if not isinstance(target_data, dict):
                        print(f"跳过目标文件（JSON 顶层不是对象）: {target_file}")
                        stats["skipped"] += 1
                        continue
                else:
                    # 目标不存在时自动创建，避免丢失 subresults 中独有领域。
                    target_data = {
                        "field": field_name,
                        "strategy": _to_strategy_tag(target_strategy_file),
                        "model_name": "deepseek-v3.2",
                        "questions": [],
                    }

                questions = target_data.get("questions")
                if not isinstance(questions, list):
                    print(f"跳过目标文件（缺少 questions 列表）: {target_file}")
                    stats["skipped"] += 1
                    continue

                # 按用户要求：index 不改，原样直接追加。
                questions.extend(examples)
                target_data["questions"] = questions

                if not dry_run:
                    _dump_json(target_file, target_data)

                stats["target_files_written"] += 1
                stats["questions_appended"] += len(examples)
                print(
                    f"已追加: {source_file} -> {target_file} (新增 {len(examples)} 题)"
                )
            except Exception as exc:  # noqa: BLE001
                print(f"跳过文件: {source_file}，原因: {exc}")
                stats["skipped"] += 1

    return stats


def main(argv: Iterable[str] | None = None) -> int:
    args = _parse_args([] if argv is None else argv)

    repo_root = Path(__file__).resolve().parent.parent
    source_root = Path(args.source) if args.source else (repo_root / "subresults" / "deepseek")
    target_root = Path(args.target) if args.target else (repo_root / "results" / "deepseek-v3.2")

    stats = append_subresults_to_results(source_root, target_root, dry_run=args.dry_run)

    print("\n处理完成:")
    print(f"策略目录数: {stats['strategy_dirs']}")
    print(f"源文件数: {stats['source_files']}")
    print(f"写入目标文件次数: {stats['target_files_written']}")
    print(f"追加题目总数: {stats['questions_appended']}")
    print(f"跳过数: {stats['skipped']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(__import__("sys").argv[1:]))

