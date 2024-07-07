from llm.model import openai_client
from constants import OPENAI_TTS_MODEL, OPENAI_TTS_VOICE


def text_to_speech(text: str, output_path: str):
    response = openai_client.audio.speech.create(
        model=OPENAI_TTS_MODEL, voice=OPENAI_TTS_VOICE, input=text
    )
    response.stream_to_file(output_path)
