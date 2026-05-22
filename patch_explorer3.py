import sys

file_path = r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\templates\saas_admin_app\saas_tenant_data_explorer.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Tab panes definition
tab_panes = '''
                <!-- Operations Bancaires Tab -->
                <div class="tab-pane fade {% if active_tab == 'operations_bancaire' %}show active{% endif %}" id="operations_bancaire" role="tabpanel">
                    <div class="glass-tab-content">
                        <div class="card-body p-0">
                            <div class="table-responsive">
                                <table class="table table-modern align-middle mb-0">
                                    <thead>
                                        <tr>
                                            <th class="ps-4"><div class="form-check"><input class="form-check-input" type="checkbox" id="selectAllOperationsBancaire"></div></th>
                                            <th>ID</th>
                                            <th>Compte Bancaire</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in operations_bancaire %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-operation-bancaire" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.compte_bancaire|default:"-" }}</td>
                                        </tr>
                                        {% empty %}
                                        <tr><td colspan="3"><div class="empty-state-container"><p>Aucune opération trouvée.</p></div></td></tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                            {% if operations_bancaire.has_other_pages %}
                            <div class="px-4 py-3 border-top border-white border-opacity-10 d-flex justify-content-between align-items-center">
                                <div class="text-muted small">Page {{ operations_bancaire.number }} sur {{ operations_bancaire.paginator.num_pages }}</div>
                                <nav>
                                    <ul class="pagination pagination-sm mb-0">
                                        {% if operations_bancaire.has_previous %}
                                        <li class="page-item"><a class="page-link rounded-pill px-3 me-2 border-0 shadow-sm" href="?ob_page={{ operations_bancaire.previous_page_number }}&tab=operations_bancaire">Précédent</a></li>
                                        {% endif %}
                                        {% if operations_bancaire.has_next %}
                                        <li class="page-item"><a class="page-link rounded-pill px-3 border-0 shadow-sm" href="?ob_page={{ operations_bancaire.next_page_number }}&tab=operations_bancaire">Suivant</a></li>
                                        {% endif %}
                                    </ul>
                                </nav>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>

                <!-- Demande Paiements Tab -->
                <div class="tab-pane fade {% if active_tab == 'demande_paiements' %}show active{% endif %}" id="demande_paiements" role="tabpanel">
                    <div class="glass-tab-content">
                        <div class="card-body p-0">
                            <div class="table-responsive">
                                <table class="table table-modern align-middle mb-0">
                                    <thead>
                                        <tr>
                                            <th class="ps-4"><div class="form-check"><input class="form-check-input" type="checkbox" id="selectAllDemandesPaiement"></div></th>
                                            <th>ID</th>
                                            <th>Client</th>
                                            <th>Date</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in demande_paiements %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-demande-paiement" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.client|default:"-" }}</td>
                                            <td>{{ item.date_demande|default:"-" }}</td>
                                        </tr>
                                        {% empty %}
                                        <tr><td colspan="4"><div class="empty-state-container"><p>Aucune demande trouvée.</p></div></td></tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                            {% if demande_paiements.has_other_pages %}
                            <div class="px-4 py-3 border-top border-white border-opacity-10 d-flex justify-content-between align-items-center">
                                <div class="text-muted small">Page {{ demande_paiements.number }} sur {{ demande_paiements.paginator.num_pages }}</div>
                                <nav>
                                    <ul class="pagination pagination-sm mb-0">
                                        {% if demande_paiements.has_previous %}
                                        <li class="page-item"><a class="page-link rounded-pill px-3 me-2 border-0 shadow-sm" href="?dmp_page={{ demande_paiements.previous_page_number }}&tab=demande_paiements">Précédent</a></li>
                                        {% endif %}
                                        {% if demande_paiements.has_next %}
                                        <li class="page-item"><a class="page-link rounded-pill px-3 border-0 shadow-sm" href="?dmp_page={{ demande_paiements.next_page_number }}&tab=demande_paiements">Suivant</a></li>
                                        {% endif %}
                                    </ul>
                                </nav>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>

                <!-- Remboursements Tab -->
                <div class="tab-pane fade {% if active_tab == 'remboursements' %}show active{% endif %}" id="remboursements" role="tabpanel">
                    <div class="glass-tab-content">
                        <div class="card-body p-0">
                            <div class="table-responsive">
                                <table class="table table-modern align-middle mb-0">
                                    <thead>
                                        <tr>
                                            <th class="ps-4"><div class="form-check"><input class="form-check-input" type="checkbox" id="selectAllRemboursements"></div></th>
                                            <th>ID</th>
                                            <th>Motif</th>
                                            <th>Montant</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in remboursements %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-remboursement" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.motif|default:"-" }}</td>
                                            <td>{{ item.montant|default:"-" }}</td>
                                        </tr>
                                        {% empty %}
                                        <tr><td colspan="4"><div class="empty-state-container"><p>Aucun remboursement trouvé.</p></div></td></tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                            {% if remboursements.has_other_pages %}
                            <div class="px-4 py-3 border-top border-white border-opacity-10 d-flex justify-content-between align-items-center">
                                <div class="text-muted small">Page {{ remboursements.number }} sur {{ remboursements.paginator.num_pages }}</div>
                                <nav>
                                    <ul class="pagination pagination-sm mb-0">
                                        {% if remboursements.has_previous %}
                                        <li class="page-item"><a class="page-link rounded-pill px-3 me-2 border-0 shadow-sm" href="?rem_page={{ remboursements.previous_page_number }}&tab=remboursements">Précédent</a></li>
                                        {% endif %}
                                        {% if remboursements.has_next %}
                                        <li class="page-item"><a class="page-link rounded-pill px-3 border-0 shadow-sm" href="?rem_page={{ remboursements.next_page_number }}&tab=remboursements">Suivant</a></li>
                                        {% endif %}
                                    </ul>
                                </nav>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>

                <!-- Autres Produits Tab -->
                <div class="tab-pane fade {% if active_tab == 'autres_produits' %}show active{% endif %}" id="autres_produits" role="tabpanel">
                    <div class="glass-tab-content">
                        <div class="card-body p-0">
                            <div class="table-responsive">
                                <table class="table table-modern align-middle mb-0">
                                    <thead>
                                        <tr>
                                            <th class="ps-4"><div class="form-check"><input class="form-check-input" type="checkbox" id="selectAllAutresProduits"></div></th>
                                            <th>ID</th>
                                            <th>Label</th>
                                            <th>Numéro</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {% for item in autres_produits %}
                                        <tr>
                                            <td class="ps-4"><div class="form-check"><input class="form-check-input select-autre-produit" type="checkbox" value="{{ item.id }}"></div></td>
                                            <td>{{ item.id }}</td>
                                            <td>{{ item.label|default:"-" }}</td>
                                            <td>{{ item.num|default:"-" }}</td>
                                        </tr>
                                        {% empty %}
                                        <tr><td colspan="4"><div class="empty-state-container"><p>Aucun produit trouvé.</p></div></td></tr>
                                        {% endfor %}
                                    </tbody>
                                </table>
                            </div>
                            {% if autres_produits.has_other_pages %}
                            <div class="px-4 py-3 border-top border-white border-opacity-10 d-flex justify-content-between align-items-center">
                                <div class="text-muted small">Page {{ autres_produits.number }} sur {{ autres_produits.paginator.num_pages }}</div>
                                <nav>
                                    <ul class="pagination pagination-sm mb-0">
                                        {% if autres_produits.has_previous %}
                                        <li class="page-item"><a class="page-link rounded-pill px-3 me-2 border-0 shadow-sm" href="?ap_page={{ autres_produits.previous_page_number }}&tab=autres_produits">Précédent</a></li>
                                        {% endif %}
                                        {% if autres_produits.has_next %}
                                        <li class="page-item"><a class="page-link rounded-pill px-3 border-0 shadow-sm" href="?ap_page={{ autres_produits.next_page_number }}&tab=autres_produits">Suivant</a></li>
                                        {% endif %}
                                    </ul>
                                </nav>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
'''

target = '                \n            </div>\n        </div>\n    </div>\n</div>\n\n<!-- Modal Modification Spécialité -->'
if target in content:
    content = content.replace(target, tab_panes + target)
else:
    print('Failed to find the target string for tab insertion')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Patch 3 applied')
