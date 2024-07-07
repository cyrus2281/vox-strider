import pyaudio
import wave

from constants import AUDIO_BUFFER_CHUNK_SIZE


def play_audio(filename: str):
    # Open the WAV file
    wf = wave.open(filename, "rb")

    # Create a PyAudio instance
    p = pyaudio.PyAudio()

    # Open a stream with the appropriate settings
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )

    # Read data in chunks and play
    chunk_size = AUDIO_BUFFER_CHUNK_SIZE
    data = wf.readframes(chunk_size)

    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()
