from django.shortcuts import render
from django.http import JsonResponse
from .models import *




def AttentesPaiements(request):
    
    context = {
       
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/comptabilite/tresorerie/attentes_de_paiement.html', context)

def ApiListeDemandePaiement(request):
    listes = ClientPaiementsRequest.objects.all().values('motif','id','specialite__label','specialite__prix', 'formation__nom','formation__frais_assurance','formation__frais_inscription', 'demandes__visiteur__nom', 'demandes__visiteur__prenom','amount','created_at','etat')
    for liste in listes:
        liste_obj = ClientPaiementsRequest.objects.get(id=liste['id'])
        liste['motif_label'] = liste_obj.get_motif_display()
    return JsonResponse(list(listes), safe=False)

def PageDetailsDemandePaiement(request, pk):
    context = {
        'tenant' : request.tenant,
        'pk' : pk,
    }
    return render(request, "tenant_folder/comptabilite/tresorerie/details_attente_paiement.html", context)

def ApiGetDetailsDemandePaiement(request):
    id= request.GET.get('id_demande')
    obj = ClientPaiementsRequest.objects.get(id = id)
    data = {
        'demandeur_nom' : obj.demandes.visiteur.nom,
        'demandeur_prenom': obj.demandes.visiteur.prenom,
    }
    return JsonResponse(data, safe=False)

def ApiDeleteDemandePaiement(request):
    id_demande = request.GET.get('id_demande')
    obj = ClientPaiementsRequest(id = id_demande)
    obj.delete()

    return JsonResponse({'status' : 'success', "message" : "La suppréssion a été effectuer avec succès"})


def PageConfigPaiementSeuil(request):
    return render(request, 'tenant_folder/comptabilite/tresorerie/config.html', {'tenant' : request.tenant})

def ApiListSeuilPaiement(request):
    liste = SeuilPaiements.objects.all().values('id','specialite','specialite__label','specialite__code','label','valeur','created_at','updated_at')
    
    return JsonResponse(list(liste), safe=False)

def ApiListeSpecialite(request):
    liste = Specialites.objects.all().values('id','label','code')
    return JsonResponse(list(liste), safe=False)

def ApiAddNewSeuil(request):
    label = request.POST.get('label')
    specialite = request.POST.get('specialite')
    valeur = request.POST.get('valeur')
    if label and specialite and valeur:
        new_seuil = SeuilPaiements(
            label = label,
            specialite = Specialites.objects.get(id = specialite),
            valeur = valeur
        )
        new_seuil.save()
        return JsonResponse({'status' : 'success', 'message' : "Les données ont été enregistrer avec succès"})
    else:
        return JsonResponse({'status' : 'error', 'message' : "Veuillez remplir tous les champs"})
    
def ApiDeleteSeuil(request):

    id = request.GET.get('id')
    if id:
        obj = SeuilPaiements.objects.get(id = id)
        obj.delete()
        return JsonResponse({'status' : 'success' , 'message' : "La suppression à été effectuer avec succès"})
    else:
        return JsonResponse({'status' : 'error' , 'message' : "Erreur, l'objet n'a pas été trouvé !"})
    
def ApiGetPaiementLine(request):
    pass

def ApiGetRequestPaiementsLine(request):
    id= request.GET.get('id')

    request = ClientPaiementsRequest.objects.get(id=id)
    lignes = clientPaiementsRequestLine.objects.filter(paiement_request=request)

    data = []
    for ligne in lignes:
        data.append({
            'id': ligne.id,
            'label': ligne.get_motif_paiement_display(),  
            'montant_paye': ligne.montant_paye
        })

    return JsonResponse(data, safe=False)

def ApiListPaiementDone(request):
    id = request.GET.get('id')

    demande_obj = ClientPaiementsRequest.objects.get(id = id)
    listes = Paiements.objects.filter(paiement_line__id = demande_obj.id)

    data = []
    for liste in listes:
        data.append({
            'id' : liste.id,
            'montant_paye' : liste.montant_paye,
            'data_paiement' : liste.data_paiement,
            'observation' : liste.observation,
        })

    return JsonResponse(data, safe=False)