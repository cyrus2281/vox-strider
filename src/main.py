from dotenv import load_dotenv
load_dotenv()

from camera.camera import setup_camera
from pilot.pilot import get_pilot
# from robot.loop import loop

from pilot.pilot import get_pilot

initial_state = "Initial"
command_queue = []

def move(direction):
    print("fn move", direction)

def turn(angle):
    print("fn turn", angle)
    
def stop():
    print("fn stop")
    
def end_task(message):
    print("fn end_task", message)
    
tools_mapping = {
    "move": move,
    "turn": turn,
    "stop": stop,
    "end_task": end_task,
}

def main():
    camera = setup_camera()
    pilot = get_pilot(tools_mapping, initial_state)
    pilot("Drive to the brown ball") # this should come to inputs
    # loop(command_queue)

if __name__ == "__main__":
    main()