import RPi.GPIO as GPIO
from time import sleep 

from robot.controllers.dc_motor import DCMotor
from robot.controllers.servo_motor import ServoMotor
from robot.controllers.accelerometer import Accelerometer

# Accelerometer sensor
ACC_SCL_PIN = 0
ACC_SDA_PIN = 0

# Servo Motors
LEFT_SERVO_PIN = 0
RIGHT_SERVO_PIN = 0

# DC MotorS
RIGHT_DC_PIN_1 = 0
RIGHT_DC_PIN_2 = 0
RIGHT_DC_PIN_EN = 0

LEFT_DC_PIN_1 = 0
LEFT_DC_PIN_2 = 0
LEFT_DC_PIN_EN = 0

def loop(command_queue):
    print("Starting GPIO setup")
    # setup
    GPIO.setmode(GPIO.BCM)

    # Motors
    ## Servo Motors
    right_servo = ServoMotor(RIGHT_SERVO_PIN)
    left_servo = ServoMotor(LEFT_SERVO_PIN)
    ## DC Motors
    right_dc = DCMotor(RIGHT_DC_PIN_1, RIGHT_DC_PIN_2, RIGHT_DC_PIN_EN)
    left_dc = DCMotor(LEFT_DC_PIN_1, LEFT_DC_PIN_2, LEFT_DC_PIN_EN)
    # Accelerometer sensor
    acc_sensor = Accelerometer(
        ACC_SCL_PIN, 
        ACC_SDA_PIN,
        right_dc,
        left_dc
    )

    print("Motors and sensor setup completed")

    try:
    # loop
        print("Starting Loop")
        while True:
            pass

    except KeyboardInterrupt:
        # force exit - clean up
        print("KeyboardInterrupt - Cleaning up")
        pass

    finally:
        # natural exit - clean up
        print("Program exiting - Cleaning up")
        pass