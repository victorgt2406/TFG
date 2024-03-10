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

# Function to answer a question with pre-context
def answer(question:str):
    # Pre-context to be included with every question
    pre_context = "You will be an assistant who is going to respond concisely and directly to the question without additional details."
    
    # Tokenize the pre-context and the question together
    input_text = f"{pre_context}\nUser: {question}\nAssistant: "
    encoded_input = tokenizer(input_text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(device)
    
    # Generate an answer from the model
    outputs = model.generate(
    **encoded_input,
    max_length=512,
    pad_token_id=tokenizer.eos_token_id,
    temperature=0.1,
    top_k=20,
    top_p=0.6,
    repetition_penalty=1.2,
    no_repeat_ngram_size=2,
    num_return_sequences=1,
    do_sample=True,
)

    # Decode the generated tokens to a string
    res = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Output only the answer, removing the input text
    answer_start = res.find("\nAssistant: ") + len("\nAssistant: ")
    print(res[answer_start:])

# Start the question-answer loop
if __name__ == "__main__":
    while True:
        question = input("Enter your question (or type 'quit' to exit): ")
        if question.lower() == 'quit':
            break

        answer(question)
