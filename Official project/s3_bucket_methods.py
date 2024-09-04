import boto3
import pandas as pd
from io import StringIO
from MatchScraper import scrape_player_data
from preprocessData import preprocess_data
from MatchScraper import scrape_new_matches
from MatchScraper import new_matches_exist

# Function to save a player's data to a CSV in the S3 bucket
def save_player_data_to_s3(player_id, df):
    s3_client = boto3.client('s3')
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    file_name = f'player_data_{player_id}.csv'
    s3_client.put_object(Bucket='your-bucket-name', Key=file_name, Body=csv_buffer.getvalue())

# Function to load a player's data from their S3 bucket CSV
def load_player_data_from_s3(player_id):
    s3_client = boto3.client('s3')
    file_name = f'player_data_{player_id}.csv'
    try:
        obj = s3_client.get_object(Bucket='your-bucket-name', Key=file_name)
        df = pd.read_csv(obj['Body'])
        return df
    except s3_client.exceptions.NoSuchKey:
        return None


# Main function to load existing or scrape new player data
# Main function to load existing or scrape new player data
def scrape_or_load_player_data(player_id, opposing_team):
    # Check if data already exists in S3
    existing_data = load_player_data_from_s3(player_id)
    
    if existing_data is not None:
        """
        Concatenate new scrape data into old df and return/preprocess the newest df 
        and save it to the s3 bucket
        """
        
        latest_match_date = existing_data['Date'].max()
        
        # Check if there are new matches since the latest match date
        if new_matches_exist(player_id, latest_match_date):
            # Scrape only the new matches
            new_data = scrape_new_matches(player_id, latest_match_date)
            
            # Concatenate new scraped data into the existing DataFrame
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
            
            # Save the updated DataFrame back to S3
            save_player_data_to_s3(player_id, combined_data)
        else:
            # No new data to scrape, just return the existing data
            combined_data = existing_data

        return combined_data
        
    else:
        """
        If no data exists when use whole scraper, preprocess it, save to bucket, and send df
        """
        # No data exists, scrape all data for the player
        scraped_data = scrape_player_data(player_id)
        
        # Preprocess the data as needed (including datetime conversion)
        processed_data = preprocess_data(scraped_data, opposing_team)
        
        # Save the new data to S3
        save_player_data_to_s3(player_id, processed_data)
        return processed_data

