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
# model_name = "deepseek-v3.2"
# model_name = "qwen3-235b-a22b"
# model_name = "qwen2.5-vl-72b"

# MODEL = Model(api_key, base_url, model_name, temperature=0.3)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# 题目数据
question_data = {
    "year": "2022",
    "category": "（全国乙卷）",
    "question": "4. 嫦娥二号卫星在完成探月任务后, 继续进行深空探测, 成为我国第一颗环绕太阳飞行的 人造行星, 为研究嫦娥二号绕日周期与地球绕日周期的比值, 用到数列 $\\left\\{b_{n}\\right\\}: b_{1}=1+\\frac{1}{a_{1}}$, $b_{2}=1+\\frac{1}{a_{1}+\\frac{1}{a_{2}}}, \\quad b_{3}=1+\\frac{1}{a_{1}+\\frac{1}{a_{2}+\\frac{1}{a_{3}}}}, \\cdots$, 依此类推, 其中 $a_{k} \\in \\mathbf{N}^{\\star}(k=1,2, \\cdots)$. 则 ()\nA. $b_{1}<b_{5}$\nB. $b_{3}<b_{8}$\nC. $b_{6}<b_{2}$\nD. $b_{4}<b_{7}$\n",
    "answer": [
        "D"
    ],
    "analysis": "【详解】解: 因为 $a_{k} \\in \\mathbf{N}^{*}(k=1,2, \\cdots)$,\n\n所以 $a_{1}<a_{1}+\\frac{1}{a_{2}}, \\frac{1}{a_{1}}>\\frac{1}{a_{1}+\\frac{1}{a_{2}}}$, 得到 $b_{1}>b_{2}$,\n\n同理 $a_{1}+\\frac{1}{a_{2}}>a_{1}+\\frac{1}{a_{2}+\\frac{1}{a_{3}}}$, 可得 $b_{2}<b_{3}, b_{1}>b_{3}$\n\n又因为 $\\frac{1}{a_{2}}>\\frac{1}{a_{2}+\\frac{1}{a_{3}+\\frac{1}{a_{4}}}}, a_{1}+\\frac{1}{a_{2}+\\frac{1}{a_{3}}}<a_{1}+\\frac{1}{a_{2}+\\frac{1}{a_{3}+\\frac{1}{a_{4}}}}$ ，\n\n故 $b_{2}<b_{4}, b_{3}>b_{4}$;\n\n以此类推, 可得 $b_{1}>b_{3}>b_{5}>b_{7}>\\cdots, b_{7}>b_{8}$, 故 $\\mathrm{A}$ 错误;\n\n$b_{1}>b_{7}>b_{8}$, 故 B 错误; \n\n$$\n\\begin{aligned}\n& \\frac{1}{a_{2}}>\\frac{1}{a_{2}+\\frac{1}{a_{3}+\\cdots \\frac{1}{a_{6}}}} \\text {, 得 } b_{2}<b_{6} \\text {, 故 C 错误; } \\\\\n& a_{1}+\\frac{1}{a_{2}+\\frac{1}{a_{3}+\\frac{1}{a_{4}}}}>a_{1}+\\frac{1}{a_{2}+\\cdots \\frac{1}{a_{6}+\\frac{1}{a_{7}}}} \\text {, 得 } b_{4}<b_{7} \\text {, 故 D 正确. }\n\\end{aligned}\n$$\n\n故选: D.\n",
    "index": 330,
    "score": 5
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

# 图片
# pictures = question_data['picture']

# 领域通用提示词
# general_prompt = (
#     "请解答下面的自然科学问题\n仔细阅读题目,解答其中的问题，请你严格使用如下的思考解答策略和回答格式来解答问题并将思考过程写在【解析】和<eoe>之间。你的答案请写在【答案】和<eoa>之间\n完整的题目回答格式如下：\n【解析】 ...<eoe>\n【答案】...<eoa>\n \n请你严格按照上述格式作答；如果不止一道题，请分别作答，最终所有答案排好顺序全都写在【答案】...<eoa>中，只写答案字母，如【解析】 ...<eoe>\n【答案】A A B B C<eoa>。\n题目和思考策略如下："
# ,)

# 多模态领域提示词
general_prompt = "请解答下面的问题\n仔细阅读题目,解答其中的问题，请你严格使用如下的思考解答策略和回答格式来解答问题并将思考过程写在【解析】和<eoe>之间。你的答案请写在【答案】和<eoa>之间\n完整的题目回答格式如下：\n【解析】 ...<eoe>\n【答案】...<eoa>\n \n请你严格按照上述格式作答；如果不止一道题，请分别作答，最终所有答案排好顺序全都写在【答案】...<eoa>中，只写答案字母，如【解析】 ...<eoe>\n【答案】A A B B C<eoa>。\n策略、题目如下：",


# 策略
s_index = 8
strategy_description = STRATEGIES[s_index]["description"]
strategy_name = STRATEGIES[s_index]["name"]

full_prompt = f"{general_prompt}\n\n【解题策略】\n{strategy_description}\n\n【题目】\n{question}"

# full_prompt = "你是deepseek-v3.2吗？"
print(full_prompt)



# 请求
# response = MODEL.execute(full_prompt,pictures=pictures)
# print(json.dumps(response.text, indent=2, ensure_ascii=False))
# response_data = response.json()
# model_output = response_data["choices"][0]["message"]["content"]
# model_output = input("请输入模型输出:")
# model_answer = extract_objective_answer(model_output, question_type='single_question_choice')
#
# print(model_output)
# print(model_answer)

model_answer = []
choice = input("请输入模型答案：")

model_answer.append(choice)
print(strategy_name)
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
    # 'model_output': model_output
}

print(json.dumps(model_answer_dict, indent=2, ensure_ascii=False))