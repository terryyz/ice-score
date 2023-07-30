from typing import Dict
from transformers import StoppingCriteria, StoppingCriteriaList

class EndOfFunctionCriteria(StoppingCriteria):
    """Custom `StoppingCriteria` which checks if all generated functions in the batch are completed."""

    def __init__(self, start_length, eof_strings, tokenizer):
        self.start_length = start_length
        self.eof_strings = eof_strings
        self.tokenizer = tokenizer

    def __call__(self, input_ids, scores, **kwargs):
        """Returns true if all generated sequences contain any of the end-of-function strings."""
        decoded_generations = self.tokenizer.batch_decode(
            input_ids[:, self.start_length :]
        )
        done = []
        for decoded_generation in decoded_generations:
            done.append(
                any(
                    [
                        stop_string in decoded_generation
                        for stop_string in self.eof_strings
                    ]
                )
            )
        return all(done)

def create_model_config(
    message: str,
    max_new_tokens: int=1024,
    temperature: float = 0.2,
    top_p: float = 0.95,
    repetition_penalt: float = 1.2
) -> Dict:
    config = {
            "message": message,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "repetition_penalty": repetition_penalt,
        }
    return config

def request_model_engine(
    tokenizer,
    model,
    config: Dict
):
    message = config.pop("message")
    prompt_tokenized = tokenizer(message, return_tensors="pt")
    input_ids = prompt_tokenized["input_ids"].to('cuda')
    token_len = input_ids.shape[1]

    stop_words=["<|user|>", "<|end|>", "### End"]
    stopping_criteria = StoppingCriteriaList([EndOfFunctionCriteria(token_len, stop_words, tokenizer)])
    outputs = model.generate(
                            input_ids,
                            **config,
                            eos_token_id=tokenizer.eos_token_id,
                            pad_token_id=tokenizer.pad_token_id, 
                            stopping_criteria=stopping_criteria
                            )
    return tokenizer.decode(outputs[:, token_len:][0])