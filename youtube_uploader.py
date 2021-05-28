#-*- coding: utf-8 -*-

import os
import time
import pyautogui as pg
import keyboard
import urllib
import replay_maker

def pressed(key, num):
    for i in range(0, num):
        keyboard.press(key)
        time.sleep(0.2)
        keyboard.release(key)
        time.sleep(1)

def upload(match_info):
    id = match_info['id']
    player = match_info['name']
    region = match_info['region']
    pro_name = match_info['pro_name']
    tier = match_info['tier']
    position = match_info['position']
    champion = match_info['champion']
    vs_player = match_info['vs_name']
    vs_champion = match_info['vs_champion']
    patch = 'Patch ' + match_info['patch']
    kill = match_info['kill']
    badge = match_info['badge']

    # 크롬 열기 Point(x=560, y=1065)
    pg.moveTo(560, 1065)
    pg.click()
    time.sleep(3)

    # 주소 입력 Point(x=161, y=51)
    pg.moveTo(161, 51)
    pg.click()
    time.sleep(1)
    url = 'https://studio.youtube.com'
    keyboard.write(url)

    # 페이지 이동
    pressed('enter', 1)
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
    pg.moveTo(597, 56)
    pg.click()
    time.sleep(1)
    keyboard.write('C:\\Users\\okeyd\\Documents\\League of Legends\\Highlights')
    pressed('enter', 1)
    time.sleep(1)

    pressed('tab', 5)

    player_parse = urllib.parse.quote(player) # 한글 깨짐 방지
    keyboard.write(f"{id}_{player_parse}")
    time.sleep(1)
    pressed('enter', 1)

    while True:
        if replay_maker.find_image('det.png') != False:
            print('loaded!')
            time.sleep(3)
            break
        
        print('loading...')
        time.sleep(5)

    title = f'{pro_name.upper()} {champion.upper()} {kill}! - {champion} vs {vs_champion} | {region} Challenger SoloQ | {patch}'
    keyboard.write(title) # 제목

    pressed('tab', 2)

    description = f'#{pro_name.replace(" ", "")} #{champion.replace(" ", "")} #challenger \n{player} {champion} vs {vs_player} {vs_champion} \n{region} Solo {patch}'

    keyboard.write(description)  # 설명
    time.sleep(1)

    pressed('tab', 2)

    pressed('enter', 1)    # 썸네일
    time.sleep(1)
    pg.moveTo(597, 56)
    pg.click()
    keyboard.write("C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\img\\thumbnails")
    pressed('enter', 1)
    time.sleep(1)

    # 썸네일 파일 선택
    pressed('tab', 5)

    player_parse = urllib.parse.quote(player) # 한글 깨짐 방지
    keyboard.write(f"{id}_{player_parse}")
    time.sleep(1)
    pressed('enter', 1)

    pressed('tab', 6)
    pressed('enter', 1)
    pressed('tab', 1)
    pressed('enter', 1)
    pressed('tab', 2)
    pressed('enter', 1)
    pressed('tab', 3)
    pressed('down', 1)
    pressed('tab', 5)
    pressed('enter', 1)

    while True:
        if replay_maker.find_image('sd.png') != False:
            print('video loaded!')
            time.sleep(5)
            break
        
        print('video loading...')
        time.sleep(5)

    pressed('tab', 12)
    pressed('enter', 1)
    pressed('tab', 11)
    pressed('enter', 1)
    
    pg.moveTo(589, 544)
    pg.click()
    time.sleep(1)

    pg.moveTo(1402, 966)
    pg.click()
    time.sleep(10)

    pg.moveTo(1895, 13)
    pg.click()
    time.sleep(1)

# while True:
#     print("mouse position : ", pg.position())
#     time.sleep(1)

# match_info = {
#                     'id': 5211349961,
#                     'name': 'Hide on bush',
#                     'pro_name': 'T1 Faker',
#                     'region': 'KR',
#                     'tier': 'c',
#                     'position': 3,
#                     'champion': 'Viktor',
#                     'vs_name': 'ddd',
#                     'vs_champion': 'Le',
#                     'team': '',
#                     'patch': '11.10.3',
#                     'record': False,
#                     'upload': False
#                 }

# id = match_info['id']
# player = match_info['name']
# region = match_info['region']
# pro_name = match_info['pro_name']
# tier = match_info['tier']
# position = match_info['position']
# champion = match_info['champion']
# vs_player = match_info['vs_name']
# vs_champion = match_info['vs_champion']
# patch = 'Patch ' + match_info['patch']

# description = f'#{player.replace(" ", "")} #{pro_name.replace(" ", "")} #{champion.replace(" ", "")} #challenger #LoL \n{player} {champion} vs {vs_player} {vs_champion} \n{region} Solo {patch}'

# print(description)