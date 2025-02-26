from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
from t_tresorerie.models import *
from t_formations.models import *
from django.db import transaction


def listeVisiteurs(request):
    liste = Visiteurs.objects.all()
    return render(request, 'tenant_folder/crm/liste_visiteurs.html', {'liste': liste})

@transaction.atomic
def nouveauVisiteur(request):
    form = VisiteurForm()
    if request.method == 'POST':
        form = VisiteurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visiteur ajouté avec succès')
            return redirect('t_crm:liste_visiteurs')
    else:
        context = {
            'form' : form,
        }
        return render(request, 'tenant_folder/crm/nouveau_visiteur.html', context)

def ApprouveVisiteurInscription(request,pk):
    visiteur = Visiteurs.objects.get(id= pk)
    
    new_paie_request = ClientPaiementsRequest(
        created_by = request.user,
        client = visiteur,
        amount = visiteur.formation__frais_inscription
    )

    new_paie_request.save()
    visiteur.has_paied = True
    visiteur.save()

def modifierVisiteur(request, id):
    pass

def supprimerVisiteur(request):
    pk = request.POST.get('id')
    visiteur = Visiteurs.objects.get(id = pk)
    visiteur.delete()
    messages.success(request, 'Visiteur supprimé avec succès')
    return JsonResponse({'status': 'success'})

def detailsVisiteur(request, pk):
    obj = Visiteurs.objects.get(id = pk)
    context = {
        'obj' : obj,
        'tenant' : request.tenant
    }
    return render(request,'tenant_folder/crm/details_visiteur.html', context)

def ApiGetSpecialite(request):
    formation_id = request.GET.get('formation_id')
    
    specialites = Specialites.objects.filter(formation = formation_id).values('id','label')
    return JsonResponse(list(specialites), safe=False)

@transaction.atomic
def ConfirmeDemandeInscription(request, pk):
    pass