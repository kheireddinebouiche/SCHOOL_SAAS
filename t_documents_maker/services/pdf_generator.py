from xhtml2pdf import pisa
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Génère des PDFs avec xhtml2pdf (Windows-friendly)"""

    def __init__(self, html_content, options=None):
        self.html_content = html_content
        self.options = options or {}
        self.page_size = self.options.get('page_size', 'A4')
        self.orientation = self.options.get('page_orientation', 'portrait')

    def generate(self):
        """Génère le PDF"""
        try:
            print(f"\n=== GÉNÉRATION PDF (xhtml2pdf) ===")
            print(f"Page size: {self.page_size}")
            print(f"Orientation: {self.orientation}")

            # CSS pour la mise en page
            page_css = self._get_page_css()

            # Enveloppe le HTML
            html_final = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
{page_css}
</style>
</head>
<body>
{self.html_content}
</body>
</html>"""

            # Génère le PDF
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(
                html_final,
                pdf_buffer,
                encoding='UTF-8'
            )

            if pisa_status.err:
                print(f"❌ ERREUR: {pisa_status.err}")
                return None, False, str(pisa_status.err)

            pdf_bytes = pdf_buffer.getvalue()
            print(f"✅ PDF généré ({len(pdf_bytes)} bytes)")
            return pdf_bytes, True, None

        except Exception as e:
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            return None, False, str(e)

    def _get_page_css(self):
        """CSS pour la page"""
        orientation = self.orientation.lower() if self.orientation else 'portrait'

        if orientation == 'landscape':
            size_css = "@page { size: landscape; margin: 1cm; }"
        else:
            size_css = "@page { size: A4 portrait; margin: 1cm; }"

        css = f"""
        {size_css}
        * {{ margin: 0; padding: 0; }}
        body {{ font-family: Arial, sans-serif; font-size: 12px; color: #000; }}
        h1, h2, h3, h4, h5, h6 {{ margin: 15px 0 10px 0; line-height: 1.2; }}
        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 20px; }}
        p {{ margin: 10px 0; line-height: 1.5; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        td, th {{ border: 1px solid #000; padding: 5px; }}
        """
        return css


