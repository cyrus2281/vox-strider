'''
Credits:
- http://www.electronicwings.com
- https://www.electronicwings.com/raspberry-pi/mpu6050-accelerometergyroscope-interfacing-with-raspberry-pi
'''
import smbus
from time import sleep
from robot.controllers.gpio_interface import GPIO_Interface
from robot.controllers import dc_motor

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47
DEVICE_ADDRESS = 0x68   # MPU6050 device address


class Accelerometer(GPIO_Interface):
    def __init__(self, right_dc: dc_motor.DCMotor, left_dc: dc_motor.DCMotor):
        self.bus = smbus.SMBus(1)
        self.right_dc = right_dc
        self.left_dc = left_dc
        self.MPU_Init()

    def MPU_Init(self):
        #write to sample rate register
        self.bus.write_byte_data(DEVICE_ADDRESS, SMPLRT_DIV, 7)
        #Write to power management register
        self.bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 1)
        #Write to Configuration register
        self.bus.write_byte_data(DEVICE_ADDRESS, CONFIG, 0)
        #Write to Gyro configuration register
        self.bus.write_byte_data(DEVICE_ADDRESS, GYRO_CONFIG, 24)
        #Write to interrupt enable register
        self.bus.write_byte_data(DEVICE_ADDRESS, INT_ENABLE, 1)

    def read_raw_data(self, addr):
        #Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(DEVICE_ADDRESS, addr)
        low = self.bus.read_byte_data(DEVICE_ADDRESS, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value
    
    def loop(self):
        #Read Accelerometer raw value
        acc_x = self.read_raw_data(ACCEL_XOUT_H)
        acc_y = self.read_raw_data(ACCEL_YOUT_H)
        acc_z = self.read_raw_data(ACCEL_ZOUT_H)
        
        #Read Gyroscope raw value
        gyro_x = self.read_raw_data(GYRO_XOUT_H)
        gyro_y = self.read_raw_data(GYRO_YOUT_H)
        gyro_z = self.read_raw_data(GYRO_ZOUT_H)
        
        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        
        Gx = gyro_x/131.0
        Gy = gyro_y/131.0
        Gz = gyro_z/131.0
        

        print("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az)
        direction = dc_motor.Direction.BACKWARD if Ax > 0.3 else \
            (dc_motor.Direction.FORWARD if Ax < 0.1 else dc_motor.Direction.STOP)
        speed = dc_motor.Speed.MEDIUM
        print("\tAx=%.2f" %Ax, direction ,speed)
        self.right_dc.move(direction, speed)
        self.left_dc.move(direction, speed)
