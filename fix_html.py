import re

file_path = 'c:/Users/kheir/Documents/saldae/SCHOOL_SAAS/templates/tenant_folder/conseil/configure-devis.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update table headers
content = content.replace('<th style="width: 35%;">Service / Designation</th>', '<th style="width: 25%;">Service / Designation</th>')
content = content.replace('<th style="width: 10%;" class="text-center">Quantité</th>', '<th style="width: 10%;" class="text-center">Quantité</th>\n                                        <th style="width: 10%;" class="text-center">Unité</th>')

# 2. Add input to tfoot (newItemRow)
qty_input = '''                                        <td>
                                            <input type="number" class="form-control form-control-premium text-center" id="newQty" value="1" min="1">
                                        </td>'''
unit_input = '''\n                                        <td>
                                            <select class="form-select form-select-premium text-center" id="newUnit">
                                                <option value="jour">Jour</option>
                                                <option value="groupe">Groupe</option>
                                                <option value="participant" selected>Participant</option>
                                                <option value="heure">Heure</option>
                                            </select>
                                        </td>'''
content = content.replace(qty_input, qty_input + unit_input)

# 3. Add to items.push in initial state
content = content.replace('quantity: parseMoney("{{ l.quantite|floatformat:2 }}"),', 'quantity: parseMoney("{{ l.quantite|floatformat:2 }}"),\n            unit: "{{ l.unite|default:\'participant\' }}",')

# 4. Add to addItemBtn listener variables
content = content.replace('const q = parseFloat(newQty.value);', 'const q = parseFloat(newQty.value);\n                const u = document.getElementById(\'newUnit\').value;')

# 5. Add to itemData inside addItemBtn listener
content = content.replace('quantity: q,', 'quantity: q,\n                    unit: u,')

# 6. Add reset logic to addItemBtn listener and removeItem
content = content.replace('newQty.value="1";', 'newQty.value="1"; document.getElementById(\'newUnit\').value="participant";')

# 7. Add to window.editItem
content = content.replace('newQty.value = it.quantity;', 'newQty.value = it.quantity;\n            document.getElementById(\'newUnit\').value = it.unit || "participant";')

# 8. Add to renderItems
qty_td = '''                    <td class="text-center">
                        <span class="badge bg-light text-dark border px-2 py-1 fs-12 fw-bold shadow-sm"></span>
                    </td>'''
unit_td = '''\n                    <td class="text-center">
                        <span class="badge bg-light text-secondary border px-2 py-1 fs-12 shadow-sm text-capitalize"></span>
                    </td>'''
content = content.replace(qty_td, qty_td + unit_td)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Done HTML')
