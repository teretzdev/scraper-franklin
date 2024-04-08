import os
import re
import csv
import openpyxl
import PyPDF2

def parsePDF(pdfPath):
    with open(pdfPath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = []
        for page in reader.pages:
            text.append(page.extract_text())
    return '\n'.join(text)

def isValidRecord(record):
    # Check if a record is valid based on certain keywords or patterns
    invalid_patterns = [
        r'Franklin County Sheriff\'s Office',
        r'Booking Records between',
        r'ARRESTED ON',
        r'BOOK AND RELEASE',
        r'HOLD FOR',
        r'SERVING SENTENCE',
        r'WARRANT',
        r'24 HOUR HOLD',
        r'MISC\. ORDINANCE VIOLATION',
        r'© \d{4} - \d{4} Omnigo Software St\. Louis MO omnigo\.com'
    ]
    return not any(re.search(pattern, record) for pattern in invalid_patterns)

def prepareRecordForCsv(record):
    # Extracting the name
    nameMatch = re.search(r'([A-Z]+), ([A-Z]+(?: [A-Z]+)?)', record)
    lastName = nameMatch.group(1) if nameMatch else ''
    firstName = nameMatch.group(2) if nameMatch else ''

    # Extracting the address
    addressMatch = re.search(r'(\d+ [A-Z\s]+), ([A-Z\s]+), ([A-Z]{2}) (\d{5})', record)
    address = addressMatch.group(1) if addressMatch else ''
    city = addressMatch.group(2) if addressMatch else ''
    state = addressMatch.group(3) if addressMatch else ''
    zipCode = addressMatch.group(4) if addressMatch else ''

    # Extracting charges and warrant numbers
    charges = re.findall(r'([A-Z\s]+) - (\d{2}-[A-Z]{2,5}-\d{3,5})', record)
    charges = charges if charges else [('N/A', 'N/A')]

    return {
        'LastName': lastName,
        'FirstName': firstName,
        'Address': address,
        'City': city,
        'State': state,
        'ZipCode': zipCode,
        'Charges': charges
    }

if __name__ == "__main__":
    pdfText = parsePDF('Franklin.pdf')
    records = pdfText.split('\n\n')  # Splitting records based on double newlines

    wb = openpyxl.Workbook()
    ws = wb.active
    headers = ['LastName', 'FirstName', 'Address', 'City', 'State', 'ZipCode'] + [f'Charge{i}Desc' for i in range(1, 4)] + [f'Charge{i}WarrantNumber' for i in range(1, 4)]
    ws.append(headers)

    processed_count = 0
    for record in records:
        if not isValidRecord(record):
            continue

        recordData = prepareRecordForCsv(record)
        row = [
            recordData['LastName'], recordData['FirstName'], recordData['Address'], recordData['City'],
            recordData['State'], recordData['ZipCode']
        ]

        for charge in recordData['Charges'][:3]:
            row.extend(charge)
        ws.append(row)
        processed_count += 1

    print(f"Total records processed: {processed_count}")
    wb.save('inmate_records.xlsx')
