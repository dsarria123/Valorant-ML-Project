from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
from MatchScraper import scrape_player_data  # Assuming this is your custom scraping module

# Example values
player_id = '9'
opposing_team = 'LOUD'

def exponential_smoothing(series, alpha=0.3):
    result = [series[0]]  # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result
    
def buildModel(data, agent, opposing_team):
    """
    Build and evaluate a regression model using the specified features.
    """
    
    # Convert 'KAST' to numeric, handling missing and improper formats
    data['KAST'] = pd.to_numeric(data['KAST'].str.rstrip('%'), errors='coerce') / 100
    
    # Ensure 'Kills' is numeric for exponential smoothing
    data['Kills'] = pd.to_numeric(data['Kills'], errors='coerce').fillna(0)
    data['Smoothed Kills'] = exponential_smoothing(data['Kills'].values)
    
    # Feature engineering
    data['Weighted Kills Against Opposing Team'] = data.apply(
        lambda row: row['Kills'] * 1.5 if row['Opposite team'] == opposing_team else row['Kills'], axis=1)
    average_kills_with_agent = data[data['Agent'] == agent]['Kills'].mean()
    data['Agent Performance Weight'] = average_kills_with_agent
    
    # Select features for transformation
    numeric_features = ['ACS', 'Smoothed Kills', 'Weighted Kills Against Opposing Team', 'Agent Performance Weight', 'KAST']
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features)])

    # Define features and target variable
    X = data[numeric_features]
    y = data['Kills']  # Assuming 'Kills' is the target variable
    
    # Apply transformations
    X_processed = preprocessor.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    
    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions and evaluate the model
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    feature_coefficients = pd.Series(model.coef_, index=numeric_features)
    
    return predictions, mse, r2, feature_coefficients

if not player_id.isdigit():
    print("Not a valid ID. Player ID must be a number.")
else:
    scrapedData = scrape_player_data(player_id)  # Assuming this function returns a DataFrame
    specificData = scrapedData[scrapedData['Opposite team'] == opposing_team]
    agentPrediction = specificData['Agent'].mode()[0] if not specificData.empty else 'DefaultAgent'
    predictions, mse, r2, feature_coefficients = buildModel(scrapedData, agentPrediction, opposing_team)
    
    # Print out detailed analysis information
    print(f"Predicted Kills (First Test Sample): {predictions[0]}")
    print(f"Mean Squared Error: {mse}")
    print(f"R^2 Score: {r2}")
    print("Feature Coefficients:\n", feature_coefficients)
