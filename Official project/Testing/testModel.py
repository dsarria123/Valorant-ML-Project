'''
Contains code for creating, training, and testing your regression model.
This module would handles everything related to machine learning
selecting the model, training it with your dataset, tuning hyperparameters, and evaluating its performance.
'''

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from MatchScraper import scrape_player_data
from sklearn.preprocessing import StandardScaler
import pandas as pd


# Simulate receiving values (Step 1)
player_id = '9'  # Example ID
opposing_team = 'Paper Rex'  # Example opposing team

def exponential_smoothing(series, alpha=0.3):
    result = [series[0]]  # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

def buildModel(data, agent, opposing_team):
    """
    Build and evaluate a regression model using the specified features.
    
    Parameters:
    - data: DataFrame containing player performance data.
    - agent: The agent predicted to be most likely played.
    - opposing_team: Name of the opposing team to weight kills against.
    """
    
    # Ensure KST is in a proper numerical format
    data['KST'] = data['KST'].str.rstrip('%').astype(float) / 100
    
    # Filter data for performances with the specified agent
    agent_data = data[data['Agent'] == agent]
    
    # Calculate average kills with the agent for weighting
    average_kills_with_agent = agent_data['Kills'].mean()
    
    # Apply exponential smoothing to 'Kills'
    data['Smoothed Kills'] = exponential_smoothing(data['Kills'].values)
    
    # Create a feature for kills against the specified opposing team
    data['Weighted Kills Against Opposing Team'] = data.apply(lambda row: row['Kills'] * 1.5 if row['Opposite team'] == opposing_team else row['Kills'], axis=1)
    
    # Agent Performance Weight: Use average kills with the agent as a feature
    data['Agent Performance Weight'] = average_kills_with_agent
    
    # Include KST as a feature, now properly formatted
    # Other features are included as before
    X = data[['ACS', 'Smoothed Kills', 'Weighted Kills Against Opposing Team', 'Agent Performance Weight', 'KST']]
    y = data['Kills']  # Target variable
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # Model building
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Prediction
    predictions = model.predict(X_test)
    
    # Evaluation
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    # New: Output feature coefficients for analysis
    feature_coefficients = pd.Series(model.coef_, index=['ACS', 'Smoothed Kills', 'Weighted Kills Against Opposing Team', 'Agent Performance Weight', 'KST'])
    
    # Return detailed metrics and model insights
    return predictions, mse, r2, feature_coefficients



    

if not player_id.isdigit():
    print("Not a valid ID. Player ID must be a number.")
else:
    scrapedData = scrape_player_data(player_id)  # Make sure this function is defined and returns the expected DataFrame
    specificData = scrapedData[scrapedData['Opposite team'] == opposing_team]
    agentPrediction = specificData['Agent'].mode()[0]
    predictions, mse, r2, feature_coefficients = buildModel(scrapedData, agentPrediction, opposing_team)
    
    # New: Print out detailed analysis information
    print(f"Predicted Kills (First Test Sample): {predictions[0]}")
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
    print("Feature Coefficients:\n", feature_coefficients)

