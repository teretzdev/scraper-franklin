const fs = require('fs');
const patterns = require('./headersMatcher');
const writeToCsv = require('./csvWriter');

function prepareRecordForCsv(record) {
    const fullNameMatch = record.match(patterns.fullNamePattern);
    let lastName = '', firstName = '', middleName = '';
    if (fullNameMatch) {
        const nameParts = fullNameMatch[0].split(', ');
        lastName = nameParts[0];
        const firstMiddleName = nameParts[1].split(' ');
        firstName = firstMiddleName[0];
        middleName = firstMiddleName.slice(1).join(' ');
    }

    const addressMatch = record.match(patterns.addressPattern);
    let address = 'N/A', city = 'N/A', state = 'N/A', zipCode = 'N/A';
    if (addressMatch) {
        const addressParts = addressMatch[0].split(',');
        address = addressParts[0].trim();
        if (addressParts.length > 1) {
            const cityStateZip = addressParts[1].trim().split(' ');
            city = cityStateZip[0];
            state = cityStateZip[1];
            zipCode = cityStateZip[2];
        }
    }

    const arrestStatusMatch = record.match(patterns.arrestStatusPattern);
    const arrestStatus = arrestStatusMatch ? arrestStatusMatch[0].replace(/\n/g, ' ') : 'N/A';

    const chargesMatches = Array.from(record.matchAll(patterns.chargePattern));
    let charges = [];
    for (let i = 0; i < chargesMatches.length; i++) {
        charges.push({
            desc: chargesMatches[i][1] || 'N/A',
            warrantNumber: chargesMatches[i][2] || 'N/A'
        });
    }

    // Ensuring the charges array has at least 3 elements filled with 'N/A' if less than 3 charges exist
    while (charges.length < 3) {
        charges.push({ desc: 'N/A', warrantNumber: 'N/A' });
    }

    return {
        LastName: lastName,
        FirstName: firstName,
        MiddleName: middleName,
        Address: address,
        City: city,
        State: state,
        ZipCode: zipCode,
        ArrestStatus: arrestStatus,
        Charge1Desc: charges[0]?.desc ?? 'N/A',
        Charge1WarrantNumber: charges[0]?.warrantNumber ?? 'N/A',
        Charge2Desc: charges[1]?.desc ?? 'N/A',
        Charge2WarrantNumber: charges[1]?.warrantNumber ?? 'N/A',
        Charge3Desc: charges[2]?.desc ?? 'N/A',
        Charge3WarrantNumber: charges[2]?.warrantNumber ?? 'N/A',
    };
}

async function processAndWriteToCsv() {
    try {
        const data = await fs.promises.readFile('./extracted_text.json', 'utf8');
        const textBlocks = JSON.parse(data);

        let allRecords = [];
        textBlocks.forEach(block => {
            const records = block.split(/\n(?=[A-Z]+, [A-Z]+(?: [A-Z]+)?)/);
            records.forEach(record => {
                const preparedRecord = prepareRecordForCsv(record);
                if (preparedRecord.LastName !== '') { // Ensuring only valid records are added
                    allRecords.push(preparedRecord);
                }
            });
        });

        const headers = ['LastName', 'FirstName', 'MiddleName', 'Address', 'City', 'State', 'ZipCode', 'ArrestStatus', 'Charge1Desc', 'Charge1WarrantNumber', 'Charge2Desc', 'Charge2WarrantNumber', 'Charge3Desc', 'Charge3WarrantNumber'];
        
        await writeToCsv('./output.csv', headers, allRecords.flat());
        console.log(`CSV file has been written successfully. Total records processed: ${allRecords.length}`);
    } catch (error) {
        console.error('An error occurred:', error);
    }
}

processAndWriteToCsv();
