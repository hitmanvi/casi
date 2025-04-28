// Function to make a single request
async function makeRequest(page) {
  const resp = await fetch("https://slotcatalog.com/index.php", {
    "headers": {
      "accept": "*/*",
      "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6", 
      "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
      "priority": "u=1, i",
      "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
      "sec-ch-ua-mobile": "?0",
      "sec-ch-ua-platform": "\"macOS\"",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors", 
      "sec-fetch-site": "same-origin",
      "x-requested-with": "XMLHttpRequest",
      "cookie": "PHPSESSID=s40oo95apcihfvkikuaeel4fg7; _ga=GA1.1.2126622304.1745734846; cookie-ok=1; cf_clearance=LLNoyrTouSk5cBbDnjSXNvzQbP1Qf908catoVJX_d7M-1745738457-1.2.1.1-wdaN56ki63BEMJo1lm3mknTFGhlTU3Cmnllr0ilzeJ_0noDiC6WI6awTqjTonZNdSf3wwUrJm_UfFRwDkNVS5Agsot6ljZvr.G2OMg99FxeeNTSBH9cDoF.APP_su2QzAlTVSDMcM7YTLucbD1XYNMtlG3Q7NaCmIYyYY2MEdGaZB5xsiHzIT7sBj7lIkNDXYOS3WsU02E0fgEW7pNY5wvzgK_swozG_s8wRyk0jBWO7nFjTQ6WX1aK1z17DMzjWZycKy9zYrkK7in3JAmELkhUJ1FskdVyBCMpCdrh9AuJAu6xz.wc54iLORP9.P8CtqyVY0w7GGL91z1Jy4RbOKzbVv.ff0V.xc369TrQwvAI; pv=15; _ga_V8JCB553MD=GS1.1.1745734845.1.1.1745738799.0.0.0",
      "Referer": "https://slotcatalog.com/en/Providers",
      "Referrer-Policy": "strict-origin-when-cross-origin"
    },
    "body": `blck=fltrProvBlk&ajax=1&lang=en&p=${page}&translit=Providers&sorting=PRANK&cISO=CA`,
    "method": "POST"
  });

  const data = await resp.text();
  return data;
}

// Make requests for pages 1-29
async function getAllPages() {
  for (let page = 1; page <= 29; page++) {
    try {
      const data = await makeRequest(page);
      // Save the data to a file
      const fs = require('fs');
      fs.writeFileSync(`page_${page}.html`, data);
      console.log(`Saved page ${page}`);
      
      // Add a small delay between requests
      await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (error) {
      console.error(`Error fetching page ${page}:`, error);
    }
  }
}

// Run the requests
getAllPages();
