import { fileURLToPath } from 'url';
import { dirname } from 'path';
import fs from 'fs';
import path from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function fetchAllGames(provider) {
  let page = 1;
  let hasMoreGames = true;
  const outputDir = path.join(__dirname, 'games_data');
  
  // Create directory if it doesn't exist
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir);
  }
  
  // Create a filename with timestamp
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const outputPath = path.join(outputDir, `${provider}_games.html`);
  
  // Initialize the output file
  fs.writeFileSync(outputPath, '');
  
  console.log(`Starting to fetch all games data for ${provider}...`);
  
  while (hasMoreGames) {
    console.log(`Fetching page ${page}...`);
    
    const response = await fetch("https://slotcatalog.com/index.php", {
      "headers": {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "cookie": "PHPSESSID=uk1encj3ur5f2rlmt5trvnbt0q; _ga=GA1.1.2111868525.1745805557; cf_clearance=I3.g1EZPpAwM1htQZIF93UBWz6SCqmDWKsxps90ekPg-1745805557-1.2.1.1-liu6aXZzm.pv6ybwdGjlaqqHK88_.RF758Pp3rtUI32rFqBN.lpJm6V08DGMM5uAH0eDmxxMeRetN45sGCezVjtYm6GGfxNkonheDrH8yEF9iDpxoF2gg9GiVwVEYgTSqJJb8rk2x6wIRWUc884m23AMLsyIPBS0SXucJCoOhPjYUW39rju79eK7efRzM6314dt1Sjh.aVf7tqOE.NIoXk.ftrkyqJ_u_hJAPbypZ_ZZUjWb3KNgywvZsLFlkfSmSQdMg6796ARlWprioEh5CIXfU_65c5eWUHpQiGvYuBCMtJltf91izUMiZnCpKyDtct2do1L8DmxjZhYDDPZyrr4WPDIIjgT5HlrAcdSAcN4; _ga_V8JCB553MD=GS1.1.1745805557.1.1.1745805566.0.0.0",
        "Referer": `https://slotcatalog.com/en/soft/${provider}`,
        "Referrer-Policy": "strict-origin-when-cross-origin"
      },
      "body": `lang=en&tag=BRAND&brandtranslit=${provider}&blck=pLoadMoreBrandGames&ajax=1&p=${page}&ver=0`,
      "method": "POST"
    });
    
    const data = await response.text();
    
    // Check if the response contains game cards
    if (!data.includes('<div class="slotCard">')) {
      hasMoreGames = false;
      console.log(`No more games found at page ${page}.`);
    } else {
      // Append the data to the file
      fs.appendFileSync(outputPath, data);
      console.log(`Data from page ${page} appended to file.`);
      
      // Increment page number for next request
      page++;
      
      // Add a small delay to avoid overwhelming the server
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  console.log(`All game data saved to: ${outputPath}`);
}

// Function to extract provider data from provider_details.json
async function extractProviderData() {
  try {
    
    // Read the providers.json file
    const providersPath = path.join(__dirname, 'providers.json');
    const providersData = fs.readFileSync(providersPath, 'utf8');
    const providersArray = JSON.parse(providersData);
    
    console.log(`Found ${providersArray.length} providers in providers.json`);
    
    // Extract provider names from the title field
    const providers = providersArray.map(provider => {
      if (provider.title) {
        // Extract the provider name from the href field
        const providerName = provider.href.split('/').pop();
        return {
          name: provider.title,
          formattedName: providerName,
          totalGames: 0 // We don't have this information from providers.json
        };
      }
      return null;
    }).filter(provider => provider !== null);
    
    console.log(`Successfully extracted ${providers.length} provider names`);
    
    // Create a directory for game data if it doesn't exist
    const gameDataDir = path.join(__dirname, 'game_data');
    if (!fs.existsSync(gameDataDir)) {
      fs.mkdirSync(gameDataDir);
      console.log(`Created directory: ${gameDataDir}`);
    }
    
    // Process each provider
    for (const provider of providers) {
      
      console.log(`Processing provider: ${provider.name} (${provider.formattedName})`);
      console.log(`Expected total games: ${provider.totalGames}`);
      
      // Fetch games for this provider
      await fetchAllGames(provider.formattedName);
      
      // Add a delay between providers to avoid overwhelming the server
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
    
    console.log('Completed fetching games for all providers');
  } catch (error) {
    console.error('Error extracting provider data:', error);
  }
}

// Main function to start the process
async function main() {
  await extractProviderData();
}

// Run the main function
main().catch(error => {
  console.error('Error in main execution:', error);
});


