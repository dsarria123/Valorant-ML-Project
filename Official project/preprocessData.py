import pandas as pd

def exponential_smoothing(series, alpha=0.3):
    result = [series[0]]  # First value is the same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result

def preprocess_data(data, opposing_team):
    """Preprocess the data for modeling."""

    #Date time
    data['Date'] = pd.to_datetime(data['Date'])
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