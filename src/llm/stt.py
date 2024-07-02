from llm.model import openai_client


def speech_to_text(audio_path: str):
    response = openai_client.audio.speech.create(
        model="stt-1", voice="echo", input=audio_path
    )
    return response.get("transcription")
