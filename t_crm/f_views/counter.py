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
        
        # Get or create counter for today
        counter, created = CrmCounter.objects.get_or_create(
            date_counter=today,
            defaults={'visite_counter': 0, 'phone_counter': 0}
        )
        
        # Increment the appropriate counter
        if counter_type == 'visit':
            counter.visite_counter += 1
        elif counter_type == 'call':
            counter.phone_counter += 1
            
        counter.save()
        
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error'})


@login_required(login_url="institut_app:login")
def get_activity_history(request):
    # Get all counters ordered by date
    counters = CrmCounter.objects.all().order_by('-date_counter')
    
    data = []
    for counter in counters:
        data.append({
            'date': counter.date_counter.strftime('%Y-%m-%d') if counter.date_counter else '',
            'visits': counter.visite_counter,
            'calls': counter.phone_counter,
            'user': 'Admin'  # In a real implementation, this would be the actual user
        })
    
    return JsonResponse(data, safe=False)

