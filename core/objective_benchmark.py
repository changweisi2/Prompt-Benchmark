
from Model import Model # 模型
from api_key import api_key_HUAWEI





def main():
    api_key = api_key_HUAWEI
    base_url = "https://api.modelarts-maas.com/v2/chat/completions"

    DeepSeek_R1 = Model(api_key, base_url, model_name="DeepSeek-R1", temperature=0.3, max_tokens=4096)




if __name__ == "__main__" :
    main()
