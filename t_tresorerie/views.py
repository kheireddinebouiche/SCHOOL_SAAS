from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from t_crm.models import FicheDeVoeux,RemiseAppliquerLine,RemiseAppliquer
from t_remise.models import *
from django.db.models import Sum
from django.db.models import Q


def AttentesPaiements(request):
    
    context = {
       
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/comptabilite/tresorerie/attentes_de_paiement.html', context)

@login_required(login_url="insitut_app:login")
def ApiListeDemandePaiement(request):
    listes = ClientPaiementsRequest.objects.select_related("promo", "specialite", "client").all()
    
    data = []
    for obj in listes:
        data.append({
            "id": obj.id,
            "motif": obj.motif,
            "motif_label": obj.get_motif_display(),
            "promo": obj.promo.id if obj.promo else None,
            "promo_session": obj.promo.session if obj.promo else None,
            "promo_begin" : obj.promo.begin_year,
            "promo_end" : obj.promo.end_year,
            "specialite": obj.specialite.id if obj.specialite else None,
            "amount" : obj.specialite.formation.prix_formation,
            "nom": obj.client.nom if obj.client else None,
            "prenom": obj.client.prenom if obj.client else None,
            "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "etat": obj.etat,
            "etat_label": obj.get_etat_display() if hasattr(obj, "get_etat_display") else None,
        })
    
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
def PageDetailsDemandePaiement(request, pk):
    context = {
        'tenant' : request.tenant,
        'pk' : pk,
    }
    return render(request, "tenant_folder/comptabilite/tresorerie/details_attente_paiement.html", context)

@login_required(login_url="institut_app:login")
def ApiLoadRefundData(request):
    liste = Rembourssements.objects.all().values('client__nom', 'client__prenom', 'client__id', 'motif_rembourssement', 'etat','created_at', 'id').order_by('-created_at')
    for i in liste:
        i_obj = Rembourssements.objects.get(id = i['id'])
        i['etat_label'] = i_obj.get_etat_display()
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadRefundDetails(request):
    if request.method == "GET":
        id = request.GET.get('id')
        obj = Rembourssements.objects.get(id = id)
        paiement_lines = Paiements.objects.filter(prospect = obj.client, context='frais_f').aggregate(total=Sum('montant_paye'))['total'] or 0

        data= {
            'client_id': obj.client.id,
            'client_nom' : obj.client.nom,
            'client_prenom' : obj.client.prenom,
            'motif_rembourssement' : obj.motif_rembourssement,
            'date_demande' : obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'etat' : obj.get_etat_display(),
            'paiement_total' : paiement_lines,
        }
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'status' : 'error', 'message' : "Méthode non autorisée"}, status=405)
        
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAccepteRembourssement(request):
    montantRembourser = request.GET.get('montantRembourser')
    dateRemboursement = request.GET.get('dateRemboursement')
    modePaiement = request.GET.get('modePaiement')
    client = request.GET.get('client')

    data= {
        'montantRembourser' : montantRembourser,
        'dateRemboursement' : dateRemboursement,
        'modePaiement' : modePaiement,
        'client' : client,
    }

    return JsonResponse({'status' : 'success', 'data' : data})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiRejectRembourssement(request):
    pass

