import os
import crawler
import database
import replay_maker

players = [['Hide on bush', 3], ['T1 Canna', 1], ['T1 Teddy', 4]]

# 선수의 다운로드 폴더가 없으면 생성
def make_download_dir(players):
    path_dir = "C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\downloads"
    file_list = os.listdir(path_dir)

    for p in players:
        if not p[0] in file_list:
            os.makedirs(path_dir + "\\" + p[0])

# 선수의 완료 리스트가 없으면 생성
def make_done_list(players):
    path_dir = "C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\done_list"
    file_list = os.listdir(path_dir)

    for p in players:
        if not f'{p[0]}.txt' in file_list:
            txt_name = os.path.join(path_dir, f'{p[0]}.txt')
            f = open(txt_name, 'w')
            f.close()

print("Start")

make_done_list(players)
make_download_dir(players)

df = crawler.downloader(players[0])
database.insert(df, players[0][0])
# replay_maker.recorder()