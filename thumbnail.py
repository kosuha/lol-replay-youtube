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

    if player == "Hide on bush":
        player = "T1 Faker"

    thumbnail_img = Image.open(f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\img\\champions\\{champion.upper()}.jpg")
    bright = ImageEnhance.Brightness(thumbnail_img)
    thumbnail_img = bright.enhance(0.7)
    
    font_1_size = 150
    font_2_size = 170

    if len(player) > 12:
        font_1_size = 100

    if len(champion) > 10:
        font_2_size = 130
    
    font_1 = ImageFont.truetype("fonts\Kanit-BlackItalic.ttf", font_1_size)
    font_2 = ImageFont.truetype("fonts\PermanentMarker-Regular.ttf", font_2_size)

    draw = ImageDraw.Draw(thumbnail_img)
    x = math.floor(thumbnail_img.size[0] * 0.1)
    y = math.floor(thumbnail_img.size[1] * 0.4)
    xy_margin = 100
    shadow_offset = 10

    draw.text((x - shadow_offset, y - shadow_offset), player, (0,0,0), font=font_1, align='center')
    draw.text((x, y), player, (255,255,255), font=font_1, align='center')

    draw.text((x - 50 - shadow_offset, y + xy_margin - shadow_offset), f'"{champion}"', (0,0,0), font=font_2, align='center')
    draw.text((x - 50, y + xy_margin), f'"{champion}"', (255,255,0), font=font_2, align='center')
    
    player_parse = urllib.parse.quote(match_info['name']) # 한글 깨짐 방지
    thumbnail_img.save(f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\img\\thumbnails\\{id}_{player_parse}.jpg","JPEG")
