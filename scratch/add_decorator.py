import re

with open('institut_app/decorators.py', 'r', encoding='utf-8') as f:
    content = f.read()

decorator_code = """
def submenu_access_required(module_code, submenu_code):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            try:
                from institut_app.models import UserSubMenuAccess
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
"""

if 'def submenu_access_required' not in content:
    with open('institut_app/decorators.py', 'a', encoding='utf-8') as f:
        f.write("\n" + decorator_code)
    print("Decorator added.")
else:
    print("Decorator already exists.")
