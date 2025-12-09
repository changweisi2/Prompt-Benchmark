import json
import os

classification_filename = {
    "Fields\MathematicalReasoning.json": [
        0, 1, 2, 4, 7, 8, 9, 12, 15, 16, 17, 18, 20, 21, 23, 24,
        28, 29, 32, 33, 34, 36, 37, 39, 40, 41, 42, 44, 45, 47,
        49, 50, 51, 53, 54, 56, 57, 59, 60, 62, 63, 65, 66, 68,
        69, 71, 72, 74, 75, 77, 78, 80
    ],
    "Fields\LogicalReasoning.json": [
        0, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 19, 22, 25,
        26, 27, 30, 31, 35, 38, 43, 46, 48, 50, 52, 55, 58, 61,
        64, 67, 70, 73, 76, 79
    ],
    "Fields\Lang_Comp_and_Produc.json": [],
    "Fields\Scientific_Inquiry.json": [],
    "Fields\Sociocultural_Understanding.json": [],
    "Fields\Data_and_StatisticalLiteracy.json": [],
    "Fields\Commonsense_and_WorldKnowledge.json": [
        1, 5, 6, 7, 10, 13, 21, 31, 52, 67, 70
    ],
    "Fields\Creative_and_Open-ended_Questions.json": [],
}



source_file = "ObjectiveProblems\2010-2025_Physics_MCQs.json"   # 题目源文件

# -------------------------------
# 1. 读取源 JSON（含 questions 数组）
# -------------------------------
with open(source_file, "r", encoding="utf-8") as f:
    source_data = json.load(f)

source_questions = source_data["questions"]

# 建一个 index → question 映射表
index_map = {q["index"]: q for q in source_questions}

# -------------------------------
# 2. 处理每个分类文件
# -------------------------------
for filename, idx_list in classification_filename.items():

    # ---- 若目标文件不存在 → 创建空模板 ----
    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        empty_content = {"keywords": "", "questions": []}
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(empty_content, f, ensure_ascii=False, indent=4)

    # ---- 读取已有文件 ----
    with open(filename, "r", encoding="utf-8") as f:
        target_data = json.load(f)

    # 若不存在 questions 字段，补一个
    if "questions" not in target_data:
        target_data["questions"] = []

    # ---- 根据 index 追加内容 ----
    for idx in idx_list:
        if idx in index_map:
            target_data["questions"].append(index_map[idx])
        else:
            print(f"[警告] 源文件中找不到 index={idx}")

    # ---- 写回文件（不覆盖已有 questions，只是追加） ----
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(target_data, f, ensure_ascii=False, indent=4)

    print(f"已写入：{filename} 追加 {len(idx_list)} 个题目")


