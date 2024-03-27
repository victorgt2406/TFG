from abc import ABC, abstractmethod
from transformers import PreTrainedTokenizer, PreTrainedModel


class LlmTemplate(ABC):
    """
    Abstract class for any LLM that supports the Hugging Face Transformers Library

    - Method `ask` should be implemented to process the message and return a string with response to that message
    """

    def __init__(self, name, tokenizer: PreTrainedTokenizer, model: PreTrainedModel) -> None:
        self.name = name
        self.tokenizer = tokenizer
        self.model = model

    @ abstractmethod
    def ask(self, message: str) -> str:
        """
        From a message, the LLM process it and return a response
        """
        raise NotImplementedError("The ask method needs to be implemented by subclasses.")