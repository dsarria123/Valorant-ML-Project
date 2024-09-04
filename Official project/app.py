from flask import Flask, request, render_template
from MatchScraper import scrape_player_data
from model import buildModel
from s3_bucket_methods import save_player_data_to_s3
from s3_buckets_methods import load_player_data_from_s3
from s3_buckets_methods import scrape_or_load_player_data
import numpy as np
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
    #Eventually check if its even a player id and throw a message

    #Check if data needs to be fully scraped or partially scraped. Happens in there and returns new/used data.
    data = scrape_or_load_player_data(player_id, opposing_team)
    predictions, mse, r2 = buildModel(data)
    specificData = data[data['Opposite team'] == opposing_team]
    agentPrediction = specificData['Agent'].mode()[0] if not specificData.empty else 'DefaultAgent'
    sample_prediction = np.mean(predictions)
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
