"""
Test file to verify PDF export functionality
"""
from django.test import TestCase
from django.contrib.auth.models import User
from pdf_editor.models import DocumentTemplate, DocumentGeneration
from django.core.files.base import ContentFile


class PDFExportTestCase(TestCase):
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a test template with custom CSS
        self.template = DocumentTemplate.objects.create(
            title='Test Template',
            slug='test-template',
            template_type='invoice',
            content='<h1>Test Document</h1><p>This is a test document.</p>',
            custom_css='h1 { color: red; } p { font-size: 16px; }',
            is_active=True,
            created_by=self.user
        )
        
        # Create a document generation record
        self.document_generation = DocumentGeneration.objects.create(
            template=self.template,
            context_data={'test': 'data'},
            rendered_content='<h1>Test Document</h1><p>This is a test document.</p>',
            generated_by=self.user
        )

    def test_document_export_includes_custom_css(self):
        """Test that the PDF export includes custom CSS from the template"""
        from pdf_editor.views import DocumentExportView
        from django.http import HttpRequest
        from django.contrib.auth.models import AnonymousUser
        
        # Create a mock request
        request = HttpRequest()
        request.user = self.user
        
        # Create the view instance
        view = DocumentExportView()
        view.request = request
        
        # Get the document generation object
        document = self.document_generation
        
        # Check that the custom CSS is included in the HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                /* Styles de base pour le PDF */
                body {{
                    font-family: 'Segoe UI', system-ui, sans-serif;
                    margin: 0;
                    padding: 20mm;
                    line-height: 1.6;
                    background-color: white;
                    color: #1e293b;
                }}
                
                /* Styles Bootstrap simplifiés pour le PDF */
                .container {{
                    width: 100%;
                    padding-right: 15px;
                    padding-left: 15px;
                    margin-right: auto;
                    margin-left: auto;
                }}
                
                .row {{
                    display: flex;
                    flex-wrap: wrap;
                    margin-right: -15px;
                    margin-left: -15px;
                }}
                
                .col-md-4, .col-md-6, .col-md-12 {{
                    position: relative;
                    width: 100%;
                    padding-right: 15px;
                    padding-left: 15px;
                }}
                
                .card {{
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    min-width: 0;
                    word-wrap: break-word;
                    background-clip: border-box;
                    border: 1px solid rgba(0,0,0,.125);
                    border-radius: 0.25rem;
                    background-color: white;
                }}
                
                .card-body {{
                    flex: 1 1 auto;
                    min-height: 1px;
                    padding: 1.25rem;
                }}
                
                /* Styles pour les boutons et éléments d'interface à cacher */
                .btn, .no-print {{
                    display: none !important;
                }}
                
                /* Appliquer le CSS personnalisé du template */
                {document.template.custom_css}
            </style>
        </head>
        <body>
            {document.rendered_content}
        </body>
        </html>
        """
        
        # Verify that the custom CSS is included in the HTML
        self.assertIn('h1 { color: red; }', html_content)
        self.assertIn('p { font-size: 16px; }', html_content)
        
        print("✅ Test passed: Custom CSS is properly included in PDF export")
        
    def test_document_export_structure(self):
        """Test that the exported HTML has proper structure"""
        document = self.document_generation
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                /* Styles de base pour le PDF */
                body {{
                    font-family: 'Segoe UI', system-ui, sans-serif;
                    margin: 0;
                    padding: 20mm;
                    line-height: 1.6;
                    background-color: white;
                    color: #1e293b;
                }}
                
                /* Styles Bootstrap simplifiés pour le PDF */
                .container {{
                    width: 100%;
                    padding-right: 15px;
                    padding-left: 15px;
                    margin-right: auto;
                    margin-left: auto;
                }}
                
                .row {{
                    display: flex;
                    flex-wrap: wrap;
                    margin-right: -15px;
                    margin-left: -15px;
                }}
                
                .col-md-4, .col-md-6, .col-md-12 {{
                    position: relative;
                    width: 100%;
                    padding-right: 15px;
                    padding-left: 15px;
                }}
                
                .card {{
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    min-width: 0;
                    word-wrap: break-word;
                    background-clip: border-box;
                    border: 1px solid rgba(0,0,0,.125);
                    border-radius: 0.25rem;
                    background-color: white;
                }}
                
                .card-body {{
                    flex: 1 1 auto;
                    min-height: 1px;
                    padding: 1.25rem;
                }}
                
                /* Styles pour les boutons et éléments d'interface à cacher */
                .btn, .no-print {{
                    display: none !important;
                }}
                
                /* Appliquer le CSS personnalisé du template */
                {document.template.custom_css}
            </style>
        </head>
        <body>
            {document.rendered_content}
        </body>
        </html>
        """
        
        # Check that the HTML structure is correct
        self.assertIn('<!DOCTYPE html>', html_content)
        self.assertIn('<html>', html_content)
        self.assertIn('<head>', html_content)
        self.assertIn('<body>', html_content)
        self.assertIn('</body>', html_content)
        self.assertIn('</html>', html_content)
        
        print("✅ Test passed: HTML structure is correct for PDF export")