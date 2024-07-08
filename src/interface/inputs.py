from time import sleep
import pyaudio
import numpy as np
import wave

from constants import (
    AUDIO_BUFFER_CHUNK_SIZE,
    AUDIO_INPUT_RATE,
    AUDIO_NUMBER_OF_SILENT_SECONDS,
    AUDIO_THRESHOLD,
)

def record_on_sound_activity(
    output_filename,
    threshold=AUDIO_THRESHOLD,
    chunk_size=AUDIO_BUFFER_CHUNK_SIZE,
    format=pyaudio.paInt16,
    channels=1,
    rate=AUDIO_INPUT_RATE,
    num_of_silent_seconds=AUDIO_NUMBER_OF_SILENT_SECONDS,
    on_start_listening=None,
    on_stop_listening=None,
):
    on_start_listening and on_start_listening()

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    print("Listening for sound activity...")

    silent_chunks = 0
    frames = []
    recording = False
    max_silent_chunks = int(
        rate / chunk_size * num_of_silent_seconds
    )  # number of silence

    try:
        while True:
            sleep(0.001)
            data = stream.read(chunk_size)
            np_data = np.frombuffer(data, dtype=np.int16)
            volume = np.abs(np_data).mean()

            if volume > threshold:
                if not recording:
                    print("Sound detected, starting recording...")
                    recording = True
                    frames = []
                silent_chunks = 0
                frames.append(data)
            elif recording:
                silent_chunks += 1
                frames.append(data)
                if silent_chunks > max_silent_chunks:
                    print("Silence detected, stopping recording...")
                    recording = False
                    frames = frames[
                        : -int(rate / chunk_size * (num_of_silent_seconds - 1))
                    ]  # Remove the silent buffer - 1 second
                    break
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

    on_stop_listening and on_stop_listening()
    print(f"Saving audio to {output_filename}")
    wf = wave.open(output_filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()
