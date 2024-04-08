// csvWriter.js
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

async function writeToCsv(filePath, headers, data) {
	console.log('csvWrite / data pazssed to write CSV ', data)
    const csvWriter = createCsvWriter({
        path: filePath,
        header: headers.map(header => ({ id: header, title: header })),
    });

    try {
        await csvWriter.writeRecords(data);
        console.log('CSV file has been written successfully.');
    } catch (error) {
        console.error('Error writing CSV file:', error);
    }
}

module.exports = writeToCsv;
