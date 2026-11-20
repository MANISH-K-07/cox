
from fastapi import FastAPI
from pydantic import BaseModel

from app.synthesis.llm import ask_llm, get_model
from app.retrieval.graph_enhanced_search import graph_enhanced_search
from app.synthesis.answer_generator import generate_answer

from app.ingestion.pipeline import initialize_sample_data


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


class AITestRequest(BaseModel):
    prompt: str


@app.post("/ai/test")
def test_ai(request: AITestRequest):
    answer = ask_llm(request.prompt)

    return {
        "model": get_model(),
        "answer": answer
    }


class BriefRequest(BaseModel):
    question: str


@app.post("/briefs/generate")
def generate_brief(request: BriefRequest):
    retrieved_chunks = graph_enhanced_search(request.question)

    result = generate_answer(
        question=request.question,
        retrieved_chunks=retrieved_chunks
    )

    return result


@app.post("/ingest/sample-data")
def ingest_sample_data():
    result = initialize_sample_data()
    return result
