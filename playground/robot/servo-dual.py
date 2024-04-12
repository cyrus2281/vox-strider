# https://projects.raspberrypi.org/en/projects/grandpa-scarer/3

# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

# Set up pin 11 for PWM
GPIO.setup(11,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
pwm1 = GPIO.PWM(11, 50)     # Sets up pin 11 as a PWM pin

GPIO.setup(13,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
pwm2 = GPIO.PWM(13, 50)     # Sets up pin 11 as a PWM pin

pwm1.start(0)               # Starts running PWM on the pin and sets it to 0
pwm2.start(0)               # Starts running PWM on the pin and sets it to 0

for i in range(0,2):
    # Move the servo back and forth
    pwm1.ChangeDutyCycle(3) 
    pwm2.ChangeDutyCycle(12) 
    sleep(2)    
    pwm1.ChangeDutyCycle(6)
    pwm2.ChangeDutyCycle(6) 
    sleep(2)


# Clean up everything
pwm1.stop()                 # At the end of the program, stop the PWM
pwm2.stop()  
GPIO.cleanup()           # Resets the GPIO pins back to defaults