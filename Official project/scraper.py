'''
This is the first part of the software.

Dedicated to fetching data from the web, specifically from VLR.gg in your case.
Contains functions to construct URLs with player IDs and scrape the necessary data.
Specifically, using the users inputed id the program will go to this link:
https://www.vlr.gg/player/matches/####/
Make sure to handle exceptions and errors that might occur during scraping.

'''

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep

#Scrapes data and creates a df based off the user input
def scrape_player_data(player_id, opposing_team):

    # Set up the Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode, optional

    # Initialize the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#STEP 1 Navigate to the desired URL
    player_idTEST = 9
    url = f'https://www.vlr.gg/player/matches/{player_idTEST}/'
    driver.get(url)


#STEP 2 LOGIC BEING MADE IN UNOFFICIAL SCRAPER







    driver.quit()






    return f"Received in scraper - Player ID: {player_id}, Opposing Team: {opposing_team}"


