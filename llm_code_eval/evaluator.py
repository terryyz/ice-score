import re
import json
import openai
from collections import Counter
from llm_code_eval.util import prompt, nl2c_description, c2nl_description, c2c_description
from llm_code_eval.util.api_request import create_chatgpt_config, request_chatgpt_engine
from llm_code_eval.util.model_inference import create_model_config, request_model_engine

def extract_json_objects(text):
    pattern = r'\{.*?\}'
    json_strings = re.findall(pattern, text)[0]
    return json.loads(json_strings)

class ICE(object):
    def __init__(self, task="nl2c", aspect=None, model_name="gpt-3.5-turbo"):
        self.task = task
        self.aspect = aspect
        self.model_name = model_name
        if model_name in ["gpt-3.5-turbo", "gpt-4"]:
            self.tokenizer = None
            self.model = None
        else:
            from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token="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")
            self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", load_in_8bit=True, use_auth_token="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")

    def instructer(self):
        message  = prompt.INSTRUCTER_PROMPT
        if self.task == "nl2c":
            message = message.replace("{raw_instruction}", nl2c_description.PROMPT)
        elif self.task == "c2nl":
            message = message.replace("{raw_instruction}", c2nl_description.PROMPTS[self.aspect])
        elif self.task == "c2c":
            message = message.replace("{raw_instruction}", c2c_description.PROMPT)
        message = message + "\n# Detailed Evaluation Steps:\n"
        if self.model:
            config = create_model_config(message)
            message = request_model_engine(self.tokenizer, self.model, config)
        else:
            config = create_chatgpt_config(message, model=self.model_name)
            message = request_chatgpt_engine(config)["choices"][0]["message"]["content"]
        print(message)
        return message

    def calibrator(self, outputs):
        calibrated_message = ""
        for idx, output in enumerate(outputs):
            calibrated_message  += prompt.MODEL_OUT_PROMPT.replace("{raw_index}", str(idx)).replace("{raw_output}", output)
        return calibrated_message

    def scorer(self, message):
        if self.model:
            config = create_model_config(message)
            message = request_model_engine(self.tokenizer, self.model, config)
        else:
            config = create_chatgpt_config(message, model=self.model_name)
            message = request_chatgpt_engine(config)["choices"][0]["message"]["content"]
        score_json = extract_json_objects(message)
        return message, score_json

    def evaluate(self, input_context, outputs, fs=True, calibrate=True, cot=True):
        message = self.instructer()
        if fs:
            message += prompt.EXAMPLE_PROMPTS[self.task]
        message += prompt.INPUT_PROMPT.replace("{raw_input}", input_context)
        if calibrate:
            assert isinstance(outputs, list)
            message += self.calibrator(outputs)
       
        if cot:
            message += prompt.SCORES_REASON_PROMPT
        else:
            message += prompt.SCORES_ONLY_PROMPT
        out, score = self.scorer(message)
        return out, score