import re
import time

from app.brain.agent import run_jarvis
from app.voice.speech_to_text import listen
from app.voice.text_to_speech import speak


WAKE_PHRASES = [
    "hey jarvis",
    "jarvis",
    "hey jervis",
    "jervis"
]


SHUTDOWN_COMMANDS = [
    "shutdown voice mode",
    "shut down voice mode",
    "stop listening",
    "go offline",
    "goodbye"
]


def normalize(text: str) -> str:
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        "",
        text
    )

    return text.strip()


def detect_wake_word(text: str):
    normalized = normalize(text)

    for phrase in WAKE_PHRASES:

        position = normalized.find(phrase)

        if position != -1:

            command_after_wake = normalized[
                position + len(phrase):
            ].strip()

            return True, command_after_wake

    return False, ""


def should_shutdown(command: str) -> bool:
    command = normalize(command)

    return any(
        phrase in command
        for phrase in SHUTDOWN_COMMANDS
    )


def execute_command(command: str):

    if not command:
        return

    print(
        f"\nYOU: {command}"
    )

    if should_shutdown(command):

        print(
            "\nJARVIS: Voice systems going offline."
        )

        speak(
            "Voice systems going offline."
        )

        return "shutdown"

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

    return "continue"


def main():

    print(
        "\n================================"
    )

    print(
        "       JARVIS WAKE MODE"
    )

    print(
        "================================"
    )

    print(
        '\nSay "Hey Jarvis" to activate me.'
    )

    speak(
        "Wake word systems online."
    )

    while True:

        try:

            # Short low-cost listening window
            heard = listen(
                duration=3,
                model_size="tiny",
                announce=False
            )

            if not heard:
                continue

            detected, inline_command = detect_wake_word(
                heard
            )

            if not detected:
                continue

            print(
                f"\n🔵 WAKE WORD DETECTED: {heard}"
            )

            # Example:
            # "Hey Jarvis open calculator"
            if inline_command:

                result = execute_command(
                    inline_command
                )

                if result == "shutdown":
                    break

                time.sleep(1)

                continue

            # Example:
            # "Hey Jarvis"
            speak(
                "Yes?"
            )

            print(
                "\nJARVIS: Yes?"
            )

            command = listen(
                duration=6,
                model_size="base",
                announce=True
            )

            if not command:

                print(
                    "\nJARVIS: I didn't hear a command."
                )

                continue

            result = execute_command(
                command
            )

            if result == "shutdown":
                break

            # Prevent immediately hearing its own voice
            time.sleep(1)

        except KeyboardInterrupt:

            print(
                "\nJARVIS wake mode stopped."
            )

            break

        except Exception as error:

            print(
                f"\nWake mode error: {error}"
            )

            time.sleep(1)


if __name__ == "__main__":
    main()