import json

import requests

from api_key import api_key_HUAWEI
from core.Model import Model
from core.Strategies import STRATEGIES
from core.benchmark_utils import extract_objective_answer, extract_choices


api_key = api_key_HUAWEI
base_url = "https://api.modelarts-maas.com/v2/chat/completions"

# ========== 模型 ==========
# model_name = "DeepSeek-R1"
model_name = "deepseek-v3.2"
# model_name = "qwen3-235b-a22b"

MODEL = Model(api_key, base_url, model_name, temperature=0.3)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# 题目数据
question_data = {
    "year": "2023",
    "category": "全国甲卷",
    "question": "2. 在下列两个核反应方程中 $\\mathrm{X}+{ }_7^{14} \\mathrm{~N} \\rightarrow \\mathrm{Y}+{ }_8^{17} \\mathrm{O} 、 \\mathrm{Y}+{ }_3^7 \\mathrm{Li} \\rightarrow 2 \\mathrm{X}, \\mathrm{X}$ 和 $\\mathrm{Y}$ 代表两种不同的原子核, 以 $Z$和 $A$ 分别表示 $\\mathrm{X}$ 的电荷数和质量数, 则 $()$\nA. $Z=1, \\quad A=1 \\rightarrow$\nB. $Z=1, \\quad A=2$\nC. $Z=2, \\quad A=3$\nD. $Z=2, A=4$",
    "answer": [
        "D"
    ],
    "analysis": "【详解】设 $\\mathrm{Y}$ 电荷数和质量数分别为 $m$ 和 $n$, 根据核反应方程质量数和电荷数守恒可知第一个核反应方程的核电荷数和质量数满足\n$$\nA+14=n+17, \\quad Z+7=m+8\n$$\n第二个核反应方程的核电荷数和质量数满足\n$$\nn+7=2 A, \\quad m+3=2 Z\n$$\n联立解得\n$$\nZ=2, \\quad A=4\n$$\n故选 D",
    "index": 66,
    "score": 6
}

# 数据字典 键
index  = question_data['index']
year = question_data['year']
category = question_data['category']
score = question_data['score']
standard_answer =question_data['answer']
answer_length = len(standard_answer)
analysis = question_data['analysis']

# 题目
question = question_data['question'].strip() + '\n'

# 领域通用提示词
general_prompt = (
    "请解答下面的自然科学问题\n仔细阅读题目,解答其中的问题，请你严格使用如下的思考解答策略和回答格式来解答问题并将思考过程写在【解析】和<eoe>之间。你的答案请写在【答案】和<eoa>之间\n完整的题目回答格式如下：\n【解析】 ...<eoe>\n【答案】...<eoa>\n \n请你严格按照上述格式作答；如果不止一道题，请分别作答，最终所有答案排好顺序全都写在【答案】...<eoa>中，只写答案字母，如【解析】 ...<eoe>\n【答案】A A B B C<eoa>。\n题目和思考策略如下："
,)

# 策略
strategy_description = STRATEGIES[7]["description"]


full_prompt = f"{general_prompt}\n\n【解题策略】\n{strategy_description}\n\n【题目】\n{question}"

# full_prompt = "你是deepseek-v3.2吗？"
print(full_prompt)



# 请求
response = MODEL.execute(full_prompt)
print(response.text)

response_data = response.json()
model_output = response_data["choices"][0]["message"]["content"]
model_answer = extract_objective_answer(model_output, question_type='single_question_choice')

print(model_output)
print(model_answer)



# 数据字典
model_answer_dict = {
    'index': index,
    'year': year,
    'category': category,
    'score': score,
    'question': question,
    'standard_answer': standard_answer,
    'analysis': analysis,
    'model_answer': model_answer,
    'model_output': model_output
}

print(model_answer_dict)