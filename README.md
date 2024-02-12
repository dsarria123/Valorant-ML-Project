# Valorant-Kill-Predictor
Building a linear regression model using Python scikit-learn(tensor flow for the new model) to predict player kills in Valorant matches.
The goal will be to create a little program or website where you plug in the players name, and team they are versing. This will then be plugged into a webscraper to gather all data possible from vlr.gg which has every single pro match from every single pro player. This data will be used to make a more accurate prediction. I will be building the model using tensor flow.

# Part 1 Web Scraping 3/4
Build webscraper that extracts the players statistics from all his recorded matches on vlr.gg.
- Methods used: MatchScraper.py, Table Scraper.py, getPlayerName.py, getOpposingTeam.py

TODO: Finish getOpposingTeam.py

# Part 2 Cleaning and Feature engineering
The data frame that was scraped gets sent to clean. Then this data will be used to create the statistics we want to show on the website. As well as being sent to the model.

TODO: Figure out what statistics.




