from django.shortcuts import redirect
from django.contrib.auth import logout
from .models import UserSession
from django.urls import reverse

class DeviceLockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip for public schema as institut_app namespace won't be available
        if hasattr(request, 'tenant') and request.tenant.schema_name == 'public':
            return self.get_response(request)

        # Exempt the blocked page and login/logout to avoid loops
        exempt_urls = [
            reverse('institut_app:ShowBlockedConnexion'),
            reverse('institut_app:login'),
            reverse('institut_app:logout'),
        ]
        
        if request.path in exempt_urls:
            return self.get_response(request)

        if request.user.is_authenticated:
            # Vérifier la configuration globale d'abord si pas sur le schéma public
            if hasattr(request, 'tenant') and request.tenant.schema_name != 'public':
                from .models import GlobalConfiguration
                try:
                    config = GlobalConfiguration.get_solo()
                    if not config.device_lock_enabled:
                        return self.get_response(request)
                except Exception:
                    pass

            try:
                # Use hasattr or try/except to handle potential missing session_info
                if hasattr(request.user, 'session_info'):
                    session_info = request.user.session_info
                    
                    # Si le verrouillage est désactivé pour cet utilisateur, on ne fait rien
                    if not session_info.is_device_lock_enabled:
                        return self.get_response(request)
                    
                    # If a device lock is registered for this user
                    if session_info.device_uuid:
                        device_lock_cookie = request.COOKIES.get('device_lock')
                        
                        # Verify if the cookie matches the registered UUID
                        if str(session_info.device_uuid) != device_lock_cookie:
                            logout(request)
                            request.session["allow_blocked_page"] = True
                            return redirect('institut_app:ShowBlockedConnexion')
            except Exception:
                # Fallback for any errors to avoid breaking the app
                pass

        response = self.get_response(request)
        return response

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip for public schema as institut_app namespace won't be available
        if hasattr(request, 'tenant') and request.tenant.schema_name == 'public':
            return self.get_response(request)

        if request.user.is_authenticated:
            # Exempt URLs to avoid loops
            exempt_urls = [
                reverse('institut_app:logout'),
                reverse('institut_app:ChangePasswordForce'),
            ]
            
            # Also exempt admin views if user is superadmin (optional, but safer)
            # if request.path.startswith('/admin/'): return self.get_response(request)
            
            if request.path in exempt_urls:
                return self.get_response(request)
            
            # Static/Media
            from django.conf import settings
            if settings.STATIC_URL and request.path.startswith(settings.STATIC_URL):
                return self.get_response(request)
            if settings.MEDIA_URL and request.path.startswith(settings.MEDIA_URL):
                return self.get_response(request)

            # Check if tenant has force password change enabled
            if hasattr(request, 'tenant') and request.tenant.force_password_change:
                from .models import Profile
                profile, created = Profile.objects.get_or_create(user=request.user)
                
                # Check if user needs to change password
                # 1. Never changed password
                # 2. Changed password before the last reset date
                needs_change = False
                if not profile.last_password_change:
                    needs_change = True
                elif request.tenant.password_reset_date and profile.last_password_change < request.tenant.password_reset_date:
                    needs_change = True
                    
                if needs_change:
                    return redirect('institut_app:ChangePasswordForce')
                    
        return self.get_response(request)
