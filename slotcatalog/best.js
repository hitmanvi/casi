import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Read countries from countries.txt
const readCountries = () => {
  try {
    const countriesPath = path.join(__dirname, 'countries.txt');
    const countriesData = fs.readFileSync(countriesPath, 'utf-8');
    return countriesData.split('\n').filter(country => country.trim() !== '');
  } catch (error) {
    console.error('Error reading countries file:', error);
    return [];
  }
};

// Fetch data for a specific country and page
const fetchData = async (country, page) => {
  try {
    const response = await fetch(`https://slotcatalog.com/index.php?ajax=1&lang=en&p=${page}&translit=The-Best-Slots&ajax=1&blck=top_games_page`, {
      "headers": {
        "accept": "text/html, */*; q=0.01",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "cookie": `PHPSESSID=uk1encj3ur5f2rlmt5trvnbt0q; ucISO=${country}`,
        "Referer": "https://slotcatalog.com/en/The-Best-Slots",
        "Referrer-Policy": "strict-origin-when-cross-origin"
      },
      "method": "GET"
    });
    return await response.text();
  } catch (error) {
    console.error(`Error fetching data for country ${country}, page ${page}:`, error);
    return null;
  }
};

// Process all countries
const processAllCountries = async () => {
  const countries = readCountries();
  console.log(`Found ${countries.length} countries to process`);
  
  // Create games_data directory if it doesn't exist
  const dataDir = path.join(__dirname, 'games_data');
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
  }
  
  for (const country of countries) {
    console.log(`Processing country: ${country}`);
    
    // Fetch both pages
    const page1Data = await fetchData(country, 1);
    const page2Data = await fetchData(country, 2);
    
    if (page1Data && page2Data) {
      // Combine the data (simple concatenation for HTML content)
      const combinedData = page1Data + page2Data;
      
      // Save to file
      const filePath = path.join(dataDir, `best_slots_${country}.html`);
      fs.writeFileSync(filePath, combinedData);
      console.log(`Saved data for ${country} to ${filePath}`);
    } else {
      console.log(`Skipping ${country} due to fetch errors`);
    }
    
    // Add a small delay to avoid overwhelming the server
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  console.log('All countries processed');
};

// Run the main function
processAllCountries().catch(error => {
  console.error('Error in main process:', error);
});