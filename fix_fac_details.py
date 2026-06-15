import re

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/tenant_folder/conseil/details_facture.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace header
old_header = """                                            <th style="width: 50%">Désignation des prestations</th>
                                            <th class="text-center">Qté</th>
                                            <th class="text-end">Prix Unit. HT</th>"""
new_header = """                                            <th style="width: 40%">Désignation des prestations</th>
                                            <th class="text-center">Qté</th>
                                            <th class="text-center">Unité</th>
                                            <th class="text-end">Prix Unit. HT</th>"""
content = content.replace(old_header, new_header)

# Replace body
old_body = """                                            <td class="text-center fw-bold text-dark">{{ item.quantite|floatformat:0 }}</td>
                                            <td class="text-end text-muted">{{ item.prix_unitaire|floatformat:2 }}</td>"""
new_body = """                                            <td class="text-center fw-bold text-dark">{{ item.quantite|floatformat:0 }}</td>
                                            <td class="text-center text-muted text-capitalize"><span class="badge bg-light text-secondary border px-2 py-1 fs-12 shadow-sm">{{ item.unite|default:"participant" }}</span></td>
                                            <td class="text-end text-muted">{{ item.prix_unitaire|floatformat:2 }}</td>"""
content = content.replace(old_body, new_body)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done details_facture")
