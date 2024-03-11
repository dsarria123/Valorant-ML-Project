from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
import pandas as pd
import numpy as np

# Load data directly from the CSV file
data = pd.read_csv('/Users/diegosarria/Valorant-ML-Project/output.csv')  # Make sure to update this path

opposing_team = 'LOUD'  # Example opposing team

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
    data['KAST'] = data['KAST'].replace('', np.nan).str.rstrip('%').astype(float) / 100
    
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
    
    # Prepare features and target variable
    X = data[['ACS', 'Smoothed Kills', 'Weighted Kills Against Opposing Team', 'Agent Performance Weight', 'KAST']]
    y = data['Kills']
    
    # Impute missing values
    imputer = SimpleImputer(strategy='mean')  # You can change strategy to 'median' or 'most_frequent' if it makes more sense for your data
    
    # Scale features
    scaler = StandardScaler()
    
    # Create a pipeline that first imputes missing values, then scales the data
    pipeline = make_pipeline(imputer, scaler)
    
    X_processed = pipeline.fit_transform(X)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    
    # Model building
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Prediction
    predictions = model.predict(X_test)
    
    # Evaluation
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    feature_coefficients = pd.Series(model.coef_, index=['ACS', 'Smoothed Kills', 'Weighted Kills Against Opposing Team', 'Agent Performance Weight', 'KAST'])
    
    return predictions, mse, r2, feature_coefficients

# Assuming 'Agent' column exists and can be used for agent prediction
agentPrediction = data['Agent'].mode()[0]  # Default prediction method without scraping

predictions, mse, r2, feature_coefficients = buildModel(data, agentPrediction, opposing_team)

# Print out detailed analysis information
print(f"Predicted Kills (First Test Sample): {predictions[0]}")
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
print("Feature Coefficients:\n", feature_coefficients)
