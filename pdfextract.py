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

    parser = PDFParser(open(pdf_path, 'rb'))
    doc = PDFDocument(parser)
    fields = resolve1(doc.catalog['AcroForm'])['Fields']
    for i in fields:
        field = resolve1(i)
        name, value = field.get('T'), field.get('V')
        if name and name in field_mapping:
            mapped_name = field_mapping[name]
            if isinstance(value, str):
                value = value.strip("b'/'")
            else:
                value = str(value).strip("b'/") 

            print('{0} = {1}'.format(mapped_name, value))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <pdf_file_path>")
    else:
        pdf_path = sys.argv[1]
        extract_data(pdf_path)
