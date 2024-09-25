import boto3
import pandas as pd
from io import StringIO



# Function to save a player's data to a CSV in the S3 bucket
def save_player_data_to_s3(player_id, df):
    # Initialize boto3 client with hardcoded credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    file_name = f'player_data_{player_id}.csv'
    s3_client.put_object(Bucket='valggscrapeddata', Key=file_name, Body=csv_buffer.getvalue())

# Function to load a player's data from their S3 bucket CSV
def load_player_data_from_s3(player_id):
    # Initialize boto3 client with hardcoded credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )

    file_name = f'player_data_{player_id}.csv'
    try:
        obj = s3_client.get_object(Bucket='valggscrapeddata', Key=file_name)
        df = pd.read_csv(obj['Body'])
        return df
    except s3_client.exceptions.NoSuchKey:
        return None




