import os
import crawler
import replay_maker

players = ['hide on bush', 'T1 Canna', 'T1 Teddy']

def make_download_dir(players):
    path_dir = "C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\downloads"
    file_list = os.listdir(path_dir)
    print(file_list)

    for p in players:
        if not p in file_list:
            os.makedirs(path_dir + "\\" + p)

print("Start")

make_download_dir(players)
# crawler.downloader('hide on bush')
# replay_maker.recorder()