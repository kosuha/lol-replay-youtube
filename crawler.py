#-*- coding: utf-8 -*-

from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys    # 키보드 사용
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
import time
import urllib

driver_file = 'C:/Users/okeyd/Documents/lol-replay-youtube/chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')    # headless chrome 옵션 적용
options.add_argument('disable-gpu')    # GPU 사용 안함
options.add_argument('lang=ko_KR')    # 언어 설정
driver = webdriver.Chrome(driver_file) # 옵션 적용

def crawler(player):
    player_parse = urllib.parse.quote(player) # 한글 깨짐 방지
    download_replay_tag= '.GameItemList>.GameItemWrap:nth-child(1)>div>.Content>.StatsButton>.Content>.Item>a'
    game_type_tag= '.GameItemList>.GameItemWrap:nth-child(1)>div>.Content>.GameStats>.GameType'
    game_length_tag= '.GameItemList>.GameItemWrap:nth-child(1)>div>.Content>.GameStats>.GameLength'

    url = f'https://www.op.gg/summoner/userName={player_parse}'

    print("-" * 100)

    driver.get(url) # 크롤링할 사이트 호출
    print(url)

    try:
        # 3초간 로딩 대기
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, download_replay_tag))
        )

        game_type = driver.find_element_by_css_selector(game_type_tag).text
        print(game_type)

        game_length = driver.find_element_by_css_selector(game_length_tag).text
        print(game_length)

        download_replay = driver.find_element_by_css_selector(download_replay_tag)
        download_replay.click()
        time.sleep(1)
        driver.switch_to_alert().accept()
        

    # 예외처리
    except TimeoutException:
        print('해당 페이지에 정보가 존재하지 않습니다.')
        driver.quit()
        print("-" * 100)
        return -1

crawler('hide on bush')