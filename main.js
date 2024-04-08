const fs = require('fs');
const pdf = require('pdf-parse');
const xl = require('excel4node');

async function extractTextFromPdf(pdfPath) {
  const dataBuffer = fs.readFileSync(pdfPath);
  try {
    const data = await pdf(dataBuffer);
    console.log("PDF text extracted successfully.");
    return data.text;
  } catch (error) {
    console.error("Error extracting text from PDF:", error);
  }
}

function parsePdfContent(pdfText) {
  const records = [];
  let currentRecord = {};

  // Placeholder regex patterns - ADJUST THESE BASED ON YOUR PDF
  const personPattern = /([A-Z]+),\s*([A-Z]+(?:\s[A-Z]+)?)\s*(\d+\s[A-Z].+?),\s*([A-Z ]+),\s*([A-Z]{2})\s*(\d{5})\s*(ARRESTED ON WARRANT|24 HOUR HOLD|SERVING SENTENCE|HOLD FOR USMS|FEDERAL DETAINER|PROBATION VIOLATION|BOOK AND RELEASE)/;
  const chargePattern = /([^\d]+)\s+(\d{2}[A-Z]{2}-CR\d{5,6})$/;

  pdfText.split('\n').forEach(line => {
    let match = line.match(personPattern);
    if (match) {
      if (Object.keys(currentRecord).length) records.push(currentRecord);
      currentRecord = {
        LastName: match[1],
        FirstName: match[2],
        Address: match[3],
        City: match[4],
        State: match[5],
        ZipCode: match[6],
        ArrestStatus: match[7],
        Charges: []
      };
    } else {
      match = line.match(chargePattern);
      if (match && currentRecord.Charges) {
        currentRecord.Charges.push({
          Desc: match[1],
          WarrantNumber: match[2]
        });
      }
    }
  });

  if (Object.keys(currentRecord).length) records.push(currentRecord);
  console.log("PDF content parsed successfully.");
	console.log(records);
  return records;
}

// Function to write the parsed data to an Excel file
function writeToExcel(parsedRecords) {
  const wb = new xl.Workbook();
  const ws = wb.addWorksheet('Sheet 1');

  // Define headers
  const headers = ['LastName', 'FirstName', 'Address', 'City', 'State', 'ZipCode', 'ArrestStatus', 'ChargeDesc', 'WarrantNumber'];
  headers.forEach((header, index) => ws.cell(1, index + 1).string(header));

  // Populate data
  let row = 2;
  parsedRecords.forEach(record => {
    record.Charges.forEach(charge => {
      ws.cell(row, 1).string(record.LastName);
      ws.cell(row, 2).string(record.FirstName);
      ws.cell(row, 3).string(record.Address);
      ws.cell(row, 4).string(record.City);
      ws.cell(row, 5).string(record.State);
      ws.cell(row, 6).string(record.ZipCode);
      ws.cell(row, 7).string(record.ArrestStatus);
      ws.cell(row, 8).string(charge.Desc);
      ws.cell(row, 9).string(charge.WarrantNumber);
      row++;
    });
  });

  // Save the Excel file
  wb.write('ParsedFranklinData.xlsx', function(err, stats) {
    if (err) {
      console.error("Error writing to Excel file:", err);
    } else {
      console.log("Data written to Excel file successfully.");
    }
  });
}

async function processPdf() {
  const pdfPath = './Franklin.pdf'; // Replace with your PDF's path
  const pdfText = await extractTextFromPdf(pdfPath);
console.log(pdfText);
  const parsedRecords = parsePdfContent(pdfText);
  writeToExcel(parsedRecords);
}

processPdf();
