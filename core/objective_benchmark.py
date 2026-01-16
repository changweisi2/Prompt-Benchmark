import json
import os

from Model import Model # 模型
from api_key import api_key_HUAWEI

from Fields import FIELDS
from Strategies import STRATEGIES
from core.benchmark_utils import load_questions_from_file, to_tackle_questions


def main():
    api_key = api_key_HUAWEI
    base_url = "https://api.modelarts-maas.com/v2/chat/completions"
    model_name = "DeepSeek-R1"


    MODEL = Model(api_key, base_url, model_name, temperature=0.3, max_tokens=4096)

    for field_index, field in enumerate(FIELDS):
        for strategy in STRATEGIES :
            current_root = os.path.dirname(os.path.abspath(__file__))
            prompt_file_path = os.path.join(current_root,"Obj_Prompt.json")
            with open(prompt_file_path,'r',encoding="utf-8") as f :
                prompts = json.load(f)

            general_prompt = prompts["examples"][field_index]["prefix_prompt"]

            project_root = os.path.dirname(current_root)
            source_file_path = os.path.join(project_root, "Objective",field + ".json")

            data = load_questions_from_file(source_file_path)
            num = len(data)



            to_tackle_questions(data,
                                0,
                                num,
                                MODEL,
                                general_prompt,
                                field=field,
                                strategy=strategy)


if __name__ == "__main__" :
    main()
