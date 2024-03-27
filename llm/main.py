import os
from dotenv import load_dotenv
from fastapi import FastAPI
from api_models import AskModel
from llm_models import TinyLlamaChatBot

load_dotenv()

app = FastAPI()
llm_model = TinyLlamaChatBot()

@app.post("/ask")
async def ask(question: AskModel):
    answer = llm_model.ask(question.message)
    # return {"answer": answer}
    return answer

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("LLM_PORT") or 3000)
    print(f"Running LLM API at http://localhost:{port} 🚀")
    uvicorn.run(app, host="0.0.0.0", port=port)
