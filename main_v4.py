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

def prepareRecordForCsv(record):
    non_record_patterns = [
        r'MISC\. ORDINANCE VIOLATION',
        r'© \d{4} - \d{4} Omnigo Software St\. Louis MO omnigo\.com'
    ]
    for pattern in non_record_patterns:
        if re.search(pattern, record):
            return None  # Return None to indicate this is not a record

    fullNameMatch = re.match(r'([A-Z]+),\s*([A-Z]+(?:\s[A-Z]+)?)', record)
    if fullNameMatch:
        nameParts = fullNameMatch.groups()
        lastName = nameParts[0].strip()
        firstMiddleNameParts = nameParts[1].split()
        firstName = firstMiddleNameParts[0] if firstMiddleNameParts else ''
        middleName = ' '.join(firstMiddleNameParts[1:]) if len(firstMiddleNameParts) > 1 else ''
    else:
        lastName = ''
        firstName = ''
        middleName = ''

    addressMatch = re.match(r'(\d+ [A-Z\s]+),\s*([A-Z\s]+),\s*([A-Z]{2})\s*(\d+)', record)
    if addressMatch:
        addressParts = addressMatch.group().split(',')
        address = addressParts[0].strip()
        cityStateZip = addressParts[1].strip().split()
        city = cityStateZip[0]
        state = cityStateZip[1]
        zipCode = cityStateZip[2] if len(cityStateZip) == 3 else ''
    else:
        address = ''
        city = ''
        state = ''
        zipCode = ''

    arrestStatusMatch = re.match(r'(ARRESTED ON\s+WARRANT|HOLD FOR USMS|24 HOUR HOLD|SERVING SENTENCE|HOLD FOR USMS|FEDERAL DETAINER|PROBATION VIOLATION|BOOK AND RELEASE)', record)
    arrestStatus = arrestStatusMatch[0].replace('\n', ' ') if arrestStatusMatch else ''

    chargesMatches = re.findall(r'([^\d]+)\s+(\d{2}[A-Z]{2}-CR\d{5,6})', record)
    charges = [{'desc': match[0] or 'N/A', 'warrantNumber': match[1] or 'N/A'} for match in chargesMatches]
    while len(charges) < 3:
        charges.append({'desc': 'N/A', 'warrantNumber': 'N/A'})

    return {
        'LastName': lastName,
        'FirstName': firstName,
        'MiddleName': middleName,
        'Address': address,
        'City': city,
        'State': state,
        'ZipCode': zipCode,
        'ArrestStatus': arrestStatus,
        'Charge1Desc': charges[0]['desc'],
        'Charge1WarrantNumber': charges[0]['warrantNumber'],
        'Charge2Desc': charges[1]['desc'],
        'Charge2WarrantNumber': charges[1]['warrantNumber'],
        'Charge3Desc': charges[2]['desc'],
        'Charge3WarrantNumber': charges[2]['warrantNumber'],
    }

if __name__ == "__main__":
    try:
        pdfText = parsePDF('Franklin.pdf')
        records = pdfText.split('\n')
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append([
            'LastName', 'FirstName', 'MiddleName', 'Address', 'City', 'State', 'ZipCode', 'ArrestStatus',
            'Charge1Desc', 'Charge1WarrantNumber', 'Charge2Desc', 'Charge2WarrantNumber', 'Charge3Desc', 'Charge3WarrantNumber'
        ])
        name_count = 0
        processed_count = 0
        for record in records:
            recordData = prepareRecordForCsv(record)
            if recordData is None:
                continue  # Skip non-records
            elif recordData['LastName']:
                ws.append([
                    recordData['LastName'],
                    recordData['FirstName'],
                    recordData['MiddleName'],
                    recordData['Address'],
                    recordData['City'],
                    recordData['State'],
                    recordData['ZipCode'],
                    recordData['ArrestStatus'],
                    recordData['Charge1Desc'],
                    recordData['Charge1WarrantNumber'],
                    recordData['Charge2Desc'],
                    recordData['Charge2WarrantNumber'],
                    recordData['Charge3Desc'],
                    recordData['Charge3WarrantNumber'],
                ])
                processed_count += 1
                name_count += 1
            else:
                print(f"Skipped record due to empty last name or format mismatch: {record}")
        print(f"Total records processed: {processed_count}")
        print(f"Total names counted: {name_count}")
        print(f"Total records expected: {len(records)}")
        wb.save('inmate_records.xlsx')
    except Exception as e:
        print(f"An error occurred: {e}")
