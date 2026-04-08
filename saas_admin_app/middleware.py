from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin
from .models import SaaSMaintenanceConfiguration
import logging

logger = logging.getLogger(__name__)

class SaaSMaintenanceMiddleware(MiddlewareMixin):
    """
    Middleware qui bloque l'accès à la plateforme si le mode développement (maintenance)
    est activé, à l'exception des URLs nécessaires (saas-admin, static, media).
    """
    def process_request(self, request):
        path = request.path_info
        
        # Toujours autoriser les assets (static/media) et le panel superadmin (saas-admin)
        if path.startswith('/saas-admin/') or path.startswith('/static/') or path.startswith('/media/') or path.startswith('/admin/'):
            return None
        
        # Vérifier si on est en mode maintenance
        try:
            config = SaaSMaintenanceConfiguration.get_solo()
            if config.is_maintenance_mode:
                return render(request, 'public_folder/maintenance.html', {
                    'message': config.maintenance_message,
                    'end_time': config.maintenance_end_time.isoformat() if config.maintenance_end_time else None
                }, status=503)
        except Exception as e:
            # En cas d'erreur de BDD (par ex lors d'une migration), on ignore
            logger.error(f"Erreur lors de la vérification de la maintenance : {e}")
            pass
            
        return None
