import re

with open('templates/tenant_folder/menu.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(
    r"(PageBrouillardBanque ImputationBancaire PageRecouvrement PageSituationComptes)",
    r"PageBrouillardBanque PageSuiviChequesEmis ImputationBancaire PageRecouvrement PageSituationComptes",
    content
)

content = re.sub(
    r"(<a href=\"\{% url 't_tresorerie:PageBrouillardBanque' %\}\" class=\"nav-link [^\"]+\"[^>]*>\s*<span>Brouillard de banque</span>\s*</a>)",
    r"\1\n                                                <a href=\"{% url 't_tresorerie:PageSuiviChequesEmis' %}\" class=\"nav-link {% if request.resolver_match.url_name == 'PageSuiviChequesEmis' %}active{% endif %} d-flex align-items-center py-1 px-2 rounded-2\">\n                                                    <span>Chèques émis</span>\n                                                </a>",
    content
)

with open('templates/tenant_folder/menu.html', 'w', encoding='utf-8') as f:
    f.write(content)
