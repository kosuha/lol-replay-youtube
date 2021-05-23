import os
import crawler
import database
import urllib
import replay_maker
import pandas as pd
import config.conn as db
from sqlalchemy import create_engine
import thumbnail

# DB에 연결
engine = create_engine(db.conn)
conn = engine.connect()

players = [['Gen G Ruler', 4]]

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

    data = database.select(player[0])

    for i in range(0, len(data)):
        match_info = data.iloc[i]
        thumbnail.thumbnail_maker(match_info)
        player_parse = urllib.parse.quote(match_info['name']) # 한글 깨짐 방지
        replay_maker.run(player_parse, match_info)

        player_ = data.iloc[0]['name'].replace(" ", "_").lower()
        data = pd.read_sql_query(f"update {player_} set record=1 where id={data.iloc[0]['id']}", engine)