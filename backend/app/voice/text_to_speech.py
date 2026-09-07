import pyttsx3


_engine = pyttsx3.init()

_engine.setProperty(
    "rate",
    180
)


def speak(text: str):

    if not text:
        return

    _engine.say(text)
    _engine.runAndWait()