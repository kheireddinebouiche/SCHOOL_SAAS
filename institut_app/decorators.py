from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from .views import Error404
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
                    return JsonResponse({'status': 'error', 'message': 'Module non accessible'}, status=403)
                return redirect('institut_app:Error404')

            if not umr.has_permission(permission):
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'Permission insuffisante'}, status=403)
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
                    return JsonResponse({'status': 'error', 'message': 'Rôle non défini pour ce module'}, status=403)
                return redirect('institut_app:Error404')

            if umr.role.name not in roles:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'status': 'error', 'message': 'Rôle non autorisé'}, status=403)
                return redirect('institut_app:Error404')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator