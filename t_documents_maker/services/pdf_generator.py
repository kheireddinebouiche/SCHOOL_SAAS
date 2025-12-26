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