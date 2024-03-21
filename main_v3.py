import os
import re
import csv
import openpyxl
import PyPDF2
def parsePDF(pdfPath):
    with open(pdfPath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = []
        for page in range(reader.numPages):
            text.append(reader.getPage(page).extractText())
        return '\n'.join(text)

def prepareRecordForCsv(record):
    fullNameMatch = re.match(r'([A-Z]+),\s*([A-Z]+(?:\s[A-Z]+)?)\s*(\d+\s[A-Z].+?),\s*([A-Z ]+),\s*([A-Z]{2})\s*(\d{5})\s*(ARRESTED ON\s+WARRANT|24 HOUR HOLD|SERVING SENTENCE|HOLD FOR USMS|FEDERAL DETAINER|PROBATION VIOLATION|BOOK AND RELEASE)', record)
    lastName = ''
    firstName = ''
    middleName = ''
    if fullNameMatch:
        constName = fullNameMatch[0].split(', ')[0]
        lastName = constName.split(',')[0]
        constFirstMiddleName = constName.split(' ')[1].split(' ')
        firstName = constFirstMiddleName[0]
        if len(constFirstMiddleName) > 1:
            middleName = constFirstMiddleName[1]

    addressMatch = re.match(r'(\d+ [A-Z\s]+),\s*([A-Z\s]+),\s*([A-Z]{2})\s*(\d+)', record)
    address = ''
    city = ''
    state = ''
    zipCode = ''
    if addressMatch:
        address = addressMatch[0].split(',')[0].strip()
        if addressMatch[0].split(',').length > 1:
            constCityStateZip = addressMatch[0].split(',')[1].strip().split(' ')
            city = constCityStateZip[0]
            state = constCityStateZip[1]
            zipCode = constCityStateZip[2]

    arrestStatusMatch = re.match(r'(ARRESTED ON\s+WARRANT|HOLD FOR USMS|24 HOUR HOLD|SERVING SENTENCE|HOLD FOR USMS|FEDERAL DETAINER|PROBATION VIOLATION|BOOK AND RELEASE)', record)
    arrestStatus = arrestStatusMatch[0].replace('\n', ' ')

    chargesMatches = re.findall(r'([^\d]+)\s+(\d{2}[A-Z]{2}-CR\d{5,6})/g', record)
    charges = []
    for i in range(len(chargesMatches)):
        charges.append({
            'desc': chargesMatches[i][0] or 'N/A',
            'warrantNumber': chargesMatches[i][1] or 'N/A'
        })

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
    constRecords = recordPattern.split(pdfText)
    records = []
    for i in range(len(constRecords)):
        records = records + constRecords[i].split('\n')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Inmate Records"
    headers = ['LastName', 'FirstName', 'MiddleName', 'Address', 'City', 'State', 'ZipCode', 'ArrestStatus', 'Charge1Desc', 'Charge1WarrantNumber', 'Charge2Desc', 'Charge2WarrantNumber', 'Charge3Desc', 'Charge3WarrantNumber']
    ws.append(headers)
    for r in records:
        constRecord = prepareRecordForCsv(r)
        if constRecord['LastName'] != '':
            ws.append([
                constRecord['LastName'],
                constRecord['FirstName'],
                constRecord['MiddleName'],
                constRecord['Address'],
                constRecord['City'],
                constRecord['State'],
                constRecord['ZipCode'],
                constRecord['ArrestStatus'],
                constRecord['Charge1Desc'],
                constRecord['Charge1WarrantNumber'],
                constRecord['Charge2Desc'],
                constRecord['Charge2WarrantNumber'],
                constRecord['Charge3Desc'],
                constRecord['Charge3WarrantNumber'],
            ])

    print(len(records))
    wb.save('inmate_records.xlsx')


processAndWriteToXlsx()
