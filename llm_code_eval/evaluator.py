import re
import json
import openai
from collections import Counter
from llm_code_eval.util import prompt, nl2c_description, c2nl_description, c2c_description
from llm_code_eval.util.api_request import create_chatgpt_config, request_chatgpt_engine
from llm_code_eval.util.model_inference import create_model_config, request_model_engine
from transformers import AutoModelForCausalLM, AutoTokenizer, StoppingCriteria, StoppingCriteriaList

def extract_json_objects(text):
    json_objects = []
    pattern = r'\{.*?\}'
    json_strings = re.findall(pattern, text)

    for json_str in json_strings:
        try:
            json_obj = json.loads(json_str)
            json_objects.append(json_obj)
        except json.JSONDecodeError:
            continue
    return json_objects

class ICE(object):
    def __init__(self, task="nl2c", aspect=None, model_name="gpt-3.5-turbo"):
        self.task = task
        self.aspect = aspect
        self.model_name = model_name
        if model_name in ["gpt-3.5-turbo", "gpt-4"]:
            self.tokenizer = None
            self.model = None
        else:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", load_in_8bit=True)
    def instructer(self):
        message  = prompt.INSTRUCTER_PROMPT
        if self.task == "nl2c":
            message = message.replace("{raw_instruction}", nl2c_description.PROMPT)
        elif self.task == "c2nl":
            message = message.replace("{raw_instruction}", c2nl_description.PROMPTS[self.aspect])
        elif self.task == "c2c":
            message = message.replace("{raw_instruction}", c2c_description.PROMPT)
        if self.tokenizer:
            config = create_model_config(message)
            ret = request_model_engine(self.tokenizer, self.model, config)
        else:
            config = create_chatgpt_config(message, model=self.model_name)
            ret = request_chatgpt_engine(config)
        return ret

    def calibrator(self, outputs):
        calibrated_message = ""
        for idx, output in enumerate(outputs):
            calibrated_message  += prompt.MODEL_OUT_PROMPT.replace("{raw_index}", idx).replace("{raw_input}", output)
        return calibrated_message

    def scorer(self, message):
        if self.tokenizer:
            config = create_model_config(message)
            ret = request_model_engine(self.tokenizer, self.model, config)
        else:
            config = create_chatgpt_config(message, model=self.model_name)
            ret = request_chatgpt_engine(config)
        score_json = extract_json_objects(ret)
        assert len(score_json) == 1
        return score_json

    def evaluate(self, outputs, fs=True, calibrate=True, cot=True):
        message = ""
        message += self.instructer()
        if fs:
            message += prompt.EXAMPLE_PROMPTS[self.task]
        if calibrate:
            assert isinstance(outputs, list)
        message += self.calibrator(outputs)
            
        if cot:
            message += prompt.SCORES_REASON_PROMPT
        else:
            message += prompt.SCORES_ONLY_PROMPT
        if self.tokenizer:
            out = request_model_engine(self.tokenizer, self.model, config)
        else:
            out = request_chatgpt_engine(message)
        score = self.scorer(out)
        return out, score
        