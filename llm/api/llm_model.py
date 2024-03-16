"Function to load the LLM choosen"
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from printlog import PrintlogEnum, printlog


def generate_llm_tokenizer(device:str = "cuda" if torch.cuda.is_available() else "cpu", model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    "Return the model selected"

    printlog(f"The LLM is using {device}", PrintlogEnum.INFO)
    torch.set_default_device(device)

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    # else:
    #     raise ValueError("ERROR: Tokenizer Error, Model did not load correctly")

    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", trust_remote_code=True).to(device)

    return model, tokenizer


def encode_text(text:str, tokenizer, device="cuda" if torch.cuda.is_available() else "cpu"):
    return tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)

def decode_text(output, tokenizer):
    return tokenizer.decode(output, skip_special_tokens=True)