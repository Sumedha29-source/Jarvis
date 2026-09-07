from app.brain.agent import run_jarvis

from app.voice.speech_to_text import listen
from app.voice.text_to_speech import speak


EXIT_COMMANDS = {
    "exit",
    "quit",
    "goodbye",
    "goodbye jarvis",
    "stop jarvis"
}


def clean_command(command: str) -> str:

    command = command.lower().strip()

    command = command.replace(".", "")
    command = command.replace(",", "")
    command = command.replace("?", "")
    command = command.replace("!", "")

    return command


def main():

    print("\n================================")
    print("       JARVIS VOICE MODE")
    print("================================\n")

    speak("JARVIS voice systems online.")

    while True:

        input(
            "\nPress ENTER when you're ready to speak..."
        )

        try:

            command = listen(duration=6)

        except Exception as error:

            print(
                f"\nMicrophone error: {error}"
            )

            continue

        if not command:

            print(
                "JARVIS: I couldn't hear anything."
            )

            continue

        print(
            f"\nYOU: {command}"
        )

        normalized = clean_command(command)

        if normalized in EXIT_COMMANDS:

            print(
                "\nJARVIS: Shutting down voice mode."
            )

            speak(
                "Voice mode shutting down."
            )

            break

        print(
            "\nJARVIS is thinking..."
        )

        result = run_jarvis(command)

        message = result.get(
            "message",
            "I couldn't complete that request."
        )

        print(
            f"\nJARVIS: {message}"
        )

        speak(message)


if __name__ == "__main__":
    main()