import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set the default device to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
torch.set_default_device(device)

# Load the model and tokenizer
model_name = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Explicitly set the pad token to eos_token if not already set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", trust_remote_code=True).to(device)

pre_context = "The following is a series of questions and answers on various topics:"

# Function to ask a question with pre-context
def ask_question_with_context(question):
    # Tokenize the pre-context and the question together
    encoded_input = tokenizer(pre_context + "\nQ: " + question + "\nA:", return_tensors='pt', padding=True, truncation=True, max_length=256).to(device)
    
    # Generate an answer from the model
    outputs = model.generate(**encoded_input, max_length=256, pad_token_id=tokenizer.eos_token_id, temperature=0.7, top_k=50)

    # Decode the generated tokens to a string and print the answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Output only the answer, not the pre-context
    print(answer.split("\nA:")[-1].strip())

# Loop to ask multiple questions
if __name__ == "__main__":
    while True:
        question = input("Enter your question (or type 'quit' to exit): ")
        if question.lower() == 'quit':
            break

        ask_question_with_context(question)
