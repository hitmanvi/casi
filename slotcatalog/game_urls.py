import os
import json
import sys

def find_missing_game_details():
    # Define paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    game_urls_path = os.path.join(script_dir, 'game_urls.json')
    game_details_dir = os.path.join(script_dir, 'game_details')
    
    # Check if directories and files exist
    if not os.path.exists(game_urls_path):
        print(f"Error: game_urls.json not found at {game_urls_path}")
        sys.exit(1)
    
    if not os.path.exists(game_details_dir):
        print(f"Error: game_details directory not found at {game_details_dir}")
        sys.exit(1)
    
    # Load game URLs from JSON file
    try:
        with open(game_urls_path, 'r', encoding='utf-8') as f:
            game_urls = json.load(f)
        print(f"Loaded {len(game_urls)} game URLs from game_urls.json")
    except Exception as e:
        print(f"Error loading game_urls.json: {e}")
        sys.exit(1)
    
    # Get list of existing HTML files
    existing_html_files = set()
    for filename in os.listdir(game_details_dir):
        if filename.endswith('.html'):
            existing_html_files.add(filename)
    
    print(f"Found {len(existing_html_files)} HTML files in game_details directory")
    
    # Find missing game details
    missing_urls = []
    for url in game_urls:
        # Extract game name from URL for filename
        game_name = url.split('/')[-1]
        expected_html_file = f"{game_name}.html"
        
        if expected_html_file not in existing_html_files:
            missing_urls.append(url)
    
    print(f"Found {len(missing_urls)} game URLs without corresponding HTML files")
    
    # Output missing URLs
    if missing_urls:
        output_file = os.path.join(script_dir, 'missing_game_urls.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(missing_urls, f, indent=2)
        print(f"Missing game URLs saved to {output_file}")
    else:
        print("All game URLs have corresponding HTML files")
    
    return missing_urls

if __name__ == "__main__":
    missing_urls = find_missing_game_details()
    print(f"Total missing URLs: {len(missing_urls)}")
