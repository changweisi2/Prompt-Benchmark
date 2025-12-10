import json
import os


# Physics Objective 

# classification_filename = {
#     "Fields\Mathematical_Reasoning.json": [
#         0, 1, 2, 4, 7, 8, 9, 12, 15, 16, 17, 18, 20, 21, 23, 24,
#         28, 29, 32, 33, 34, 36, 37, 39, 40, 41, 42, 44, 45, 47,
#         49, 50, 51, 53, 54, 56, 57, 59, 60, 62, 63, 65, 66, 68,
#         69, 71, 72, 74, 75, 77, 78, 80
#     ],
#     "Fields\Logical_Reasoning.json": [
#         0, 2, 3, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 19, 22, 25,
#         26, 27, 30, 31, 35, 38, 43, 46, 48, 50, 52, 55, 58, 61,
#         64, 67, 70, 73, 76, 79
#     ],
#     "Fields\Lang_Comp_and_Produc.json": [],
#     "Fields\Natural_Science.json": [],
#     "Fields\Sociocultural_Understanding.json": [],
#     "Fields\Data_and_StatisticalLiteracy.json": [],
#     "Fields\Commonsense_and_WorldKnowledge.json": [
#         1, 5, 6, 7, 10, 13, 21, 31, 52, 67, 70
#     ],
#     "Fields\Creative_and_Open-ended_Questions.json": [],
# }

# Chemistry Objective 

# classification_filename = {
#     "Fields\Mathematical_Reasoning.json": [
#     1, 2, 4, 5, 6, 9, 10, 11, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142
#     ],
#     "Fields\Logical_Reasoning.json": [
#     0, 3, 7, 8, 12, 13, 19, 33, 34, 51, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142
#     ],
#     "Fields\Lang_Comp_and_Produc.json": [],
#     "Fields\Natural_Science.json": [
#     ],
#     "Fields\Sociocultural_Understanding.json": [],
#     "Fields\Data_and_StatisticalLiteracy.json": [],
#     "Fields\Commonsense_and_WorldKnowledge.json": [
#         19, 37, 46, 61, 71, 85, 89, 95, 100, 104, 106, 110, 113, 116, 119, 124, 128, 131, 133, 136
#     ],
#     "Fields\Creative_and_Open-ended_Questions.json": [],
#     "Fields\Multimodal_Information_Processing.json": []
# }

# Biology Objective

# classification_filename = {
#     "Fields/Mathematical_Reasoning.json": [
#         5, 17, 41, 64, 99, 104, 105, 111, 116, 138, 139, 142, 146, 149, 154, 158, 159, 164
#     ],
#     "Fields/Logical_Reasoning.json": [
#         0, 1, 2, 3, 4, 6, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 45, 46, 47, 48, 50, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 100, 101, 102, 103, 106, 107, 108, 109, 110, 112, 113, 114, 115, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 140, 141, 143, 144, 145, 147, 148, 150, 151, 152, 153, 155, 156, 157, 160, 161, 162, 163, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179
#     ],
#     "Fields/Lang_Comp_and_Produc.json": [],
#     "Fields/Natural_Science.json": [
#     ],
#     "Fields/Sociocultural_Understanding.json": [],
#     "Fields/Data_and_StatisticalLiteracy.json": [
#         5, 17, 41, 44, 57, 64, 99, 104, 105, 111, 116, 120, 122, 138, 139, 142, 146, 149, 154, 158, 159, 164, 174
#     ],
#     "Fields/Commonsense_and_WorldKnowledge.json": [
#         1, 3, 7, 13, 21, 31, 44, 51, 67, 73, 97, 112, 118
#     ],
#     "Fields/Creative_and_Open-ended_Questions.json": [],

# }

# Political_Science Objective

classification_filename = {
    "Fields\Mathematical_Reasoning.json": [],
    "Fields\Logical_Reasoning.json": [
        243, 244, 254, 264, 265, 274, 275, 276, 283, 285, 286, 296, 297, 306, 307, 
        317, 318, 319, 326, 331, 336, 337, 338, 339, 340, 344, 348, 358, 359
    ],
    "Fields\Lang_Comp_and_Produc.json": [
        251, 325, 335, 356
    ],
    "Fields\Natural_Science.json": [
    ],
    "Fields\Sociocultural_Understanding.json": [
    ],
    "Fields\Data_and_StatisticalLiteracy.json": [
        246, 279, 300, 311, 345, 349, 352
    ],
    "Fields\Commonsense_and_WorldKnowledge.json": [
        274, 280, 281, 295, 303, 307, 320, 323, 331, 333, 347, 350, 353, 354, 358
    ],
    "Fields\Creative_and_Open-ended_Questions.json": [
    ],

}

# History Objective



# Geography Objective



# source_file = "ObjectiveProblems/2010-2025_Physics_MCQs.json"   # 题目源文件
source_file = "ObjectiveProblems/2010-2025_Chemistry_MCQs.json"  
# source_file = "ObjectiveProblems/2010-2025_Biology_MCQs.json"  
# source_file = "ObjectiveProblems/2010-2025_Political_Science_MCQs.json"  
# source_file = "ObjectiveProblems/2010-2025_History_MCQs.json"  
# source_file = "ObjectiveProblems/2010-2025_Geography_MCQs.json"  
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

    # # ---- 若目标文件不存在 → 创建空模板 ----
    # if not os.path.exists(filename):
    #     os.makedirs(os.path.dirname(filename), exist_ok=True)
    #     empty_content = {"keywords": "", "questions": []}
    #     with open(filename, "w", encoding="utf-8") as f:
    #         json.dump(empty_content, f, ensure_ascii=False, indent=4)

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


