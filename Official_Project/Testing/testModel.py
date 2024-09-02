from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np

# Load data directly from the CSV file
data = pd.read_csv('newOutput.csv')  # Make sure to update this path

opposing_team = 'LOUD'  # Example opposing team

def exponential_smoothing(series, alpha=0.3):
    """Apply exponential smoothing to a series of values."""
    result = [series[0]]  # First value is the same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n - 1])
    return result

def preprocess_data(data, agent, opposing_team):
    """Preprocess the data for modeling."""
    # Extract the middle value between slashes in 'Deaths' and convert to numeric
    data['Deaths'] = data['Deaths'].apply(lambda x: int(x.split('/')[1]) if isinstance(x, str) and '/' in x else x)
    
    # Remove '%' from KAST and convert to numeric
    data['KAST'] = data['KAST'].str.rstrip('%').astype(float) / 100

    # Ensure numeric conversion for ACS and Kills
    data['ACS'] = pd.to_numeric(data['ACS'], errors='coerce').fillna(0)
    data['Kills'] = pd.to_numeric(data['Kills'], errors='coerce').fillna(0)

    # Apply exponential smoothing to 'Kills'
    data['Smoothed Kills'] = exponential_smoothing(data['Kills'].values)

    # Create a feature for kills against the specified opposing team
    data['Weighted Kills Against Opposing Team'] = data.apply(
        lambda row: row['Kills'] * 1.5 if row['Opposite team'] == opposing_team else row['Kills'], axis=1
    )

    # Filter data for performances with the specified agent
    agent_data = data[data['Agent'] == agent]

    # Calculate average kills with the agent for weighting
    average_kills_with_agent = agent_data['Kills'].mean()
    data['Agent Performance Weight'] = average_kills_with_agent

    return data

def buildModel(data, agentPrediction, opposingTeam):
    """Build and evaluate the linear regression model."""
    # Preprocess the data
    data = preprocess_data(data, agentPrediction, opposingTeam)

    # Define features and target variable
    numeric_features = ['ACS', 'Smoothed Kills', 'Weighted Kills Against Opposing Team', 'Agent Performance Weight', 'KAST']
    X = data[numeric_features]
    y = data['Kills']

    # Create a preprocessing pipeline with imputation and scaling
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])

    # Apply the preprocessing pipeline
    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features)
    ])

    X = data[numeric_features]
    y = data['Kills']

    # Process the features
    X_processed = preprocessor.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # Get feature coefficients
    feature_coefficients = pd.Series(model.coef_, index=numeric_features)

    return predictions, mse, r2, feature_coefficients

# Assuming 'Agent' column exists and can be used for agent prediction
agentPrediction = data['Agent'].mode()[0]  # Default prediction method without scraping

# Build the model
predictions, mse, r2,feature_coefficients = buildModel(data, agentPrediction, opposing_team)

# Print out detailed analysis information
print(f"Predicted Kills (First Test Sample): {predictions[0]}")
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
print("Feature Coefficients:\n", feature_coefficients)