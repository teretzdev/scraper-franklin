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
    fullNameMatch = re.match(r'([A-Z]+),\s*([A-Z]+(?:\s[A-Z]+)?)\s*(\d+\s[A-Z].+?),\s*([A-Z ]+),\s*([A-Z]{2})\s*(\d{5})\s*(ARRESTED ON\s+WARRANT|24 HOUR HOLD|SERVING SENTENCE|HOLD FOR USMS|FEDERAL DETAINER|PROBATION VIOLATION|BOOK AND RELEASE)', record)
    lastName = ''
    firstName = ''
    middleName = ''
def prepareRecordForCsv(record):
    ...
    if fullNameMatch:
        constNameParts = fullNameMatch.group().split(', ')
        lastName = constNameParts[0].strip()
        constFirstMiddleNameParts = constNameParts[1].split() if len(constNameParts) > 1 else []
        firstName = constFirstMiddleNameParts[0] if constFirstMiddleNameParts else ''
        middleName = ' '.join(constFirstMiddleNameParts[1:]) if len(constFirstMiddleNameParts) > 1 else ''
        firstName = constFirstMiddleNameParts[0] if constFirstMiddleNameParts else ''
        middleName = ' '.join(constFirstMiddleNameParts[1:]) if len(constFirstMiddleNameParts) > 1 else ''
    ...

    addressMatch = re.match(r'(\d+ [A-Z\s]+),\s*([A-Z\s]+),\s*([A-Z]{2})\s*(\d+)', record)
    address = ''
    city = ''
    state = ''
    zipCode = ''
    if addressMatch:
        addressParts = addressMatch.group().split(',')
        address = addressParts[0].strip()
        if len(addressParts) > 1:
            cityStateZip = addressParts[1].strip().split()
            if len(cityStateZip) >= 3:
                city = cityStateZip[0]
                state = cityStateZip[1]
                zipCode = cityStateZip[2]
            elif len(cityStateZip) == 2:
                city = cityStateZip[0]
                state = cityStateZip[1]

    arrestStatusMatch = re.match(r'(ARRESTED ON\s+WARRANT|HOLD FOR USMS|24 HOUR HOLD|SERVING SENTENCE|HOLD FOR USMS|FEDERAL DETAINER|PROBATION VIOLATION|BOOK AND RELEASE)', record)
    arrestStatus = ''
    if arrestStatusMatch:
        arrestStatus = arrestStatusMatch[0].replace('\n', ' ')

    chargesMatches = re.findall(r'([^\d]+)\s+(\d{2}[A-Z]{2}-CR\d{5,6})', record)
    charges = []
    for i in range(len(chargesMatches)):
        charges.append({
            'desc': chargesMatches[i][0] or 'N/A',
            'warrantNumber': chargesMatches[i][1] or 'N/A'
        })

    # Ensuring the charges array has at least 3 elements filled with 'N/A' if less than 3 charges exist
    while len(charges) < 3:
        charges.append({'desc': 'N/A', 'warrantNumber': 'N/A'})

    # Ensuring the charges array has at least 3 elements filled with 'N/A' if less than 3 charges exist
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


def processAndWriteToCsv():
    pdfPath = 'Franklin.pdf'  # Updated to the correct PDF file name
    pdfText = parsePDF(pdfPath)  # Now using PyPDF2 for PDF text extraction
def processAndWriteToXlsx():
    pdfPath = 'Franklin.pdf'
    pdfText = parsePDF(pdfPath)
    print(pdfText)
    recordPattern = re.compile(r'\n(?=[A-Z]+, [A-Z]+(?: [A-Z]+)?)')
    records = recordPattern.split(pdfText)
    records = []
    for record in constRecords:
        if record.strip() == '':
            continue
        constRecord = prepareRecordForCsv(record)
        if constRecord['LastName'] != '':
            ws.append([
                record['LastName'],
                constRecord['FirstName'],
                constRecord['MiddleName'],
                constRecord['Address'],
                record['City'],
                constRecord['State'],
                constRecord['ZipCode'],
                constRecord['ArrestStatus'],
                constRecord['Charge1Desc'],
                constRecord['Charge1WarrantNumber'],
                record['Charge2Desc'],
                constRecord['Charge2WarrantNumber'],
                constRecord['Charge3Desc'],
                constRecord['Charge3WarrantNumber'],
            ])

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inmate Records"
    headers = ['LastName', 'FirstName', 'MiddleName', 'Address', 'City', 'State', 'ZipCode', 'ArrestStatus', 'Charge1Desc', 'Charge1WarrantNumber', 'Charge2Desc', 'Charge2WarrantNumber', 'Charge3Desc', 'Charge3WarrantNumber']
    ws.append(headers)  # This line is correct and should remain as is
    for r in records:
        constRecord = prepareRecordForCsv(r)
        if constRecord['LastName'] != '':
            ws.append([
                constRecord['LastName'],
                constRecord['FirstName'],
                constRecord['MiddleName'],
                constRecord['Address'],
                record['City'],
                constRecord['State'],
                constRecord['ZipCode'],
                constRecord['ArrestStatus'],
                constRecord['Charge1Desc'],
                constRecord['Charge1WarrantNumber'],
                record['Charge2Desc'],
                constRecord['Charge2WarrantNumber'],
                constRecord['Charge3Desc'],
                constRecord['Charge3WarrantNumber'],
            ])  # This line is correct and should remain as is

    print(len(records))
    wb.save('inmate_records.xlsx')


processAndWriteToXlsx()
