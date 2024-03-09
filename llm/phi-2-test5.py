import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set the default device to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device {device}")
torch.set_default_device(device)

# Load the model and tokenizer
model_name = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Explicitly set the pad token to eos_token if not already set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", trust_remote_code=True).to(device)

# Function to ask a question with pre-context
def give_context(context:str):
    encoded_input = tokenizer(context, return_tensors='pt', padding=True, truncation=True, max_length=256).to(device)
    
    # Generate an answer from the model
    outputs = model.generate(**encoded_input, max_length=256, pad_token_id=tokenizer.eos_token_id, temperature=0.7, top_k=50)

    # Decode the generated tokens to a string and print the answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(answer)

# Function to ask a question with pre-context
def answer(question:str):
    # Tokenize the pre-context and the question together
    encoded_input = tokenizer("User: " + question + "\nAssistant: ", return_tensors='pt', padding=True, truncation=True, max_length=256).to(device)
    
    # Generate an answer from the model
    outputs = model.generate(**encoded_input, max_length=256, pad_token_id=tokenizer.eos_token_id, temperature=0.7, top_k=50)

    # Decode the generated tokens to a string and print the answer
    res = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Output only the answer, not the pre-context
    # print(answer.split("\nAssistant: ")[-1].strip())
    print(res)

# Loop to ask multiple questions
if __name__ == "__main__":
    give_context("You will be an assistant who is goint to be asked in spanish or english. You will answer with the same language asked. You will respond with next questions.")
    while True:
        question = input("Enter your question (or type 'quit' to exit): ")
        if question.lower() == 'quit':
            break

        answer(question)
