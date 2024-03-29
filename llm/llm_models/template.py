from abc import ABC, abstractmethod
from transformers import PreTrainedTokenizer, PreTrainedModel


class LlmTemplate(ABC):
    """
    Abstract class for any LLM that supports the Hugging Face Transformers Library

    - Method `ask` should be implemented to process the message and return a string with response to that message
    """

    def __init__(self, name:str, tokenizer: PreTrainedTokenizer, model: PreTrainedModel, device: str) -> None:
        self.name = name
        self.tokenizer = tokenizer
        self.model = model
        self.device = device
    
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

    def generate_text(self, message:str, context:str, msg_start:str, msg_end:str) -> str:
        "Send a message to the LLM to create text"
        input_text = f"{context}{msg_start}{message}{msg_end}"
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
        answer_start = res.find(msg_end) + len(msg_end)
        answer: str = res[answer_start:]

        return answer

    @ abstractmethod
    def ask(self, message: str) -> str:
        """
        From a message, the LLM will response to the question as an Assistant
        """
        raise NotImplementedError("The ask method needs to be implemented by subclasses.")
    
    @ abstractmethod
    def get_terms(self, message: str) -> str:
        """
        From a message, the LLM will response with a list of terms from the text provided
        """
        raise NotImplementedError("The ask method needs to be implemented by subclasses.")