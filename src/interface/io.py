import os

from interface.inputs import record_on_sound_activity
from interface.outputs import play_audio
from llm.stt import speech_to_text
from llm.tts import text_to_speech


def get_input(set_input):
    print("Setting Goal")
    # Temporarily in audio path
    temp_in_audio_path = "temp_in_audio_snapshot.wav"
    # Get the audio input from the user
    record_on_sound_activity(temp_in_audio_path)
    # Convert the audio input to text
    input_text = speech_to_text(temp_in_audio_path)
    print("User Goal:", input_text)
    # Set the input text
    set_input(input_text)
    # remove the temporary audio file
    os.remove(temp_in_audio_path)

    def task_ended(msg):
        # This should be sent back to LLM
        print("Task ended with status: ", msg)
        # Temporarily out audio path
        temp_output_audio_path = "temp_output_audio_snapshot.mp3"
        # Convert the text to audio
        text_to_speech(msg, temp_output_audio_path)
        # Play the audio
        play_audio(temp_output_audio_path)

    return task_ended
