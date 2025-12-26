import re
from jinja2 import Environment, select_autoescape
from datetime import datetime
from typing import Dict, Any, List
from html import unescape

class TemplateProcessor:
    def __init__(self, html_content: str):
        self.html_content = html_content
        self.env = Environment(autoescape=select_autoescape(['html', 'xml']))
        self._add_filters()
    
    def _add_filters(self):
        """Filtres Jinja2 personnalisés"""
        def currency(value):
            try:
                return f"{float(value):,.2f} €".replace(',', ' ').replace('.', ',')
            except:
                return str(value)
        
        def date_format(value, fmt='%d/%m/%Y'):
            try:
                if isinstance(value, str):
                    return datetime.strptime(value, '%Y-%m-%d').strftime(fmt)
                return str(value)
            except:
                return str(value)
        
        self.env.filters['currency'] = currency
        self.env.filters['date_format'] = date_format
    
    def extract_variables(self) -> List[str]:
        """Extrait toutes les variables {{ }} et boucles"""
        # Décoder les entités HTML pour assurer une détection correcte
        decoded_content = unescape(self.html_content)
        variables = set()

        # Variables simples {{ variable }}
        for match in re.finditer(r'\{\{\s*([^}]+)\s*\}\}', decoded_content):
            var_name = match.group(1).strip().split('|')[0].strip()  # Ignore les filtres
            variables.add(var_name)

        # Variables avec entités HTML &#123;&#123; variable &#125;&#125;
        for match in re.finditer(r'&#123;&#123;\s*([^}]+)\s*&#125;&#125;', decoded_content):
            var_name = match.group(1).strip().split('|')[0].strip()  # Ignore les filtres
            variables.add(var_name)

        # Collections de boucles {% for item in collection %} ou &#123;% for item in collection %&#125;
        for match in re.finditer(r'for\s+\w+\s+in\s+(\w+)', decoded_content, re.IGNORECASE):
            variables.add(match.group(1))

        # Collections de boucles avec entités HTML
        for match in re.finditer(r'&#123;%\s*for\s+\w+\s+in\s+(\w+)\s*%&#125;', decoded_content, re.IGNORECASE):
            variables.add(match.group(1))

        return sorted(list(variables))
    
    def render(self, data: Dict[str, Any]) -> str:
        """Rend le template avec les données"""
        try:
            template = self.env.from_string(self.html_content)
            return template.render(**data)
        except Exception:
            # Fallback simple pour les tags {{ }}
            result = self.html_content
            for key, value in data.items():
                # CORRECTION : Regex échappée correctement
                pattern = r'\{\{\s*' + re.escape(str(key)) + r'\s*\}\}'
                replacement = str(value)
                result = re.sub(pattern, replacement, result)
            return result
    
    def get_sample_data(self) -> Dict[str, Any]:
        """Données d'exemple automatiques"""
        sample_data = {
            'titre_document': 'Mon Document Officiel',
            'nom_client': 'Dupont SARL',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'nom': 'John Doe',
            'prenom': 'Marie',
            'total': 1250.75,
            'line_items': [
                {'nom': 'Produit A', 'quantite': 2, 'prix': 150.50},
                {'nom': 'Produit B', 'quantite': 1, 'prix': 950.25},
            ],
            'eleves': [
                {'nom': 'DUPONT', 'prenom': 'Alice', 'note': 15.5, 'classe': '3ème'},
                {'nom': 'MARTIN', 'prenom': 'Paul', 'note': 14.2, 'classe': '4ème'},
            ]
        }
        
        # Ajoute les variables détectées avec des valeurs d'exemple
        for var in self.extract_variables():
            if var not in sample_data:
                if 'date' in var.lower():
                    sample_data[var] = datetime.now().strftime('%d/%m/%Y')
                elif any(x in var.lower() for x in ['prix', 'montant', 'total']):
                    sample_data[var] = 1250.75
                elif 'email' in var.lower():
                    sample_data[var] = 'exemple@email.com'
                else:
                    sample_data[var] = f'Valeur de {var}'

        return sample_data
