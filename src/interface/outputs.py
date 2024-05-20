import subprocess
from llm.model import openai_client
    
def play_text_as_audio(text, output_path):
    response = openai_client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=text
    )
    response.stream_to_file(output_path)
    subprocess.run(['aplay', output_path])
