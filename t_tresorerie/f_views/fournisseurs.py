from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from institut_app.models import Fournisseur  # Import the Fournisseur model from institut_app


@login_required(login_url="institut_app:login")
def PageFournisseur(request):
    return render(request,'tenant_folder/comptabilite/fournisseurs/liste_des_fournisseurs.html')

@login_required(login_url="institut_app:login")
def ApiListeFournisseurs(request):
    liste = Fournisseur.objects.all().values('id', 'designation','telephone')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def PageNouveauFournisseur(request):
    return render(request,'tenant_folder/comptabilite/fournisseurs/nouveau_fournisseur.html')

@login_required(login_url="institut_app:login")
@transaction.atomic
def enregistrer_fournisseur(request):
    if request.method == "POST":
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
                nis=nis
            )
            
            # Return success response
            return JsonResponse({"status": "success","message": "Le fournisseur a été enregistré avec succès."})
            
        except Exception as e:
            # Handle any errors during creation
            return JsonResponse({"status": "error", "message": f"Erreur lors de l'enregistrement du fournisseur : {str(e)}"}, status=500)
    else:
        return JsonResponse({"status":"error","message":"methode non autoriser"})      
        
