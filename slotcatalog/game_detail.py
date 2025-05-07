import json
import os

def extract_game_urls():
    """
    Extract game URLs from the games_combined.json file and save them to a file.
    """
    # Define file paths
    input_file = 'games_combined.json'
    output_file = 'game_urls.json'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return
    
    try:
        # Read the games data from the JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            games_data = json.load(f)
        
        # Extract URLs from each game
        game_urls = []
        for game in games_data:
            if 'url' in game and game['url']:
                game_urls.append(game['url'])
        
        # Save the URLs to a new JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(game_urls, f, indent=4)
        
        print(f"Successfully extracted {len(game_urls)} game URLs to '{output_file}'.")
    
    except json.JSONDecodeError:
        print(f"Error: Failed to parse '{input_file}' as JSON.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    extract_game_urls()
