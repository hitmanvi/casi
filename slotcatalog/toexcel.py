import json
import os
import pandas as pd
from pathlib import Path

def convert_json_to_csv(json_file_path, output_csv_path=None):
    """
    Extract game rankings from all countries and create a CSV file with game names in the first column
    and country codes in other columns, with values representing the game's position in each country's list.
    
    Args:
        json_file_path (str): Path to the JSON file
        output_csv_path (str, optional): Path for the output CSV file. If None, will use the same name as JSON file.
    
    Returns:
        str: Path to the created CSV file
    """
    try:
        # Load the JSON data
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # If output path not specified, create one based on input file
        if output_csv_path is None:
            output_csv_path = os.path.splitext(json_file_path)[0] + '_rankings.csv'
        
        # Dictionary to store game rankings across countries
        game_rankings = {}
        
        # Process each country's data
        for country_code, games in data.items():
            # Enumerate games to get their position (1-based index)
            for position, game in enumerate(games, 1):
                # Get game name
                game_name = game.get('name')
                
                if game_name:
                    # Initialize entry for this game if it doesn't exist
                    if game_name not in game_rankings:
                        game_rankings[game_name] = {}
                    
                    # Add the position for this country
                    game_rankings[game_name][country_code] = position
         
        # Convert the nested dictionary to a DataFrame
        df = pd.DataFrame.from_dict(game_rankings, orient='index')
        
        # Reset index to make game names a column
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'Game Name'}, inplace=True)
        # Sort the DataFrame to have Game Name and provider columns first
        # First, check if 'provider' is in the data
        provider_column = None
        for column in df.columns:
            if column.lower() == 'provider':
                provider_column = column
                break
        
        # Rearrange columns to have Game Name and provider (if exists) first
        if provider_column:
            # Get all columns except Game Name and provider
            other_columns = [col for col in df.columns if col != 'Game Name' and col != provider_column]
            # Reorder columns with Game Name and provider first
            df = df[['Game Name', provider_column] + other_columns]
        else:
            # If provider column doesn't exist, just ensure Game Name is first
            other_columns = [col for col in df.columns if col != 'Game Name']
            df = df[['Game Name'] + other_columns]
        
        # Write to CSV
        df.to_csv(output_csv_path, index=False, encoding='utf-8')
        
        print(f"CSV file with game rankings created successfully at: {output_csv_path}")
        return output_csv_path
    
    except Exception as e:
        print(f"Error converting JSON to CSV: {str(e)}")
        return None

if __name__ == "__main__":
    # Get the path to the JSON file
    base_dir = Path(__file__).parent
    json_file_path = base_dir / 'games_data' / 'all_games_by_country.json'
    
    # Convert to CSV
    convert_json_to_csv(json_file_path)
