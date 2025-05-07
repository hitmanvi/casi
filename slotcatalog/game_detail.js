const fs = require('fs');
const path = require('path');

// Function to fetch and save game details
async function fetchAndSaveGameDetail(url, outputDir) {
    try {
        const baseUrl = 'https://slotcatalog.com';
        const fullUrl = baseUrl + url;

        console.log(`Fetching: ${fullUrl}`);

        // Extract game name from URL for filename
        const gameName = url.split('/').pop();
        const outputPath = path.join(outputDir, `${gameName}.html`);

        // Skip if already downloaded
        if (fs.existsSync(outputPath)) {
            console.log(`Already exists: ${gameName}`);
            return;
        }

        const response = await fetch(fullUrl, {
            "headers": {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6",
                "cache-control": "max-age=0",
                "priority": "u=0, i",
                "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"macOS\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "cookie": "_ga=GA1.1.2111868525.1745805557; PHPSESSID=ce6q0o3dijjoiekpemcudsmm43; cf_clearance=N9NoXWQh4kizyBDHiDQKyuC4arKI13DUXwfPQUy_HHw-1746604263-1.2.1.1-Q_LTu7HFRaIxwF4eYvL.XWnqVxJ1pNNVK3eRvmH.Bq9WBfFzkCdu6joJQPAARnLEt_IWObjcffB2NgYESXE_Hc.IiCz4EHy1XMBvWCLgDYk5qpVkeKevwyt_GW7D6t9AqEEQgOssSCU6ABSBbxbX_HPmrHw1iyd4DZl1jSvRMKDoKuCmAHdM0hLthCzwrt16esMe0KY1efTfxuAmnMvBNnIRn6X7JP8xMyyvFW4b7s84hBQ4_a4ka2YGMHtFN6v13sjkPhPrsbEj_m9P._4xzeoWlo86fmcy30y6J571JHp_iNQYVbtsKLBpXbjcHObFv_IB_RfLCczA0jbPuc0MMZMWOuaIJU_hQKbKrLXiM3Y; _ga_V8JCB553MD=GS2.1.s1746604262$o4$g1$t1746604693$j0$l0$h0",
                "Referer": "https://slotcatalog.com/en/soft/Pragmatic-Play",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            },
            "method": "GET"
        });

        if (response.ok) {
            const html = await response.text();
            fs.writeFileSync(outputPath, html);
            console.log(`Saved: ${gameName}`);
        } else {
            console.error(`Failed to fetch ${gameName}: ${response.status} ${response.statusText}`);
        }
    } catch (error) {
        console.error(`Error fetching ${gameName}: ${error.message}`);
        // Wait a bit before retrying to avoid rate limiting
        await new Promise(resolve => setTimeout(resolve, 2000));

    }
}
// Read game URLs from the JSON file
const gameUrls = JSON.parse(fs.readFileSync(path.join(__dirname, 'game_urls.json'), 'utf8'));
// Create output directory if it doesn't exist
const outputDir = path.join(__dirname, 'game_details');
if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
}

// Process game URLs in parallel with concurrency control
async function processGameUrls() {
    console.log(`Processing ${gameUrls.length} game URLs...`);
    
    // Set concurrency limit - adjust based on your system and rate limits
    const concurrencyLimit = 10;
    
    // Process in batches
    for (let i = 6146; i < gameUrls.length; i += concurrencyLimit) {
        const batch = gameUrls.slice(i, i + concurrencyLimit);
        console.log(`Processing batch ${Math.floor(i/concurrencyLimit) + 1}: ${i+1}-${Math.min(i+concurrencyLimit, gameUrls.length)} of ${gameUrls.length}`);
        
        // Process batch in parallel
        await Promise.all(batch.map(async (url, index) => {
            console.log(`Starting ${i + index + 1}/${gameUrls.length}: ${url}`);
            await fetchAndSaveGameDetail(url, outputDir);
        }));
        
        // Add a small delay between batches to avoid overwhelming the server
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    
    console.log('All game details have been processed.');
}

// Start processing
processGameUrls().catch(error => {
    console.error('Error in main process:', error);
});
