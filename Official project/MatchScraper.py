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
from get_methods.getPlayerName import get_playername
from TableScraper import scrape_data

pd.set_option('display.max_rows', 100)

def scrape_player_data(player_id):

    #STEP 1 SET UP SELENIUM DRIVERS
    chrome_options = Options()
    #chrome_options.add_argument("--headless")  # Uncomment for headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    #SET UP WAIT TIMES AND JUST SOME STUFF 
    wait = WebDriverWait(driver, 1)
    match_map_data = [] 
    page_number = 1
    player_name = get_playername(player_id, driver)

    while True:
    #Grabs the url based off player id
        url = f'https://www.vlr.gg/player/matches/{player_id}/?page={page_number}'
        driver.get(url)
        
        try:
            # Collect all the match links on the current page
            match_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.wf-card.fc-flex.m-item')))
            match_urls = [link.get_attribute('href') for link in match_links]
        except TimeoutException:
            print(f"Page {page_number} took too long to load or no matches found. Ending the search.")
            break
    #STEP 2 GOES THROUGH EVERY MATCH LINK, IF ITS A BO1, MOVE TO NEXT LINK, IF NOT, SEND THE DRIVER URL AND PLAYER NAME TO "TableScraper.py"
        for match_url in match_urls:

            match_map_data.extend(scrape_data(driver, player_name, match_url))

        page_number += 1  # Increment page number to proceed to the next page of matches

    driver.quit()
    df = pd.DataFrame(match_map_data)
    
    print(df)
    df.to_csv("output.csv", index=False)  # Saves the DataFrame to output.csv without the index
    return df


# Function to check if new matches exist after the latest date
def new_matches_exist(player_id, last_match_date):
    # Initialize Selenium WebDriver
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 1)

    # Construct the URL for the player's matches
    url = f'https://www.vlr.gg/player/matches/{player_id}/'
    driver.get(url)
    
    try:
        # Find all match date elements on the page
        match_dates = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'moment-tz-convert')))
        for date_element in match_dates:
            match_date = pd.to_datetime(date_element.get_attribute('data-utc-ts'))
            
            # If a match date is newer than the last match date, return True
            if match_date > last_match_date:
                driver.quit()
                return True
    except TimeoutException:
        print("No match dates found or the page took too long to load.")
    
    driver.quit()
    return False


# Function to scrape new matches only
def scrape_new_matches(player_id, last_match_date):
    # Initialize Selenium WebDriver
    chrome_options = Options()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 1)

    new_match_data = []
    page_number = 1

    while True:
        # Construct the URL for the player's matches with pagination
        url = f'https://www.vlr.gg/player/matches/{player_id}/?page={page_number}'
        driver.get(url)

        try:
            # Collect all the match links on the current page
            match_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.wf-card.fc-flex.m-item')))
            match_urls = [link.get_attribute('href') for link in match_links]
            
            # Extract match dates and check if they are new
            for match_url in match_urls:
                driver.get(match_url)
                date_element = driver.find_element(By.CLASS_NAME, 'moment-tz-convert')
                match_date = pd.to_datetime(date_element.get_attribute('data-utc-ts'))

                if match_date > last_match_date:
                    # Scrape data for this match since it's newer
                    player_name = get_playername(player_id, driver)
                    new_match_data.extend(scrape_data(driver, player_name, match_url))
                else:
                    # If a match is older or the same as the last_match_date, stop scraping further
                    driver.quit()
                    return pd.DataFrame(new_match_data)

        except TimeoutException:
            print("Page took too long to load or no matches found.")
            break

        page_number += 1  # Increment page number to check the next page of matches

    driver.quit()
    return pd.DataFrame(new_match_data)