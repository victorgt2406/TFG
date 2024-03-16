from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
from transformers import pipeline, set_seed

# Define the request body model
class ChatInput(BaseModel):
    message: str

app = FastAPI()

# Set the default device to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device {device}")

# Initialize the pipeline for text-generation using TinyLlama
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
pipe = pipeline("text-generation", model=model_name, torch_dtype=torch.bfloat16, device_map=device)

# Set seed for reproducibility
set_seed(42)

@app.post("/chat")
async def chat_with_llama(chat_input: ChatInput):
    # Prepare the prompt
    messages = [
        {
            "role": "system",
            "content": "You are a friendly chatbot."
        },
        {
            "role": "user",
            "content": chat_input.message
        }
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # Generate a response
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    response_text = outputs[0]["generated_text"]
    
    # Extract the chatbot's response
    answer_start = response_text.rfind("Chatbot:") + len("Chatbot:")
    answer = response_text[answer_start:].strip()
    
    return {"response": answer}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
