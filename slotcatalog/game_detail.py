import os
import json
from bs4 import BeautifulSoup
import re
from pathlib import Path

def extract_game_data(html_content, filename):
    """
    Extract game data from HTML content
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    game_data = {}
    
    # Extract game title
    title_tag = soup.find('title')
    if title_tag:
        game_data['title'] = title_tag.text.strip()
    
    # Extract review content from reviewRight div
    review_right = soup.find('div', class_='reviewRight')
    if review_right:
        # Extract game name from the attributes section
        attributes_section = review_right.find('h3', id='attributes')
        if attributes_section:
            game_data['name'] = attributes_section.text.strip()
    # Extract game properties from the table in reviewRight
    property_table = review_right.find('table')
    if property_table:
        properties = {}
        rows = property_table.find_all('tr')
        for row in rows:
            prop_left = row.find('th', class_='propLeft')
            prop_right = row.find('td', class_='propRight')
            if prop_left and prop_right:
                property_name = prop_left.text.strip()
                property_value = prop_right.text.strip()
                properties[property_name] = property_value
            elif prop_right:
                # Handle rows with colspan that contain features, themes, or other tags
                # Extract the first part before ":" as key and the rest as value
                colspan_text = prop_right.get_text().strip()
                if ":" in colspan_text:
                    parts = colspan_text.split(":", 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        properties[key] = value
        
        # Move properties to the top level of game_data
        for key, value in properties.items():
            game_data[key] = value
            
    

    # Extract game URL from filename
    game_url = filename.replace('.html', '')
    game_data['url'] = f"/en/slots/{game_url}"
    
    return game_data

def process_game_files():
    """
    Process all game HTML files and convert to JSON
    """
    # Define paths
    input_dir = Path('game_details')
    output_dir = Path('game_json')
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Get list of all HTML files
    html_files = list(input_dir.glob('*.html'))
    print(f"Found {len(html_files)} HTML files to process")
    
    # Process each file
    for i, html_file in enumerate(html_files):
        try:
            filename = html_file.name
            print(f"Processing {i+1}/{len(html_files)}: {filename}")
            
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Extract game data
            game_data = extract_game_data(html_content, filename)
            
            # Save as JSON
            json_filename = filename.replace('.html', '.json')
            output_path = output_dir / json_filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(game_data, f, indent=2, ensure_ascii=False)
            
            print(f"Saved: {json_filename}")
            
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    print("All game files have been processed.")

if __name__ == "__main__":
    process_game_files()
