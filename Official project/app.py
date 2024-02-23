from flask import Flask, request, render_template
from MatchScraper import scrape_player_data
from data_processor import processdata  # Assuming this function exists
from model_builder import buildModel  # Assuming this function exists
import pandas as pd

app = Flask(__name__)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Step 1: Receive values from the form
        player_id = request.form['player_id']
        opposing_team = request.form['opposing_team']

        # Validate player ID
        if not player_id.isdigit():
            return "Not a valid ID. Player ID must be a number."

        # Step 2: Scrape player data
        scrapedData = scrape_player_data(player_id)

        # Step 3: Filter data for specific opposing team
        specificData = scrapedData[scrapedData['Opposite team'] == opposing_team]

        # Step 4: Get statistics that I want to display other than building the model(DATA_PROCESSOR.PY)
        webstats =   

        # Step 5: Build model and get predicted kill #
        prediction =  # Assuming this returns a prediction

        # Step 6: Return results 
        
        '''
    Specifically:
    @return The agent he most likely be playing 
    @return A table with the most recent matches 
    @return The prediction value
    @return Average ADS, Average ACS, versing that team 
    @CAN ONLY RETURN ONE TIME, SO FIGURE OUT HOW TO PUT ALL THE STATISTICS INTO 1 TABLE AND DISPLAY IT IN HTML?
    
    '''
        return render_template('results.html', stats=stats, prediction=prediction)




  











    else:
        # Render the form for GET requests
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
