import pandas as pd
import re
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

def parse_pdf_content(pdf_text):
    records = []
    current_record = {}
    charge_count = 0

    # Define regex patterns
    person_pattern = re.compile(
        r'(?P<LastName>[A-Z]+),\s*(?P<FirstName>[A-Z]+(?:\s[A-Z]+)?)\s*'
        r'(?P<Address>\d+\s[A-Z].+?),\s*(?P<City>[A-Z ]+),\s*(?P<State>[A-Z]{2})\s*(?P<ZipCode>\d{5})\s*'
        r'(?P<ArrestStatus>ARRESTED ON WARRANT|24 HOUR HOLD|SERVING SENTENCE|HOLD FOR USMS|FEDERAL DETAINER|PROBATION VIOLATION|BOOK AND RELEASE)'
    )
    charge_pattern = re.compile(r'(?P<Desc>[^\d]+)\s+(?P<WarrantNumber>\d{2}[A-Z]{2}-CR\d{5,6})$')

    lines = pdf_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue

        person_match = person_pattern.match(line)
        if person_match:
            if current_record:
                records.append(current_record)
            current_record = person_match.groupdict()
            current_record['Charges'] = []

        charge_match = charge_pattern.search(line)
        if charge_match and current_record:
            charge_info = charge_match.groupdict()
            current_record['Charges'].append(charge_info)

    if current_record:
        records.append(current_record)

    return records

# Path to the PDF file
pdf_path = '/mnt/data/Franklin.pdf'  # Adjusted file path

# Extract text from the PDF
pdf_text = extract_text_from_pdf(pdf_path)

# Parse the extracted text
parsed_records = parse_pdf_content(pdf_text)

# Convert parsed records to DataFrame
df_records = pd.DataFrame(parsed_records)

# Explode 'Charges' list into rows to normalize the data
df_normalized = df_records.explode('Charges').reset_index(drop=True)

# Split 'Charges' dict into separate columns
charges_df = pd.json_normalize(df_normalized['Charges'])

# Merge charges back into the main DataFrame
final_df = pd.concat([df_normalized.drop('Charges', axis=1), charges_df], axis=1)

# Write the DataFrame to an Excel file
final_df.to_excel('/mnt/data/ParsedFranklinData.xlsx', index=False)

'/mnt/data/ParsedFranklinData.xlsx'  # Provide the link to the generated Excel file for download
