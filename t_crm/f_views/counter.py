from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from ..models import *
from django.db import transaction
from django.utils.dateformat import format
import datetime
from django.db.models import F

@login_required(login_url="institut_app:login")
def ApiUpdateVisisteCounter(request):
    pass

@login_required(login_url="institut_app:login")
def ApiUpdatePhoneCallCounter(request):
    pass

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from ..models import CrmCounter

@login_required(login_url="institut_app:login")
def get_crm_counters(request):
    # Get today's date
    from datetime import date
    today = date.today()
    
    # Get or create counter for today
    counter, created = CrmCounter.objects.get_or_create(
        date_counter=today,
        defaults={'visite_counter': 0, 'phone_counter': 0}
    )
    
    data = [{
        'date_counter': counter.date_counter.strftime('%Y-%m-%d') if counter.date_counter else '',
        'visite_counter': counter.visite_counter,
        'phone_counter': counter.phone_counter
    }]
    
    return JsonResponse(data, safe=False)


@login_required(login_url="institut_app:login")
def increment_crm_counter(request):
    if request.method == 'POST' and request.POST.get('type'):
        counter_type = request.POST.get('type')
        
        # Get today's date
        from datetime import date
        today = date.today()
        
        try:
            with transaction.atomic():
                # Get or create counter for today
                counter, created = CrmCounter.objects.get_or_create(
                    date_counter=today,
                    defaults={'visite_counter': 0, 'phone_counter': 0}
                )
                
                # Record detailed activity
                activity_type_db = 'visit' if counter_type == 'visit' else 'call'
                CrmActivity.objects.create(
                    user=request.user,
                    activity_type=activity_type_db
                )
                
                # Increment the aggregate counter
                if counter_type == 'visit':
                    counter.visite_counter = F('visite_counter') + 1
                elif counter_type == 'call':
                    counter.phone_counter = F('phone_counter') + 1
                    
                counter.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error'})


@login_required(login_url="institut_app:login")
def get_activity_history(request):
    # Get last 15 activities ordered by date
    activities = CrmActivity.objects.select_related('user').order_by('-created_at')[:15]
    
    data = []
    for act in activities:
        user_name = f"{act.user.first_name} {act.user.last_name}".strip()
        if not user_name:
            user_name = act.user.username
            
        data.append({
            'date': act.created_at.strftime('%Y-%m-%d'),
            'time': act.created_at.strftime('%H:%M'),
            'visits': 1 if act.activity_type == 'visit' else 0, # compatibility if needed
            'calls': 1 if act.activity_type == 'call' else 0,
            'type': act.activity_type,
            'type_label': act.get_activity_type_display(),
            'user': user_name
        })
    
    return JsonResponse(data, safe=False)

