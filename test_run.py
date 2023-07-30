import re
import json
import openai
from collections import Counter
from llm_code_eval import ICE

if __name__ == "__main__":
    openai.api_key = "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"
    ice = ICE(task="nl2c", model_name="gpt-4")
    inputs, outputs = ("I want to do substraction for two numbers", ["def add(a, b): return a + b", "def add(a, b): return a - b", "def substract(a, b): return a - b"])
    out, score = ice.evaluate(inputs, outputs, fs=True, calibrate=True, cot=True)
    with open("tmp.txt","w") as f:
        f.write(out)