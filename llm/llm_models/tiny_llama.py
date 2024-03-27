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
        self.context = "You will be an assistant who is going to respond concisely and directly to the question without additional details."

    def ask(self, message: str) -> str:
        input_text = f"{self.context}\nUser: {message}\nAssistant: "
        encoded_input = self.encode_text(input_text)
        output = self.model.generate(
            **encoded_input,
            max_length=512,
            pad_token_id=self.tokenizer.eos_token_id,
            temperature=0.1,
            top_k=20,
            top_p=0.6,
            repetition_penalty=1.2,
            no_repeat_ngram_size=2,
            num_return_sequences=1,
            do_sample=True,
        )

        # res = tokenizer.decode(output[0], skip_special_tokens=True)
        res = self.decode_text(output[0])
        answer_start = res.find("\nAssistant: ") + len("\nAssistant: ")
        answer: str = res[answer_start:]

        return answer

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

    def encode_text(self, input_text: str):
        "Transform a string to token to then be read by the model"
        return self.tokenizer(
            input_text,
            return_tensors='pt',
            padding=True,
            truncation=True, max_length=512
        ).to(self.device)

    def decode_text(self, output):
        "Transform a token from the model to string to be read by the user"
        return self.tokenizer.decode(output, skip_special_tokens=True)
