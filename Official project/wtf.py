from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException

player_id = 9
page_number = 1


chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment for headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)



url = f'https://www.vlr.gg/player/matches/{3265}/?page={page_number}'

driver.get(url)


player_name_element = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div/div[1]/div[1]/div[2]/div[1]/h1')
player_name = player_name_element.text.strip() if player_name_element else "Unknown Player"

print(player_name)