class MultiPagePDFGenerator:
    """Génère des PDFs avec plusieurs pages, chacune pouvant avoir des paramètres différents"""

    def __init__(self, pages_data, options=None):
        self.pages_data = pages_data  # Liste de dictionnaires avec 'content', 'page_size', 'orientation'
        self.options = options or {}
        self.default_page_size = self.options.get('page_size', 'A4')
        self.default_orientation = self.options.get('page_orientation', 'portrait')
        self.header_footer_config = self.options.get('header_footer', {})

    def generate(self):
        """Génère le PDF multi-page"""
        try:
            print(f"\n=== GÉNÉRATION PDF MULTI-PAGE (xhtml2pdf) ===")
            print(f"Nombre de pages: {len(self.pages_data)}")

            # Générer le HTML complet avec toutes les pages
            html_parts = []
            for i, page_data in enumerate(self.pages_data):
                content = page_data.get('content', '')
                page_size = page_data.get('page_size', self.default_page_size)
                orientation = page_data.get('orientation', self.default_orientation)

                # Générer le CSS spécifique pour cette page
                page_css = self._get_page_css(page_size, orientation)

                # Ajouter un séparateur de page pour toutes les pages sauf la première
                if i > 0:
                    html_parts.append('<div style="page-break-before: always;"></div>')

                # Ajouter le contenu de la page avec header et footer
                page_html = f"""<div class="page-{i}">
                    {self._get_header_html()}
                    <div class="page-content">
                        {content}
                    </div>
                    {self._get_footer_html()}
                </div>"""
                html_parts.append(page_html)

            full_html = "".join(html_parts)

            # Générer le CSS global
            global_css = self._get_page_css(self.default_page_size, self.default_orientation)

            # Enveloppe le HTML
            html_final = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
{global_css}
</style>
</head>
<body>
{full_html}
</body>
</html>"""

            # Génère le PDF
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(
                html_final,
                pdf_buffer,
                encoding='UTF-8'
            )

            if pisa_status.err:
                print(f"❌ ERREUR: {pisa_status.err}")
                return None, False, str(pisa_status.err)

            pdf_bytes = pdf_buffer.getvalue()
            print(f"✅ PDF multi-page généré ({len(pdf_bytes)} bytes)")
            return pdf_bytes, True, None

        except Exception as e:
            print(f"❌ ERREUR: {e}")
            import traceback
            traceback.print_exc()
            return None, False, str(e)

    def _get_header_html(self):
        """Génère le HTML pour l'en-tête"""
        if not self.header_footer_config:
            return ""

        header_config = self.header_footer_config.get('header', {})
        if not header_config.get('enabled', False):
            return ""

        logo_html = ""
        if header_config.get('logo_path'):
            logo_html = f'<img src="{header_config["logo_path"]}" style="height: 50px; max-width: 200px;" />'

        text_html = ""
        if header_config.get('text'):
            text_html = f'<div style="font-size: 14px; font-weight: bold;">{header_config["text"]}</div>'

        # Positionnement du logo
        logo_position = header_config.get('logo_position', 'left')
        text_position = header_config.get('text_position', 'right')

        # Créer le conteneur de l'en-tête
        header_style = "display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; border-bottom: 1px solid #ccc; margin-bottom: 20px;"

        if logo_position == 'left' and text_position == 'right':
            return f'<div class="header" style="{header_style}">{logo_html}<div></div>{text_html}</div>'
        elif logo_position == 'center' or text_position == 'center':
            return f'<div class="header" style="{header_style}"><div style="flex: 1;"></div>{logo_html}{text_html}<div style="flex: 1;"></div></div>'
        else:
            return f'<div class="header" style="{header_style}">{text_html}<div></div>{logo_html}</div>'

    def _get_footer_html(self):
        """Génère le HTML pour le pied de page"""
        if not self.header_footer_config:
            return ""

        footer_config = self.header_footer_config.get('footer', {})
        if not footer_config.get('enabled', False):
            return ""

        # Générer le HTML pour le logo
        logo_html = ""
        if footer_config.get('logo_path'):
            logo_html = f'<img src="{footer_config["logo_path"]}" style="height: 30px; max-width: 150px;" />'

        # Générer le HTML pour le texte
        text_html = ""
        if footer_config.get('text'):
            text_html = f'<div style="font-size: 12px;">{footer_config["text"]}</div>'

        # Positionnement du logo
        logo_position = footer_config.get('logo_position', 'center')
        text_position = footer_config.get('text_position', 'center')

        # Créer le conteneur du pied de page
        footer_style = "display: flex; justify-content: space-between; align-items: center; padding: 10px 20px; border-top: 1px solid #ccc; margin-top: 20px; font-size: 12px;"

        if logo_position == 'left' and text_position == 'right':
            return f'<div class="footer" style="{footer_style}">{logo_html}<div></div>{text_html}</div>'
        elif logo_position == 'center' or text_position == 'center':
            return f'<div class="footer" style="{footer_style}"><div style="flex: 1;"></div>{logo_html}{text_html}<div style="flex: 1;"></div></div>'
        else:
            return f'<div class="footer" style="{footer_style}">{text_html}<div></div>{logo_html}</div>'

    def _get_page_css(self, page_size='A4', orientation='portrait'):
        """CSS pour une page spécifique"""
        orientation = orientation.lower() if orientation else 'portrait'
        page_size = page_size.upper() if page_size else 'A4'

        if orientation == 'landscape':
            size_css = f"@page {{ size: {page_size} landscape; margin: 1cm; }}"
        else:
            size_css = f"@page {{ size: {page_size} portrait; margin: 1cm; }}"

        css = f"""
        {size_css}
        * {{ margin: 0; padding: 0; }}
        body {{ font-family: Arial, sans-serif; font-size: 12px; color: #000; }}
        h1, h2, h3, h4, h5, h6 {{ margin: 15px 0 10px 0; line-height: 1.2; }}
        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 20px; }}
        p {{ margin: 10px 0; line-height: 1.5; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        td, th {{ border: 1px solid #000; padding: 5px; }}
        """
        return css