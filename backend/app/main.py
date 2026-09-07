from fastapi import FastAPI
from pydantic import BaseModel

from app.tools.apps import open_application


app = FastAPI(
    title="JARVIS",
    version="0.1.0"
)


class CommandRequest(BaseModel):
    command: str


@app.get("/")
def home():
    return {
        "name": "JARVIS",
        "status": "online",
        "message": "All systems operational."
    }


@app.post("/command")
def command(request: CommandRequest):
    command_text = request.command.lower()

    if command_text.startswith("open "):
        app_name = command_text.replace("open ", "", 1)

        return open_application(app_name)

    return {
        "success": False,
        "message": "Command not understood."
    }