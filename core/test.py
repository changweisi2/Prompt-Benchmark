from Model import Model

from api_key import api_key_HUAWEI

if __name__ == "__main__":
    api_key = api_key_HUAWEI
    base_url = "https://api.modelarts-maas.com/v2/chat/completions"

    DeepSeek_R1 = Model(api_key, base_url, model_name="DeepSeek-R1", temperature=0.3, max_tokens=4096)
    data_example =         {
            "year": "2019",
            "category": "（新课标ⅱ）",
            "question": "3．（6分）某种H+﹣ATPase是一种位于膜上的载体蛋白，具有ATP水解酶活性，能够利用\n水解ATP释放的能量逆浓度梯度跨膜转运H+．①将某植物气孔的保卫细胞悬浮在一定\npH的溶液中（假设细胞内的pH高于细胞外），置于暗中一段时间后，溶液的pH不变。\n②再将含有保卫细胞的该溶液分成两组，一组照射蓝光后溶液的pH明显降低；另一组先\n在溶液中加入H+﹣ATPase的抑制剂（抑制ATP水解），再用蓝光照射，溶液的pH不变。\n根据上述实验结果，下列推测不合理的是（）\nA．H+﹣ATPase位于保卫细胞质膜上，蓝光能够引起细胞内的H+转运到细胞外\nB．蓝光通过保卫细胞质膜上的H+﹣ATPase发挥作用导致H+逆浓度梯度跨膜运输\nC．H+﹣ATPase逆浓度梯度跨膜转运H+所需的能量可由蓝光直接提供\nD．溶液中的H+不能通过自由扩散的方式透过细胞质膜进入保卫细胞\n",
            "answer": [
                "C"
            ],
            "picture":"",
            "analysis": "【解答】解：A、分析题意可知，H+﹣ATPase位于保卫细胞质膜上，蓝光能够引起细胞\n内的H+转运到细胞外，A正确；\nB、蓝光通过保卫细胞质膜上的H+﹣ATPase发挥作用导致H+逆浓度梯度跨膜运输，B\n正确；\nC、H+﹣ATPase逆浓度梯度跨膜转运H+所需的能量由ATP水解提供，C错误；\nD、溶液中的H+不能通过自由扩散进入保卫细胞，D正确。\n故选：C。\n",
            "index": 322,
            "score": 6
        }
    choice_question = data_example['question']
    choice_picture = data_example['picture']
    choice_prompt = "请你做一道自然科学领域的题。\n请你一步一步思考。你将从A，B，C，D中选出正确的答案，并写在【答案】和<eoa>之间。\n例如：【答案】: A <eoa>\n完整的题目回答的格式如下：\n【解析】 ... <eoe>\n【答案】 ... <eoa>\n请你严格按照上述格式作答,请你严格按照上述格式作答,请你严格按照上述格式作答。\n题目如下："

    response = DeepSeek_R1.execute(choice_prompt, choice_question, choice_picture)

    # Print result.
    print(response.status_code)
    print(response.text)