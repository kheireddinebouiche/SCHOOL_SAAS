from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from t_crm.models import RemiseAppliquer,FicheDeVoeux,FicheVoeuxDouble, UserActionLog
from django.db.models import Q
from institut_app.decorators import *
from datetime import datetime
from django.db.models import Max


def clean_montant(val_str):
    if not val_str:
        return Decimal('0.00')
    val_str = str(val_str).replace(' DA', '').replace('DA', '').strip()
    val_str = val_str.replace('.', '')
    val_str = val_str.replace(',', '.')
    val_str = val_str.replace(' ', '')
    try:
        return Decimal(val_str)
    except:
        return Decimal('0.00')

@login_required(login_url="institut_app:login")
def ApiGetPaiementRequestDetails(request):
    id_client = request.GET.get('id_client')
    id_echeancier = request.GET.get('id_echeancier')
    obj_client = Prospets.objects.get(id= id_client)

    # Récuperer la promo de l etudiant
    obj_promo  = FicheDeVoeux.objects.get(prospect_id = id_client, is_confirmed=True)
    obj_promo.promo.code
    
    # Récupérer les données de l'échéancier depuis la requête
    echeancier_data = request.GET.get('echeancier_data')
    
    if echeancier_data:
        # Parser les données de l'échéancier
        echeancier_list = json.loads(echeancier_data)
        echeancier_list = sorted(echeancier_list, key=lambda x: x['date_echeance'])
        # Calculer les totaux
        total_initial = sum(clean_montant(e['montant']) for e in echeancier_list)
        total_final = sum(clean_montant(e['montant_final']) for e in echeancier_list)
        
        # Préparer les données de réponse
        data = {
            'client': {
                'id': id_client,
            },
            'echeancier': echeancier_list,
            'total_initial': str(total_initial),
            'total_final': str(total_final),
            'reduction': request.GET.get('reduction', '0') + '%' if request.GET.get('has_reduction') else '0%',
            "promo_id" : obj_promo.promo.id
            
        }
        ### Boucle pour enregistrer les paiements
        for i in echeancier_list:
            cleaned_montant = clean_montant(i['montant_final'])
            ApiStorePaiements(obj_client,i['libelle'],i['date_echeance'],cleaned_montant,obj_promo.promo.id,id_echeancier, i.get('entite_id'))  
               
        # Log de génération de l'échéancier
        UserActionLog.objects.create(
            user=request.user,
            action_type='CREATE',
            target_model='DuePaiements',
            target_id=str(id_client),
            details=f"Génération de l'échéancier de paiement ({total_final} DA) pour l'étudiant {obj_client.nom} {obj_client.prenom}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )
             
        return JsonResponse({"status":"success"})
    
    else:
        
        return JsonResponse({'error': 'Aucune donnée d\'échéancier fournie'}, status=400)
    
@login_required(login_url="institut_app:login")
def ApiGetPaiementRequestDetailsDouble(request):
    if request.method == "GET":
        id_client = request.GET.get('id_client')
        id_echeancier = request.GET.get('id_echeancier')
        obj_client = Prospets.objects.get(id= id_client)

        # Récuperer la promo de l etudiant
        obj_promo  = FicheVoeuxDouble.objects.get(prospect_id = id_client, is_confirmed=True)
        obj_promo.promo.code
        
        # Récupérer les données de l'échéancier depuis la requête
        echeancier_data = request.GET.get('echeancier_data')
        
        if echeancier_data:
            # Parser les données de l'échéancier
            echeancier_list = json.loads(echeancier_data)
            
            # Calculer les totaux
            total_initial = sum(clean_montant(e['montant']) for e in echeancier_list)
            total_final = sum(clean_montant(e['montant_final']) for e in echeancier_list)
            
            # Préparer les données de réponse
            data = {
                'client': {
                    'id': id_client,
                },
                'echeancier': echeancier_list,
                'total_initial': str(total_initial),
                'total_final': str(total_final),
                'reduction': request.GET.get('reduction', '0') + '%' if request.GET.get('has_reduction') else '0%',
                "promo_id" : obj_promo.promo.id
                
            }
            ### Boucle pour enregistrer les paiements
            for i in echeancier_list:
                cleaned_montant = clean_montant(i['montant_final'])
                ApiStorePaiementsDouble(obj_client,i['libelle'],i['date_echeance'],cleaned_montant,obj_promo.promo.id,id_echeancier,i['entite'])  
                
            # Log de génération de l'échéancier (Double)
            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='DuePaiements',
                target_id=str(id_client),
                details=f"Génération de l'échéancier de paiement Double Diplomation ({total_final} DA) pour l'étudiant {obj_client.nom} {obj_client.prenom}.",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({"status":"success"})
        
        else:
            
            return JsonResponse({'error': 'Aucune donnée d\'échéancier fournie'}, status=400)

    else:
        return JsonResponse({"status" : "error"})

### Fonction qui stock les echeanciers de paiements
@transaction.atomic
def ApiStorePaiements(client,label,date_echeance,montant,promo,echeancier, entite_id=None):
    try:
        last = DuePaiements.objects.filter(client=client).order_by('-ordre').first()
        ordre = (last.ordre + 1) if last else 1

        DuePaiements.objects.create(
            client=client,
            label=label,
            ordre=ordre,
            montant_due=montant,
            montant_restant=montant,
            ## Faire pivot par rapport aux date (Si la date est pareille) id 1 -> 2
            date_echeance=date_echeance,
            promo_id = promo,
            type = "frais_f",
            ref_echeancier_id = echeancier,
            entite_id = entite_id if entite_id else (EcheancierPaiement.objects.get(id=echeancier).entite.id if echeancier and EcheancierPaiement.objects.get(id=echeancier).entite else None),
        )
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

from django.db.models import Q, F

@transaction.atomic
def ApiStorePaiementsDouble(client,label,date_echeance,montant,promo,echeancier,entite):
    if isinstance(date_echeance, str):
        try:
            date_echeance = datetime.strptime(date_echeance, "%Y-%m-%d").date()
        except ValueError:
            try:
                date_echeance = datetime.strptime(date_echeance, "%d/%m/%Y").date()
            except ValueError:
                pass

    paiement = DuePaiements.objects.create(
        client=client,
        label=label,
        ordre=9999,
        montant_due=montant,
        montant_restant=montant,
        date_echeance=date_echeance,
        promo_id=promo if promo else None,
        type="frais_f",
        ref_echeancier_id=echeancier,
        entite_id=entite if entite else None,
    )
    all_paiements = DuePaiements.objects.filter(client=client).order_by('date_echeance', 'id')
    
    current_ordre = 0
    assigned_ordre = 0
    
    for p in all_paiements:
        current_ordre += 1
        if p.ordre != current_ordre:
            p.ordre = current_ordre
            p.save(update_fields=['ordre'])

        if p.id == paiement.id:
            assigned_ordre = current_ordre

    return JsonResponse({"status": "success","id": paiement.id,"ordre": assigned_ordre})
    
@login_required(login_url="institut_app:login")
def ApiApplyRemiseToPaiement(request):
    if request.method == "POST":
        remiseId = request.POST.get('remiseId')

        remise_obj = RemiseAppliquer.objects.get(id = remiseId)
        remise_obj.is_applicated = True
        remise_obj.save()

        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiStoreClientPaiement(request):
    echeance = request.POST.get('echeance')
    datePaiement = request.POST.get('datePaiement')
    montant = request.POST.get('montant')
    modePaiement = request.POST.get('modePaiement')
    reference = request.POST.get('reference')
    observation = request.POST.get('observation')
    clientId = request.POST.get('clientId')
    id_due_paiement = request.POST.get('id_due_paiement')
    promo = request.POST.get('promo')
    paymentType = request.POST.get('paymentType')

    try:
        due_paiement = DuePaiements.objects.get(id=id_due_paiement)

        if due_paiement.ordre and due_paiement.ordre > 1:
            previous_due = DuePaiements.objects.filter(client_id=clientId,ordre=due_paiement.ordre - 1).first()
            if previous_due and not previous_due.is_done:
                return JsonResponse({"status": "error","message": "Le paiement précédent n'est pas encore effectué."})
    
        paiement = Paiements.objects.create(
            due_paiements = due_paiement,
            prospect = Prospets.objects.get(id = clientId),
            montant_paye = montant,
            date_paiement = datePaiement,
            observation = observation,
            mode_paiement = modePaiement,
            reference_paiement = reference,
            context = "frais_f",
            paiement_label = echeance,
            promo = Promos.objects.get(code = promo) if promo else None,
            payment_type_id = paymentType if paymentType else None,
            entite = due_paiement.entite,
        )

        if(montant == DuePaiements.objects.get(id = id_due_paiement).montant_restant):
            montant_restant = 0
        else:
            montant_restant = Decimal(DuePaiements.objects.get(id = id_due_paiement).montant_restant) - Decimal(montant)

        update_due_paiement= DuePaiements.objects.get(id = id_due_paiement)
        update_due_paiement.is_done = True
        update_due_paiement.montant_restant = montant_restant
        update_due_paiement.save()

        if modePaiement == "che" or modePaiement == "vir":
            OperationsBancaire.objects.create(
                operation_type = "entree",
                paiement = paiement,
                montant = montant,
                reference_bancaire = reference,
        )

        UserActionLog.objects.create(
            user=request.user,
            action_type='CREATE',
            target_model='Paiement',
            target_id=str(paiement.id),
            details=f"Paiement de {montant} DA enregistré pour {paiement.prospect.nom} {paiement.prospect.prenom} (Echéance : {echeance}).",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({"status" : "success"})
    

    except DuePaiements.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Échéance introuvable."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
 
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeletePaiement(request):
    if request.method == "POST":
        num_bon = request.POST.get('num_bon')   
        paiement_obj = Paiements.objects.get(num = num_bon) 
        
        montant_paye = paiement_obj.montant_paye

        paiement_obj.due_paiements.montant_restant = Decimal(paiement_obj.due_paiements.montant_restant) + Decimal(montant_paye)
        paiement_obj.due_paiements.is_done = False
        paiement_obj.due_paiements.save()

        paiement_obj.delete()

        UserActionLog.objects.create(
            user=request.user,
            action_type='DELETE',
            target_model='Paiement',
            target_id=str(num_bon),
            details=f"Suppression du paiement (Bon N°: {num_bon}) d'un montant de {montant_paye} DA pour l'étudiant {paiement_obj.prospect.nom} {paiement_obj.prospect.prenom}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiApplyEcheancierSpecial(request):
    if request.method == "POST":
        id_echeancier_special = request.POST.get('id_echeancier_special')

        if not id_echeancier_special:
            return JsonResponse({"status": "error","message":"Informations manquante"})
        
        obj_echeancier_special = EcheancierSpecial.objects.get(id = id_echeancier_special)
        obj_echeancier_special.is_validate = True
        obj_echeancier_special.save()
        
        # Log de validation d'échéancier spécial
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='EcheancierSpecial',
            target_id=str(id_echeancier_special),
            details=f"Validation de l'échéancier spécial pour l'étudiant {obj_echeancier_special.prospect.nom} {obj_echeancier_special.prospect.prenom}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})


def generate_matricule_interne(promo_code):
    
    today = datetime.now()
    jour_mois = today.strftime("%d%m")  # ex: 1110 pour 11 octobre
    prefix = f"{promo_code}/{jour_mois}"

    # Chercher le dernier matricule généré avec ce préfixe
    last_matricule = Prospets.objects.filter(
        matricule_interne__startswith=prefix
    ).aggregate(max_code=Max('matricule_interne'))['max_code']

    if last_matricule:
        try:
            last_seq = int(last_matricule.split('/')[-1])
        except ValueError:
            last_seq = 0
        new_seq = last_seq + 1
    else:
        new_seq = 1

    return f"{prefix}/{new_seq:04d}"


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiConfirmInscription(request):
    if request.method == "POST":
        id_client = request.POST.get('id_preinscrit')

        promoObj = FicheDeVoeux.objects.get(prospect_id = id_client, is_confirmed=True)
        promo = promoObj.promo.code
        
        matricule = generate_matricule_interne(promo)
      
        client = Prospets.objects.get(id = id_client)
        client.matricule_interne = matricule
        client.statut = 'convertit'
        client.save()

        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='Prospets',
            target_id=str(id_client),
            details=f"Confirmation de l'inscription pour l'étudiant {client.nom} {client.prenom}. Matricule généré: {matricule}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({"status" : "success"})
    else:   
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiConfirmInscriptionDouble(request):
    if request.method == "POST":
        id_client = request.POST.get('id_preinscrit')

        promoObj = FicheVoeuxDouble.objects.get(prospect_id = id_client, is_confirmed=True)
        promo = promoObj.promo.code
        
        matricule = generate_matricule_interne(promo)
      
        client = Prospets.objects.get(id = id_client)
        client.matricule_interne = matricule
        client.statut = 'convertit'
        client.save()

        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='Prospets',
            target_id=str(id_client),
            details=f"Confirmation de l'inscription (Double Diplôme) pour l'étudiant {client.nom} {client.prenom}. Matricule généré: {matricule}.",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({"status" : "success"})
    else:   
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiRequestRefundPaiement(request):
    if request.method == "POST":
        id_client = request.POST.get('client_id')
        reason = request.POST.get('reason')
        Rembourssements.objects.create(
            client = Prospets.objects.get(id = id_client),
            motif_rembourssement = reason,
            etat = 'enc',
            is_done = False
        )
       
        return JsonResponse({"status" : "success"})
    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
def SuivieEcheancier(request):
    return render(request, 'tenant_folder/comptabilite/echeancier/suivie_echeancier.html')