import json
import os

def extract_game_info():
    """
    Extract name and image_url from all games in the all_games_by_country.json file
    and output two JSON files: one with name and image_url, and another with just names.
    """
    # Path to the input file
    input_file = 'slotcatalog/all_games_by_country.json'
    
    # Paths to the output files
    output_file = 'slotcatalog/games_simplified.json'
    names_only_file = 'slotcatalog/games_names_only.json'
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return
    
    try:
        # Read the input JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create dictionaries to store the simplified data
        simplified_data = {}
        names_only_data = {}
        
        # Process each country's games
        for country, games in data.items():
            simplified_data[country] = []
            names_only_data[country] = []
            
            for game in games:
                # Extract only name and image_url for simplified data
                simplified_game = {
                    "name": game.get("name", ""),
                    "image_url": game.get("image_url", "")
                }
                simplified_data[country].append(simplified_game)
                
                # Extract only name for names-only data
                names_only_data[country].append(game.get("name", ""))
        
        # Write the simplified data to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(simplified_data, f, indent=4, ensure_ascii=False)
        
        # Write the names-only data to the second output file
        with open(names_only_file, 'w', encoding='utf-8') as f:
            json.dump(names_only_data, f, indent=4, ensure_ascii=False)
        
        print(f"Successfully extracted game info to {output_file}")
        print(f"Successfully extracted game names to {names_only_file}")
    
    except Exception as e:
        print(f"Error processing the JSON file: {str(e)}")


def unique_rank():
    """
    Analyze the games_names_only.json file to find unique rankings.
    This function identifies unique game lists across different countries
    and outputs the count of unique rankings and the unique rankings themselves.
    """
    # Path to the names-only file
    names_only_file = 'slotcatalog/games_names_only.json'
    
    try:
        # Read the names-only JSON file
        with open(names_only_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Dictionary to store unique rankings
        unique_rankings = {}
        
        # Convert each country's game list to a tuple for hashability
        for country, games in data.items():
            games_tuple = tuple(games)
            
            # Check if this game list already exists
            found = False
            for existing_key, existing_countries in unique_rankings.items():
                if games_tuple == existing_key:
                    existing_countries.append(country)
                    found = True
                    break
            
            # If not found, add as a new unique ranking
            if not found:
                unique_rankings[games_tuple] = [country]
        
        # Print the results
        print(f"Number of unique rankings: {len(unique_rankings)}")
        print("\nUnique rankings and their countries:")
        
        for i, (games, countries) in enumerate(unique_rankings.items(), 1):
            print(f"\nRanking {i} (found in {len(countries)} countries: {', '.join(countries)})")
            print(f"Sample games: {list(games)[:5]}...")
        
        return unique_rankings
        
    except Exception as e:
        print(f"Error analyzing unique rankings: {str(e)}")
        return {}
    
    

if __name__ == "__main__":
    extract_game_info()
