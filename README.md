### Run app.py and follow the link to use the application.

# Python Web Scraping and AWS Data Management
Developed a  web scraper using Selenium and ChromeDriver to gather detailed player statistics from vlr.gg, focusing on competitive match performances. This tool efficiently navigates through player profiles and match details, extracting key data points such as kills, deaths, ACS, KAST, and ADR, as well as agent choices across multiple maps. Data is aggregated into a DataFrame.
- Files Methods used: MatchScraper.py, Table Scraper.py, getPlayerName.py

The data pipeline now includes saving and loading player data directly to and from AWS S3 buckets. Allows for persistent data storage and ensuring the model is always trained on the latest data. When new matches are detected, the scraper only fetches the new data, appends it to specific players existing dataset, and saves it back to S3, optimizing both time and resources.
- Files and Methods used: s3_buckets_methods.py
- 
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


<img width="687" alt="Screen Shot 2024-03-12 at 11 50 50 PM" src="https://github.com/dsarria123/Valorant-ML-Project/assets/107361281/91302609-0a68-407e-bb7f-0a70865f3e96">
<img width="1043" alt="Screen Shot 2024-03-12 at 11 52 08 PM" src="https://github.com/dsarria123/Valorant-ML-Project/assets/107361281/f213c527-0a07-449d-a7c5-102936749f55">