########################################## Fonction qui permet d'afficher tous les détails du demandeur de paiement ###############################
@login_required(login_url="institut_app:login")
def ApiGetDetailsDemandePaiement(request):
    id= request.GET.get('id_demande')
    obj = ClientPaiementsRequest.objects.get(id = id)
    voeux = FicheDeVoeux.objects.filter(prospect=obj.client, is_confirmed=True).select_related("specialite").first()

    special_echeancier_data = []
    has_special_echeancier = False
    echeancier_state_approuvel = False
    due_paiement_data = []
    paiements_done_data = []
    has_due_paiement = False
    has_paiement = False

    due_paiement = DuePaiements.objects.filter(client=obj.client).filter(Q(is_done=False) | Q(montant_restant__gt=0))

    if due_paiement.count() > 0:
        has_due_paiement = True
        total_initial = DuePaiements.objects.filter(client = obj.client).aggregate(total=Sum('montant_due'))['total'] or 0
        for i in due_paiement:
            due_paiement_data.append({
                'id_due_paiement' : i.id,
                'montant_due'  : i.montant_due,
                'montant_restant' : i.montant_restant,
                'label' : i.label,
                'date_echeance' : i.date_echeance,
            })
    else:
        has_due_paiement = False
        due_paiement_data = []

    done_paiements = Paiements.objects.filter(prospect = obj.client)
    if done_paiements.count()>0:
        has_paiement = True
        total_paiement = done_paiements.aggregate(total=Sum('montant_paye'))['total'] or 0
        for i in done_paiements:
            paiements_done_data.append({
                'montant_paye' : i.montant_paye,
                'date_paiement' : i.date_paiement,
                'label_paiements' : i.due_paiements.label,
                'num' : i.num,
                'mode_paiement' : i.get_mode_paiement_display(),
                'reference_paiement' : i.reference_paiement,
            })

    else:
        paiements_done_data = []

    obj_echeacncier_speial = EcheancierSpecial.objects.filter(prospect = obj.client).last()
    if obj_echeacncier_speial:
        line_echeancier_special = EcheancierPaiementSpecialLine.objects.filter(echeancier = obj_echeacncier_speial)
        echeancier_state_approuvel = obj_echeacncier_speial.is_approuved
        has_special_echeancier = True

        special_echeancier_data = []
        for i in line_echeancier_special:
            special_echeancier_data.append({
                'id_echeancier_special' : i.id,
                'taux' : i.taux,
                'value' : i.value,
                'date_echeancier' : i.date_echeancier,
                'montant_tranche' : i.montant_tranche,
            })


    echeancier = EcheancierPaiement.objects.get(formation = voeux.specialite.formation, is_default=True)
    liste_echeancier = EcheancierPaiementLine.objects.filter(echeancier = echeancier)
    
    remiseObj = RemiseAppliquerLine.objects.filter(prospect = obj.client).last()

    if remiseObj and remiseObj.remise_appliquer:
        
        remise_appliquer = remiseObj.remise_appliquer.remise.taux
        is_approuved_remise = remiseObj.remise_appliquer.is_approuved
        reduction_type = remiseObj.remise_appliquer.remise.label
        id_reduction = remiseObj.remise_appliquer.id

        remiseDatas = {
            'valeur' : remise_appliquer,
            'remise_approuver' : is_approuved_remise,
            'type_remise' : reduction_type,
            'id_applied_reduction' : id_reduction,
        }

    else:
        remiseDatas = None

    echeancier_data=[]
    for i in liste_echeancier:
        echeancier_data.append({
            'id': i.id,
            'taux' : i.taux,
            'value' : i.value,
            'montant_tranche' : i.montant_tranche,
            'date_echeancier' : i.date_echeancier,
        })

    ## Changement de d'echeancier -- a remplacer une fois valider par l'utilisateur
    if obj_echeacncier_speial and obj_echeacncier_speial.is_validate:
        echeancier_data = special_echeancier_data
    
    user_data = {
        "demandeur_nom": obj.client.nom,
        "demandeur_prenom": obj.client.prenom,
        "statut_demandeur": obj.client.statut,
        "client_id" : obj.client.id,
        "motif": obj.get_motif_display(),
        "created_at": obj.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "client_id": obj.client.id,  # Add client ID to the response
    }

    voeux_data = {
        'specialite_id' : voeux.specialite.id,
        'specialite_label' : voeux.specialite.label,
        'promo' : voeux.promo.code,
        'prix_formation' : voeux.specialite.formation.prix_formation,
        'frais_inscription' : voeux.specialite.formation.frais_inscription,
    }

    total_solde = total_initial - total_paiement if has_due_paiement and has_paiement else 0

    data = {
        'user_data' : user_data,
        'voeux' : voeux_data,
        'echeancier' : list(echeancier_data),
        'remise' : remiseDatas,
        'has_special_echeancier' : has_special_echeancier,
        'id_echeancier_special' : obj_echeacncier_speial.id if obj_echeacncier_speial else None,
        'special_echeancier_line' : list(special_echeancier_data),
        'echeancier_special_state_approuvel' : echeancier_state_approuvel,
        "has_due_paiement" : has_due_paiement,
        "due_paiement_data" : due_paiement_data,
        "has_paiement" : has_paiement,
        "paiements_done_data" : paiements_done_data,
        "total_paiement" : total_paiement if has_paiement else 0,
        "total_initial" : total_initial if has_due_paiement else 0,
        "total_solde" : total_solde ,
    }

    return JsonResponse(data, safe=False)
########################################## Fonction qui permet d'afficher tous les détails du demandeur de paiement ###############################



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