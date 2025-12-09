from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from .views import Error404

def ajax_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return view_func(request, *args, **kwargs)
        return redirect('institut_app:Error404')
    return _wrapped_view