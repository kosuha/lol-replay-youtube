from thumbnail import thumbnail_maker
from moviepy.editor import *
import urllib

def video_maker(match_info):
    id = match_info['id']
    player = match_info['name']
    tier = match_info['tier']
    position = match_info['position']
    champion = match_info['champion']
    vs_player = match_info['vs_name']
    vs_champion = match_info['vs_champion']

    highlights_location = 'C:\\Users\\okeyd\\Documents\\League of Legends\\Highlights'
    highlights_list = os.listdir(highlights_location)
    clip_src = os.path.join(highlights_location, highlights_list[0])
    parent_clip = VideoFileClip(clip_src)

    # player_parse = urllib.parse.quote(player) # 한글 깨짐 방지
    # thumbnails_location = f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\img\\thumbnails\\{id}_{player_parse}.jpg"
    # thumbnail_clip = ImageClip(thumbnails_location).set_duration(1)

    

