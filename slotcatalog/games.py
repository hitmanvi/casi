import os
import re
from bs4 import BeautifulSoup
from pathlib import Path
import json
def extract_game_data(html_content):
    """
    Extract game data from HTML content containing slotCard elements.
    
    Args:
        html_content (str): HTML content to parse
        
    Returns:
        list: List of dictionaries containing game data
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    slot_cards = soup.find_all('div', class_='slotCard')
    
    games_data = []
    
    for card in slot_cards:
        game_data = {}
        
        # Extract game name
        name_element = card.find('a', class_='slotCardName')
        if name_element:
            game_data['name'] = name_element.text.strip()
        
        # Extract thumbnail
        img_element = card.find('div', class_='slotCardImage').find('img')
        if img_element and 'data-src' in img_element.attrs:
            game_data['thumbnail'] = img_element['data-src']
        
        # Extract game URL
        url_element = card.find('div', class_='slotCardImage').find('a')
        if url_element and 'href' in url_element.attrs:
            game_data['url'] = url_element['href']
        
        # Extract properties from propTable
        prop_table = card.find('div', class_='propTable')
        if prop_table:
            prop_lines = prop_table.find_all('div', class_='propTableLine')
            
            for line in prop_lines:
                # Extract property name and value
                prop_text = line.get_text().strip()
                prop_parts = prop_text.split(':', 1)
                
                if len(prop_parts) == 2:
                    prop_name = prop_parts[0].strip()
                    prop_value = prop_parts[1].strip()
                    game_data[prop_name] = prop_value
        
        games_data.append(game_data)
    
    return games_data

def process_game_files(directory_path='games_data'):
    """
    Process all HTML files in the specified directory and extract game data.
    
    Args:
        directory_path (str): Path to directory containing HTML files
        
    Returns:
        list: Combined list of game data from all files
    """
    base_dir = Path(__file__).parent
    games_dir = base_dir / directory_path
    
    all_games = []
    
    if not games_dir.exists():
        print(f"Directory not found: {games_dir}")
        return all_games
    
    for file_path in games_dir.glob('*.html'):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                games = extract_game_data(html_content)
                # Extract provider name from the file name
                provider_name = file_path.stem
                
                # Add provider name to each game
                for game in games:
                    game['provider'] = provider_name.replace('_games', '')
                
                # Save games to a JSON file named after the provider
                json_file_path = file_path.with_suffix('.json')
                try:
                    with open(json_file_path, 'w', encoding='utf-8') as json_file:
                        json.dump(games, json_file, indent=4, ensure_ascii=False)
                    print(f"Saved {len(games)} games to {json_file_path.name}")
                except Exception as e:
                    print(f"Error saving to JSON file {json_file_path.name}: {str(e)}")
                all_games.extend(games)
                print(f"Processed {file_path.name}: {len(games)} games found")
        except Exception as e:
            print(f"Error processing {file_path.name}: {str(e)}")
    
    return all_games

if __name__ == "__main__":
    games = process_game_files()
    print(f"Total games extracted: {len(games)}")
    
    # Print sample data
    if games:
        print("\nSample game data:")
        for key, value in games[0].items():
            print(f"{key}: {value}")
