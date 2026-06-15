import os

ETUDIANTS_FILE = r'C:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_etudiants\urls.py'
GROUPE_FILE = r'C:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_groupe\urls.py'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content.replace('("sco",', '("scol",')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated {file_path}")

process_file(ETUDIANTS_FILE)
process_file(GROUPE_FILE)
