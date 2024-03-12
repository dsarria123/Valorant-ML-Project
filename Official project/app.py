#app.py
from flask import Flask, request, render_template
from MatchScraper import scrape_player_data
from model import buildModel
import pandas as pd

app = Flask(__name__)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        player_id = request.form['player_id']
        opposing_team = request.form['opposing_team']
        if not player_id.isdigit():
            return "Not a valid ID. Player ID must be a number."
        scrapedData = scrape_player_data(player_id)
        specificData = scrapedData[scrapedData['Opposite team'] == opposing_team]
        agentPrediction = specificData['Agent'].mode()[0] if not specificData.empty else 'DefaultAgent'
        predictions, mse, r2 = buildModel(scrapedData, agentPrediction, opposing_team)
        sample_prediction = predictions[0] if len(predictions) > 0 else None
        stats = {
            'agentPrediction': agentPrediction,
            'recent_matches': specificData.tail(5).to_dict('records'),
            'avg_acs': specificData['ACS'].mean() if not specificData.empty else 0,
            'avg_kills': specificData['Kills'].mean() if not specificData.empty else 0,
            'sample_prediction': sample_prediction,
            'mse': mse,
            'r2_score': r2
        }
        return render_template('results.html', stats=stats)
    else:
        return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
