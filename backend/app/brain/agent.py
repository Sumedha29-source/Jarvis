from ollama import chat

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


MODEL = "qwen3:4b"


SYSTEM_PROMPT = """
You are JARVIS, an intelligent local desktop AI assistant.

You can talk naturally with the user and use tools to perform
real actions on their Windows computer.

Rules:
1. Use tools whenever the user asks you to perform an available action.
2. Never claim an action worked unless the tool confirms success.
3. For normal conversation, answer directly.
4. Keep responses concise and natural.
5. Never invent system information.
6. If you cannot perform something yet, say that clearly.
"""


def tool_open_application(app_name: str) -> dict:
    """
    Open an application on the user's computer.

    Args:
        app_name: Application name such as calculator,
                  Chrome, VS Code, Notepad or Paint.
    """
    return open_application(app_name)


def tool_google_search(query: str) -> dict:
    """
    Search Google.

    Args:
        query: The user's Google search query.
    """
    return google_search(query)


def tool_youtube_search(query: str) -> dict:
    """
    Search YouTube.

    Args:
        query: The user's YouTube search query.
    """
    return youtube_search(query)


def tool_get_cpu_usage() -> dict:
    """Get the current CPU usage."""
    return get_cpu_usage()


def tool_get_ram_usage() -> dict:
    """Get the current RAM usage."""
    return get_ram_usage()


def tool_get_battery_status() -> dict:
    """Get battery percentage and charging status."""
    return get_battery_status()


def tool_get_system_status() -> dict:
    """Get overall computer status."""
    return get_system_status()


TOOLS = [
    tool_open_application,
    tool_google_search,
    tool_youtube_search,
    tool_get_cpu_usage,
    tool_get_ram_usage,
    tool_get_battery_status,
    tool_get_system_status
]


FUNCTIONS = {
    "tool_open_application": tool_open_application,
    "tool_google_search": tool_google_search,
    "tool_youtube_search": tool_youtube_search,
    "tool_get_cpu_usage": tool_get_cpu_usage,
    "tool_get_ram_usage": tool_get_ram_usage,
    "tool_get_battery_status": tool_get_battery_status,
    "tool_get_system_status": tool_get_system_status
}


def run_jarvis(user_command: str):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_command
        }
    ]

    for _ in range(5):

        response = chat(
            model=MODEL,
            messages=messages,
            tools=TOOLS
        )

        messages.append(response.message)

        tool_calls = response.message.tool_calls or []

        # No tools requested = normal final response
        if not tool_calls:
            return {
                "success": True,
                "message": response.message.content
            }

        for call in tool_calls:

            function_name = call.function.name
            arguments = call.function.arguments

            function = FUNCTIONS.get(function_name)

            if function is None:
                result = {
                    "success": False,
                    "message": f"Unknown tool: {function_name}"
                }

            else:
                try:
                    result = function(**arguments)

                except Exception as error:
                    result = {
                        "success": False,
                        "message": str(error)
                    }

            # Give the actual tool result back to JARVIS
            messages.append(
                {
                    "role": "tool",
                    "tool_name": function_name,
                    "content": str(result)
                }
            )

    return {
        "success": False,
        "message": "Maximum number of tool actions reached."
    }
