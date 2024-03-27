import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from printlog import PrintlogEnum, printlog

class TinyLlamaChat:
    def __init__(self, model_name="PY007/TinyLlama-1.1B-Chat-v0.4", device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")
        printlog(f"Initializing TinyLlama with device: {self.device}", PrintlogEnum.INFO)
        
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto").to(self.device)
        
        self.pipeline = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            torch_dtype=torch.float16,
            device_map="auto" if self.device == "cuda" else None
        )
        
        self.CHAT_EOS_TOKEN_ID = 32002  # End-of-sequence token ID for chat
    
    def ask(self, prompt, max_new_tokens=1024, top_k=50, top_p=0.9, num_return_sequences=1, repetition_penalty=1.1):
        formatted_prompt = f"user\n{prompt}\nassistant\n"
        sequences = self.pipeline(
            formatted_prompt,
            do_sample=True,
            top_k=top_k,
            top_p=top_p,
            num_return_sequences=num_return_sequences,
            repetition_penalty=repetition_penalty,
            max_new_tokens=max_new_tokens,
            eos_token_id=self.CHAT_EOS_TOKEN_ID,
        )
        return sequences

# Example usage:
if __name__ == "__main__":
    chat_model = TinyLlamaChat()
    prompt = "How to get in a good university?"
    sequences = chat_model.ask(prompt)
    
    for seq in sequences:
        print(f"Result: {seq['generated_text']}")
