"""将 subresults 中的领域命名对齐为 core/Fields.py 中的标准命名。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

# 以 results/core 的命名为准，将 subresults 中的历史命名映射到标准命名。
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


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _dump_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.write("\n")


def _normalize_field(name: str) -> str:
    """将字段名归一化；不在映射中的名称保持原样。"""
    return FIELD_NAME_MAP.get(name, name)


def _process_one_file(path: Path) -> Tuple[bool, bool, str, str]:
    """处理单个 JSON 文件。

    返回：
    - changed_json: 是否改写了 JSON 内容
    - renamed_file: 是否重命名了文件
    - old_name: 旧文件 stem
    - new_name: 新文件 stem
    """
    data = _load_json(path)
    if not isinstance(data, dict):
        return False, False, path.stem, path.stem

    old_stem = path.stem
    new_stem = _normalize_field(old_stem)

    changed_json = False

    # 顶层字段历史上使用了 category，这里按标准字段名更新其值。
    if isinstance(data.get("category"), str):
        old_category = data["category"]
        new_category = _normalize_field(old_category)
        if new_category != old_category:
            data["category"] = new_category
            changed_json = True

    # 兼容可能存在的 field 字段，保持与标准命名一致。
    if isinstance(data.get("field"), str):
        old_field = data["field"]
        new_field = _normalize_field(old_field)
        if new_field != old_field:
            data["field"] = new_field
            changed_json = True

    if changed_json:
        _dump_json(path, data)

    renamed_file = False
    if new_stem != old_stem:
        new_path = path.with_name(f"{new_stem}{path.suffix}")
        if new_path.exists():
            raise FileExistsError(f"目标文件已存在，无法重命名：{new_path}")
        path.rename(new_path)
        renamed_file = True

    return changed_json, renamed_file, old_stem, new_stem


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    subresults_dir = repo_root / "subresults"

    if not subresults_dir.exists():
        print(f"未找到目录：{subresults_dir}")
        return 1

    json_files = sorted(subresults_dir.rglob("*.json"))
    updated_json = 0
    renamed_files = 0
    skipped = 0

    for file_path in json_files:
        try:
            changed_json, renamed_file, old_name, new_name = _process_one_file(file_path)
            if changed_json:
                updated_json += 1
            if renamed_file:
                renamed_files += 1
                print(f"已重命名：{old_name}.json -> {new_name}.json")
        except Exception as exc:  # noqa: BLE001
            skipped += 1
            print(f"跳过文件：{file_path}，原因：{exc}")

    print("\n处理完成：")
    print(f"扫描文件数：{len(json_files)}")
    print(f"更新 JSON 内容数：{updated_json}")
    print(f"重命名文件数：{renamed_files}")
    print(f"跳过文件数：{skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

