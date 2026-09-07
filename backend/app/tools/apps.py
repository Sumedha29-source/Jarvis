import subprocess
import webbrowser


def open_application(app_name: str):
    app_name = app_name.lower().strip()

    applications = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe"
    }

    if app_name in applications:
        subprocess.Popen(applications[app_name])

        return {
            "success": True,
            "message": f"Opening {app_name}"
        }

    if app_name == "chrome":
        webbrowser.open("https://www.google.com")

        return {
            "success": True,
            "message": "Opening browser"
        }

    return {
        "success": False,
        "message": f"I don't know how to open {app_name} yet."
    }