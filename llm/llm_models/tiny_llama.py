import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, PreTrainedTokenizer, PreTrainedModel
from llm_models.template import LlmTemplate
from printlog import PrintlogEnum, printlog


class TinyLlamaChatBot(LlmTemplate):
    def __init__(self) -> None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
        model, tokenizer = self.generate_llm_tokenizer(
            model_name=name, device=device)
        super().__init__(name, tokenizer, model, device)
        # self.context = "You will be an assistant who is going to respond concisely and directly to the question without additional details."

    def ask(self, message: str) -> str:

        context = "You will be an assistant who is going to respond concisely and directly to the question without additional details."
        msg_start = "\nUser: "
        msg_end = "\nAssistant: "
        answer = self.generate_text(message, context, msg_start, msg_end)

        return answer
    
    def get_terms(self, message: str) -> str:

        context = """You are an assistant programmed to extract specific terms from a given text. 
        Your task is to identify key terms related to the prompt and list them separated by commas,
        like in this example: "ExampleText: ... \nExampleTerms: term 1, "term 2, ..., term n".
        No explanations, interpretations, or any supplementary information. Only listing the terms as they are requested.
        """
        msg_start = "\nText: "
        msg_end = "\nTerms: "

        response = self.generate_text(message, context, msg_start, msg_end)
        print(response)

        response = response.lower()
        response = response.split("\n")[0]
        response = response.strip()
        response = response.replace(", ",",")
        response = response.replace(".","")
        response = response.replace(" ","-")
        
        print(response)
        response_list = response.split(",")
        return response_list

    def generate_llm_tokenizer(self, model_name: str, device: str) -> tuple[PreTrainedModel, PreTrainedTokenizer]:
        "Return the model selected"

        printlog(f"The LLM is using {device}", PrintlogEnum.INFO)
        torch.set_default_device(device)

        tokenizer = AutoTokenizer.from_pretrained(
            model_name, trust_remote_code=True)

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            model_name, torch_dtype="auto", trust_remote_code=True).to(device)

        printlog("✅ The LLM and Tokenizer are ready!", PrintlogEnum.INFO)
        return model, tokenizer
