from llm.model import openai_client
from constants import OPENAI_VLM_MODEL, OPENAI_MAX_TOKENS

llm_system_prompt = (
    "You are a robot controller. You are given the task to control a using "
    "the given tools to achieve the given goal. Use vision to navigate the "
    "robot, avoid obstacles, and reach the destination. The robot has a "
    "camera sensor that capture images on intervals.\n"
    "Once the goal is achieved or it is not possible to achieve the goal, "
    "end the task.\n"
)
llm_system_prompt_message = {
    "role": "system",
    "content": [
        {"type": "text", "text": llm_system_prompt},
    ],
}


def get_llm_tool(name, description, parameters=None, required=[]):
    tool = {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
        },
    }

    if parameters:
        properties = {}
        for key, value in parameters.items():
            properties[key] = {}
            for field_name, field in value.items():
                properties[key][field_name] = field
        tool["function"]["parameters"] = {
            "type": "object",
            "properties": properties,
            "required": required,
        }

    return tool


def get_llm_image_message(encoded_image, goal, current_state, previous_state):
    prompt = (
        "Given the front-view image of the vehicle, give the next instructions.\n"
        "The red lines indicate the predicted path of the vehicle.\n\n"
        f"Goal: {goal}\n\n"
        f"Previous state: {previous_state}\n"
        f"Current State: {current_state}\n\n"
        "Instructions:"
    )

    return {
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"},
            },
        ],
    }


def get_llm_response(input_messages, tools):
    messages = [llm_system_prompt_message] + input_messages

    response = openai_client.chat.completions.create(
        model=OPENAI_VLM_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="required",
        max_tokens=OPENAI_MAX_TOKENS,
    )
    response_message = response.choices[0].message
    return response_message
