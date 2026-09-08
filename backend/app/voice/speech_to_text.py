import os
import tempfile

import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000

_models = {}


def get_model(model_size: str = "base"):
    if model_size not in _models:
        print(f"Loading Whisper '{model_size}' model...")

        _models[model_size] = WhisperModel(
            model_size,
            device="cpu",
            compute_type="int8"
        )

    return _models[model_size]


def listen(
    duration: float = 6,
    model_size: str = "base",
    announce: bool = True
) -> str:

    if announce:
        print(f"\n🎙 Listening for {duration} seconds...")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    if announce:
        print("✓ Recording complete.")
        print("🧠 Transcribing...")

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_path = temp_file.name
    temp_file.close()

    sf.write(
        temp_path,
        audio,
        SAMPLE_RATE
    )

    try:
        model = get_model(model_size)

        segments, _ = model.transcribe(
            temp_path,
            beam_size=3,
            vad_filter=True,
            condition_on_previous_text=False
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)