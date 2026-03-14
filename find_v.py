
import os

filepath = r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\tenant_folder\comptabilite\paiements\liste_des_paiements.html"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "v>" in line:
        # Check if it's part of a tag like <div>
        if not ("<div" in line or "</div" in line or "div>" in line or "button>" in line or "span>" in line or "table>" in line or "tr>" in line or "td>" in line or "ul>" in line or "li>" in line or "a>" in line):
             print(f"Found suspicious 'v>' on line {i+1}: {line.strip()}")
        elif line.strip() == "v>":
             print(f"Found literal 'v>' on line {i+1}: {line.strip()}")
