from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from t_crm.models import *
from django.db.models import Count



@login_required(login_url="institut_app:login")
def StudentDetails(request, pk):
    context = {
        'pk' : pk,
    }
    return render(request, 'tenant_folder/student/profile_etudiant.html',context)