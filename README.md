# VoxStrider

A self-balancing self-driving bipedal robot controlled through computer vision and natural language prompting with text-to-voice and voice-to-text interface


**Work in progress**


## Requirements

- rpicam-jpeg 
- portaudio19-dev

## Installation

```bash
sudo apt-get install portaudio19-dev
pip install -r requirements.txt
```

Create `.env` file with the following content:

```bash
OPENAI_API_KEY=your_openai_api_key
TURN_OFF_MOTORS=false
TURN_OFF_CAMERA=false
MANUAL_TASK_CONTROL=false
```

## Running

```bash
python src/main.py
```