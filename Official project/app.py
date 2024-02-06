'''
START HERE

Frontend handling will be done here.

How to use the flask application:
    In terminal put these in:
    cd "c:/Users/Diego/Valorant-Kill-Predictor/Official project"
    python app.py
    You'll see output in the console indicating that 
    the server is running, typically on http://127.0.0.1:5000/ or http://localhost:5000/



'''
from flask import Flask, request
from main import runModel

app = Flask(__name__)

@app.route('/submit', methods=['POST'])

def submit():

    #Step 1. Receive values
    player_id = request.form['player_id']
    opposing_team = request.form['opposing_team']

    #Check to see if player ID is wrong
    if not player_id.isdigit():
        return "Not a valid ID. Player ID must be a number."
    

    # Step 2: The id and opposing team get sent to main.py where everything will happen
    expectedValue = runModel(player_id, opposing_team)

     #STEP LAST(2)
    # Return the response (or process it further as needed)
    return f"{expectedValue}"



if __name__ == '__main__':
    app.run(debug=True)

