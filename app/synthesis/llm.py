import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is missing from .env")

    return OpenAI(api_key=api_key)


def get_model():
    return os.getenv("OPENAI_MODEL", "gpt-6-luna")


def ask_llm(prompt: str) -> str:
    client = get_client()
    model = get_model()

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text
