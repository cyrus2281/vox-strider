from llm.model import openai_client
from constants import OPENAI_STT_MODEL


def speech_to_text(audio_path: str):
    audio_file = open(audio_path, "rb")
    transcription = openai_client.audio.transcriptions.create(
        model=OPENAI_STT_MODEL, file=audio_file
    )
    return transcription.text
