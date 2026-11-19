from fastapi import FastAPI
# check 2
from pydantic import BaseModel
from app.synthesis.llm import ask_llm, get_model

app = FastAPI(
    title="Co-X API",
    description="AI-powered knowledge synthesis backend",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "project": "Co-X",
        "status": "running",
        "message": "Welcome to the Co-X backend!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

# check 2
class AITestRequest(BaseModel):
    prompt: str


@app.post("/ai/test")
def test_ai(request: AITestRequest):
    answer = ask_llm(request.prompt)

    return {
        "model": get_model(),
        "answer": answer
    }
