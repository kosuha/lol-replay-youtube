import os
import time
import crawler
import database
import urllib
import replay_maker
import pandas as pd
import thumbnail
import youtube_uploader
import pymysql

players = [['Hide on bush', 3, 'T1 Faker']]

# 선수의 다운로드 폴더가 없으면 생성
def make_download_dir(players):
    path_dir = "C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\downloads"
    file_list = os.listdir(path_dir)

    for p in players:
        player_parse = urllib.parse.quote(p[0]) # 한글 깨짐 방지
        if not player_parse in file_list:
            os.makedirs(path_dir + "\\" + player_parse)

print("Start")

make_download_dir(players)
crawler.champion_image()

for player in players:
    df = crawler.downloader(player)

    if df.empty == False:
        database.insert(df, player[0])

    while True:
        highlights_location = 'C:\\Users\\okeyd\\Documents\\League of Legends\\Highlights'

        data = database.select_upload(player[0])

        if data.empty:
            break

        match_info = data.iloc[0]

        thumbnail.thumbnail_maker(match_info)

        if match_info['record'] == 0:
            player_parse = urllib.parse.quote(match_info['name']) # 한글 깨짐 방지
            record_result = replay_maker.run(player_parse, match_info)
            if record_result == False:
                continue
            player_ = data.iloc[0]['name'].replace(" ", "_").lower()
            database.recorded(match_info['name'], match_info['id'])

        time.sleep(3)

        youtube_uploader.upload(match_info)
        database.uploaded(match_info['name'], match_info['id'])
        player_parse = urllib.parse.quote(match_info['name'])
        remove_target = os.path.join(highlights_location, f"{match_info['id']}_{player_parse}.webm")
        os.remove(remove_target)

        print(match_info['name'], match_info['id'], "done!")

print("End")
