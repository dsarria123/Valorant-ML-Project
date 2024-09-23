#Scrape_or_load.py
import pandas as pd
from load_or_save_S3 import load_player_data_from_s3
from load_or_save_S3 import save_player_data_to_s3
from MatchScraper import scrape_player_data
from preprocessData import preprocess_data
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

# Main function to load existing or scrape new player data and put it into df
def scrape_or_load_player_data(player_id, opposing_team):

    # Check if data already exists in S3
    existing_data = load_player_data_from_s3(player_id)
    
    if existing_data is not None:
    
        #Get first row of existing data
        existingfirstRow = existing_data.iloc[0]

        #Start the scraper for the player, it will send in existing first Row so that 
        # whenever it scrapes the table from each link and preprocesses it, if it matches
        #then return what it has gotten so far 
        newData = scrape_player_data(player_id, opposing_team,existingfirstRow)
        
        #Add whatever new data to the existing_Data
        df = pd.concat([newData, existing_data], ignore_index=True)


        #Save that to the s3 bucket and return it
        save_player_data_to_s3(player_id, df)

        return df
        
    else:
        """
        If no data exists when use whole scraper, preprocess it, save to bucket, and send df
        """
        # No data exists, scrape all data for the player
        scraped_data = scrape_player_data(player_id, opposing_team, None)
        
        # Save the new data to S3
        save_player_data_to_s3(player_id, scraped_data)
        return scraped_data


