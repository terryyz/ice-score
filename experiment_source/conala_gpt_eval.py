import json
import openai
from glob import glob
from tqdm import tqdm
import backoff
import asyncio
from typing import Any
openai.api_key=""

prompt1=\
"""\
You will be given the code snippet for a problem.
Your task is to rate the code snippet only on one metric.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Usefulness (0-4) Usefulness of the code snippet based on the problem description.

- A score of 0: Snippet is not at all helpful, it is irrelevant to the problem.
- A score of 1: Snippet is slightly helpful, it contains information relevant to the problem, but it is easier to write the solution from scratch.
- A score of 2: Snippet is somewhat helpful, it requires significant changes (compared to the size of the snippet), but is still useful.
- A score of 3: Snippet is helpful, but needs to be slightly changed to solve the problem.
- A score of 4: Snippet is very helpful, it solves the problem.

Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the problem. Check if the code snippet covers all required functionalities of the problem, and if it presents them in a clear and logical order. 
3. Assign a score for usefulness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{INTENT}}

Code Snippet:

{{CODE}}

Evaluation Form:
Usefulness (scores ONLY)
"""

prompt2=\
"""\
You will be given the code snippet for a problem.
Your task is to rate the code snippet only on one metric.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Usefulness (0-4) Usefulness of the code snippet based on the problem description and the comparison of reference code.

- A score of 0: Snippet is not at all helpful, it is irrelevant to the problem.
- A score of 1: Snippet is slightly helpful, it contains information relevant to the problem, but it is easier to write the solution from scratch.
- A score of 2: Snippet is somewhat helpful, it requires significant changes (compared to the size of the snippet), but is still useful.
- A score of 3: Snippet is helpful, but needs to be slightly changed to solve the problem.
- A score of 4: Snippet is very helpful, it solves the problem.

Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the problem and reference code. Check if the code snippet covers all required functionalities of the problem, and if it presents them in a clear and logical order. 
3. Assign a score for usefulness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{INTENT}}

Reference Code:

{{REFERENCE}}

Code Snippet:

{{CODE}}

Evaluation Form:
Usefulness (scores ONLY)
"""

prompt3=\
"""\
You will be given the code snippet for a problem.
Your task is to rate the code snippet only on one metric.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Usefulness (0-4) Usefulness of the code snippet based on the problem description.

- A score of 0: Snippet is not at all helpful, it is irrelevant to the problem.
- A score of 1: Snippet is slightly helpful, it contains information relevant to the problem, but it is easier to write the solution from scratch.
- A score of 2: Snippet is somewhat helpful, it requires significant changes (compared to the size of the snippet), but is still useful.
- A score of 3: Snippet is helpful, but needs to be slightly changed to solve the problem.
- A score of 4: Snippet is very helpful, it solves the problem.

Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the problem. Check if the code snippet covers all required functionalities of the problem, and if it presents them in a clear and logical order. 
3. Assign a score for usefulness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{INTENT}}

Code Snippet:

{{CODE}}

Evaluation Form:
Usefulness:
Step-by-step Evaluation:
"""

prompt4=\
"""\
You will be given the code snippet for a problem.
Your task is to rate the code snippet only on one metric.
Please make sure you read and understand these instructions carefully.
Please keep this document open while reviewing, and refer to it as needed.

Evaluation Criteria:
Usefulness (0-4) Usefulness of the code snippet based on the problem description and the comparison of reference code.

- A score of 0: Snippet is not at all helpful, it is irrelevant to the problem.
- A score of 1: Snippet is slightly helpful, it contains information relevant to the problem, but it is easier to write the solution from scratch.
- A score of 2: Snippet is somewhat helpful, it requires significant changes (compared to the size of the snippet), but is still useful.
- A score of 3: Snippet is helpful, but needs to be slightly changed to solve the problem.
- A score of 4: Snippet is very helpful, it solves the problem.

Evaluation Steps:
1. Read the problem carefully and identify required functionalities of the implementation.
2. Read the code snippet and compare it to the problem and reference code. Check if the code snippet covers all required functionalities of the problem, and if it presents them in a clear and logical order. 
3. Assign a score for usefulness on a scale of 0 to 4, where 0 is the lowest and 4 is the highest based on the Evaluation Criteria.

Problem:

{{INTENT}}

Reference Code:

{{REFERENCE}}

Code Snippet:

{{CODE}}

Evaluation Form:
Usefulness:
Step-by-step Evaluation:
"""
@backoff.on_exception(backoff.expo, (openai.error.RateLimitError,
                                     openai.error.APIConnectionError))
def get_output(intent, code):
    message_json=[{"role": "system", 
                    "content": prompt1.replace("{{INTENT}}",intent).replace("{{CODE}}",code)}]
    out=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=message_json,
    )["choices"][0]["message"]

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
    conala_models_list = ['baseline', 'tranx-annot', 'best-tranx', 'best-tranx-rerank', 'codex']
    with open('data/to-grade/conala/conala-human-grades.json') as f:
        data = json.load(f)
    try:
        with open("conala_gpt35.json") as f:
            orginal_results=json.load(f)
        length=len(orginal_results)
    except:
        orginal_results=[]
        length=0
    results=[]
    for d in tqdm(data[length:]):
        intent=d['intent']
        snippet=d['snippet'][0]
        inputs = []
        for k in conala_models_list:
            code = d[k]
            inputs.append([{"role": "user",
                            "content": prompt1.replace("{{INTENT}}",intent).replace("{{CODE}}",code).replace("{{REFERENCE}}",snippet)
                            }])
        predictions = asyncio.run(dispatch_openai_requests(
                                                        inputs,
                                                        model="gpt-3.5-turbo")
            )
        assert len(predictions) == len(inputs)
        results = dict()
        [results.update({f"grade-{k}":d[f"grade-{k}"],
                          f"gpt3.5-grade-{k}": predictions[i]["choices"][0]["message"]['content']})
                            for i,k in enumerate(conala_models_list)]
        orginal_results.append(results)    
        with open("conala_gpt35.json", "w") as f:
            json.dump(orginal_results, f, indent=4)
