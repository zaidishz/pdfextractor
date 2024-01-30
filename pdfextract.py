import sys
import argparse
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

def extract_text_from_pdf(pdf_path):
    fp = open(pdf_path, 'rb')
    parser = PDFParser(fp)
    doc = PDFDocument(parser)

    # Extract information from AcroForm fields
    acroform_info = resolve1(doc.catalog.get('AcroForm'))

    if acroform_info:
        fields = acroform_info.get('Fields', [])
        for field_ref in fields:
            field = resolve1(field_ref)
            field_type = field.get('FT')

            # check the field type
            if field_type and field_type.name == 'Tx':
                field_name = field.get('T')
                field_value = field.get('V')

                # output field name and value
                print(f'Field Name: {field_name}, Value: {field_value}')

    fp.close()

def main():
    parser = argparse.ArgumentParser(description='Extract text from PDF AcroForm fields.')
    parser.add_argument('pdf_path', type=str, help='Path to the PDF file')
    args = parser.parse_args()

    extract_text_from_pdf(args.pdf_path)

if __name__ == '__main__':
    main()
