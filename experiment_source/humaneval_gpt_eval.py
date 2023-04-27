import json
import openai
from glob import glob
from tqdm import tqdm
import backoff
import asyncio
from typing import Any
import random
openai.api_key=""

prompt1="""\
You will be given the code snippet for a problem. 
Your task is to rate the code snippet only on one metric.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Functional Correctness (0-4) - Execution-based quality of the code snippet combined with the problem. The correctness is measured by the all possible unit tests, and the comparison of the reference code. The combination of the code snippet and the problem should pass all the possible tests based on your understanding of the reference code. The length of the code snippet can not determine the correctness. You need to assess the logics line by line.
- A score of 0  (failing all possible test) means that the code snippet is totally incorrect and meaningless.
- A score of 4  (passing all possible test) means that the code snippet is totally correct and can handle all cases.


Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the problem. Check if the code snippet covers all required functionalities of the problem. 
3. Assign a score for functional correctness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{INTENT}}

Code Snippet:

{{CODE}}

Evaluation Form:
Functional Correctness (scores ONLY):
"""

prompt2="""\
You will be given the code snippet for a problem. 
Your task is to rate the code snippet only on one metric.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Functional Correctness (0-4) - Execution-based quality of the code snippet combined with the problem. The correctness is measured by the all possible unit tests, and the comparison of the reference code. The combination of the code snippet and the problem should pass all the possible tests based on your understanding of the reference code. The length of the code snippet can not determine the correctness. You need to assess the logics line by line.
- A score of 0  (failing all possible test) means that the code snippet is totally incorrect and meaningless.
- A score of 4  (passing all possible test) means that the code snippet is totally correct and can handle all cases.


Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the reference code. Check if the code snippet covers all required functionalities of the problem, and if it is as good as the reference code. 
3. Assign a score for functional correctness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{INTENT}}

Reference Code:

{{REFERENCE}}

Code Snippet:

{{CODE}}

Evaluation Form:
Functional Correctness (scores ONLY):
"""
@backoff.on_exception(backoff.expo, (openai.error.RateLimitError,
                                     openai.error.APIConnectionError))
def get_output(intent, code, snippet):
    message_json=[{"role": "user", 
                    "content": prompt1.replace("{{INTENT}}",intent).replace("{{CODE}}",code).replace("{{REFERENCE}}",snippet)}]
    out=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=message_json,
    )["choices"][0]["message"]["content"]

    return out


async def dispatch_openai_requests(
    messages_list: list[list[dict[str,Any]]],
    model: str,
) -> list[str]:
    """Dispatches requests to OpenAI API asynchronously.
    
    Args:
        messages_list: List of messages to be sent to OpenAI ChatCompletion API.
        model: OpenAI model to use.
        temperature: Temperature to use for the model.
        max_tokens: Maximum number of tokens to generate.
        top_p: Top p to use for the model.
    Returns:
        List of responses from OpenAI API.
    """
    async_responses = [
        openai.ChatCompletion.acreate(
            model=model,
            messages=x,
            temperature=0,
        )
        for x in messages_list
    ]
    return await asyncio.gather(*async_responses)

if __name__ == "__main__":
    while True:
        try:
            for file in glob("data/*java*-0.8-keep"):
                language = file.split("_")[1]
                try:
                    with open("humaneval_gpt35.json") as f:
                        orginal_results=json.load(f)
                        length = len(orginal_results)
                except:
                    orginal_results=[]
                    length=0
                with open(file+"/human_grade.json") as f:
                    data=json.load(f)
                print(language,length)
                for id,d in enumerate(tqdm(data[length:])):
                    tmp_results=[]
                    intent=d['intent']
                    snippet=d['snippet'][0]
                    inputs = []
                    ks = []
                    for k in list(d.keys()):
                        if k.isnumeric():
                            code = d[k]
                            ks.append(k)
                            inputs.append([{"role": "user",
                                            "content": prompt2.replace("{{INTENT}}",intent).replace("{{CODE}}",code).replace("{{REFERENCE}}",snippet)
                                            }])
                    try:
                        random.seed(42)
                        idx = random.sample(range(len(inputs)), 20)
                        inputs = [inputs[i] for i in idx]
                        ks = [ks[i] for i in idx]
                    except:
                        pass
                    predictions = asyncio.run(dispatch_openai_requests(
                                                                inputs,
                                                                model="gpt-3.5-turbo")
                    )
                    orginal_results.append({f"grade-{k}":{**d[f"grade-{k}"],
                                    "raw_output": predictions[j]["choices"][0]["message"]['content']}
                                    for j,k in enumerate(ks)})
                    with open("humaneval_gpt35.json", "w") as f:
                        json.dump(orginal_results, f, indent=4)
        except:
            pass
