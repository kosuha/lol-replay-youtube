#-*- coding: utf-8 -*-

import os
import time
from numpy import string_
import pyautogui as pg
import keyboard
import database
import urllib

shift_list = [':', '_']

def write(string):
    string = list(string)
    for c in string:
        if c in shift_list or c.isupper():
            keyboard.press('shift')
        keyboard.press(c)
        time.sleep(0.1)
        if c in shift_list or c.isupper():
            keyboard.release('shift')
        keyboard.release(c)
        time.sleep(0.1)

# 크롬 열기 Point(x=560, y=1065)
pg.moveTo(560, 1065)
pg.click()
time.sleep(3)

# 주소 입력 Point(x=161, y=51)
pg.moveTo(161, 51)
pg.click()
url = 'https://studio.youtube.com'
write(url)

# 페이지 이동
keyboard.press('enter')
time.sleep(0.1)
keyboard.release('enter')
time.sleep(3)

# 업로드 창 열기
pg.moveTo(1782, 108)
pg.click()
time.sleep(1)
pg.moveTo(1767, 142)
pg.click()
time.sleep(1)

# 파일 선택 창 열기, 파일 선택, 열기 버튼
pg.moveTo(960, 676)
pg.click()
time.sleep(1)
pg.moveTo(219, 151)
pg.click()
time.sleep(1)
pg.moveTo(771, 519)
pg.click()
time.sleep(10)

while True:
    print("mouse position : ", pg.position())
    time.sleep(1)

