import json
from pilot.control_llm import get_llm_tool, get_llm_image_message, get_llm_response
from pilot.utils import add_guides_to_image_and_encode


tools = [
    {
        "name": "move",
        "description": "Move the vehicle in the given direction for the given duration",
        "parameters": {
            "direction": {
                "type": "string",
                "description": "The direction to move the vehicle",
                "enum": ["forward", "backward"],
            },
            "duration": {
                "type": "number",
                "description": "Duration to move in the direciton in seconds (default is 2)",
            },
        },
        "required": ["direction"],
    },
    {
        "name": "turn",
        "description": "Turns the vehicle for the given angle (Positive for right, Negative for left)",
        "parameters": {
            "angle": {
                "type": "number",
                "description": "The angle to turn the vehicle in degrees (Positive for right, Negative for left)",
            },
        },
        "required": ["angle"],
    },
    {
        "name": "stop",
        "description": "Stop the vehicle",
    },
    {
        "name": "end_task",
        "description": "When the goal is achieve or it is not possible to achieve the goal, end the task",
        "parameters": {
            "message": {
                "type": "string",
                "description": "Indicating whether the goal is achieved or the reasoning for why it is not possible to achieve the goal.",
            },
        },
        "required": ["message"],
    },
]

tools = [get_llm_tool(**tool) for tool in tools]


def get_state_from_tool(tasks):
    msg = ""
    for name, args in tasks:
        if msg != "":
            msg += ", and then "

        if name == "move":
            msg += f"moving {args['direction']}"
        elif name == "turn":
            msg += f"turning {args['angle']} degrees"
        elif name == "stop":
            msg += "stopped"
        elif name == "end_task":
            msg += "task ended"
        else:
            msg += "Unknown"
    return msg


def truncate_history(history, num_of_events):
    # In the history, cutting based on the last num_of_events of messages
    # where the message role was "user"
    user_msg_indexes = [
        index
        for index, msg in enumerate(history)
        if (msg["role"] == "user" if isinstance(msg, dict) else msg.role == "user")
    ]
    if len(user_msg_indexes) > num_of_events:
        history = history[user_msg_indexes[-num_of_events] :]

    return history


def get_pilot(tools_mapping, initial_state, latest_snapshot_path):
    # Check there's a function for every tool
    for tool in tools:
        if tool["function"]["name"] not in tools_mapping:
            raise ValueError(f"No function for tool {tool['function']['name']}")

    # Control parameters
    num_of_events = 3

    # States
    history = []
    previous_state = "Initial"
    current_state = initial_state

    def get_next_action(goal):
        nonlocal history, previous_state, current_state

        # Create action request
        encoded_image = add_guides_to_image_and_encode(latest_snapshot_path)
        next_action = get_llm_image_message(
            encoded_image, goal, current_state, previous_state
        )

        # Get next action
        history.append(next_action)
        response = get_llm_response(history, tools)

        # Handle action
        tool_calls = response.tool_calls
        if tool_calls:
            tasks = []
            history.append(response)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                function_response = tools_mapping[function_name](**function_args)
                tasks.append((function_name, function_args))
                history.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response or "Done",
                    }
                )
            # Update states
            history = truncate_history(history, num_of_events)
            previous_state = current_state
            current_state = get_state_from_tool(tasks)
            print("current_state:", current_state)

    return get_next_action
