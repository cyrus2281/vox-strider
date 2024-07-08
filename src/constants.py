import os

# Application constants
TURN_ON_PILOT = os.getenv("TURN_OFF_PILOT", "false").lower() != "true"
TURN_ON_CAMERA = os.getenv("TURN_OFF_CAMERA", "false").lower() != "true"
TURN_ON_MOTORS = os.getenv("TURN_OFF_MOTORS", "false").lower() != "true"
MANUAL_TASK_CONTROL = os.getenv("MANUAL_TASK_CONTROL", "false").lower() == "true"

# Application States
INITIAL_STATE = "Initial"
# LOOP_SLEEP = 1 / 30
LOOP_SLEEP = 1

# Paths
LATEST_SNAPSHOT_PATH = "latest_snapshot.jpg"
SNAPSHOT_AFFIX = "snapshot.jpg"
SNAPSHOT_WITH_LINES_AFFIX = " with_lines_snapshot.jpg"
BEEP_AUDIO_IN_PATH= "src/assets/103755-Electronic_device_beeps_10-SFXBible-ss05899.wav"
BEEP_AUDIO_OUT_PATH= "src/assets/101603-Electronic_device_blips_04-SFXBible-ss05912.wav"


# OpenAI Constants
OPENAI_TTS_MODEL = "tts-1"
OPENAI_TTS_VOICE = "echo"
OPENAI_STT_MODEL = "whisper-1"
OPENAI_VLM_MODEL = "gpt-4o"
OPENAI_MAX_TOKENS = 300

# Camera Constants
SNAPSHOT_RESOLUTION = (720, 480)
SNAPSHOT_INTERVAL = 0.5
SNAPSHOT_ROTATION = 180

# Snapshot Processing Constants
SNAPSHOT_SPACE_BETWEEN_LINES = 400
SNAPSHOT_LINE_LENGTH = 250
SNAPSHOT_LINE_THICKNESS = 4
SNAPSHOT_LINES_INWARD_ANGLE = 15

# Input Audio Constants
AUDIO_THRESHOLD=500
AUDIO_BUFFER_CHUNK_SIZE=2048
AUDIO_INPUT_RATE=44100
AUDIO_NUMBER_OF_SILENT_SECONDS=2

# GPIO Constants

## Servo Motors
LEFT_SERVO_PIN = 0
RIGHT_SERVO_PIN = 0

## DC Motor
RIGHT_DC_PIN_EN = 16
RIGHT_DC_PIN_1 = 18
RIGHT_DC_PIN_2 = 22

LEFT_DC_PIN_EN = 15
LEFT_DC_PIN_1 = 13
LEFT_DC_PIN_2 = 11