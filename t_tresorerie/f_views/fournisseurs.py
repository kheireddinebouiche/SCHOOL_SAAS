from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from institut_app.models import Fournisseur  # Import the Fournisseur model from institut_app


@login_required(login_url="institut_app:login")
def PageFournisseur(request):
    return render(request,'tenant_folder/comptabilite/fournisseurs/liste_des_fournisseurs.html')

@login_required(login_url="institut_app:login")
def ApiListeFournisseurs(request):
    liste = Fournisseur.objects.all().values('id', 'designation','telephone','code','email')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def PageNouveauFournisseur(request):
    return render(request,'tenant_folder/comptabilite/fournisseurs/nouveau_fournisseur.html')

@login_required(login_url="institut_app:login")
@transaction.atomic
def enregistrer_fournisseur(request):
    #if request.method == "POST":
    try:
        # Get form data from POST request
        designation = request.POST.get('designation', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        commune = request.POST.get('commune', '').strip()
        wilaya = request.POST.get('wilaya', '').strip()
        pays = request.POST.get('pays', '').strip()
        rc = request.POST.get('rc', '').strip()
        nif = request.POST.get('nif', '').strip()
        art = request.POST.get('art_impot', '').strip()  # Note: in the form it's 'art_impot', but in model it's 'art'
        nis = request.POST.get('nis', '').strip()
        code = request.POST.get('code','').strip()
        telephone = request.POST.get('telephone','').strip()
        email = request.POST.get('email','').strip()
        site_web = request.POST.get('site_web','').strip()

        # Create a new Fournisseur instance
        Fournisseur.objects.create(
            designation=designation,
            adresse=adresse,
            commune=commune,
            wilaya=wilaya,
            pays=pays,
            rc=rc,
            nif=nif,
            art=art,
            nis=nis,
            code = code,
            telephone = telephone,
            email = email,
            site_web = site_web
        )
        
        # Return success response
        return JsonResponse({"status": "success","message": "Le fournisseur a été enregistré avec succès."})
        
    except Exception as e:
        # Handle any errors during creation
        return JsonResponse({"status": "error", "message": f"Erreur lors de l'enregistrement du fournisseur : {str(e)}"}, status=500)
    # else:
    #     return JsonResponse({"status":"error","message":"methode non autoriser"})      

@login_required(login_url="institut_app:login")
def PageDetailsFournisseur(request, pk):
    if not pk:
        return redirect('t_tresorerie:PageFournisseur')
    
    fournisseur = Fournisseur.objects.get(id = pk)
    context = {
        'fournisseur' : fournisseur
    }
    return render(request, 'tenant_folder/comptabilite/fournisseurs/details_fournisseur.html',context)

@login_required(login_url="institut_app:login")
def ApiLoadFournisseur(request):
    if request.method == "GET":
        liste = Fournisseur.objects.all().values('id','designation')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error","message":"méthode non autorisée"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def UpdateFournisseur(request):
    if request.method =="POST":
        id = request.POST.get('id')
        code = request.POST.get('code')
        designation = request.POST.get('designation')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        commune = request.POST.get('commune')
        wilaya = request.POST.get('wilaya')
        pays = request.POST.get('pays')
        rc = request.POST.get('rc')
        nif = request.POST.get('nif')
        art = request.POST.get('art')
        nis = request.POST.get('nis')
        banque = request.POST.get('banque')
        num_compte = request.POST.get('num_compte')
        code_banque = request.POST.get('code_banque')
        observation = request.POST.get('observation')
        site_web = request.POST.get('site_web')

        fournisseur = Fournisseur.objects.get(id = id)
        
        fournisseur.code = code
        fournisseur.designation = designation
        fournisseur.telephone = telephone
        fournisseur.adresse = adresse
        fournisseur.commune = commune
        fournisseur.wilaya = wilaya
        fournisseur.pays = pays
        fournisseur.rc = rc
        fournisseur.nif = nif
        fournisseur.art = art
        fournisseur.nis = nis
        fournisseur.banque = banque
        fournisseur.num_compte = num_compte
        fournisseur.code_banque = code_banque
        fournisseur.observation = observation
        fournisseur.email = email
        fournisseur.site_web = site_web

        fournisseur.save()
        messages.success(request, "Les informations du fournisseur ont été modifiées.")
        return JsonResponse({"status":"success"})

    else:
        return JsonResponse({"status":"error","message":"methode non autoriser"})
