const fs = require('fs');

const parsePDF = async (jsonPath) => {
    const data = fs.readFileSync(jsonPath);  // Read the JSON file
    const pagesText = JSON.parse(data);  // Parse the JSON content
    return pagesText.join('\n');  // Combine text from all pages, separated by newlines
};

module.exports = parsePDF;
