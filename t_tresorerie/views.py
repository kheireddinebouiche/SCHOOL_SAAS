from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required

def AttentesPaiements(request):
    
    context = {
       
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/comptabilite/tresorerie/attentes_de_paiement.html', context)

def ApiListeDemandePaiement(request):
    listes = ClientPaiementsRequest.objects.all().values('motif','id','specialite__label','specialite__prix', 'formation__nom','formation__frais_assurance','formation__frais_inscription', 'client__nom', 'client__prenom','amount','created_at','etat')
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
        'demandeur_nom' : obj.client.nom,
        'demandeur_prenom': obj.client.prenom,
        'motif' : obj.get_motif_display(),
        'created_at' : obj.created_at,
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


from django.db.models import Q

def ApiGetRequestPaiementsLine(request):
    id= request.GET.get('id')

    request = ClientPaiementsRequest.objects.get(id=id)
    lignes = clientPaiementsRequestLine.objects.filter(paiement_request=request).filter(Q(etat="auc") | Q(etat="part"))  
    

    data = []
    for ligne in lignes:
        data.append({
            'id': ligne.id,
            'label': ligne.get_motif_paiement_display(),  
            'montant_paye': ligne.montant_paye,
            'montant_restant': ligne.montant_restant,
            'etat' : ligne.etat,
        })

    return JsonResponse(data, safe=False)

def ApiListPaiementDone(request):
    id = request.GET.get('id')

    demande_obj = ClientPaiementsRequest.objects.get(id = id)
    listes = Paiements.objects.filter(paiement_line__paiement_request__id = demande_obj.id)

    data = []
    for liste in listes:
        data.append({
            'id' : liste.id,
            'label' : liste.paiement_line.get_motif_paiement_display(),
            'etat_label' : liste.get_etat_display(),
            'etat' : liste.etat,
            'montant_paye' : liste.montant_paye,
            'date_paiement' : liste.date_paiement,
            'observation' : liste.observation,
        })

    return JsonResponse(data, safe=False)

@transaction.atomic
def ApiStorePaiement(request):

    due_paiements = request.POST.get('due_paiements')
    date_paiement = request.POST.get('date_paiement')
    received_amount = request.POST.get('received_amount')
    observation = request.POST.get('observation')
    mode_paiement = request.POST.get('mode_paiement')
    paiement_ref = request.POST.get('paiement_ref')
    
    if not due_paiements or not date_paiement or not received_amount or not mode_paiement:
        return JsonResponse({'status' : 'error', 'message' : "Veuillez remplir tous les champs"})
    else:


        paiement_line_obj = clientPaiementsRequestLine.objects.get(id = due_paiements)

        if paiement_line_obj.montant_restant >= Decimal(received_amount):

            if paiement_line_obj.montant_paye == Decimal(received_amount):
                paiement_line_obj.etat= "ter"
                paiement_line_obj.montant_restant = 0
            else:
                paiement_line_obj.etat= "part"
                paiement_line_obj.montant_restant = paiement_line_obj.montant_restant - Decimal(received_amount)
            
            if paiement_line_obj.montant_restant == 0:
                paiement_line_obj.etat = "ter"

            paiement_line_obj.save()

            new_paiement = Paiements(
                paiement_line = paiement_line_obj,
                montant_paye = received_amount,
                date_paiement = date_paiement,
                observation = observation,
                mode_paiement = mode_paiement,
                reference_paiement = paiement_ref,
            )

            new_paiement.save()

            if paiement_line_obj.montant_restant == 0:
                paiement_line_obj.etat = "ter"


            return JsonResponse({'status' : 'success', 'message' : 'Le paiement à été enregistrer avec succès'})
        
        elif paiement_line_obj.montant_restant < Decimal(received_amount):

            return JsonResponse({'status' : 'error', 'message' : 'Le montant payé ne peut pas être supérieur au montant restant à payer'})
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Le montant payé ne peut pas être supérieur au montant restant à payer'})

def ApiDetailsReceivedPaiement(request):
    id = request.GET.get('id')

    paiement_obj = Paiements.objects.get(id = id)

    data = {
        'montant_paye' : paiement_obj.montant_paye,
        'date_paiement' : paiement_obj.date_paiement,
        'observation' :  paiement_obj.observation,
        'mode_paiement' : paiement_obj.mode_paiement,
        'reference_paiement' : paiement_obj.reference_paiement,
    }

    return JsonResponse(data, safe=False)

def ApiDeletePaiement(request):
    if request.user.has_perm('t_tresorerie.delete_paiements'):
        id= request.GET.get('id')
        if id:
            obj = Paiements.objects.get(id = id)

            obj.paiement_line.montant_restant = obj.paiement_line.montant_restant + Decimal(obj.montant_paye)

            if obj.paiement_line.montant_paye == obj.paiement_line.montant_paye:
                obj.paiement_line.etat = "auc"
            else:
                obj.paiement_line.etat = "part"

            obj.paiement_line.save()
            obj.delete()
            return JsonResponse({'status' : 'success', 'message' : "La suppression à été effectuer avec succès"})
        else:
            return JsonResponse({'status' : 'error', 'message' : "Erreur, l'objet n'a pas été trouvé !"})
    else:
        return JsonResponse({'status' : 'error', 'message' : "Vous n'avez pas le droit d'effectuer cette action"})
    
@login_required(login_url='institut_app:login')
def PageRemboursement(request):
    return render(request, 'tenant_folder/comptabilite/tresorerie/remboursement.html',{'tenant' : request.tenant})

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiSetRembourssement(request):
    id = request.GET.get('id')
    paiement = Paiements.objects.get(id = id)

    paiement.etat = "dmr"
    paiement.save()

    return JsonResponse({'status' : 'success', 'message' : "La demande de remboursement à été enregistrer avec succès"})