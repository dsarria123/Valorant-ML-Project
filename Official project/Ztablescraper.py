from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException
import time

def scrape_data(driver, player_name):
    wait = WebDriverWait(driver, 10)
    player_stats = []

    # Get all clickable map boxes
    all_map_boxes = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'vm-stats-gamesnav-item')))
    clickable_map_boxes = [box for box in all_map_boxes if 'mod-disabled' not in box.get_attribute('class')]

    for box in clickable_map_boxes:
        # Click on the map box
        wait.until(EC.element_to_be_clickable(box)).click()
        time.sleep(1)  # Wait for the content to load

        # XPath for map name
        # This XPath should select the element that contains the map name
        map_name_xpath = '//*[@id="wrapper"]/div[1]/div[3]/div[6]/div/div[1]/div[2]/div/div[2]/div'
        map_name_element = driver.find_element(By.XPATH, map_name_xpath)
        map_name = map_name_element.text.strip()

     

        # CSS Selector for kills
        kills_selector = '#wrapper > div.col-container > div.col.mod-3 > div:nth-child(6) > div > div.vm-stats-container > div:nth-child(1) > div:nth-child(4) > div:nth-child(1) > table > tbody > tr:nth-child(1) > td.mod-stat.mod-vlr-kills > span > span.side.mod-side.mod-both'
        kills = driver.find_element(By.CSS_SELECTOR, kills_selector).text.strip()

        # Assuming team name is same across all maps
        team_name_selector = '#wrapper > div.col-container > div.col.mod-3 > div.wf-card.match-header > div.match-header-vs > a.match-header-link.wf-link-hover.mod-2 > div > div.wf-title-med'
        team_name = driver.find_element(By.CSS_SELECTOR, team_name_selector).text.strip()

        player_stats.append({
            'Map': map_name,
            'Team': team_name,
            'Player': player_name,
            'Kills': kills
        })

    return player_stats

# Set up Selenium driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment for headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the URL
url = 'https://www.vlr.gg/294973/team-ludwig-vs-team-tarik-ludwig-x-tarik-invitational-2-match'
driver.get(url)

# Scrape the data
player_name = 'TenZ'
results = scrape_data(driver, player_name)

# Convert results to a DataFrame and print
df = pd.DataFrame(results)
print(df)

# Clean up
driver.quit()

