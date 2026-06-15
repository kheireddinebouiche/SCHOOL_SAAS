import re

with open('temp_template.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix encoding
c = c.replace('TÚl', 'Tél')
c = c.replace('RÚf', 'Réf')
c = c.replace("d'ÚchÚance", "d'échéance")
c = c.replace('FacturÚ Ó', 'Facturé à')
c = c.replace('DÚsignation', 'Désignation')
c = c.replace('QtÚ', 'Qté')
c = c.replace('CoordonnÚes', 'Coordonnées')
c = c.replace('gÚnÚrÚ', 'généré')

# Remove Au profit de in client box
target_to_remove = '{% if client_initial %}<p style="margin: 0; font-style: italic;">Au profit de : {{ client_initial }}</p>{% endif %}\n'
c = c.replace(target_to_remove, '')

# Fix None address
c = c.replace('{{ client_adresse }}<br>', '{% if client_adresse and client_adresse != "None" %}{{ client_adresse }}<br>{% endif %}')
c = c.replace('{{ entreprise_adresse }}<br>', '{% if entreprise_adresse and entreprise_adresse != "None" %}{{ entreprise_adresse }}<br>{% endif %}')

with open('temp_template.html', 'w', encoding='utf-8') as f:
    f.write(c)
