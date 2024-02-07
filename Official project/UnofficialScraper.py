#This code loads every game but not some parts of it, refer back to it
'''
def scrape_player_data(player_id):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    wait = WebDriverWait(driver, 10)
    
    match_map_data = []
    page_number = 1

    while True:
        url = f'https://www.vlr.gg/player/matches/{player_id}/?page={page_number}'
        driver.get(url)
        
        try:
            # Check for the presence of match links on the current page, if none found assume end of pages
            match_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.wf-card.fc-flex.m-item')))
        except TimeoutException:
            print(f"No matches found on page {page_number} or the page took too long to respond. Ending the search.")
            break

        for link in match_links:
            href = link.get_attribute('href')
            # Open each match detail page in a new tab to avoid StaleElementReferenceException
            driver.execute_script(f"window.open('{href}');")
            driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab
            try:
                # Check if it's a single-map match first
                single_map_name_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.map > div > span')))
                map_name = single_map_name_element[0].text.strip()
                match_id = href.split('/')[-2]
                match_map_data.append({'Match ID': match_id, 'Map Name': map_name})
            except TimeoutException:
                # If it's not a single-map match, look for multiple maps
                map_links = driver.find_elements(By.CSS_SELECTOR, 'div.vm-stats-gamesnav-item:not(.mod-all) span')
                for map_span in map_links:
                    map_name = map_span.text.strip()
                    if map_name != "All Maps":
                        match_map_data.append({'Match ID': match_id, 'Map Name': map_name})
            finally:
                driver.close()  # Close the tab
                driver.switch_to.window(driver.window_handles[0])  # Switch back to the main window

        page_number += 1  # Increment the page number for pagination

    driver.quit()
    
    df = pd.DataFrame(match_map_data)
    print(df)
    return df

player_id = input("Enter the player ID: ")
df = scrape_player_data(player_id)

'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

pd.set_option('display.max_rows', 100)

def scrape_player_data(player_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Uncomment for headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    wait = WebDriverWait(driver, 10)
    match_map_data = []
    page_number = 1

    while True:
        url = f'https://www.vlr.gg/player/matches/{player_id}/?page={page_number}'
        driver.get(url)
        
        try:
            # Collect all the match links on the current page
            match_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.wf-card.fc-flex.m-item')))
            match_urls = [link.get_attribute('href') for link in match_links]
        except TimeoutException:
            print(f"Page {page_number} took too long to load or no matches found. Ending the search.")
            break

        for match_url in match_urls:
            driver.get(match_url)
            try:
                # Check for a single map first
                map_name_elements = driver.find_elements(By.CSS_SELECTOR, 'div.map > div > span')
                if map_name_elements:
                    map_name = map_name_elements[0].text.strip()
                    match_id = match_url.split('/')[-2]
                    match_map_data.append({'Match ID': match_id, 'Map Name': map_name})
                else:
                    # If multiple maps, get the map names from the navigation bar
                    map_nav_items = driver.find_elements(By.CSS_SELECTOR, 'div.vm-stats-gamesnav-item.js-map-switch')
                    for item in map_nav_items:
                        map_name = item.text.strip()
                        if map_name != "All Maps":
                            match_map_data.append({'Match ID': match_id, 'Map Name': map_name})
            except TimeoutException:
                print(f"Timeout occurred while trying to load maps for match {match_url}")

        page_number += 1  # Increment page number to proceed to the next page of matches

    driver.quit()
    df = pd.DataFrame(match_map_data)
    
    print(df)
    return df

player_id = input("Enter the player ID: ")
df = scrape_player_data(player_id)
df.to_csv("output.csv", index=False)  # Saves the DataFrame to output.csv without the index

