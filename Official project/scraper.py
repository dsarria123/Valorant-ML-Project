'''
This is the first part of the software.

Dedicated to fetching data from the web, specifically from VLR.gg in your case.
Contains functions to construct URLs with player IDs and scrape the necessary data.
Specifically, using the users inputed id the program will go to this link:
https://www.vlr.gg/player/matches/####/
Make sure to handle exceptions and errors that might occur during scraping.

'''
#Scrapes data and creates a df based off the user input
def scrape_player_data(player_id, opposing_team):

    return f"Received in scraper - Player ID: {player_id}, Opposing Team: {opposing_team}"


