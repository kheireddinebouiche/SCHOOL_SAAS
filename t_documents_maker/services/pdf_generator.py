from weasyprint import HTML, CSS
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Génère des PDFs avec WeasyPrint (Windows-friendly)"""

    def __init__(self, html_content, options=None):
        self.html_content = html_content
        self.options = options or {}
        self.page_size = self.options.get('page_size', 'A4')
        self.orientation = self.options.get('page_orientation', 'portrait')

    def generate(self):
        """Génère le PDF"""
        try:
            print(f"\n=== GÉNÉRATION PDF (WeasyPrint) ===")
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

            # Génère le PDF avec WeasyPrint
            html_doc = HTML(string=html_final)
            css_doc = CSS(string=page_css)

            pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc])

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
            size_css = "@page { size: landscape; margin: 0; }"
        else:
            size_css = "@page { size: A4 portrait; margin: 0; }"

        # Use default margins if not specified in options
        top_margin = self.options.get('margins', {}).get('top', 2.0) if hasattr(self, 'options') else 2.0
        bottom_margin = self.options.get('margins', {}).get('bottom', 2.5) if hasattr(self, 'options') else 2.5
        left_margin = self.options.get('margins', {}).get('left', 1.5) if hasattr(self, 'options') else 1.5
        right_margin = self.options.get('margins', {}).get('right', 1.5) if hasattr(self, 'options') else 1.5

        css = f"""
        {size_css}
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        * {{ margin: 0; padding: 0; }}
        body {{ font-family: 'Poppins', Arial, sans-serif; font-size: 12px; color: #000; position: relative; }}
        .page-canvas, .page-content {{ position: relative; width: 21cm; height: 29.7cm; box-sizing: border-box; overflow: hidden; }}
        .page-content {{ padding: 0; }} /* No margins - elements positioned as they appear in editor */
        h1, h2, h3, h4, h5, h6 {{ margin: 15px 0 10px 0; line-height: 1.2; }}
        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 20px; }}
        p {{ margin: 10px 0; line-height: 1.5; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        td, th {{ border: 1px solid #000; padding: 5px; }}

        /* Shape styles for PDF rendering - preserve exact sizes from editor */
        .shape-line {{
            display: block !important;
            background: #000 !important;
            z-index: 50 !important;
            position: absolute !important;
            height: 2px !important;
        }}

        .shape-line.horizontal {{
            height: 2px !important;
        }}

        .shape-line.vertical {{
            width: 2px !important;
            display: inline-block !important;
            vertical-align: middle !important;
        }}

        .shape-frame {{
            display: block !important;
            z-index: 50 !important;
            position: absolute !important;
            min-width: 50px !important;
            min-height: 50px !important;
        }}

        .shape-frame.solid {{
            border: 2px solid #000 !important;
        }}

        .shape-frame.dashed {{
            border: 2px dashed #000 !important;
        }}

        .shape-frame.dotted {{
            border: 2px dotted #000 !important;
        }}

        /* Page number styles for PDF rendering */
        .page-number {{
            display: block;
            font-size: 12px;
            color: #666;
            font-family: 'Poppins', Arial, sans-serif;
            padding: 2px 6px;
            background: #e2e8f0;
            border: 1px solid #cbd5e0;
            font-weight: bold;
            position: absolute;
        }}

        /* Jinja block styles for PDF rendering */
        .jinja-block {{
            background: #fff3cd;
            border: 2px dashed #ffc107;
            padding: 2px 6px;
            margin: 0 2px;
            display: inline-block;
            vertical-align: middle;
        }}

        /* Image styles for PDF rendering - preserve exact sizes from editor */
        .image-element {{
            position: absolute !important;
            margin: 0 !important;
            display: block !important;
        }}

        .image-element img {{
            width: 100% !important;
            height: 100% !important;
            object-fit: contain !important;
        }}
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
            print(f"\n=== GÉNÉRATION PDF MULTI-PAGE (WeasyPrint) ===")
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

            # Génère le PDF avec WeasyPrint
            html_doc = HTML(string=html_final)
            css_doc = CSS(string=global_css)

            pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc])

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
            size_css = f"@page {{ size: {page_size} landscape; margin: 0; }}"
        else:
            size_css = f"@page {{ size: {page_size} portrait; margin: 0; }}"

        css = f"""
        {size_css}
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        * {{ margin: 0; padding: 0; }}
        body {{ font-family: 'Poppins', Arial, sans-serif; font-size: 12px; color: #000; position: relative; }}
        .page-canvas, .page-content {{ position: relative; width: 21cm; height: 29.7cm; box-sizing: border-box; overflow: hidden; }}
        .page-content {{ padding: 0; }} /* No margins - elements positioned as they appear in editor */
        h1, h2, h3, h4, h5, h6 {{ margin: 15px 0 10px 0; line-height: 1.2; }}
        h1 {{ font-size: 24px; }}
        h2 {{ font-size: 20px; }}
        p {{ margin: 10px 0; line-height: 1.5; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        td, th {{ border: 1px solid #000; padding: 5px; }}

        /* Shape styles for PDF rendering - preserve exact sizes from editor */
        .shape-line {{
            display: block !important;
            background: #000 !important;
            z-index: 50 !important;
            position: absolute !important;
            height: 2px !important;
        }}

        .shape-line.horizontal {{
            height: 2px !important;
        }}

        .shape-line.vertical {{
            width: 2px !important;
            display: inline-block !important;
            vertical-align: middle !important;
        }}

        .shape-frame {{
            display: block !important;
            z-index: 50 !important;
            position: absolute !important;
            min-width: 50px !important;
            min-height: 50px !important;
        }}

        .shape-frame.solid {{
            border: 2px solid #000 !important;
        }}

        .shape-frame.dashed {{
            border: 2px dashed #000 !important;
        }}

        .shape-frame.dotted {{
            border: 2px dotted #000 !important;
        }}

        /* Page number styles for PDF rendering */
        .page-number {{
            display: block;
            font-size: 12px;
            color: #666;
            font-family: 'Poppins', Arial, sans-serif;
            padding: 2px 6px;
            background: #e2e8f0;
            border: 1px solid #cbd5e0;
            font-weight: bold;
            position: absolute;
        }}

        /* Jinja block styles for PDF rendering */
        .jinja-block {{
            background: #fff3cd;
            border: 2px dashed #ffc107;
            padding: 2px 6px;
            margin: 0 2px;
            display: inline-block;
            vertical-align: middle;
        }}

        /* Image styles for PDF rendering - preserve exact sizes from editor */
        .image-element {{
            position: absolute !important;
            margin: 0 !important;
            display: block !important;
        }}

        .image-element img {{
            width: 100% !important;
            height: 100% !important;
            object-fit: contain !important;
        }}
        """
        return css