from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import os
import urllib
import math
 
def thumbnail_maker(match_info):
    id = match_info['id']
    player = match_info['name']
    tier = match_info['tier']
    position = match_info['position']
    champion = match_info['champion']
    vs_player = match_info['vs_name']
    vs_champion = match_info['vs_champion']
    badge = match_info['badge']
    kill = match_info['kill']

    if player == "Hide on bush":
        player = "T1 Faker"

    thumbnail_img = Image.open(f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\img\\champions\\{champion.upper()}.jpg")
    bright = ImageEnhance.Brightness(thumbnail_img)
    thumbnail_img = bright.enhance(0.7)
    
    player_font_size = 140
    champion_font_size = 170

    if len(player) > 11:
        player_font_size = 100

    if len(champion) > 10:
        champion_font_size = 130
    
    player_font = ImageFont.truetype("fonts\Kanit-BlackItalic.ttf", player_font_size)
    champion_font = ImageFont.truetype("fonts\PermanentMarker-Regular.ttf", champion_font_size)
    badge_font = ImageFont.truetype("fonts\Kanit-BlackItalic.ttf", 70)
    kill_font = ImageFont.truetype("fonts\Kanit-BlackItalic.ttf", 100)
    

    draw = ImageDraw.Draw(thumbnail_img)
    x = math.floor(thumbnail_img.size[0] * 0.1)
    y = math.floor(thumbnail_img.size[1] * 0.4)
    xy_margin = 100
    shadow_offset = 10

    draw.text((x - shadow_offset, y - shadow_offset), player, (0,0,0), font=player_font, align='center')
    draw.text((x, y), player, (255,255,255), font=player_font, align='center')

    draw.text((x - 50 - shadow_offset, y + xy_margin - shadow_offset), f'"{champion}"', (0,0,0), font=champion_font, align='center')
    draw.text((x - 50, y + xy_margin), f'"{champion}"', (255,255,0), font=champion_font, align='center')

    draw.text((x - shadow_offset + 155, y + xy_margin - shadow_offset + 150), f'{kill}', (0,0,0), font=kill_font, align='center')
    draw.text((x + 150, y + xy_margin + 155), f'{kill}', (255,50,50), font=kill_font, align='center')
    
    player_parse = urllib.parse.quote(match_info['name']) # 한글 깨짐 방지
    thumbnail_img.save(f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\img\\thumbnails\\{id}_{player_parse}.jpg","JPEG")

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
#                     'badge': 'MVP',
#                     'kill': 'Double Kill',
#                     'patch': '11.10.3',
#                     'record': False,
#                     'upload': False
#                 }

# thumbnail_maker(match_info)