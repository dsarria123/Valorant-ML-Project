from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor 

# Load data directly from the CSV file
data = pd.read_csv('output.csv')  # Updated path to loaded data file

opposing_team = 'LOUD'  # Example opposing team

def exponential_smoothing(series, alpha=0.3):
    """Apply exponential smoothing to a series of values."""
    result = [series[0]]  # First value is the same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n - 1])
    return result

def exponential_smoothing(series, alpha=0.3):
    result = [series[0]]  # First value is the same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

def preprocess_data(data, opposing_team):
    """Preprocess the data for modeling."""
    # Extract numeric values from 'Deaths' using regex to handle cases like '/ 10 /'
    data['Deaths'] = data['Deaths'].str.extract(r'/\s*(\d+)\s*/').astype(float).fillna(1)  # Fill with 1 to avoid division by zero
    
    # Ensure all necessary columns are numeric, handling errors by coercing them to NaN
    data['Kills'] = pd.to_numeric(data['Kills'], errors='coerce').fillna(0).astype(int)
    data['Assists'] = pd.to_numeric(data['Assists'], errors='coerce').fillna(0).astype(int)
    
    # Remove '%' from KAST and handle non-numeric cases by converting to NaN, then to float
    data['KAST'] = pd.to_numeric(data['KAST'].str.rstrip('%'), errors='coerce').fillna(0) / 100
    
    # Ensure numeric conversion for ACS and handle non-numeric entries
    data['ACS'] = pd.to_numeric(data['ACS'].apply(lambda x: ''.join(filter(str.isdigit, str(x)))), errors='coerce').fillna(0)
    data['ADR'] = pd.to_numeric(data['ADR'], errors='coerce').fillna(0)
    
    # Apply exponential smoothing to 'Kills'
    data['Smoothed Kills'] = exponential_smoothing(data['Kills'].values)
    
    # Create a feature for kills against the specified opposing team
    data['Weighted Kills Against Opposing Team'] = data.apply(
        lambda row: row['Kills'] * 1.5 if row['Opposite team'] == opposing_team else row['Kills'], axis=1
    )
    
    # Normalize KAST
    data['Normalized KAST'] = (data['KAST'] - data['KAST'].mean()) / data['KAST'].std()
    
    # ACS per Death
    data['ACS per Death'] = data['ACS'] / data['Deaths']  # Deaths is already handled for division by zero
    
    # Kill-to-Death Ratio (KDR)
    data['KDR'] = data['Kills'] / data['Deaths']  # Deaths is already handled for division by zero
    
    # Impact Score
    data['Impact Score'] = (data['Kills'] * 0.4) + (data['ACS'] * 0.3) + (data['KAST'] * 0.3)
    
    # KAD Ratio
    data['KAD Ratio'] = (data['Kills'] + data['Assists']) / data['Deaths']  # Deaths is already handled for division by zero

    return data




def build_optimized_random_forest_model(data, opposing_team):
    """Build and evaluate the optimized Random Forest model."""
    
    # Preprocess the data
    data = preprocess_data(data, opposing_team)

    # Define features and target variable
    numeric_features = ['Smoothed Kills', 'Weighted Kills Against Opposing Team', 'Normalized KAST', 
                        'ACS per Death', 'KDR', 'Impact Score', 'KAD Ratio']

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

    # Initialize the Random Forest Regressor with best parameters from Grid Search
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, max_features='sqrt', min_samples_split=2, min_samples_leaf=1, random_state=42)

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

# Build the optimized Random Forest model with additional features
predictions, mse, r2, feature_importances = build_optimized_random_forest_model(data, opposing_team)

# Calculate the average predicted kills
avg_kills = np.mean(predictions)

# Print out updated analysis information
print(f"Average Predicted Kills: {avg_kills}")
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")
print("Feature Importances:\n", feature_importances)
