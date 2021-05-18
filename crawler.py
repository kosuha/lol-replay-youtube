#-*- coding: utf-8 -*-

from selenium import webdriver    # 라이브러리에서 사용하는 모듈만 호출
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait   # 해당 태그를 기다림
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException    # 태그가 없는 예외 처리
import time
import urllib

def downloader(player):
    options = webdriver.FirefoxOptions()

    driver_file = r"C:/Users/okeyd/Documents/lol-replay-youtube/geckodriver.exe"
    download_location = f"C:\\Users\\okeyd\\Documents\\lol-replay-youtube\\downloads\\{player}"

    options.set_preference("browser.download.folderList", 2) # 다운로드 파일을 원하는 위치로 보내기
    options.set_preference("browser.download.manager.showWhenStarting", False) # 다운로드 관리자 창 비활성화
    options.set_preference("browser.download.dir", download_location) # 경로 설정
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "doesn/matter") # 파일을 여는 데 사용할 파일 형식 묻지 않도록 MIME 설정

    options.add_argument('--headless')  # headless chrome 옵션 적용
    options.add_argument('--disable-gpu')   # GPU 사용 안함

    driver = webdriver.Firefox(executable_path = driver_file, firefox_options=options) # 옵션 적용

    player_parse = urllib.parse.quote(player) # 한글 깨짐 방지
    url = f'https://www.op.gg/summoner/userName={player_parse}'

    print("-" * 100)

    driver.get(url) # 크롤링할 사이트 호출
    print(url)

    try:
        # 3초간 로딩 대기
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.GameItemList'))
        )

        for i in range(20, 0, -1):
            download_replay_tag= f'.GameItemList>.GameItemWrap:nth-child({i})>div>.Content>.StatsButton>.Content>.Item>a'
            game_type_tag= f'.GameItemList>.GameItemWrap:nth-child({i})>div>.Content>.GameStats>.GameType'
            game_length_tag= f'.GameItemList>.GameItemWrap:nth-child({i})>div>.Content>.GameStats>.GameLength'
            data_game_id= driver.find_element_by_css_selector(f'.GameItemList>.GameItemWrap:nth-child({i})>div').get_attribute('data-game-id')
            print(data_game_id)

            game_type = driver.find_element_by_css_selector(game_type_tag).text
            print(game_type)
            if game_type != '솔랭':
                continue

            game_length = driver.find_element_by_css_selector(game_length_tag).text
            print(game_length)

            download_replay = driver.find_element_by_css_selector(download_replay_tag)
            download_replay.click()
            time.sleep(1)

            driver.switch_to_alert().accept()
            time.sleep(1)

            popup_close_tag= f'.DimmedBlock>div>table>tbody>tr>td>div>.Close'
            popup_close = driver.find_element_by_css_selector(popup_close_tag)
            popup_close.click()
            time.sleep(1)

    # 예외처리
    except TimeoutException:
        print('해당 페이지에 정보가 존재하지 않습니다.')
        driver.quit()
        print("-" * 100)
        return -1