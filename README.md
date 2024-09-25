### Run with docker:

1. docker pull dsarria123/my-app:latest

2. docker run -p 5000:5000 \
-e AWS_ACCESS_KEY_ID=(Will give this upon request) \
-e AWS_SECRET_ACCESS_KEY=(Will give this upon request) \
-e AWS_DEFAULT_REGION=us-east-1 \
your-dockerhub-dsarria123/my-app:latest


# Python Web Scraping and AWS Data Management
Developed a  web scraper using Selenium and ChromeDriver to gather detailed player statistics from vlr.gg, focusing on competitive match performances. This tool efficiently navigates through player profiles and match details, extracting key data points such as kills, deaths, ACS, KAST, and ADR, as well as agent choices across multiple maps. Data is aggregated into a DataFrame.
- Files Methods used: MatchScraper.py, Table Scraper.py, getPlayerName.py

The data pipeline now includes saving and loading player data directly to and from AWS S3 buckets. Allows for persistent data storage and ensuring the model is always trained on the latest data. When new matches are detected, the scraper only fetches the new data, appends it to specific players existing dataset, and saves it back to S3, optimizing both time and resources.
- Files and Methods used: s3_buckets_methods.py
  
#  Preprocessing
Extracting numeric values from columns like Kills, Deaths, and Assists. 

Handling missing data using imputation techniques. 

Normalizing values and creating custom features such as weighted kills against a specific opposing team, ACS per Death, and KAST normalization.

Applying exponential smoothing on kills to stabilize trends in the data over time.

-Files and Methods used: preprocessData.py

# Model Building
Features used: Smoothed Kills, Weighted Kills Against Opposing Team, Normalized KAST, ACS per Death, KDR, Impact Score, KAD Ratio.

Model: Random Forest Regressor, with fine-tuned hyperparameters such as the number of estimators, max depth, and max features.

Evaluation: The model is evaluated using Mean Squared Error (MSE) and R² scores.

# Front end
Developed a Flask web application that interfaces with the predictive model. The application allows users to input a player's ID and the name of the opposing team. Upon submission, the application dynamically renders predictions and statistical insights, including the predicted kills for the next match, Mean Squared Error (MSE), R² score, most likely agent to be used, and average statistics against the opposing team.
- Methods/file used: app.py, input.html, output.html


![Screenshot 2024-09-05 202655](https://github.com/user-attachments/assets/17b70e50-5c79-4403-9a36-c7e1b3afed53)

# Changes to make
Implement docker, push image to docker hub so people can just pull and run my image.
Comparison for new scrape data to top row csv in s3 bucket, keep scraping until it reaches top row then stop.(For scrape_new_data method)

