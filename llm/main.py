import os
from dotenv import load_dotenv
from fastapi import FastAPI
from models import AskModel
from llm_model import generate_llm_tokenizer, encode_text, decode_text

load_dotenv()

app = FastAPI()

model, tokenizer = generate_llm_tokenizer()

llm_context = {
    "pre_context": "You will be an assistant who is going to respond concisely and directly to the question without additional details.",
}

@app.post("/ask")
async def ask(question: AskModel):
    "Gets a question form the message field of the json body and returns an answer to the question"

    pre_context = "You will be an assistant who is going to respond concisely and directly to the question without additional details."
    str_input = f"{pre_context}\nUser: {question.message}\nAssistant: "
    encoded_input = encode_text(str_input, tokenizer)
    # Generate an answer from the model
    output = model.generate(
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

    # res = tokenizer.decode(output[0], skip_special_tokens=True)
    res = decode_text(output[0], tokenizer)
    answer_start = res.find("\nAssistant: ") + len("\nAssistant: ")
    answer = res[answer_start:]
    
    return {"answer": answer}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("LLM_PORT")) # type: ignore
    print(f"Running LLM API at http://localhost:{port} 🚀")
    uvicorn.run(app, host="0.0.0.0", port=port)
