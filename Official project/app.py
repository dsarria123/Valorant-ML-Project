from flask import Flask, request, render_template
from MatchScraper import scrape_player_data
from model import buildModel
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    # Simply render the input form when the root URL is accessed.
    return render_template('input.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Process the form submission.
    player_id = request.form['player_id']
    opposing_team = request.form['opposing_team']
    if not player_id.isdigit():
        return "Not a valid ID. Player ID must be a number."
    scrapedData = scrape_player_data(player_id)
    specificData = scrapedData[scrapedData['Opposite team'] == opposing_team]
    
     # Ensure the data is numeric
    specificData['ACS'] = pd.to_numeric(specificData['ACS'], errors='coerce')
    specificData['Kills'] = pd.to_numeric(specificData['Kills'], errors='coerce')

    agentPrediction = specificData['Agent'].mode()[0] if not specificData.empty else 'DefaultAgent'
    predictions, mse, r2 = buildModel(scrapedData, agentPrediction, opposing_team)
    sample_prediction = predictions[0] if len(predictions) > 0 else None
    stats = {
        'agentPrediction': agentPrediction,
        'recent_matches': specificData.tail(9).to_dict('records'),
        'avg_acs': specificData['ACS'].mean() if not specificData.empty else 0,
        'avg_kills': specificData['Kills'].mean() if not specificData.empty else 0,
        'sample_prediction': sample_prediction,
        'mse': mse,
        'r2_score': r2
    }
    return render_template('output.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True)
