import os

from Model import Model
from api_key import api_key_HUAWEI
from benchmark_utils import load_questions_from_file, to_tackle_questions, write_results_to_file
import json
from Strategies import STRATEGIES


if __name__ == "__main__":
    api_key = api_key_HUAWEI
    base_url = "https://api.modelarts-maas.com/v2/chat/completions"

    DeepSeek_R1 = Model(api_key, base_url, model_name="DeepSeek-R1", temperature=0.3, max_tokens=4096)

    field = "objective_benchmark_test"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    source_file_path = os.path.join(current_dir, field + ".json")

    data = load_questions_from_file(source_file_path)
    num = len(data)

    general_prompt ="请你做一道自然科学相关的题目。\n请你一步一步思考。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答,请你严格按照上述格式作答,请你严格按照上述格式作答。\n题目如下："

    strategy = STRATEGIES[0]
    model_answer_dictlist = to_tackle_questions(data, 0, num, DeepSeek_R1, general_prompt, field=field, strategy=strategy)


