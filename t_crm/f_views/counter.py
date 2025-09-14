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

@login_required(login_url="institut_app:login")
def get_crm_counters(request):
    date = datetime.date.today()
    object = CrmCounter.objects.filter(date_counter = date).values('id','visite_counter','phone_counter')

    return JsonResponse(list(object), safe=False)



@login_required(login_url="institut_app:login")
@transaction.atomic
def increment_crm_counter(request):
    type = request.POST.get('type')
    today = datetime.date.today()

    if type == "visit":
        obj, created = CrmCounter.objects.get_or_create(
            date_counter=today,
            defaults={"visite_counter": 1}
        )
        if not created:
            CrmCounter.objects.filter(pk=obj.pk).update(visite_counter=F("visite_counter") + 1)



    else:

        obj, created = CrmCounter.objects.get_or_create(
            date_counter = today,
            defaults={"phone_counter" : 1}
        )
        if not created:
            CrmCounter.objects.filter(pk=obj.pk).update(phone_counter=F("phone_counter") + 1)

    return JsonResponse({"status": "success"})

