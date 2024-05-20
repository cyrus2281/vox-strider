from dotenv import load_dotenv

from interface.inputs import get_input

load_dotenv()

from camera.camera import setup_camera
from pilot.pilot import get_pilot

# from robot.loop import loop

from pilot.pilot import get_pilot

initial_state = "Initial"
latest_snapshot_path = "latest_snapshot.jpg"
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

objective = ""

def main():
    setup_camera(latest_snapshot_path, 0.5)
    pilot = get_pilot(tools_mapping, initial_state, latest_snapshot_path)
    
    def set_goal(obj):
        global objective
        objective = obj
        pilot(objective)
    
    get_input(set_goal)
    
    # loop(command_queue)

if __name__ == "__main__":
    main()
