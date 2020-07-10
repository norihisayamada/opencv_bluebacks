# -*- coding: utf-8 -*-
import picamera
import picamera.array
import cv2
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

version = cv2.__version__.split(".")
CVversion = int(version[0])

with picamera.PiCamera() as camera:
    with picamera.array.PiRGBArray(camera) as stream:
        camera.resolution = (320, 240)
        camera.framerate = 15

        while True:
            # stream.arrayにBGRの順で映像データを格納
            camera.capture(stream, 'bgr', use_video_port=True)
            # 映像データをグレースケール画像grayに変換
            gray = cv2.cvtColor(stream.array, cv2.COLOR_BGR2GRAY)
            # ガウシアンぼかしを適用して、認識精度を上げる
            blur = cv2.GaussianBlur(gray, (9,9), 0)
            # ハフ変換を適用し、映像内の円を探す
            if CVversion == 2:
                circles = cv2.HoughCircles(blur, cv2.cv.CV_HOUGH_GRADIENT,
                      dp=1, minDist=50, param1=120, param2=40,
                      minRadius=5, maxRadius=100)
            else:
                circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT,
                      dp=1, minDist=50, param1=120, param2=40,
                      minRadius=5, maxRadius=100)

            if circles is not None:
                for c in circles[0]:
                    # 見つかった円の上に赤い円を元の映像(system.array)上に描画
                    # c[0]:x座標, c[1]:y座標, c[2]:半径
                    cv2.circle(stream.array, (c[0],c[1]), c[2], (0,0,255), 2)

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
