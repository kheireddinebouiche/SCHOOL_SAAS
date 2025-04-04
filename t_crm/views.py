from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
from t_tresorerie.models import *
from t_formations.models import *
from django.db import transaction


def listeVisiteurs(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/crm/liste_visiteurs.html',context)

def ApiListeVisiteurs(request):
    liste = Visiteurs.objects.filter().values('id','cin','etat','type_visiteur','nom','prenom','email','telephone','created_at')

    for l in liste:
        l_obj = Visiteurs.objects.get(id=l['id'])
        l['type_visiteur_label'] = l_obj.get_type_visiteur_display()
        l['etat_label'] = l_obj.get_etat_display()

    return JsonResponse(list(liste), safe=False)

@transaction.atomic
def nouveauVisiteur(request):
    form = VisiteurForm()
    demande = DemandeInscriptionForm()
    if request.method == 'POST':
        form = VisiteurForm(request.POST)
        demande = DemandeInscriptionForm(request.POST)
        if form.is_valid() and demande.is_valid():
            visiteur = form.save()

            formation = demande.cleaned_data.get('formation')
            specialite = demande.cleaned_data.get('specialite')
            formule = demande.cleaned_data.get('formule')
            session = demande.cleaned_data.get('session')

            if formation and specialite and formule and session:
                demande = DemandeInscription(
                    visiteur = visiteur,
                    formation = formation, 
                    specialite = specialite,
                    session = session,
                    formule = formule,
                )
                demande.save()

            messages.success(request, 'Visiteur ajouté avec succès')
            return redirect('t_crm:liste_visiteurs')
    else:
        context = {
            'form' : form,
            'demande' : demande,
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
    demande_inscription = DemandeInscription.objects.filter(visiteur = visiteur).count()
    if demande_inscription > 0:
        return JsonResponse({'success': False, 'message': 'Impossible de supprimer le visiteur car il a une demande d\'inscription en cours.'})
    else:
        visiteur.delete()
        return JsonResponse({'success': True, 'message': 'Visiteur supprimé avec succès'})

def detailsVisiteur(request, pk):
    obj = Visiteurs.objects.get(id = pk)
    context = {
        'obj' : obj,
        'tenant' : request.tenant
    }
    return render(request,'tenant_folder/crm/details_visiteur.html', context)

@transaction.atomic
def updateVisiteur(request,pk):
    obj = Visiteurs.objects.get(id = pk)
    form = VisiteurForm(instance=obj)
    if request.method == "POST":
        form = VisiteurForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"Les informations ont été sauvegarder ave succès")
            return redirect("t_crm:details_visiteur", pk)
        
        else:
            messages.error(request, "Une erreur c'est produite lors du traitement du formulaire")
            return redirect('t_crm:updateVisiteur', pk)
        
    else:

        context = {
            'form' : form,
            'tenant' : request.tenant
        }
        return render(request, "tenant_folder/crm/update_visiteur.html",context)

def ApiGetSpecialite(request):
    formation_id = request.GET.get('formation_id')
    
    specialites = Specialites.objects.filter(formation = formation_id).values('id','label')
    return JsonResponse(list(specialites), safe=False)

@transaction.atomic
def ConfirmeDemandeInscription(request, pk):
    visiteur = Visiteurs.objects.get(id = pk)
    
    paiement_request = ClientPaiementsRequest.objects.create(
        client = visiteur,
        formation = visiteur.formation,
        specialite = visiteur.specialite,

        amount = (visiteur.formation.frais_inscription + visiteur.specialite.prix) / int(visiteur.specialite.nb_tranche),

        created_by = request.user,  

    )

    paiement_request.save()
    messages.success(request, 'Demande d\'inscription confirmée avec succès')
    return redirect('t_crm:details_visiteur', pk = pk)

def ApiGETDemandeInscription(request):
    id_visiteur = request.GET.get('id_visiteur')
    demandes = DemandeInscription.objects.filter(visiteur = id_visiteur).values('id','formation','specialite__label','created_at','etat')
    for demande in demandes:
        demande_obj = DemandeInscription.objects.get(id=demande['id'])
        demande['etat_label'] = demande_obj.get_etat_display()
    return JsonResponse(list(demandes), safe=False)
