from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from t_crm.models import Prospets


@login_required(login_url="institut_app:login")
def ApiListeProspect(request):
    liste = Prospets.objects.filter(type_prospect="entreprise", context="con", is_client=False).values('id','slug','nom','prenom','etat','entreprise','poste_dans_entreprise','observation','context','created_at','telephone','email')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def ApiCreateProspect(request):
    if request.method == "POST":
        entreprise = request.POST.get('entreprise')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        indicatif = request.POST.get('indicatif')
        canal = request.POST.get('canal')
        observation = request.POST.get('observation')
        type_prospect = request.POST.get('type_prospect', 'entreprise')
        
        adresse = request.POST.get('adresse')
        wilaya = request.POST.get('wilaya')
        code_zip = request.POST.get('code_zip')

        try:
            Prospets.objects.create(
                entreprise=entreprise,
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                indic=indicatif,
                canal=canal,
                observation=observation,
                type_prospect=type_prospect,
                adresse=adresse,
                wilaya=wilaya,
                code_zip=code_zip,
                context='con'
            )
            return JsonResponse({'status': 'success', 'message': 'Prospect créé avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur lors de la création : {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)