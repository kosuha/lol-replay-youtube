import os
import crawler
import replay_maker

players = ['hide on bush', 'T1 Canna', 'T1 Teddy']

# 선수의 다운로드 폴더가 없으면 생성
def make_download_dir(players):
    path_dir = "C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\downloads"
    file_list = os.listdir(path_dir)
    print(file_list)

    for p in players:
        if not p in file_list:
            os.makedirs(path_dir + "\\" + p)

# 선수의 완료 리스트가 없으면 생성
def make_done_list(players):
    path_dir = "C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\done_list"
    file_list = os.listdir(path_dir)
    print(file_list)

    for p in players:
        if not f'{p}.txt' in file_list:
            txt_name = os.path.join(path_dir, f'{p}.txt')
            f = open(txt_name, 'w')
            f.close()

print("Start")

make_download_dir(players)
crawler.downloader('hide on bush')
# replay_maker.recorder()