import RPi.GPIO as GPIO
from time import sleep, time

from robot.controllers.dc_motor import DCMotor
from robot.controllers.servo_motor import ServoMotor
from robot.controllers.accelerometer import Accelerometer
from robot.command_queue import CommandQueue

# Servo Motors
LEFT_SERVO_PIN = 0
RIGHT_SERVO_PIN = 0

# DC MotorS
RIGHT_DC_PIN_EN = 16
RIGHT_DC_PIN_1 = 18
RIGHT_DC_PIN_2 = 22

LEFT_DC_PIN_EN = 15
LEFT_DC_PIN_1 = 13
LEFT_DC_PIN_2 = 11

# DELAY = 1 / 30
DELAY = 1


def loop(command_queue: CommandQueue):
    print("Starting GPIO setup")
    # setup
    GPIO.setmode(GPIO.BOARD)

    # Motors
    ## Servo Motors
    right_servo = ServoMotor(RIGHT_SERVO_PIN)
    left_servo = ServoMotor(LEFT_SERVO_PIN)
    ## DC Motors
    right_dc = DCMotor(RIGHT_DC_PIN_1, RIGHT_DC_PIN_2, RIGHT_DC_PIN_EN)
    left_dc = DCMotor(LEFT_DC_PIN_1, LEFT_DC_PIN_2, LEFT_DC_PIN_EN)
    # Accelerometer sensor
    acc_sensor = Accelerometer(right_dc, left_dc)

    print("Motors and sensor setup completed")

    task_duration = None
    task = None

    try:
        # loop
        print("Starting Loop")
        while True:
            print("Loop")
            # acc_sensor.loop()
            right_dc.loop()
            left_dc.loop()

            # Dequeueing commands
            if not task:
                task = command_queue.dequeue()
                if task:
                    task_duration = time() + task["duration"]
            else:
                right_dc.move(task["right_dc"], task["speed"])
                left_dc.move(task["left_dc"], task["speed"])

            if task and time() > task_duration:
                # Task completed
                task = None

            # Loop sleep
            sleep(DELAY)

    except KeyboardInterrupt:
        # force exit - clean up
        print("KeyboardInterrupt")

    finally:
        # clean up
        print("Cleaning up")
        GPIO.cleanup()
