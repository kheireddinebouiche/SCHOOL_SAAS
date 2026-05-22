import sys

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Operations Bancaires Tab
ob_old = '''                                            <th>Compte Bancaire</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in operations_bancaire %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-operation-bancaire" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.compte_bancaire|default:"-" }}</td>
                                        </tr>'''
ob_new = '''                                            <th>Compte Bancaire</th>
                                            <th class="pe-4 text-end">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in operations_bancaire %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-operation-bancaire" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.compte_bancaire|default:"-" }}</td>
                                            <td class="pe-4 text-end">
                                                <button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'operation_bancaire')" title="Supprimer">
                                                    <i class="ri-delete-bin-line"></i>
                                                </button>
                                            </td>
                                        </tr>'''
if ob_old in content:
    content = content.replace(ob_old, ob_new)

# 2. Update Demandes Remboursement
dmp_old = '''                                            <th>Date</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in demande_paiements %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-demande-paiement" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.client|default:"-" }}</td>
                                            <td>{{ item.date_demande|default:"-" }}</td>
                                        </tr>'''
dmp_new = '''                                            <th>Date</th>
                                            <th class="pe-4 text-end">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in demande_paiements %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-demande-paiement" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.client|default:"-" }}</td>
                                            <td>{{ item.date_demande|default:"-" }}</td>
                                            <td class="pe-4 text-end">
                                                <button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'demande_paiement')" title="Supprimer">
                                                    <i class="ri-delete-bin-line"></i>
                                                </button>
                                            </td>
                                        </tr>'''
if dmp_old in content:
    content = content.replace(dmp_old, dmp_new)

# 3. Update Remboursements
rem_old = '''                                            <th>Montant</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in remboursements %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-remboursement" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.motif|default:"-" }}</td>
                                            <td>{{ item.montant|default:"-" }}</td>
                                        </tr>'''
rem_new = '''                                            <th>Montant</th>
                                            <th class="pe-4 text-end">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in remboursements %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-remboursement" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.motif|default:"-" }}</td>
                                            <td>{{ item.montant|default:"-" }}</td>
                                            <td class="pe-4 text-end">
                                                <button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'remboursement')" title="Supprimer">
                                                    <i class="ri-delete-bin-line"></i>
                                                </button>
                                            </td>
                                        </tr>'''
if rem_old in content:
    content = content.replace(rem_old, rem_new)

# 4. Update Autres Produits
ap_old = '''                                            <th>Numéro</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in autres_produits %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-autre-produit" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.label|default:"-" }}</td>
                                            <td>{{ item.num|default:"-" }}</td>
                                        </tr>'''
ap_new = '''                                            <th>Numéro</th>
                                            <th class="pe-4 text-end">Actions</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in autres_produits %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-autre-produit" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.label|default:"-" }}</td>
                                            <td>{{ item.num|default:"-" }}</td>
                                            <td class="pe-4 text-end">
                                                <button class="btn btn-soft-danger btn-sm rounded-circle p-0 avatar-xs" onclick="confirmDeleteDataExplorer('{{ item.id }}', 'autre_produit')" title="Supprimer">
                                                    <i class="ri-delete-bin-line"></i>
                                                </button>
                                            </td>
                                        </tr>'''
if ap_old in content:
    content = content.replace(ap_old, ap_new)

# Add confirmDeleteDataExplorer function
js_func = '''
    function confirmDeleteDataExplorer(id, modelName) {
        Swal.fire({
            title: 'Êtes-vous sûr ?',
            text: "Vous allez supprimer cet élément. Cette action est irréversible !",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#ef4444',
            cancelButtonColor: '#64748b',
            confirmButtonText: 'Oui, supprimer',
            cancelButtonText: 'Annuler',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                $.ajax({
                    url: "{% url 'saas_admin_app:saas_bulk_delete_action' institut.id %}",
                    type: "POST",
                    data: {
                        'model': modelName,
                        'ids': JSON.stringify([id]),
                        'csrfmiddlewaretoken': '{{ csrf_token }}'
                    },
                    success: function(response) {
                        if (response.status === 'success') {
                            Swal.fire('Supprimé !', response.message, 'success').then(() => location.reload());
                        } else {
                            Swal.fire('Erreur', response.message, 'error');
                        }
                    },
                    error: function(xhr) {
                        Swal.fire('Erreur', 'Une erreur est survenue lors de la suppression.', 'error');
                    }
                });
            }
        });
    }
'''

target_str = "// === Global Search & Filters ==="
if target_str in content and "confirmDeleteDataExplorer" not in content:
    content = content.replace(target_str, js_func + "\\n    " + target_str)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated single delete mechanism successfully')
