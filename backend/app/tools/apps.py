import os
import shutil
import subprocess
import webbrowser
from urllib.parse import quote_plus


def open_application(app_name: str):
    app_name = app_name.lower().strip()

    simple_apps = {
        "calculator": "calc.exe",
        "calc": "calc.exe",
        "notepad": "notepad.exe",
        "paint": "mspaint.exe",
    }

    # Basic Windows apps
    if app_name in simple_apps:
        subprocess.Popen(simple_apps[app_name])

        return {
            "success": True,
            "message": f"Opening {app_name}."
        }

    # VS Code
    if app_name in ["vscode", "vs code", "visual studio code"]:

        code_path = shutil.which("code")

        if code_path:
            subprocess.Popen([code_path])

            return {
                "success": True,
                "message": "Opening Visual Studio Code."
            }

        possible_path = os.path.join(
            os.environ.get("LOCALAPPDATA", ""),
            "Programs",
            "Microsoft VS Code",
            "Code.exe"
        )

        if os.path.exists(possible_path):
            subprocess.Popen([possible_path])

            return {
                "success": True,
                "message": "Opening Visual Studio Code."
            }

        return {
            "success": False,
            "message": "Visual Studio Code was not found."
        }

    # Chrome
    if app_name in ["chrome", "google chrome"]:

        chrome_paths = [
            os.path.join(
                os.environ.get("PROGRAMFILES", ""),
                "Google",
                "Chrome",
                "Application",
                "chrome.exe"
            ),
            os.path.join(
                os.environ.get("PROGRAMFILES(X86)", ""),
                "Google",
                "Chrome",
                "Application",
                "chrome.exe"
            ),
            os.path.join(
                os.environ.get("LOCALAPPDATA", ""),
                "Google",
                "Chrome",
                "Application",
                "chrome.exe"
            ),
        ]

        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path])

                return {
                    "success": True,
                    "message": "Opening Google Chrome."
                }

        # Fallback
        webbrowser.open("https://www.google.com")

        return {
            "success": True,
            "message": "Chrome was not found, so I opened your default browser."
        }

    return {
        "success": False,
        "message": f"I don't know how to open '{app_name}' yet."
    }


def google_search(query: str):
    query = query.strip()

    if not query:
        return {
            "success": False,
            "message": "No search query was provided."
        }

    url = "https://www.google.com/search?q=" + quote_plus(query)

    webbrowser.open(url)

    return {
        "success": True,
        "message": f"Searching Google for {query}."
    }


def youtube_search(query: str):
    query = query.strip()

    if not query:
        return {
            "success": False,
            "message": "No search query was provided."
        }

    url = (
        "https://www.youtube.com/results?search_query="
        + quote_plus(query)
    )

    webbrowser.open(url)

    return {
        "success": True,
        "message": f"Searching YouTube for {query}."
    }