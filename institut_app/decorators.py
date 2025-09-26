from functools import wraps
from django.http import JsonResponse


def ajax_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return view_func(request, *args, **kwargs)
        return JsonResponse({"status": "error", "message": "Accès non autorisé"}, status=403)
    return _wrapped_view