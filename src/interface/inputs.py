from interface.outputs import play_text_as_audio

def get_input(set_input):
    print("Setting Goal")
    # This should come from LLM
    set_input("Drive to the brown ball")
    
    def task_ended(msg):
        # This should be sent back to LLM
        print("Task ended with status: ", msg)
        play_text_as_audio(msg, "temp_output_audio_snapshot.mp3")
    
    return task_ended