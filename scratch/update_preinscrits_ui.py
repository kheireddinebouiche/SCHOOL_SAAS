import sys

filename = 'templates/tenant_folder/crm/preinscrits/liste-des-preinscrits.html'
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add the select menu to the HTML
html_to_find = '<select id="filter-specialite" class="form-select modern-select py-2 px-3" style="max-width: 250px;">'
html_to_add = '''<select id="filter-completion" class="form-select modern-select py-2 px-3" style="max-width: 220px;" title="Filtrer par complétude">
                                <option value="">Toutes les complétudes</option>
                                <option value="info_incomplete">Informations Incomplètes</option>
                                <option value="doc_incomplet">Dossier Incomplet</option>
                            </select>

                            '''
content = content.replace(html_to_find, html_to_add + html_to_find)

# 2. Update loadProspects
js_find1 = '''var sortOrder = $('#sort-order').val() || 'nom_asc';'''
js_add1 = '''var sortOrder = $('#sort-order').val() || 'nom_asc';
        var completionFilter = $('#filter-completion').val();'''
content = content.replace(js_find1, js_add1)

js_find2 = '''              'sort': sortOrder,
              'page': currentPage'''
js_add2 = '''              'sort': sortOrder,
              'completion': completionFilter,
              'page': currentPage'''
content = content.replace(js_find2, js_add2)

# 3. Update Event Listeners
# Let's search for the block that binds changes to filters
js_find3 = '''$('#filter-promo, #filter-specialite, #filter-prospect, #month-filter, #sort-order').on('change', function() {'''
js_add3 = '''$('#filter-promo, #filter-specialite, #filter-prospect, #month-filter, #sort-order, #filter-completion').on('change', function() {'''
if js_find3 in content:
    content = content.replace(js_find3, js_add3)
else:
    # Let's try another variation
    js_find4 = '''$('#filter-promo, #filter-specialite, #month-filter, #sort-order').on('change', function() {'''
    js_add4 = '''$('#filter-promo, #filter-specialite, #month-filter, #sort-order, #filter-completion').on('change', function() {'''
    content = content.replace(js_find4, js_add4)

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)
print('Updated liste-des-preinscrits.html successfully.')
