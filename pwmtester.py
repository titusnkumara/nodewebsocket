import RPi.GPIO as IO
import time

IO.setwarnings(False)
IO.setmode (IO.BCM)

leftForwardPIN = 19
leftBackwordPIN = 26

rightForwardPIN = 16
rightBackwordPIN = 21

IO.setup(leftForwardPIN,IO.OUT)
IO.setup(leftBackwordPIN,IO.OUT)
IO.setup(rightForwardPIN,IO.OUT)
IO.setup(rightBackwordPIN,IO.OUT)

leftForward = IO.PWM(leftForwardPIN,100)
leftBackword = IO.PWM(leftBackwordPIN,100)
rightForward = IO.PWM(rightForwardPIN,100)
rightBackword = IO.PWM(rightBackwordPIN,100)


leftForward.start(0)
leftBackword.start(0)
rightForward.start(0)
rightBackword.start(0)

while 1:
    leftForward.ChangeDutyCycle(0)
    leftBackword.ChangeDutyCycle(100)
    rightForward.ChangeDutyCycle(0)
    rightBackword.ChangeDutyCycle(100)
    time.sleep(0.03)
