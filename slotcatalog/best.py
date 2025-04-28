import os
from pathlib import Path
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    # Get the path to the best_slots.html file
    base_dir = Path(__file__).parent
    html_file_path = base_dir / 'games_data' / 'best_slots.html'
    
    # Extract countries
    countries = extract_countries_from_html(html_file_path)
    
    if countries:
        print(f"Found {len(countries)} countries")
        
        # Save countries to file
        output_file = base_dir / 'countries.txt'
        save_countries_to_file(countries, output_file)
    else:
        print("No countries found in the HTML file.")
