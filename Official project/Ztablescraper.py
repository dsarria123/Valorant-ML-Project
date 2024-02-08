from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_data(driver, player_name, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    player_stats = []

    # Get all clickable map boxes, except 'All Maps'
    all_map_boxes = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.vm-stats-gamesnav-item:not([data-game-id="all"])')))

    for box_index, box in enumerate(all_map_boxes):
        driver.execute_script("arguments[0].click();", box)  # Use JavaScript to click to avoid issues with element not being clickable
        map_name = box.text.strip()

        # Use a dynamic wait to ensure the table updates after clicking
        specific_table_selector = f"div.vm-stats-game[data-game-id='{box.get_attribute('data-game-id')}'] .wf-table-inset"
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, specific_table_selector)))
            stats_table = driver.find_element(By.CSS_SELECTOR, specific_table_selector)


            # Extract player stats from the table
           
            player_row = stats_table.find_element(By.XPATH, f".//tr[td[contains(.,'{player_name}')]]")
            acs = player_row.find_elements(By.CSS_SELECTOR, 'td.mod-stat span.mod-both')[1].text.strip()  # Example for ACS, adjust index as needed
            kills = player_row.find_element(By.CSS_SELECTOR, 'td.mod-stat.mod-vlr-kills span.mod-both').text.strip()
            deaths = player_row.find_element(By.CSS_SELECTOR, 'td.mod-stat.mod-vlr-deaths span.mod-both').text.strip()
            assists = player_row.find_element(By.CSS_SELECTOR, 'td.mod-stat.mod-vlr-assists span.mod-both').text.strip()
            kast = player_row.find_elements(By.CSS_SELECTOR, 'td.mod-stat span.mod-both')[6].text.strip()  # Example for ADR, adjust index as needed
            adr = player_row.find_elements(By.CSS_SELECTOR, 'td.mod-stat span.mod-both')[7].text.strip()  # Example for ADR, adjust index as needed


            #This code can find all the first amount of kills in first  game of each match INCLUDING SECOND? but not the amount of kills in the rest of the game
            #player_name_xpath = f"//tr[.//td//div[contains(text(), '{player_name}')]]"
            #player_row = stats_table.find_element(By.XPATH, player_name_xpath)
            #kills = player_row.find_element(By.CSS_SELECTOR, 'td.mod-stat.mod-vlr-kills span.mod-both').text.strip()

            player_stats.append({'Map': map_name, 'Player': player_name, 'Kills': kills, 'Deaths': deaths, 'Assists': assists, 'ACS': acs, 'KAST': kast, 'ADR': adr})
        
        except TimeoutException:
            print(f"Timeout or data not found for map {map_name}.")

        except NoSuchElementException:
            print(f"Tenz cant be found in this map {map_name}.")
    return player_stats


# Set up Selenium driver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment for headless mode
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# List of URLs to scrape
urls = [
    'https://www.vlr.gg/294973/team-ludwig-vs-team-tarik-ludwig-x-tarik-invitational-2-match',
    'https://www.vlr.gg/25200/xset-vs-sentinels-champions-tour-north-america-stage-3-challengers-1-gf',
    'https://www.vlr.gg/286660/sentinels-vs-paper-rex-afreecatv-valorant-league-gf/?game=149811&tab=overview'
]

# Define the player name you're looking for
player_name = 'TenZ'

# Initialize an empty DataFrame to hold all results
all_results_df = pd.DataFrame()

# Loop over the URLs and scrape data from each
for url in urls:
    results = scrape_data(driver, player_name, url)  # Pass the URL to the scrape_data function
    temp_df = pd.DataFrame(results)
    all_results_df = pd.concat([all_results_df, temp_df], ignore_index=True)

# Print and/or save the combined results
print(all_results_df)

# Clean up: close the browser window
driver.quit()
