import RPi.GPIO as GPIO
from time import sleep 

from robot.controllers.dc_motor import DCMotor
from robot.controllers.servo_motor import ServoMotor
from robot.controllers.accelerometer import Accelerometer

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

def loop(command_queue):
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
    acc_sensor = Accelerometer(
        right_dc,
        left_dc
    )

    print("Motors and sensor setup completed")

    try:
    # loop
        print("Starting Loop")
        while True:
            acc_sensor.loop()
            right_dc.loop()
            left_dc.loop()
            sleep(.1)

    except KeyboardInterrupt:
        # force exit - clean up
        print("KeyboardInterrupt")

    finally:
        # clean up
        print("Cleaning up")
        GPIO.cleanup()