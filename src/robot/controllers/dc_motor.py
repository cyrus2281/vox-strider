from enum import Enum
import RPi.GPIO as GPIO  
from robot.controllers.gpio_interface import GPIO_Interface

class Direction(Enum):
    FORWARD = 'forward'
    BACKWARD = 'backward'
    STOP = 'stop'

class Speed(Enum):
    LOW = 25
    MEDIUM = 50
    HIGH = 75

class DCMotor(GPIO_Interface):
    
    def __init__(self, pin1, pin2, en_pin):
        self.pin1 = pin1
        self.pin2 = pin2
        self.en_pin = en_pin
        self.direction = Direction.STOP
        self.prev_direction = ''
        self.setup()
        
    def setup(self):
        GPIO.setup(self.pin1,GPIO.OUT)
        GPIO.setup(self.pin2,GPIO.OUT)
        GPIO.setup(self.en_pin,GPIO.OUT)
        
        GPIO.output(self.pin1,GPIO.LOW)
        GPIO.output(self.pin2,GPIO.LOW)
        
        self.pmw=GPIO.PWM(self.en_pin,1000)
        self.pmw.start(Speed.LOW.value)
    
    def loop(self):
        if self.direction==Direction.STOP:
            GPIO.output(self.pin1,GPIO.LOW)
            GPIO.output(self.pin2,GPIO.LOW)

        elif self.direction==Direction.FORWARD:
            GPIO.output(self.pin1,GPIO.HIGH)
            GPIO.output(self.pin2,GPIO.LOW)

        elif self.direction==Direction.BACKWARD:
            GPIO.output(self.pin1,GPIO.LOW)
            GPIO.output(self.pin2,GPIO.HIGH)
            
    def move(self, direction: Direction, speed: Speed):
        if direction != self.prev_direction:
            self.direction = direction
            self.prev_direction = direction
        
        if speed is not None:
            self.pmw.ChangeDutyCycle(speed.value)
            
        