import os
import json
from bs4 import BeautifulSoup

def parse_provider_details():
    details_dir = "slotcatalog/details"
    all_provider_details = []
    
    # Iterate through all HTML files in details directory
    for filename in os.listdir(details_dir):
        if filename.endswith(".html"):
            with open(os.path.join(details_dir, filename), 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find the provider attributes table
            attr_div = soup.find('div', class_='provFormalAttr')
            if not attr_div:
                continue
                
            table = attr_div.find('table')
            if not table:
                continue
                
            provider_details = {}
            
            # Extract each row's key-value pair
            for row in table.find_all('tr'):
                # Get the header text (key)
                header = row.find('th', class_='propLeft')
                if not header:
                    continue
                key = header.text.strip().rstrip(':')
                
                # Get the value
                value_cell = row.find('td', class_='propRight')
                if not value_cell:
                    continue
                    
                # If there's a link, get both the link text and href
                value = value_cell.find('a')
                if value:
                    link_text = value.text.strip()
                    link_href = value.get('href', '')
                    value = {
                        'text': link_text,
                        'href': link_href
                    }
                else:
                    value = value_cell.text.strip()
                
                # Get provider logo image URL if present
                logo_img = soup.find('div', class_='provider-page-scr').find('img')
                if logo_img:
                    provider_details['Logo'] = logo_img.get('src', '')
                provider_details[key] = value
                provider_details['name'] = filename.split('.')[0].split('_')[0]
            if provider_details:
                all_provider_details.append(provider_details)
                
    return all_provider_details

def save_provider_details():
    details = parse_provider_details()
    with open('provider_details.json', 'w', encoding='utf-8') as f:
        json.dump(details, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    save_provider_details()
