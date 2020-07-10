# -*- coding: utf-8 -*-
import picamera
import picamera.array
import cv2
import math
from time import sleep
import smbus
import math
import pygame
import sys

pygame.init()
size=(320,240)
screen = pygame.display.set_mode(size)

def pygame_imshow(array):
    b,g,r = cv2.split(array)
    rgb = cv2.merge([r,g,b])
    surface1 = pygame.surfarray.make_surface(rgb)       
    surface2 = pygame.transform.rotate(surface1, -90)
    surface3 = pygame.transform.flip(surface2, True, False)
    screen.blit(surface3, (0,0))
    pygame.display.flip()

cascade_path =  "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"
cascade = cv2.CascadeClassifier(cascade_path)

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

def getPCA9685Duty(id, val):
    val_min = 0
    val_max = 4095
    servo_min = 143 # 50Hzで0.7ms
    servo_max = 410 # 50Hzで2.0ms  (中心は276)
    if id==1 :
        servo_min = 193 # 50Hzで0.95ms
        servo_max = 360 # 50Hzで1.8ms
    duty = (servo_min-servo_max)*(val-val_min)/(val_max-val_min) + servo_max
    # 一般的なサーボモーターはこちらを有効に
    #duty = (servo_max-servo_min)*(val-val_min)/(val_max-val_min) + servo_min
    if duty > servo_max:
        duty = servo_max
    if duty < servo_min:
        duty = servo_min
    return int(duty)

bus = smbus.SMBus(1)
address_pca9685 = 0x40

resetPCA9685()
setPCA9685Freq(50)

prev_x = 160
prev_y = 120
prev_input_x = 2048
prev_input_y = 2048

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)
        camera.framerate = 15

        while True:
            # stream.arrayにBGRの順で映像データを格納
            camera.capture(stream, 'bgr', use_video_port=True)
            # 映像データをグレースケール画像grayに変換
            gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
            # grayから顔を探す
            facerect = cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2, minSize=(30,30), maxSize=(150,150))

            if len(facerect) > 0:
                # 複数見つかった顔のうち、以前の顔の位置に最も近いものを探す
                mindist = 320+240
                minindx = 0
                indx = 0
                for rect in facerect:
                    dist = math.fabs(rect[0]+rect[2]/2-prev_x) + math.fabs(rect[1]+rect[3]/2-prev_y)
                    if dist < mindist:
                        mindist = dist
                        minindx = indx
                    indx += 1

                # 現在の顔の位置
                face_x = facerect[minindx][0]+facerect[minindx][2]/2
                face_y = facerect[minindx][1]+facerect[minindx][3]/2

                # 元の画像(system.array)上の、顔がある位置に赤い四角を描画
                cv2.rectangle(stream.array, tuple(facerect[minindx][0:2]),tuple(facerect[minindx][0:2]+facerect[minindx][2:4]), (0,0,255), thickness=2)

                dx = face_x-160  # 左右中央からのずれ
                dy = face_y-120  # 上下中央からのずれ

                # サーボモーターを回転させる量を決める定数
                ratio_x =  3
                ratio_y = -3

                duty0 = getPCA9685Duty(0, ratio_x*dx + prev_input_x)
                setPCA9685Duty(0, 0, duty0)

                duty1 = getPCA9685Duty(1, ratio_y*dy + prev_input_y)
                setPCA9685Duty(1, 0, duty1)

                # サーボモーターに対する入力値を更新
                prev_input_x = ratio_x*dx + prev_input_x
                if prev_input_x > 4095:
                    prev_input_x = 4095
                if prev_input_x < 0:
                    prev_input_x = 0
                prev_input_y = ratio_y*dy + prev_input_y
                if prev_input_y > 4095:
                    prev_input_y = 4095
                if prev_input_y < 0:
                    prev_input_y = 0

                # 以前の顔の位置を更新
                prev_x = face_x
                prev_y = face_y

            # pygameで画像を表示
            pygame_imshow(stream.array)

            # "q"を入力でアプリケーション終了
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

            # streamをリセット
            stream.seek(0)
            stream.truncate()
