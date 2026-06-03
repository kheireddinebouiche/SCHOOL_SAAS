from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from .models import *

def ajax_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return view_func(request, *args, **kwargs)
        return redirect('institut_app:Error404')
    return _wrapped_view

def module_permission_required(module_name, permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            try:
                umr = UserModuleRole.objects.get(
                    user=request.user,
                    module__name=module_name
                )
            except UserModuleRole.DoesNotExist:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'Module non accessible'})
                return redirect('institut_app:Error404')

            if not umr.has_permission(permission):
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'Permission insuffisante'})
                return redirect('institut_app:Error404')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def role_required(module_name, roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            try:
                umr = UserModuleRole.objects.select_related(
                    'role', 'module'
                ).get(
                    user=request.user,
                    module__name=module_name
                )
            except UserModuleRole.DoesNotExist:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'Rôle non défini pour ce module'})
                return redirect('institut_app:Error404')

            if umr.role.name not in roles:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'Rôle insuffisant'})
                return redirect('institut_app:Error404')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def superuser_required(view_func):
    """
    Décorateur qui vérifie que l'utilisateur est un superutilisateur.
    Sinon, renvoie vers Error404 ou retourne un JSON pour AJAX,
    évitant ainsi la redirection vers la page de login.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Accès refusé. Réservé aux superutilisateurs.'})
        return redirect('institut_app:Error404')
    return _wrapped_view

def submenu_access_required(module_code, submenu_code):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            try:
                from institut_app.models import UserSubMenuAccess
                
                if isinstance(submenu_code, (list, tuple)):
                    access = UserSubMenuAccess.objects.filter(
                        user=request.user,
                        module_code=module_code,
                        submenu_code__in=submenu_code,
                        is_active=True
                    ).exists()
                    if not access:
                        raise Exception("No access")
                else:
                    access = UserSubMenuAccess.objects.get(
                        user=request.user,
                        module_code=module_code,
                        submenu_code=submenu_code,
                        is_active=True
                    )
            except Exception:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({'status': 'error', 'message': 'Accès non autorisé au sous-menu'})
                from django.shortcuts import redirect
                return redirect('institut_app:Error404')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
