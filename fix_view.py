import re

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/t_conseil/views.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# For ApiSaveDevisItems parsing:
old_extract = '''                quantite = item.get('quantity')
                price = item.get('unitPrice')'''
new_extract = '''                quantite = item.get('quantity')
                unite = item.get('unit', 'participant')
                price = item.get('unitPrice')'''
content = content.replace(old_extract, new_extract)

# For ApiSaveDevisItems creating:
old_create = '''                    long_description=long_description,
                    quantite=qty,
                    prix_unitaire=unit_price,'''
new_create = '''                    long_description=long_description,
                    quantite=qty,
                    unite=unite,
                    prix_unitaire=unit_price,'''
content = content.replace(old_create, new_create)

# Same for Facture just in case
# We might not need to if it's not implemented the same way, but it's safe to check.
# Let's save.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done view')
