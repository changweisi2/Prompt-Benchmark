import json

import requests

from api_key import api_key_HUAWEI
from core.Model import Model
from core.Strategies import STRATEGIES
from core.benchmark_utils import extract_objective_answer, extract_choices


api_key = api_key_HUAWEI
base_url = "https://api.modelarts-maas.com/v2/chat/completions"
model_name = "DeepSeek-R1"


MODEL = Model(api_key, base_url, model_name, temperature=0.3)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

general_prompt = "请解答下面的语言理解问题\n仔细阅读题目并充分结合你已有的知识，解答其中的问题，请你严格使用如下的思考解答策略来解答问题并将思考过程写在【解析】和<eoe>之间。你的答案请写在【答案】和<eoa>之间\n完整的题目回答格式如下：\n【解析】 ...<eoe>\n【答案】...<eoa>\n \n请你严格按照上述格式作答；如果不止一道题，请分别作答，最终所有答案排好顺序全都写在【答案】...<eoa>中，只写答案字母，如【解析】 ...<eoe>\n【答案】A A B B C<eoa>。\n题目和思考策略如下：",
strategy_description = STRATEGIES[0]["description"]
question = "阅读下面短文 ，从短文后各题所给的 A、B、C和D四个选项中 ，选出可以\n填入空白处的最佳选项。  \nIn 1973,  I was teaching  elementary  school.  Each  day, 27 kids  41  “The  \nThinking  Laboratory.”  That was the   42   students  voted  for after deciding  that \n“Room  104”  was too   43   . \nFreddy  was an average    44  , but not an average  person.  He had the rare \nbalance  of fun and compassion （同情） . He would     45    the loudest  over fun and \nbe the saddest  over anyone’s    46    . \nBefore  the school  year    47    , I gave  the kids a special     48    , \nT-shirts  with the words  “Verbs  Are Your    49   ” on them.  I had advised  the kids \nthat while  verbs（动词） may seem  dull, most  of the  50    things  they do throughout  \ntheir lives  will be verbs.  \nThrough  the years,  I’d run into former  students  who would  provide     51    \non old classmates.  I learned  that Freddy  did several  jobs after his   52    from  high \nschool  and remained  the same   53    person  I met forty  years  before.  Once,  while  \nworking  overnight  at a store,  he let a homeless  man   54   in his truck.  Another  \ntime,  he   55   a friend  money  to buy a house  . \nJust last year,  I was  56  a workshop  when  someone  knocked  at the classroom  \ndoor.  A woman   57  the interruption  and handed  me an envelope.  I stopped  \nteaching  and   58   it up. Inside  were  the “Verbs”  shirt and a   59   from  \nFreddy’s  mother.  “Freddy  passed  away  on Thanksgiving.  He wanted  you to have  \nthis.”  \nI told the story  to the class.  As sad as it was, I couldn’t  help smiling.  Although  \nFreddy  was taken  from  us, we all   60   something  from  Freddy.  \n  41. A. built  B. entered  C. decorated  D. ran \n42. A. name  B. rule C. brand  D. plan  \n43. A. small  B. dark  C. strange  D. dull \n44. A. scholar  B. student  C. citizen  D. worker  \n45. A. speak  B. sing  C. question  D. laugh  \n46. A. misfortune  B. disbelief  C. dishonesty  D. mistake  \n47. A. changed  B. approached  C. returned  D. ended  \n48. A. lesson  B. gift C. report  D. message  \n49. A. Friends  B. Awards  C. Masters  D. Tasks  \n50. A. simple  B. unique  C. fun D. clever  \n51. A. assessments  B. comments  C. instructions  D. updates  \n52. A. graduation  B. retirement  C. separation  D. resignation  \n53. A. daring  B. modest  C. caring  D. smart  \n54. A. wait  B. sleep  C. study  D. live \n55. A. paid  B. charged  C. lent D. owed  \n56. A. observing  B. preparing  C. designing  D. conducting  \n57. A. regretted  B. avoided  C. excused  D. ignored  \n58. A. opened  B. packed  C. gave  D. held  \n59. A. picture  B. bill C. note  D. diary  \n60. A. chose  B. took  C. expected  D. borrowed\n",

full_prompt = f"{general_prompt}\n\n【解题策略】\n{strategy_description}\n\n【题目】\n{question}"
print(full_prompt)


data = {
    "model": f"{model_name}",  # model参数
    "temperature": 0.3,
    "messages": [
        {
            "role": "user",
            "content": full_prompt
        }
    ]
}

response = requests.post(base_url, headers=headers, data=json.dumps(data), verify=True)
response_data = response.json()
model_output = response_data["choices"][0]["message"]["content"]
model_answer = extract_objective_answer(model_output, question_type='single_question_choice')

print(response.text)
print(model_output)

print(model_answer)


# answer ="【答案】B A D B D A D B A C D A C B C D C C A C B<eoa> "
#
# model_answer = extract_objective_answer(answer, question_type='single_question_choice')
#
# print(extract_choices(answer))
# print(model_answer)