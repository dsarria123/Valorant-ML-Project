'''
Contains code for creating, training, and testing your regression model.
This module would handles everything related to machine learning
selecting the model, training it with your dataset, tuning hyperparameters, and evaluating its performance.
'''

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def buildModel(data, agent):
    # Filter data for the agent
    agent_data = data[data['Agent(Will show the agent played as first columns)'] == agent]
    
    # Feature engineering could be more sophisticated here
    # For simplicity, let's use ACS and Kills as features
    X = agent_data[['ACS', 'Kills']]
    y = agent_data['Kills']  # Assuming the target is to predict Kills
    
    # Splitting data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Building and training the model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Making predictions
    predictions = model.predict(X_test)
    
    # Evaluating the model (This step is optional and for demonstration)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    # Return a sample prediction or model evaluation
    return predictions[0], mse, r2  # Simplified return for demonstration

    return 