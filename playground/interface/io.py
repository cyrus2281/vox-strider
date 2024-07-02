import pyaudio
import numpy as np
import wave

def record_on_sound_activity(output_filename, threshold=500, chunk_size=1024, format=pyaudio.paInt16, channels=1, rate=44100, number_of_silent_seconds=2):
    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
    
    print("Listening for sound activity...")
    
    silent_chunks = 0
    frames = []
    recording = False
    max_silent_chunks = int(rate / chunk_size * number_of_silent_seconds)  # number_of_silent_seconds of silence

    try:
        while True:
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
                    frames = frames[:-max_silent_chunks]  # Remove the last number_of_silent_seconds of silence
                    break
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
    
    print(f"Saving audio to {output_filename}")
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(filename):
    # Open the WAV file
    wf = wave.open(filename, 'rb')

    # Create a PyAudio instance
    p = pyaudio.PyAudio()

    # Open a stream with the appropriate settings
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read data in chunks and play
    chunk_size = 1024
    data = wf.readframes(chunk_size)

    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()
   

if __name__ == '__main__':
    output_path = 'output_snapshot.wav'
    record_on_sound_activity(output_path) 
    play_audio(output_path)