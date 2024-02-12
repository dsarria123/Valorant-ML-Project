import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import csv


import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Set up the Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode, optional
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the webpage
#urls = urls = [
 #    'https://www.vlr.gg/294973/team-ludwig-vs-team-tarik-ludwig-x-tarik-invitational-2-match',
     #'https://www.vlr.gg/25200/xset-vs-sentinels-champions-tour-north-america-stage-3-challengers-1-gf',
 #    'https://www.vlr.gg/286660/sentinels-vs-paper-rex-afreecatv-valorant-league-gf/?game=149811&tab=overview'
#]

# List of URLs to scrape
urls = [
    'https://www.vlr.gg/7719/cloud9-blue-vs-t1-cloud9-to-the-skyes-invitational-quarterfinals',
    'https://www.vlr.gg/7433/sentinels-vs-cloud9-blue-jbl-quantum-cup-tournament-r5'
]


for i, url in enumerate(urls):
    driver.get(url)
    # Find elements with 'mod-stat mod-vlr-kills' classes and extract text
    mod_vlr_kills_elements = driver.find_elements(By.CSS_SELECTOR, '.mod-stat.mod-vlr-kills')
    mod_vlr_kills_values = [element.text for element in mod_vlr_kills_elements if element.text.strip() != ""]

    # Save the non-empty values to a CSV file
    with open(f'output_{i}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for value in mod_vlr_kills_values:
            writer.writerow([value])

# Close the driver
driver.quit()



# Define the player name you're looking for
player_name = 'TenZ'
