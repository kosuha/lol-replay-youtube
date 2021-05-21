#-*- coding: utf-8 -*-

import os
from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
import time
import urllib
import pandas as pd

def downloader(player):
    options = webdriver.FirefoxOptions()

    driver_file = r"C:/Users/okeyd/Documents/lol-replay-youtube/geckodriver.exe"
    download_location = f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\downloads\\{player[0]}"

    options.set_preference("browser.download.folderList", 2) # 다운로드 파일을 원하는 위치로 보내기
    options.set_preference("browser.download.manager.showWhenStarting", False) # 다운로드 관리자 창 비활성화
    options.set_preference("browser.download.dir", download_location) # 경로 설정
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "doesn/matter") # 파일을 여는 데 사용할 파일 형식 묻지 않도록 MIME 설정

    options.add_argument('--headless')  # headless 옵션 적용
    options.add_argument('--disable-gpu')   # GPU 사용 안함

    driver = webdriver.Firefox(executable_path = driver_file, firefox_options=options) # 옵션 적용

    player_parse = urllib.parse.quote(player[0]) # 한글 깨짐 방지
    url = f'https://www.op.gg/summoner/userName={player_parse}'

    print("-" * 100)

    driver.get(url) # 크롤링할 사이트 호출
    print(url)

    try:
        # 3초간 로딩 대기
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.GameItemList'))
        )

        # 언어 설정 변경
        language_tag = f'.opgg-language__open'
        language_button = driver.find_element_by_css_selector(language_tag)
        language_button.click()
        time.sleep(1)
        english_tag= f'.DimmedBlockInner>div>.modal-content>div:nth-child(3)>ul>li:nth-child(2)>a'
        english = driver.find_element_by_css_selector(english_tag)
        english.click()
        time.sleep(1)
        language_save_tag= f'.modal-footer>button'
        language_save = driver.find_element_by_css_selector(language_save_tag)
        language_save.click()
        time.sleep(3)

        tier_tag= f'.TierRankInfo>.TierRank'
        tier = driver.find_element_by_css_selector(tier_tag).text

        dfs = []

        for i in range(20, 0, -1):
            download_replay_tag= f'.GameItemList>.GameItemWrap:nth-child({i})>div>.Content>.StatsButton>.Content>.Item:nth-child(1)>a'
            game_type_tag= f'.GameItemList>.GameItemWrap:nth-child({i})>div>.Content>.GameStats>.GameType'
            game_length_tag= f'.GameItemList>.GameItemWrap:nth-child({i})>div>.Content>.GameStats>.GameLength'
            summoner_name_tag= f'.GameItemList>.GameItemWrap:nth-child({i})>div>.Content>div>.Team>div:nth-child({player[1]})>.SummonerName'
            summoner_champion_tag= f'.GameItemList>.GameItemWrap:nth-child({i})>div>.Content>div>.Team>div:nth-child({player[1]})>.ChampionImage>div:nth-child(1)'
            
            summoners = driver.find_elements_by_css_selector(summoner_name_tag)
            summoners_champion = driver.find_elements_by_css_selector(summoner_champion_tag)
            data_game_id= driver.find_element_by_css_selector(f'.GameItemList>.GameItemWrap:nth-child({i})>div').get_attribute('data-game-id')
            game_length = driver.find_element_by_css_selector(game_length_tag).text
            game_length = (int(game_length[:game_length.index('m')]) * 60) + int(game_length[game_length.index('m')+1:game_length.index('s')])
            
            # 선수 주 포지션이 아닐 경우 패스
            if summoners[0].text.lower() != player[0].lower() and summoners[1].text.lower() != player[0].lower():
                continue

            # 이미 있는 리플레이는 패스
            file_list = os.listdir(download_location)
            if f'{data_game_id}.bat' in file_list:
                continue
            
            # 솔랭이 아니면 패스
            game_type = driver.find_element_by_css_selector(game_type_tag).text
            if game_type != 'Ranked Solo':
                continue

            # 리플레이 다운로드 리플레이가 없으면 패스
            try:
                download_replay = driver.find_element_by_css_selector(download_replay_tag)
                download_replay.click()
                time.sleep(1)

                driver.switch_to_alert().accept()
                time.sleep(1)
                popup_close_tag= f'.DimmedBlock>div>table>tbody>tr>td>div>.Close'
                popup_close = driver.find_element_by_css_selector(popup_close_tag)
                popup_close.click()
                time.sleep(1)
            except:
                continue
            
            # 다운로드한 파일명 바꾸기
            src = os.path.join(download_location, f'LOL_OPGG_Observer_{data_game_id}_replay.bat')
            new_name = os.path.join(download_location, f'{data_game_id}.bat')
            os.rename(src, new_name)

            match_info_dict = {
                'id': data_game_id,
                'name': player[0],
                'tier': tier,
                'position': player[1],
                'length': game_length,
                'champion': '',
                'vs_name': '',
                'vs_champion': '',
                'team': '',
                'record': False,
                'upload': False
            }

            # 팀 구분하고 매치 정보 저장
            if summoners[0].text == player[0]:
                match_info_dict['champion'] = summoners_champion[0].text
                match_info_dict['vs_champion'] = summoners_champion[1].text
                match_info_dict['vs_name'] = summoners[1].text
                match_info_dict['team'] = 'blue'

            if summoners[1].text == player[0]:
                match_info_dict['champion'] = summoners_champion[1].text
                match_info_dict['vs_champion'] = summoners_champion[0].text
                match_info_dict['vs_name'] = summoners[0].text
                match_info_dict['team'] = 'red'

            match_info_df = pd.DataFrame(match_info_dict, index=[0])
            print(match_info_df)
            dfs.append(match_info_df)

        df = pd.concat(dfs)
        
        # 20개가 넘어가면 오래된 파일은 삭제
        file_list = os.listdir(download_location)
        if len(file_list) > 20:
            remove_length = len(file_list) - 20
            for i in range(0, remove_length):
                remove_target = os.path.join(download_location, file_list[i])
                os.remove(remove_target)
        
        print("-" * 100)
        driver.quit()
        return df

    # 예외처리
    except TimeoutException:
        print('해당 페이지에 정보가 존재하지 않습니다.')
        driver.quit()
        print("-" * 100)
        return -1