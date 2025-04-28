import os
from pathlib import Path
from bs4 import BeautifulSoup
import glob
import json

def extract_countries_from_html(html_file_path):
    """
    Extract country ISO codes from the best_slots.html file.
    
    Args:
        html_file_path (str): Path to the HTML file containing country data
        
    Returns:
        list: List of country ISO codes
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the country selector dropdown
        country_select = soup.find('select', {'name': 'ucountry'})
        
        if not country_select:
            print("Country selector not found in the HTML file.")
            return []
        
        countries = []
        
        # Extract country ISO codes
        for option in country_select.find_all('option'):
            country_iso = option.get('value')
            
            if country_iso:
                countries.append(country_iso)
        
        return countries
    
    except Exception as e:
        print(f"Error extracting countries: {str(e)}")
        return []

def save_countries_to_file(countries, output_file):
    """
    Save the extracted country ISO codes to a file.
    
    Args:
        countries (list): List of country ISO codes
        output_file (str): Path to save the countries data
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for country in countries:
                file.write(f"{country}\n")
        
        print(f"Countries saved to {output_file}")
    except Exception as e:
        print(f"Error saving countries to file: {str(e)}")


def extract_games_from_html(soup):
    try:
        # Find all game items (arrow card items based on best_slots_AF.html)
        game_items = soup.find_all('div', class_='arrowCardItem')
        games = []
        
        for item in game_items:
            game = {}
            
            # Extract game name
            name_elem = item.find('h3', class_='arrowCardName')
            if name_elem:
                game['name'] = name_elem.text.strip()
            
            # Extract game URL
            link_elem = item.find('a', class_='slotPageOverlay-link')
            if link_elem and 'href' in link_elem.attrs:
                game['game_url'] = link_elem['href']
            
            # Extract game image URL
            img_elem = item.find('div', class_='gameItemimg').find('img')
            if img_elem and 'src' in img_elem.attrs:
                game['image_url'] = img_elem['src']
            
            # Extract provider from the prop table
            prop_table = item.find('div', class_='propTable')
            if prop_table:
                # Find all property lines in the prop table
                prop_lines = prop_table.find_all('div', class_='propTableLine')
                for prop_line in prop_lines:
                    # Extract property text
                    prop_text = prop_line.get_text().strip()
                    # Split by colon to separate property name and value
                    if ':' in prop_text:
                        prop_parts = prop_text.split(':', 1)
                        prop_name = prop_parts[0].strip().lower().replace(' ', '_')
                        prop_value = prop_parts[1].strip()
                        
                        # Special handling for provider which has a link
                        if prop_name == 'provider':
                            provider_elem = prop_line.find('a')
                            if provider_elem:
                                prop_value = provider_elem.text.strip()
                        
                        # Add the property to the game dictionary
                        game[prop_name] = prop_value
            
            # Extract SlotRank if available
            slotrank_block = item.find('div', class_='slotrank-block')
            if slotrank_block:
                rank_text = slotrank_block.get_text().strip()
                # Extract the numeric rank
                import re
                rank_match = re.search(r'SlotRank\s+(\d+)', rank_text)
                if rank_match:
                    game['rank'] = int(rank_match.group(1))
            
            if game:  # Only add if we found some data
                games.append(game)
        
        return games
    
    except Exception as e:
        print(f"Error extracting games: {str(e)}")
        return []


if __name__ == "__main__":
    # Get all best_slots_XX.html files from games_data directory
    games_data_dir = os.path.join(os.path.dirname(__file__), 'games_data')
    best_slots_files = glob.glob(os.path.join(games_data_dir, 'best_slots_*.html'))
    
    # Dictionary to store games data by country code
    all_games_by_country = {}
    
    for file_path in best_slots_files:
        # Extract country code from filename (best_slots_XX.html)
        country_code = os.path.basename(file_path).split('_')[-1].split('.')[0]
        
        # Read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Parse the HTML and extract games data
        soup = BeautifulSoup(html_content, 'html.parser')
        games_list = extract_games_from_html(soup)
        
        # Store the games list with country code as key
        all_games_by_country[country_code] = games_list
        
        print(f"Processed {country_code}: Found {len(games_list)} games")
    
    print(f"Processed data for {len(all_games_by_country)} countries")
    # Save the games data to a JSON file
    output_file = os.path.join(os.path.dirname(__file__), 'games_data', 'all_games_by_country.json')
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_games_by_country, file, indent=4, ensure_ascii=False)
    
    print(f"Games data saved to {output_file}")
