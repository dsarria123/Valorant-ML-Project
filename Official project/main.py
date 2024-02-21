'''
This is where the the user input is brought to have everything done to it
APP.py brings the values 
Those values get sent to the function in scraper.py to return a dataframe
That data frame gets sent to the function in data_processor to return a processed data frame
That processed data frame then gets sent to the model builder 
That model is then used to return an expected value
That expected value is returned to app.py to get returned to the user

'''

from MatchScraper import scrape_player_data
from data_processor import processdata
from model_builder import buildModel

#Main function
def runModel(player_id, opposing_team):
    
    #STEP 3 DATA GETS SENT TO SCRAPE
    scrapeddata = scrape_player_data(player_id)
    #STEP 4 SCRAPED DATA GETS SEND TO CLEAN, AND MADE INTO A NEW DATASET INCLUDING NEW FEATURES, ETC.
    gooddata = processdata(scrapeddata)
    #STEP 5 GOOD DATA GETS SENT TO RUN THROUGH THE MODEL
    'expectedValue = buildModel(gooddata)'

    #STEP LAST(1). Gets sent back to app.py
    'CURRENTLY SCRAPEDDATA TO JUST MAKE SURE EVERYTHING IS WORKING CORRECTLY'
    return scrapeddata