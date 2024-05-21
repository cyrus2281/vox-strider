from robot.controllers.dc_motor import Direction, Speed
import threading
# 90 degrees takes 1 second
turn_multiplier = 1 / 90


class CommandQueue:

    def __init__(self, request_next_action=None):
        self.queue = []
        self.pending_request_action = False

        if request_next_action:
            self.request_next_action_fn = request_next_action

    def add_request_next_action_fn(self, fn):
        self.request_next_action_fn = fn
        
    def request_next_action(self):
        if self.pending_request_action:
            return
        print("CommandQueue: Request next action")
        self.pending_request_action = True
        loop_thread = threading.Thread(target=self.request_next_action_fn)
        loop_thread.start()


    def size(self):
        return len(self.queue)

    def is_empty(self):
        return self.size() == 0

    def add_task(self, entry):
        print("Task added: ", entry)
        self.queue.append(entry)
        self.pending_request_action = False

    def dequeue(self):
        if self.is_empty():
            self.request_next_action()
            return None

        entry = self.queue.pop(0)

        if entry["type"] == "callback":
            return entry["arg"]()
        elif entry["type"] == "stop":
            return {
                "right_dc": Direction.STOP,
                "left_dc": Direction.STOP,
                "duration": 0,
                "speed": None,
            }
        elif entry["type"] == "move":
            direction = (
                Direction.FORWARD
                if entry["arg"][0] == "forward"
                else Direction.BACKWARD
            )
            return {
                "right_dc": direction,
                "left_dc": direction,
                "duration": entry["arg"][1],
                "speed": entry["arg"][2] or Speed.MEDIUM,
            }
        elif entry["type"] == "turn":
            angle = entry["arg"][0]
            duration = abs(angle) * turn_multiplier
            return {
                "right_dc": Direction.FORWARD if angle < 0 else Direction.BACKWARD,
                "left_dc": Direction.FORWARD if angle > 0 else Direction.BACKWARD,
                "duration": duration,
                "speed": entry["arg"][1] or Speed.MEDIUM,
            }
