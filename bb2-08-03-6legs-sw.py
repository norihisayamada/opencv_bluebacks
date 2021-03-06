# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
from time import sleep
import math

def setDuty3_0(duty0, duty1, duty2):
    p0.ChangeDutyCycle(duty0)
    p1.ChangeDutyCycle(duty1)
    p2.ChangeDutyCycle(duty2)

def setDuty3_3(duty3, duty4, duty5):
    p3.ChangeDutyCycle(duty3)
    p4.ChangeDutyCycle(duty4)
    p5.ChangeDutyCycle(duty5)

def setDuty6(duty0, duty1, duty2, duty3, duty4, duty5):
    p0.ChangeDutyCycle(duty0)
    p1.ChangeDutyCycle(duty1)
    p2.ChangeDutyCycle(duty2)
    p3.ChangeDutyCycle(duty3)
    p4.ChangeDutyCycle(duty4)
    p5.ChangeDutyCycle(duty5)
    
def forwardPhase1(delay):
    setDuty3_0(LEG_F_R, LEG_F_R, LEG_F_L)
    sleep(delay)
    setDuty3_3(LEG_B_R, LEG_B_L, LEG_B_L)
    sleep(delay)
    setDuty3_0(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)
    setDuty3_3(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)

def forwardPhase2(delay):
    setDuty3_3(LEG_F_R, LEG_F_L, LEG_F_L)
    sleep(delay)
    setDuty3_0(LEG_B_R, LEG_B_R, LEG_B_L)
    sleep(delay)
    setDuty3_3(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)
    setDuty3_0(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)

def forwardMove(delay):
    forwardPhase1(delay)    
    forwardPhase2(delay)    

def backwardPhase1(delay):
    setDuty3_0(LEG_B_R, LEG_B_R, LEG_B_L)
    sleep(delay)
    setDuty3_3(LEG_F_R, LEG_F_L, LEG_F_L)
    sleep(delay)
    setDuty3_0(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)
    setDuty3_3(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)

def backwardPhase2(delay):
    setDuty3_3(LEG_B_R, LEG_B_L, LEG_B_L)
    sleep(delay)
    setDuty3_0(LEG_F_R, LEG_F_R, LEG_F_L)
    sleep(delay)
    setDuty3_3(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)
    setDuty3_0(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)

def backwardMove(delay):
    backwardPhase1(delay)    
    backwardPhase2(delay)    

def rotateRightPhase1(delay):
    setDuty3_0(LEG_B_R, LEG_B_R, LEG_F_L)
    sleep(delay)
    setDuty3_3(LEG_F_R, LEG_B_L, LEG_B_L)
    sleep(delay)
    setDuty3_0(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)
    setDuty3_3(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)

def rotateRightPhase2(delay):
    setDuty3_3(LEG_B_R, LEG_F_L, LEG_F_L)
    sleep(delay)
    setDuty3_0(LEG_F_R, LEG_F_R, LEG_B_L)
    sleep(delay)
    setDuty3_3(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)
    setDuty3_0(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)

def rotateRightMove(delay):
    rotateRightPhase1(delay)    
    rotateRightPhase2(delay)    

def rotateLeftPhase1(delay):
    setDuty3_0(LEG_F_R, LEG_F_R, LEG_B_L)
    sleep(delay)
    setDuty3_3(LEG_B_R, LEG_F_L, LEG_F_L)
    sleep(delay)
    setDuty3_0(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)
    setDuty3_3(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)

def rotateLeftPhase2(delay):
    setDuty3_3(LEG_F_R, LEG_B_L, LEG_B_L)
    sleep(delay)
    setDuty3_0(LEG_B_R, LEG_B_R, LEG_F_L)
    sleep(delay)
    setDuty3_3(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)
    setDuty3_0(NEUTRAL, NEUTRAL, NEUTRAL)
    sleep(delay)

def rotateLeftMove(delay):
    rotateLeftPhase1(delay)    
    rotateLeftPhase2(delay)    

def stopMove(delay):
    setDuty6(NEUTRAL, NEUTRAL, NEUTRAL, NEUTRAL, NEUTRAL, NEUTRAL) 
    sleep(delay)
  
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT) # id 0
GPIO.setup(24, GPIO.OUT) # id 1
GPIO.setup(23, GPIO.OUT) # id 2
GPIO.setup(22, GPIO.OUT) # id 3
GPIO.setup(27, GPIO.OUT) # id 4
GPIO.setup(18, GPIO.OUT) # id 5


p0 = GPIO.PWM(25, 50)
p1 = GPIO.PWM(24, 50)
p2 = GPIO.PWM(23, 50)
p3 = GPIO.PWM(22, 50)
p4 = GPIO.PWM(27, 50)
p5 = GPIO.PWM(18, 50)


p0.start(6.25) # (3.5+9.0)/2
p1.start(6.25) # (3.5+9.0)/2
p2.start(6.25) # (3.5+9.0)/2
p3.start(6.25) # (3.5+9.0)/2
p4.start(6.25) # (3.5+9.0)/2
p5.start(6.25) # (3.5+9.0)/2


NEUTRAL = 6.25
LEG_F_R = NEUTRAL + 2
LEG_F_L = NEUTRAL - 2
LEG_B_R = NEUTRAL - 2
LEG_B_L = NEUTRAL + 2

DELAY = 1.0

try:
    while True:
        forwardMove(DELAY)
        backwardMove(DELAY)
        rotateRightMove(DELAY)
        rotateLeftMove(DELAY)

except KeyboardInterrupt:
    stopMove(DELAY)
    p0.stop()
    p1.stop()
    p2.stop()
    p3.stop()
    p4.stop()
    p5.stop()
    pass
