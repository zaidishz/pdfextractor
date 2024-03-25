import tkinter as tk
from tkinter import filedialog, messagebox
import fitz  # Import PyMuPDF
import pandas as pd
import os
import glob

def extract_form_fields(pdf_file_path, field_name_mapping):
    doc = fitz.open(pdf_file_path)
    data_dict = {}
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        widgets = page.widgets()
        for widget in widgets:
            field_name = widget.field_name
            field_value = widget.field_value
            if field_name and field_value and field_name in field_name_mapping:
                mapped_name = field_name_mapping.get(field_name, field_name)
                data_dict[mapped_name] = field_value
    doc.close()
    return data_dict

def process_pdf_folder(pdf_folder_path, field_name_mapping):
    pdf_file_paths = glob.glob(os.path.join(pdf_folder_path, '*.pdf'))
    aggregated_data = []
    for pdf_path in pdf_file_paths:
        extracted_data = extract_form_fields(pdf_path, field_name_mapping)
        if extracted_data:
            aggregated_data.append(extracted_data)
    if aggregated_data:
        df = pd.DataFrame(aggregated_data)
        output_excel_path = os.path.join(pdf_folder_path, 'aggregated_output.xlsx')
        df.to_excel(output_excel_path, index=False)
        messagebox.showinfo("Success", f"Data extracted from the PDFs has been saved to {output_excel_path}")
    else:
        messagebox.showinfo("No Data", "No valid data found to include in the DataFrame.")

def main():
    root = tk.Tk()
    root.withdraw()
    pdf_folder_path = filedialog.askdirectory(title="Select Folder with PDF files")
    if not pdf_folder_path:
        messagebox.showwarning("No Folder Selected", "You must select a folder. Exiting application.")
        return

    field_name_mapping = {
    '1.1': 'Nachname',
    '1.2': 'Vorname',
    '1.3': 'Geburtsdatum',
    '1.4': 'Geschlecht',
    '1.5': 'Straße',
    '1.5NR': 'Hausnummer',
    '1.6PLZ': 'PLZ',
    '1.6': 'Ort',
    '1.7': 'Telefon',
    '1.8': 'E-Mail',
    '1.9.1': 'Staatsangehörigkeit(1)',
    '1.9.2': 'Staatsangehörigkeit(2)',
    '1.10Einschreibung': 'Einschreibung',
    '1.11': 'Besteht eine Behinderung',
    '2.1': 'Welche art der Behinderung',
    '2.2': 'Wann erwarben Sie die Behinderung',
    '2.3.HZB': 'Wo erwarben Sie die Behinderung',
    '2.3BL': 'Wo erwarben Sie die Behinderung?',
    '2.4': 'Bitte geben Sie an, ob Sie eine der folgenden Leistungen beziehen:',
    '3.1': 'Wo erfolgte die Hochschulzugangsberechtigung?',
    '3.2': 'Bitte geben Sie das Kfz-Kennzeichen',
    '3.3': 'Bezeichnung der Hochschuleinrichtung',
    '3.4M': 'Monat',
    '3.4J': 'Jahr',
    '4.1': 'Zur Promotion berechtigende',
    '4.2': 'Art des Abschlusses',
    '4.3': 'In welchem Studiengang wurden Sie geprüft',
    '4.4': 'Mit welcher Gesamtnote wurde die Prüfung beurteilt?',
    '4.5': 'Wann wurde das Prüfungsergebnis offiziell festgestellt?',
    '4.6': 'Wo erwarben Sie den Hochschulabschluss?',
    '4.7': 'Bitte geben Sie das Kfz-Kennzeichen des Erwerbsortes an?',
    '4.8': 'Bezeichnung der Hochschuleinrichtung',
    '5.1': 'Fachgebiet',
    'ArtProm': 'Art der Promotion',
    '5.3': 'Art der Dissertation',
    '5.4': 'Teilnahme an einem strukturierten Promotionsprogramm',
    '5.5.Block': 'Thema der Dissertation',
    '5.6': 'Betreuer/in der Dissertation',
    '6Ort': 'Ort',
    '6Datum': 'Datum'
    }

    process_pdf_folder(pdf_folder_path, field_name_mapping)

if __name__ == "__main__":
    main()
