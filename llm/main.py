import os
from dotenv import load_dotenv
from fastapi import FastAPI
from api_models import AskModel, ContextModel
from llm_models import TinyLlamaChatBot

load_dotenv()

app = FastAPI()
llm_model = TinyLlamaChatBot()

@app.post("/ask")
async def ask(question: AskModel):
    "ask to the model"
    answer = llm_model.ask(question.message)
    return answer

@app.post("/get_terms")
async def get_terms(question: AskModel):
    "ask to the model"
    answer = llm_model.get_terms(question.message)
    return answer

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("LLM_PORT") or 3001)
    print(f"Running LLM API at http://localhost:{port} 🚀")
    uvicorn.run(app, host="0.0.0.0", port=port)
