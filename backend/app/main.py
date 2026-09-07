from fastapi import FastAPI
from pydantic import BaseModel

from app.brain.agent import run_jarvis


app = FastAPI(
    title="JARVIS",
    description="Multimodal Local AI Desktop Assistant",
    version="0.3.0"
)


class CommandRequest(BaseModel):
    command: str


@app.get("/")
def home():
    return {
        "name": "JARVIS",
        "version": "0.3.0",
        "brain": "Qwen3 4B",
        "status": "online",
        "message": "All systems operational."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/command")
def process_command(request: CommandRequest):
    return run_jarvis(request.command)