import os
import django
import sys

# Ajouter le répertoire racine au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from saas_admin_app.email_utils import send_platform_email

def test_send_email():
    print("Test de l'envoi d'email via la configuration globale SaaS...")
    success = send_platform_email(
        subject="Test de configuration Email - School SaaS",
        message="Ceci est un message de test envoyé depuis la plateforme centrale.",
        recipient_list=["test@example.com"], # Remplacer par un vrai email si nécessaire
        html_message="<p>Ceci est un message de <strong>test</strong> envoyé depuis la plateforme centrale.</p>"
    )
    
    if success:
        print("Succès: L'email a été envoyé (ou du moins remis au serveur SMTP) avec succès.")
    else:
        print("Échec: L'email n'a pas pu être envoyé. Vérifiez les logs ou la configuration.")

if __name__ == "__main__":
    test_send_email()
