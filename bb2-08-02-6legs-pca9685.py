# -*- coding: utf-8 -*-
from time import sleep
import smbus
import math

def resetPCA9685():
    bus.write_byte_data(address_pca9685, 0x00, 0x00)

def setPCA9685Freq(freq):
    freq = 0.9*freq # Arduinoのライブラリより
    prescaleval = 25000000.0    # 25MHz
    prescaleval /= 4096.0       # 12-bit
    prescaleval /= float(freq)
    prescaleval -= 1.0
    prescale = int(math.floor(prescaleval + 0.5))
    oldmode = bus.read_byte_data(address_pca9685, 0x00)
    newmode = (oldmode & 0x7F) | 0x10             # スリープモード
    bus.write_byte_data(address_pca9685, 0x00, newmode) # スリープモードへ
    bus.write_byte_data(address_pca9685, 0xFE, prescale) # プリスケーラーをセット
    bus.write_byte_data(address_pca9685, 0x00, oldmode)
    sleep(0.005)
    bus.write_byte_data(address_pca9685, 0x00, oldmode | 0xa1)

def setPCA9685Duty(channel, on, off):
    channelpos = 0x6 + 4*channel
    try:
        bus.write_i2c_block_data(address_pca9685, channelpos, [on&0xFF, on>>8, off&0xFF, off>>8] )
    except IOError:
        pass

def setPCA9685Duty3(channel, on1, off1, on2, off2, on3, off3):
    channelpos = 0x6 + 4*channel
    data = [on1&0xFF, on1>>8, off1&0xFF, off1>>8,
            on2&0xFF, on2>>8, off2&0xFF, off2>>8,
            on3&0xFF, on3>>8, off3&0xFF, off3>>8]
    bus.write_i2c_block_data(address_pca9685, channelpos, data)

def setPCA9685Duty6(channel, on1, off1, on2, off2, on3, off3 , on4, off4, on5, off5, on6, off6):
    channelpos = 0x6 + 4*channel
    data = [on1&0xFF, on1>>8, off1&0xFF, off1>>8,
            on2&0xFF, on2>>8, off2&0xFF, off2>>8,
            on3&0xFF, on3>>8, off3&0xFF, off3>>8,
            on4&0xFF, on4>>8, off4&0xFF, off4>>8,
            on5&0xFF, on5>>8, off5&0xFF, off5>>8,
            on6&0xFF, on6>>8, off6&0xFF, off6>>8]
    bus.write_i2c_block_data(address_pca9685, channelpos, data)

def forwardPhase1(delay):
    setPCA9685Duty3(0, 0, LEG_F_R, 0, LEG_F_R, 0, LEG_F_L)
    sleep(delay)
    setPCA9685Duty3(3, 0, LEG_B_R, 0, LEG_B_L, 0, LEG_B_L)
    sleep(delay)
    setPCA9685Duty3(0, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
    setPCA9685Duty3(3, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)

def forwardPhase2(delay):
    setPCA9685Duty3(3, 0, LEG_F_R, 0, LEG_F_L, 0, LEG_F_L)
    sleep(delay)
    setPCA9685Duty3(0, 0, LEG_B_R, 0, LEG_B_R, 0, LEG_B_L)
    sleep(delay)
    setPCA9685Duty3(3, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
    setPCA9685Duty3(0, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)

def forwardMove(delay):
    forwardPhase1(delay)
    forwardPhase2(delay)

def backwardPhase1(delay):
    setPCA9685Duty3(0, 0, LEG_B_R, 0, LEG_B_R, 0, LEG_B_L)
    sleep(delay)
    setPCA9685Duty3(3, 0, LEG_F_R, 0, LEG_F_L, 0, LEG_F_L)
    sleep(delay)
    setPCA9685Duty3(0, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
    setPCA9685Duty3(3, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)

def backwardPhase2(delay):
    setPCA9685Duty3(3, 0, LEG_B_R, 0, LEG_B_L, 0, LEG_B_L)
    sleep(delay)
    setPCA9685Duty3(0, 0, LEG_F_R, 0, LEG_F_R, 0, LEG_F_L)
    sleep(delay)
    setPCA9685Duty3(3, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
    setPCA9685Duty3(0, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)

def backwardMove(delay):
    backwardPhase1(delay)
    backwardPhase2(delay)

def rotateRightPhase1(delay):
    setPCA9685Duty3(0, 0, LEG_B_R, 0, LEG_B_R, 0, LEG_F_L)
    sleep(delay)
    setPCA9685Duty3(3, 0, LEG_F_R, 0, LEG_B_L, 0, LEG_B_L)
    sleep(delay)
    setPCA9685Duty3(0, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
    setPCA9685Duty3(3, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)

def rotateRightPhase2(delay):
    setPCA9685Duty3(3, 0, LEG_B_R, 0, LEG_F_L, 0, LEG_F_L)
    sleep(delay)
    setPCA9685Duty3(0, 0, LEG_F_R, 0, LEG_F_R, 0, LEG_B_L)
    sleep(delay)
    setPCA9685Duty3(3, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
    setPCA9685Duty3(0, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)

def rotateRightMove(delay):
    rotateRightPhase1(delay)
    rotateRightPhase2(delay)

def rotateLeftPhase1(delay):
    setPCA9685Duty3(0, 0, LEG_F_R, 0, LEG_F_R, 0, LEG_B_L)
    sleep(delay)
    setPCA9685Duty3(3, 0, LEG_B_R, 0, LEG_F_L, 0, LEG_F_L)
    sleep(delay)
    setPCA9685Duty3(0, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
    setPCA9685Duty3(3, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)

def rotateLeftPhase2(delay):
    setPCA9685Duty3(3, 0, LEG_F_R, 0, LEG_B_L, 0, LEG_B_L)
    sleep(delay)
    setPCA9685Duty3(0, 0, LEG_B_R, 0, LEG_B_R, 0, LEG_F_L)
    sleep(delay)
    setPCA9685Duty3(3, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
    setPCA9685Duty3(0, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)

def rotateLeftMove(delay):
    rotateLeftPhase1(delay)
    rotateLeftPhase2(delay)

def stopMove(delay):
    setPCA9685Duty6(0,0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL, 0, NEUTRAL)
    sleep(delay)
  
bus = smbus.SMBus(1)
address_pca9685 = 0x40

resetPCA9685()
setPCA9685Freq(50)

NEUTRAL = 276
LEG_F_R = NEUTRAL + 100
LEG_F_L = NEUTRAL - 100
LEG_B_R = NEUTRAL - 100
LEG_B_L = NEUTRAL + 100

DELAY = 1.0

try:
    while True:
        forwardMove(DELAY)
        backwardMove(DELAY)
        rotateRightMove(DELAY)
        rotateLeftMove(DELAY)

except KeyboardInterrupt:
    stopMove(DELAY)
    pass
