import logging
from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from saas_admin_app.models import SaaSEmailConfiguration

logger = logging.getLogger(__name__)

def get_platform_email_backend():
    """
    Récupère le backend SMTP configuré dans le SaaS Admin (schéma public).
    Retourne (backend, from_email, email_enabled)
    """
    try:
        # Comme saas_admin_app est probablement dans SHARED_APPS, ceci interroge le schéma public.
        config = SaaSEmailConfiguration.get_solo()
        
        if not config.email_enabled:
            return None, None, False
            
        # Le port 465 nécessite SSL (Implicit TLS), pas STARTTLS (use_tls).
        # Le port 587 nécessite STARTTLS (use_tls).
        use_ssl = config.email_use_tls if config.email_port == 465 else False
        use_tls = config.email_use_tls if config.email_port != 465 else False

        backend = EmailBackend(
            host=config.email_host,
            port=config.email_port,
            username=config.email_host_user,
            password=config.email_host_password,
            use_tls=use_tls,
            use_ssl=use_ssl,
            fail_silently=False,
            timeout=10,
        )
        return backend, config.default_from_email, True
        
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de la configuration email SaaS: {e}")
        return None, None, False

def send_platform_email(subject, message, recipient_list, html_message=None, reply_to=None, from_email_display=None):
    """
    Envoie un email en utilisant la configuration globale du SaaS Admin de manière thread-safe.
    
    :param subject: L'objet de l'email
    :param message: Le contenu texte brut de l'email
    :param recipient_list: Liste des adresses emails destinataires
    :param html_message: (Optionnel) Le contenu HTML de l'email
    :param reply_to: (Optionnel) Liste d'adresses email de réponse (ex: ['contact@ecole.com'])
    :param from_email_display: (Optionnel) Nom d'affichage personnalisé de l'expéditeur
    :return: True si l'envoi a réussi, False sinon
    """
    backend, from_email, is_enabled = get_platform_email_backend()
    
    if not is_enabled or not backend:
        logger.warning("Tentative d'envoi d'email ignorée: Configuration désactivée ou indisponible.")
        return False
        
    try:
        sender = from_email or settings.DEFAULT_FROM_EMAIL
        if from_email_display:
            # Aligner sur le domaine expéditeur réel du SMTP pour éviter le spoofing
            from_addr = sender
            if '<' in sender and '>' in sender:
                from_addr = sender.split('<')[1].split('>')[0]
            sender = f"{from_email_display} <{from_addr}>"

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=sender,
            to=recipient_list,
            connection=backend,
            reply_to=reply_to
        )
        
        if html_message:
            email.attach_alternative(html_message, "text/html")
            
        email.send(fail_silently=False)
        return True
        
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email platforme: {e}")
        return False
