import codecs
import os
import re
import json
from tqdm import  tqdm
import time

from core.Model import Model


def extract_choices(answer_part):
    """
    从文本中提取选项字母（保序去重）
    """
    found = re.findall("[A-Z]", answer_part)
    result = []
    for c in found:
        if c not in result:
            result.append(c)
    return result


def extract_objective_answer(model_output, question_type, answer_length=None):
    """
    从模型输出中提取选择题答案。

    预期的模型输出格式：
    'single_choice' (单选题): 答案应为 model_output 中的最后一个大写字母，例如："...【答案】 A <eoa>"
    'multi_question_choice' (组合选择题): "...【答案】A ... 【答案】C ..." 或者在输出开头写下答案，例如 "A C D E F...."
    'multi_choice' (多选题): "...【答案】 ABD " 或者在输出末尾写下答案，例如 "... ACD"
    'five_out_of_seven' (七选五): 答案应为 model_output 中的前五个大写字母，例如 "A C D F B ...."
    """
    model_answer = []
    try:
        # 统一预处理
        content = re.sub(r'\s+', '', model_output)

        # 正则匹配
        match = re.search(r'【答案】(.*?)<eoa>', content)
        if match :
            answer_part = match.group(1).strip()
        else :
            answer_part = None
    except Exception as e:
        print("解析失败:"+e)


    # ===== 选择题 =====
    if question_type == 'single_question_choice':
        choices = extract_choices(answer_part)
        if not choices:
            choices = extract_choices(content[-20:], 'A-Z')
        if choices:
            model_answer.append(''.join(choices))

    # ===== 组合选择题（多个单选）=====
    elif question_type == 'multi_question_choice':
        choices = extract_choices(answer_part, 'A-Z')
        if not choices:
            choices = extract_choices(content, 'A-Z')
        if answer_length:
            model_answer = choices[:answer_length]
        else:
            model_answer = choices

    # ===== 七选五 =====
    elif question_type == 'five_out_of_seven':
        choices = extract_choices(content, 'ABCDEFG')
        model_answer = choices[:5]


    return model_answer

def load_questions_from_file(source_file_path:str):
    """
    从文件中加载题目集
    """
    with open(source_file_path, "r",encoding="utf-8") as f:
        data = json.load(f)['questions']
    f.close()

    return data


def to_tackle_questions(data,start_index,end_index,model:Model,prompt):
    """
    进行题目解答测试
    :param data:
    :param source_file_path:
    :return:
    """
    model_answer_dictlist = []
    for i in tqdm(range(start_index, end_index)):

        # 数据字典
        index = data[i]['index']
        question = data[i]['question'].strip() + '\n'
        year = data[i]['year']
        category = data[i]['category']
        score = data[i]['score']
        standard_answer = data[i]['answer']
        answer_length = len(standard_answer)
        analysis = data[i]['analysis']

        # 请求大模型响应
        response = model.execute(prompt, question)
        response_data = response.json()

        print()
        print(response.status_code)
        print(response.text)

        model_output = response_data["choices"][0]["message"]["content"]
        model_answer = extract_objective_answer(model_output, question_type='single_question_choice')

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
        model_answer_dictlist.append(model_answer_dict)

        # 延迟请求
        time.sleep(5)

    return model_answer_dictlist


def write_results_to_file(field,strategy,model:Model, model_answer_dictlist):



    model_name=model.model_name

    save_directory = "results/"+model_name+"/"+field+"/"+strategy

    file_name = ".json"
    result_file_path = os.path.join(save_directory, file_name)
    with codecs.open(result_file_path, 'w', 'utf-8') as f:
        output = {
            'field' : field,
            'strategy' : strategy,
            'model_name' : model_name,
            'questions' : model_answer_dictlist
            }
        json.dump(output, f, ensure_ascii=False, indent=4)