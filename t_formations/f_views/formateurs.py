from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import *
from ..forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django_tenants.utils import get_tenant_model, schema_context
from django.http import JsonResponse
from django.db.models import Q



login_required(login_url="institut_app:login")
def PageFormateurs(request):
    liste = Formateurs.objects.all()
    context = {
        "formateurs" : liste
    }
    return render(request, 'tenant_folder/formateur/liste_des_formateur.html', context)

@login_required(login_url="institut_app:login")
@transaction.atomic
def create_formateur(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        diplome = request.POST.get('diplome')

        Formateurs.objects.create(
            nom = nom,
            prenom = prenom,
            telephone = telephone,
            email = email,
            diplome = diplome,
        )
        messages.success(request,'Les données du formateur ont été sauvegarder avec succès.')
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({"status" : "error","message":"Method non autoriser"})