from llm.model import openai_client


def text_to_speech(text: str, output_path: str):
    response = openai_client.audio.speech.create(
        model="tts-1", voice="echo", input=text
    )
    response.stream_to_file(output_path)
