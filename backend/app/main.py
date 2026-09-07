from fastapi import FastAPI
from pydantic import BaseModel

from app.tools.apps import (
    open_application,
    google_search,
    youtube_search
)

from app.tools.system import (
    get_cpu_usage,
    get_ram_usage,
    get_battery_status,
    get_system_status
)


app = FastAPI(
    title="JARVIS",
    description="Multimodal AI Desktop Assistant",
    version="0.2.0"
)


class CommandRequest(BaseModel):
    command: str


@app.get("/")
def home():
    return {
        "name": "JARVIS",
        "version": "0.2.0",
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

    command = request.command.lower().strip()

    # OPEN APPLICATION
    if command.startswith("open "):

        app_name = command.removeprefix("open ").strip()

        return open_application(app_name)

    # GOOGLE SEARCH
    if command.startswith("search google for "):

        query = command.removeprefix(
            "search google for "
        ).strip()

        return google_search(query)

    # YOUTUBE SEARCH
    if command.startswith("search youtube for "):

        query = command.removeprefix(
            "search youtube for "
        ).strip()

        return youtube_search(query)

    # CPU
    if command in [
        "cpu usage",
        "cpu status",
        "check cpu"
    ]:
        return get_cpu_usage()

    # RAM
    if command in [
        "ram usage",
        "memory usage",
        "ram status"
    ]:
        return get_ram_usage()

    # BATTERY
    if command in [
        "battery",
        "battery status",
        "battery percentage"
    ]:
        return get_battery_status()

    # SYSTEM
    if command in [
        "system status",
        "computer status",
        "system info"
    ]:
        return get_system_status()

    return {
        "success": False,
        "message": (
            "I understood your request as a command, "
            "but I don't have a tool for it yet."
        )
    }