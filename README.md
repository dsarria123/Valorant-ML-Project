### Run app.py and follow the link to use the application.

# Web Scraping 
Developed a  web scraper using Selenium and ChromeDriver to gather detailed player statistics from vlr.gg, focusing on competitive match performances. This tool efficiently navigates through player profiles and match details, extracting key data points such as kills, deaths, ACS, KAST, and ADR, as well as agent choices across multiple maps. Data is aggregated into a DataFrame and saved as a CSV file, offering a foundational dataset for predictive analytics in player performance.
- Methods used: MatchScraper.py, Table Scraper.py, getPlayerName.py

# Model
Changing to implement AWS SageMaker
- Methods used: model.py

# Front end
Developed a Flask web application that interfaces with the predictive model. The application allows users to input a player's ID and the name of the opposing team. Upon submission, the application dynamically renders predictions and statistical insights, including the predicted kills for the next match, Mean Squared Error (MSE), R² score, most likely agent to be used, and average statistics against the opposing team.
- Methods/file used: app.py, input.html, output.html

<img width="687" alt="Screen Shot 2024-03-12 at 11 50 50 PM" src="https://github.com/dsarria123/Valorant-ML-Project/assets/107361281/91302609-0a68-407e-bb7f-0a70865f3e96">
<img width="1043" alt="Screen Shot 2024-03-12 at 11 52 08 PM" src="https://github.com/dsarria123/Valorant-ML-Project/assets/107361281/f213c527-0a07-449d-a7c5-102936749f55">
