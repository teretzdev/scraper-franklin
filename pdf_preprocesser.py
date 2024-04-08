import fitz  # PyMuPDF for reading PDFs
import json
import re  # Regular expressions for pattern matching

def extract_text_and_count_records(pdf_path, json_path):
    doc = fitz.open(pdf_path)
    total_records = 0  # Initialize a counter for the records
    pattern = re.compile(r'[A-Z]{2,}, [A-Z]{2,}')  # Regex pattern for full names in uppercase

    pages_text = []
    for page in doc:
        page_text = page.get_text("text")
        pages_text.append(page_text)
        total_records += len(pattern.findall(page_text))  # Count matches of the pattern

    with open(json_path, 'w') as f:
        json.dump(pages_text, f)  # Save the extracted text to a JSON file
    
    doc.close()
    return total_records

if __name__ == "__main__":
    record_count = extract_text_and_count_records('Franklin.pdf', 'extracted_text.json')
    print(f"Total possible records in PDF: {record_count}")
    with open('record_count.txt', 'w') as f:  # Output the count to a file
        f.write(str(record_count))
