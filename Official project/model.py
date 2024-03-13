# model.py
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np

def exponential_smoothing(series, alpha=0.3):
    result = [series[0]]  # First value is the same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

def preprocess_data(data, agentPrediction, opposing_team):
    data['Deaths'] = data['Deaths'].str.extract('(\d+)').astype(float)
    data['KAST'] = pd.to_numeric(data['KAST'].str.rstrip('%'), errors='coerce') / 100
    data['Kills'] = pd.to_numeric(data['Kills'], errors='coerce').fillna(0)
    data['ACS'] = pd.to_numeric(data['ACS'], errors='coerce').fillna(0)
    data['Smoothed Kills'] = exponential_smoothing(data['Kills'].values)
    data['Weighted Kills Against Opposing Team'] = data.apply(lambda row: row['Kills'] * 1.5 if row['Opposite team'] == opposing_team else row['Kills'], axis=1)
    average_kills_with_agent = data[data['Agent'] == agentPrediction]['Kills'].mean()
    data['Agent Performance Weight'] = average_kills_with_agent
    return data

def buildModel(data, agentPrediction, opposingTeam):
    data = preprocess_data(data, agentPrediction, opposingTeam)
    numeric_features = ['ACS', 'Smoothed Kills', 'Weighted Kills Against Opposing Team', 'Agent Performance Weight', 'KAST']
    numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='mean')), ('scaler', StandardScaler())])
    preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, numeric_features)])
    X = data[numeric_features]
    y = data['Kills']
    X_processed = preprocessor.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_processed, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return predictions, mse, r2
