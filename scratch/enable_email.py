import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from saas_admin_app.models import SaaSEmailConfiguration

def enable_email():
    config = SaaSEmailConfiguration.get_solo()
    config.email_enabled = True
    config.save()
    print("✅ Configuration email activée dans la base de données SaaS Admin.")

if __name__ == "__main__":
    enable_email()
