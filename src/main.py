from dotenv import load_dotenv
import time
import threading
from functools import partial

load_dotenv()

from interface.inputs import get_input
from camera.camera import setup_camera
from pilot.pilot import get_pilot
from robot.loop import loop
from robot.command_queue import CommandQueue


initial_state = "Initial"
latest_snapshot_path = "latest_snapshot.jpg"
command_queue = CommandQueue()
objective = ""
task_ended = None


def move(direction, duration=2, speed=None):
    command_queue.add_task({"type": "move", "arg": (direction, duration, speed)})


def turn(angle, speed=None):
    command_queue.add_task({"type": "turn", "arg": (angle, speed)})


def stop():
    command_queue.add_task({"type": "stop", "arg": None})


def end_task(message):
    def callback():
        global task_ended
        task_ended(message)
        return None

    command_queue.add_task({"type": "callback", "arg": callback})


tools_mapping = {
    "move": move,
    "turn": turn,
    "stop": stop,
    "end_task": end_task,
}


def main():
    global task_ended
    setup_camera(latest_snapshot_path, (720, 480), 0.5)
    pilot = get_pilot(tools_mapping, initial_state, latest_snapshot_path)

    def request_next_action():
        global objective
        pilot(objective)

    command_queue.add_request_next_action_fn(request_next_action)

    loop_thread = threading.Thread(target=partial(loop, command_queue))
    loop_thread.start()

    def set_goal(obj):
        global objective
        objective = obj
        request_next_action()

    task_ended = get_input(set_goal)
    loop_thread.join()


if __name__ == "__main__":
    main()
