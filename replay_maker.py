#-*- coding: utf-8 -*-

import os
import time
import pyautogui as pg
import keyboard
import database
import urllib

def recorder(data_first):
    if data_first['team'] == 'red':
        if data_first['position'] == 1:
            position = 'q'
        if data_first['position'] == 2:
            position = 'w'
        if data_first['position'] == 3:
            position = 'e'
        if data_first['position'] == 4:
            position = 'r'
        if data_first['position'] == 5:
            position = 't'
    else:
        position = str(data_first['position'])

    # pg.typewrite(position+position, interval=0.2) # 선수 시점
    time.sleep(3)

    keyboard.press('o')
    time.sleep(0.5)
    keyboard.release('o')
    time.sleep(1)

    keyboard.press('u')
    time.sleep(0.5)
    keyboard.release('u')
    time.sleep(1)

    keyboard.press('n')
    time.sleep(0.5)
    keyboard.release('n')
    time.sleep(1)

    keyboard.press(position)
    time.sleep(0.5)
    keyboard.release(position)
    time.sleep(0.2)
    keyboard.press(position)
    time.sleep(0.5)
    keyboard.release(position)
    time.sleep(1)

    keyboard.press('p')
    time.sleep(0.5)
    keyboard.release('p')
    time.sleep(180)
    keyboard.press('p')
    time.sleep(0.5)
    keyboard.release('p')
    time.sleep(1)

    keyboard.press('ctrl')
    keyboard.press('v')
    time.sleep(0.5)
    keyboard.release('ctrl')
    keyboard.release('v')
    time.sleep(1)

    print('recording...')

def find_image(file_name):
    image_location = pg.locateOnScreen(f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\img\\{file_name}", confidence=0.9)
    if image_location != None:
        print("found!")
        return image_location

    return False

def run(player, match_info):
    working_dir = f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\downloads\\{player}"
    execute_file = os.path.join(working_dir, match_info['id'] + '.bat')

    os.chdir(working_dir)
    os.system(execute_file)

    while True:
        if find_image('cap.png') != False:
            break
        
        print('file loading...')
        time.sleep(1)

    recorder(match_info)

    while True:
        if find_image('fail.png') != False:
            keyboard.press('alt')
            keyboard.press('f4')
            time.sleep(0.5)
            keyboard.release('alt')
            keyboard.release('f4')
            time.sleep(5)
            database.failed(match_info['name'], match_info['id'])
            return False

        if find_image('end.png') != False:
            keyboard.press('ctrl')
            keyboard.press('v')
            time.sleep(0.5)
            keyboard.release('ctrl')
            keyboard.release('v')
            time.sleep(5)

            keyboard.press('alt')
            keyboard.press('f4')
            time.sleep(0.5)
            keyboard.release('alt')
            keyboard.release('f4')
            time.sleep(5)

            highlights_location = 'C:\\Users\\okeyd\\Documents\\League of Legends\\Highlights'
            file_list = os.listdir(highlights_location)
            src = os.path.join(highlights_location, file_list[0])
            player_parse = urllib.parse.quote(match_info['name']) # 한글 깨짐 방지
            new_name = os.path.join(highlights_location, f"{match_info['id']}_{player_parse}.webm")
            os.rename(src, new_name)
            print('recorded!')
            time.sleep(1)
            return True
        
        print('recording...')
        time.sleep(1)

    

