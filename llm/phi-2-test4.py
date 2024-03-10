import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Set the default device to GPU if available
torch.set_default_device("cuda")

# Load the model and tokenizer
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)

# Function to ask questions to the model
def ask_model():
    while True:
        # Get the question from user input
        question = input("Enter your question (or 'quit' to stop): ")
        if question.lower() == 'quit':
            break

        # Tokenize and generate the answer
        inputs = tokenizer.encode(question, return_tensors="pt", return_attention_mask=True)
        outputs = model.generate(inputs, max_length=200, pad_token_id=tokenizer.eos_token_id)
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        print(answer)

# Run the ask model function
ask_model()
