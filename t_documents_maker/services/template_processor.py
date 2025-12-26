from django.template import Template, Context
import re

class TemplateProcessor:
    """Traite les templates HTML avec les variables Jinja"""
    
    def __init__(self, html_content):
        self.html_content = html_content
        self.cleaned_html = self._clean_jinja_blocks()
    
    def _clean_jinja_blocks(self):
        """
        Élimine SEULEMENT les balises <span class="jinja-block">
        MAIS GARDE TOUT LE RESTE du HTML!
        """
        # Élimine seulement les balises span jinja-block
        pattern = r'<span[^>]*class="jinja-block"[^>]*>(\{\{[^}]+\}\})</span>'
        cleaned = re.sub(pattern, r'\1', self.html_content)
        
        print(f"\n=== NETTOYAGE TEMPLATE ===")
        print(f"HTML AVANT (1000 chars):\n{self.html_content[:1000]}")
        print(f"\nHTML APRÈS (1000 chars):\n{cleaned[:1000]}\n")
        
        return cleaned
    
    def render(self, context_dict):
        """Rend le template avec les variables"""
        try:
            template = Template(self.cleaned_html)
            context = Context(context_dict)
            rendered_html = template.render(context)

            print(f"\n=== RENDU TEMPLATE ===")
            print(f"Variables: {context_dict}")
            print(f"HTML RENDU (1000 chars):\n{rendered_html[:1000]}\n")

            return rendered_html

        except Exception as e:
            print(f"\n❌ ERREUR RENDU: {e}")
            import traceback
            traceback.print_exc()
            raise

    def extract_variables(self):
        """Extrait toutes les variables Jinja du contenu HTML"""
        # Trouver toutes les variables {{ variable_name }}
        pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)\s*\}\}'
        matches = re.findall(pattern, self.html_content)
        # Nettoyer les variables (supprimer les espaces et les parties après les points pour les objets)
        variables = []
        for match in matches:
            # Extraire la variable de base (sans les attributs imbriqués)
            base_var = match.split('.')[0].strip()
            if base_var and base_var not in variables:
                variables.append(base_var)
        return variables

    def get_sample_data(self):
        """Génère des données d'exemple pour l'aperçu"""
        variables = self.extract_variables()
        sample_data = {}
        for var in variables:
            sample_data[var] = f"Exemple de {var}"
        return sample_data