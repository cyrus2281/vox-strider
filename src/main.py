import threading
from functools import partial
from dotenv import load_dotenv

load_dotenv()

from constants import (
    INITIAL_STATE,
    LATEST_SNAPSHOT_PATH,
    TURN_ON_CAMERA,
    TURN_ON_PILOT,
)
from interface.io import get_input
from pilot.pilot import get_pilot
from robot.loop import loop
from robot.command_queue import CommandQueue

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
        global task_ended, objective
        objective = None
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

    if TURN_ON_CAMERA:
        from camera.camera import setup_camera

        setup_camera(LATEST_SNAPSHOT_PATH, (720, 480), 0.5)

    pilot = get_pilot(tools_mapping, INITIAL_STATE, LATEST_SNAPSHOT_PATH)

    def request_next_action():
        global objective, task_ended
        nonlocal set_goal
        if TURN_ON_PILOT:
            if objective:
                pilot(objective)
            else:
                task_ended = get_input(set_goal)

    def set_goal(obj):
        global objective
        objective = obj
        request_next_action()

    command_queue.add_request_next_action_fn(request_next_action)

    loop_thread = threading.Thread(target=partial(loop, command_queue))
    loop_thread.start()

    loop_thread.join()


if __name__ == "__main__":
    main()
