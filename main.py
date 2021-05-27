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
import pefile

players = [
    ['Hide on bush', 3, 'T1 Faker'],
    ['DK ShowMaker', 3, 'DK ShowMaker'],
    ['elole', 1, 'DK Khan'],
    ['Gen G Ruler', 4, 'Gen G Ruler'],
    ['Gen G Clid', 2, 'Gen G Clid'],
    ['T1 Gumayusi', 4, 'T1 Gumayusi']
]

def now_patch():
    pe = pefile.PE(r'C:/Riot Games/League of Legends/Game/League of Legends.exe')
    string_version_info = {}

    for fileinfo in pe.FileInfo[0]:
        if fileinfo.Key.decode() == 'StringFileInfo':
            for st in fileinfo.StringTable:
                for entry in st.entries.items():
                    string_version_info[entry[0].decode()] = entry[1].decode()

    versions = string_version_info['FileVersion'].split(".")
    version = versions[0] + "." + versions[1] + "." + versions[2][0]

    return version

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

        if match_info['record'] == 0:
            if match_info['patch'] != now_patch():
                database.failed(match_info['name'], match_info['id'])
                continue
            player_parse = urllib.parse.quote(match_info['name']) # 한글 깨짐 방지
            record_result = replay_maker.run(player_parse, match_info)
            if record_result == False:
                player_parse = urllib.parse.quote(match_info['name'])
                remove_target = os.path.join(highlights_location, f"{match_info['id']}_{player_parse}.webm")
                os.remove(remove_target)
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
