from xhtml2pdf import pisa
from io import BytesIO
from typing import Tuple, Dict

class PDFGenerator:
    """PDF universel Windows/Linux/Mac"""
    
    def __init__(self, html_content: str, options: Dict = None):
        self.html_content = html_content
        self.options = options or {}
    
    def generate(self) -> Tuple[bytes, bool, str]:
        try:
            buffer = BytesIO()
            css = self._get_css()
            
            result = pisa.CreatePDF(
                f'<html><head><style>{css}</style></head><body>{self.html_content}</body></html>',
                dest=buffer,
                encoding='UTF-8'
            )
            
            if result.err:
                return b'', False, str(result.err)
            
            buffer.seek(0)
            return buffer.getvalue(), True, ""
        except Exception as e:
            return b'', False, str(e)
    
    def _get_css(self) -> str:
        size = self.options.get('page_size', 'A4')
        orientation = self.options.get('page_orientation', 'portrait')
        
        return f"""
        @page {{
            size: {size} {orientation};
            margin: 2cm 1.5cm 2.5cm 1.5cm;
            @bottom-center {{ content: "Page " counter(page); font-size: 10px; }}
        }}
        * {{ box-sizing: border-box; }}
        body {{ 
            font-family: DejaVu Sans, Arial, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            font-size: 12pt; 
        }}
        h1 {{ font-size: 24pt; color: #2c3e50; text-align: center; margin: 1cm 0; }}
        h2 {{ font-size: 18pt; color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 8pt; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1cm 0; }}
        th {{ background: #3498db !important; color: white !important; padding: 10pt 8pt; text-align: center; }}
        td {{ border: 1pt solid #ddd; padding: 8pt; }}
        tr:nth-child(even) {{ background: #f8f9fa; }}
        .jinja-highlight {{ 
            background: #fff3cd !important; 
            border: 2px dashed #ffc107 !important; 
            padding: 4pt 8pt !important; 
        }}
        .success {{ color: #28a745; }}
        .warning {{ color: #ffc107; }}
        .danger {{ color: #dc3545; }}
        """
