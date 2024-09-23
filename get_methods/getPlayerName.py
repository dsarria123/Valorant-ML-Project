'''
Scrapes the player name based off player_id
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def get_playername(player_id, driver):
    url = f'https://www.vlr.gg/player/matches/{player_id}/'
    driver.get(url)
    player_name_element = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div/div[1]/div[1]/div[2]/div[1]/h1')
    player_name = player_name_element.text.strip() if player_name_element else "Unknown Player"

    return player_name