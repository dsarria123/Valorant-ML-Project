from flask import Flask, request, render_template
from MatchScraper import scrape_player_data
from model_builder import buildModel 
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

      
        specificData = scrapedData[scrapedData['Opposite team'] == opposing_team]

        
        # Filter data for the specific opposing team
        specificData = scrapedData[scrapedData['Opposite team'] == opposing_team]
        
        # Calculate average stats against the opposing team
        avg_acs = specificData['ACS'].mean()
        avg_kills = specificData['Kills'].mean()
        # TODO: Determine the agent he will most likely play: Do this by looking at what agents he usually plays versus this team?
        agentPrediction = 

        # Step 3: Prepare data and build model
        prediction = buildModel(scrapedData, agentPrediction)  # This will be defined next

        # Step 4: Prepare stats for display
        stats = {
            'agentPrediction': agentPrediction,
            'recent_matches': specificData.tail(5).to_dict('records'),  # Last 5 matches
            'avg_acs': avg_acs,
            'avg_kills': avg_kills,
            'prediction': prediction
        }
        '''
    Specifically:
    @return The agent he most likely be playing 
    @return A table with the most recent matches 
    @return The prediction value
    @return Average ADS, Average ACS, versing that team 
    '''
        return render_template('results.html', stats=stats)




  











    else:
        # Render the form for GET requests
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
