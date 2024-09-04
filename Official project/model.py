#Functions for model building
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

def buildModel(data):
    """Build and evaluate the optimized Random Forest model."""
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


    return predictions, mse, r2
