import os
import tempfile

import sounddevice as sd
import soundfile as sf
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
MODEL_SIZE = "base"

_model = None


def get_model():
    global _model

    if _model is None:
        print("Loading Whisper model...")

        _model = WhisperModel(
            MODEL_SIZE,
            device="cpu",
            compute_type="int8"
        )

    return _model


def listen(duration: int = 6) -> str:

    print(f"\n🎙 Listening for {duration} seconds...")

    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

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

        model = get_model()

        segments, _ = model.transcribe(
            temp_path,
            beam_size=5,
            vad_filter=True
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        )

        return text.strip()

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)