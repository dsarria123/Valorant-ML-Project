from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor  # Import Random Forest Regressor

# Load data directly from the CSV file
data = pd.read_csv('newOutput.csv')  # Make sure to update this path

opposing_team = 'LOUD'  # Example opposing team\

agentPrediction = 'omen'

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

     # Filter data for performances with the specified agent
    agent_data = data[data['Agent'] == agent]
    average_kills_with_agent = agent_data['Kills'].mean()
    data['Agent Performance Weight'] = average_kills_with_agent

    # Calculate historical kills per map
    map_kills_avg = data.groupby('Map')['Kills'].mean().reset_index()
    map_kills_avg.columns = ['Map', 'Historical Kills per Map']

    # Merge historical kills per map back into the original data
    data = data.merge(map_kills_avg, on='Map', how='left')

    # Calculate historical kills per agent
    agent_kills_avg = data.groupby('Agent')['Kills'].mean().reset_index()
    agent_kills_avg.columns = ['Agent', 'Historical Kills per Agent']

    # Merge historical kills per agent back into the original data
    data = data.merge(agent_kills_avg, on='Agent', how='left')
    return data


def build_random_forest_model(data, agentPrediction, opposingTeam):
    """Build and evaluate the Random Forest model."""
    # Preprocess the data
    data = preprocess_data(data, agentPrediction, opposingTeam)

    # Define features and target variable
    numeric_features = ['ACS', 'Smoothed Kills', 'Weighted Kills Against Opposing Team',
                        'Historical Kills per Map', 'Historical Kills per Agent']  # Added new features

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

    X_processed = preprocessor.fit_transform(X)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)

    # Initialize the Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=1000, max_depth=10, random_state=42)

    # Train the model
    rf_model.fit(X_train, y_train)

    # Make predictions
    predictions = rf_model.predict(X_test)

    # Evaluate the model
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    # Get feature importances
    feature_importances = pd.Series(rf_model.feature_importances_, index=numeric_features)

    return predictions, mse, r2, feature_importances

# Build the Random Forest model with updated features
predictions, mse, r2, feature_importances = build_random_forest_model(data, agentPrediction, opposing_team)

avg_kills = np.mean(predictions)
# Print out updated analysis information
print(f"Predicted Kills (First Test Sample): {avg_kills}")
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
print("Feature Importances:\n", feature_importances)
print(avg_kills)

