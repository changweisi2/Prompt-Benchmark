import json

filename = "ObjectiveProblems/2010-2025_Physics_MCQs.json"

# 1. 读取原文件
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 重排 index
for new_index, question in enumerate(data["questions"]):
    print(new_index);
    question["index"] = new_index

# 3. 覆盖写回原文件
with open(filename, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)