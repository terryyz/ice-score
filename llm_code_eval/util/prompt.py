INSTRUCTER_PROMPT = """You are a helpful following assistant whose goal is to formalize the given instruction and instruct the annotators to carefully follow the instruction and output the scores for each sample in a batch. The output shall be in a JSON object with the sample index as the key, e.g. {"0": SCORE_0, "1": SCORE_1, "2": SCORE_2}. You need to make the instruction in the same structure as the the following one:

## Annotation Guideline
In this task, we will ask you to select the preferred output AI model's responses to instructions.

You will read a batch of examples, which are composed of the following:

1. an Instruction we give to the AI system
2. an Input that is provided along with the instruction
3. Output (a), the first output from the AI system
4. Output (b), the first output from the AI system

Your task is to decide which response is better for each example. There are several dimensions that you can think along. Consider the following questions:

1. Is the response helpful? For example, if the instruction asked for a recipe for healthy food, and the response is a useful recipe, then we can consider it helpful.
2. Is the response language natural? For example, AI responses often have repetitions, which is not natural.
3. Is the response factual/accurate? For example, AI responses often make up new information. For example, if the response claims that Donald Trump is the current U.S. president, then you should consider it inaccurate.
4. and so on ... ultimately, you should decide which response is better based on your judgment and based on your own preference.

You should answer using only {"a": SCORE_0, "b": SCORE_1} depending on which response is better.

==================================================================================================================

Input Brief Instruction To be Formalized:

{raw_instruction}
"""

NL2C_EXAMPLE_PROMPT = """
## Input:
send a signal `signal.SIGUSR1` to the current process

### Output "0":
os.system('<unk>.png',s = 300)

### Output "1":
sys.signal(`signal.SIGUSR1`)

### Output "2":
os.system(`signal.SIGUSR1`)

### Output "3":
os.system(`< unk > < unk > < unk >`)

### Output "4":
os.kill(os.getpid(), signal.SIGUSR1)

### Reasoning Steps:
"0": The code snippet is completely unrelated to the problem. It is attempting to execute a system command with an unknown argument and a size parameter. There is no mention of signals or the current process.
"1": The code snippet uses the `sys.signal()` function to send a signal `signal.SIGUSR1`.
"2": The code snippet uses the `os.system()` function to send the signal `signal.SIGUSR1`. However, the argument passed to `os.system()` is incorrect. `signal.SIGUSR1` should be passed as an integer value, not a string.
"3": The code snippet uses the `os.system()` function, but the arguments are unknown.
"4": The code snippet uses the `os` and `signal` modules to send the required signal to the current process using the `os.kill()` function, though it can be simplified by using the `sys.signal()` function instead.

### Scores (scores only):
{"0": 0, "1": 4, "2": 1, "3": 0, "4": 3}
"""

C2NL_EXAMPLE_PROMPT = """
"""

C2C_EXAMPLE_PROMPT = """
"""

INPUT_PROMPT = """
### Input:

{raw_input}
"""

MODEL_OUT_PROMPT = """
### Index \"{raw_index}\" Output:

{raw_input}
"""

SCORES_REASON_PROMPT = """
### Reasoning Steps:
"""

SCORES_ONLY_PROMPT = """
### Scores (scores only):
"""

EXAMPLE_PROMPTS = {
    "nl2c": NL2C_EXAMPLE_PROMPT,
    "c2nl": C2NL_EXAMPLE_PROMPT,
    "c2c": C2C_EXAMPLE_PROMPT
}