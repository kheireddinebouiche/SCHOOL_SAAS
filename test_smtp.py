import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from saas_admin_app.models import SaaSEmailConfiguration
from django.core.mail import send_mail
from django.conf import settings

def test_smtp():
    config = SaaSEmailConfiguration.get_solo()
    if not config.email_enabled:
        print("Email not enabled in SaaS")
        return
        
    config.apply_email_settings()
    
    print(f"HOST: {settings.EMAIL_HOST}")
    print(f"PORT: {settings.EMAIL_PORT}")
    print(f"USER: {settings.EMAIL_HOST_USER}")
    print(f"TLS: {settings.EMAIL_USE_TLS}")
    print(f"FROM: {settings.DEFAULT_FROM_EMAIL}")
    
    try:
        res = send_mail(
            "TEST FROM ANTIGRAVITY",
            "This is a test to see if SMTP connects.",
            settings.DEFAULT_FROM_EMAIL,
            ["kheireddine.bouiche@gmail.com"],
            fail_silently=False
        )
        print(f"Result: {res}")
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")

test_smtp()
