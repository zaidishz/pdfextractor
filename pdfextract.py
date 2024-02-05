import pandas as pd
import chardet
import sys
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

def extract_data(pdf_path):
    field_mapping = {
        b'1.1': 'Nachname',
        b'1.2': 'Vorname',
        b'1.3': 'Geburtsdatum',
        b'1.4': 'Geschlecht',
        b'1.5': 'Straße',
        b'1.5NR': 'Hausnummer',
        b'1.6PLZ': 'PLZ',
        b'1.6': 'Ort',
        b'1.7': 'Telefon',
        b'1.8': 'E-Mail',
        b'1.9.1': 'Staatsangehörigkeit',
        b'1.10Einschreibung': 'Einschreibung',
        b'1.11': 'Besteht eine Behinderung',
        b'2.1': 'Welche art der Behinderung',
        b'2.2': 'Wann erwarben Sie die Behinderung',
        b'2.3.HZB': 'Wo erwarben Sie die Behinderung',
        b'2.3BL': 'Wo erwarben Sie die Behinderung?',
        b'2.4': 'Bitte geben Sie an, ob Sie eine der folgenden Leistungen beziehen:',
        b'3.1': 'Wo erfolgte die Hochschulzugangsberechtigung?',
        b'3.2': 'Bitte geben Sie das Kfz-Kennzeichen',
        b'3.3': 'Bezeichnung der Hochschuleinrichtung',
        b'3.4M': 'Monat',
        b'3.5J': 'Jahr',
        b'4.1': 'Zur Promotion berechtigende',
        b'4.2': 'Art des Abschlusses',
        b'4.3': 'In welchem Studiengang wurden Sie geprüft',
        b'4.4': 'Mit welcher Gesamtnote wurde die Prüfung beurteilt?',
        b'5.1': 'Fachgebiet',
        b'5.2': 'Art der Promotion',
        b'5.3': 'Art der Dissertation',
        b'5.4': 'Teilnahme an einem strukturierten Promotionsprogramm',
        b'5.6': 'Betreuer/in der Dissertation',
        b'6Ort': 'Ort',
        b'6Datum': 'Datum'
    }
    
    data_dict = {} 
    parser = PDFParser(open(pdf_path, 'rb')) # Open the PDF file in read-binary mode
    doc = PDFDocument(parser) # Create a PDFDocument object that stores the document structure
    fields = resolve1(doc.catalog['AcroForm'])['Fields'] # Get the form fields from the PDF
    for i in fields:
        field = resolve1(i)
        name, value = field.get('T'), field.get('V')
        if name in field_mapping:
            mapped_name = field_mapping[name] 

            
            if isinstance(value, bytes):   # If the value is a byte sequence
                result = chardet.detect(value) # Use chardet to automatically detect the encoding
                encoding = result["encoding"]
                value = value.decode(encoding, errors="replace").strip("'/") # Decode the byte sequence using the detected encoding
                
            elif isinstance(value, str):
                value = value.strip("b'/") # Remove leading and trailing characters

            data_dict[mapped_name] = value 

    df = pd.DataFrame([data_dict]) 
    df = df[[col for col in field_mapping.values() if col in df.columns]] # Reorder columns based on field_mapping, only including existing keys

    output_excel_path = pdf_path.replace('.pdf', '_output.xlsx')
    df.to_excel(output_excel_path, index=False)
    print(f"Data extracted from the PDF has been saved to {output_excel_path}")
    #print(df)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_data_extractor.py <path_to_pdf_file>")
        sys.exit(1)
    pdf_file_path = sys.argv[1]
    extract_data(pdf_file_path)
