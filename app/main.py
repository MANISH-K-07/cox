from fastapi import FastAPI

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
