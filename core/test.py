import json

import requests

from api_key import api_key_HUAWEI
from core.Model import Model
from core.Strategies import STRATEGIES
from core.benchmark_utils import extract_objective_answer, extract_choices


api_key = api_key_HUAWEI
base_url = "https://api.modelarts-maas.com/v2/chat/completions"

# ========== 模型 ==========
model_name = "DeepSeek-R1"
MODEL = Model(api_key, base_url, model_name, temperature=0.3)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

# 题目数据
question_data = {
    "year": "2019",
    "category": "（新课标ⅱ）",
    "question": "5．（6分）某种植物的羽裂叶和全缘叶是一对相对性状。某同学用全缘叶植株（植株甲）进\n行了下列四个实验。\n①让植株甲进行自花传粉，子代出现性状分离\n②用植株甲给另一全缘叶植株授粉，子代均为全缘叶\n③用植株甲给羽裂叶植株授粉，子代中全缘叶与羽裂叶的比例为1：1\n④用植株甲给另一全缘叶植株授粉，子代中全缘叶与羽裂叶的比例为3：1\n其中能够判定植株甲为杂合子的实验是（）A．①或② B．①或④ C．②或③ D．③或④\n",
    "answer": [
        "B"
    ],
    "analysis": "【解答】解：①让全缘叶植株甲进行自花传粉，子代出现性状分离，说明植株甲为杂合\n子，杂合子表现为显性性状，新出现的性状为隐性性状，①正确；\n②用植株甲给另一全缘叶植株授粉，子代均为全缘叶，说明双亲可能都是纯合子，既可\n能是显性纯合子，也可能是隐性纯合子，或者是双亲均表现为显性性状，其中之一为杂\n合子，另一个为显性纯合子，因此不能判断植株甲为杂合子，②错误；\n③用植株甲给羽裂叶植株授粉，子代中全缘叶与羽裂叶的比例为1：1，只能说明一个亲\n本为杂合子，另一个亲本为隐性纯合子，但谁是杂合子、谁是纯合子无法判断，③错误；\n④用植株甲给另一全缘叶植株授粉，子代中全缘叶与羽裂叶的比例为3：1，说明植株甲\n与另一全缘叶植株均为杂合子，④正确。\n故选：B。\n",
    "index": 234,
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
    "请解答下面的常识问题\n仔细阅读题目,解答其中的问题，请你严格使用如下的思考解答策略和回答格式来解答问题并将思考过程写在【解析】和<eoe>之间。你的答案请写在【答案】和<eoa>之间\n完整的题目回答格式如下：\n【解析】 ...<eoe>\n【答案】...<eoa>\n \n请你严格按照上述格式作答；如果不止一道题，请分别作答，最终所有答案排好顺序全都写在【答案】...<eoa>中，只写答案字母，如【解析】 ...<eoe>\n【答案】A A B B C<eoa>。\n题目和思考策略如下："
,)

# 策略
strategy_description = STRATEGIES[0]["description"]


full_prompt = f"{general_prompt}\n\n【解题策略】\n{strategy_description}\n\n【题目】\n{question}"
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