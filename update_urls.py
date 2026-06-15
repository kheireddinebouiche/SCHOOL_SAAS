import re

with open('t_tresorerie/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()

import_statement = 'from .f_views.suivi_cheques import *\n'
if import_statement not in content:
    content = content.replace('from .f_views.caisse import *', 'from .f_views.caisse import *\n' + import_statement)

route_statements = """
    # Suivi Cheques
    path('caisse/suivi-cheques-emis/', submenu_access_required("tre", "banque")(PageSuiviChequesEmis), name="PageSuiviChequesEmis"),
    path('caisse/api/suivi-cheques-emis/list/', ApiListChequesEmis, name="ApiListChequesEmis"),
    path('caisse/api/suivi-cheques-emis/update/', ApiUpdateChequeStatut, name="ApiUpdateChequeStatut"),
"""

if 'PageSuiviChequesEmis' not in content:
    content = content.replace('urlpatterns = [', 'urlpatterns = [\n' + route_statements)

with open('t_tresorerie/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)
