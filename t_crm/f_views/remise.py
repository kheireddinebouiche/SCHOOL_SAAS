from django.shortcuts import render,redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.contrib import messages
from t_formations.models import *
from django.db import transaction
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from functools import wraps
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from t_tresorerie.models import DuePaiements, Paiements
from django.utils.dateformat import format
from institut_app.decorators import module_permission_required


@login_required(login_url="institut_app:login")
def ListeRemiseApplique(request):
    return render(request,"tenant_folder/crm/remises/liste_remise_appliquer.html")

@login_required(login_url="institut_app:login")
def AipLoadRemise(request):
    remises = Remises.objects.filter(is_enabled= True).values('id','label','taux','has_to_justify', 'is_value', 'montant')
    return JsonResponse(list(remises), safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadProspectParticulier(request):
    # Filter for 'particulier' prospects in 'instance de paiement' status
    # exclude those who explicitly have a remaining debt in DuePaiements
    prospect = Prospets.objects.filter(
        type_prospect='particulier', 
        statut='instance'
    ).exclude(
        id__in=DuePaiements.objects.filter(montant_restant__gt=0).values_list('client_id', flat=True)
    ).exclude(
        context='con'
    ).values('slug','id','nom','prenom','date_naissance','statut','nin','created_at')

    for i in prospect:
        i_obj = Prospets.objects.get(id= i['id'])
        i['statut_label'] = i_obj.get_statut_display()

    return JsonResponse(list(prospect), safe=False)
 

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiStoreSingleReduction(request):
    if request.method == 'POST':
        try:
            type_remise_id = request.POST.get('type_remise')
            fichier_justificatif = request.FILES.get('fichier_justificatif')
            prospect_id = request.POST.get('prospect_id')
            
            try:
                remise = Remises.objects.get(id=type_remise_id, is_enabled=True)
            except Remises.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Type de remise invalide'}, status=400)
            
            if remise.has_to_justify and not fichier_justificatif:
                return JsonResponse({'status': 'error', 'message': 'Un fichier justificatif est requis pour cette réduction'}, status=400)
            
            if not prospect_id:
                return JsonResponse({'status': 'error', 'message': 'Aucun prospect spécifié'}, status=400)
                
            try:
                prospect = Prospets.objects.get(id=prospect_id)
            except Prospets.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Prospect introuvable'}, status=400)
            
            # Créer l'enregistrement de remise appliquée
            remise_appliquer = RemiseAppliquer.objects.create(
                remise=remise,
                fichie_justificatif=fichier_justificatif if remise.has_to_justify else None,
                is_approuved=False,
                is_applicated=False,
            )
            
            RemiseAppliquerLine.objects.create(
                remise_appliquer=remise_appliquer,
                prospect=prospect
            )
            
            return JsonResponse({'status': 'success', 'message': 'Réduction ajoutée avec succès. Elle est en attente de validation.'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiStoreApplicedReduction(request):
    if request.method == 'POST':
        try:
            # Récupérer les données du formulaire
            type_remise_id = request.POST.get('type_remise')
            fichier_justificatif = request.FILES.get('fichier_justificatif')
            
            # Vérifier si le type de remise existe
            try:
                remise = Remises.objects.get(id=type_remise_id, is_enabled=True)
            except Remises.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Type de remise invalide'}, status=400)
            
            # Vérifier si un justificatif est requis
            if remise.has_to_justify and not fichier_justificatif:
                return JsonResponse({'status': 'error', 'message': 'Un fichier justificatif est requis pour cette réduction'}, status=400)
            
            # Récupérer les prospects sélectionnés
            prospects_data = []
            index = 0
            while f"prospects[{index}][id]" in request.POST:
                prospect_info = {
                    'id': request.POST.get(f"prospects[{index}][id]"),
                }
                prospects_data.append(prospect_info)
                index += 1
            
            if not prospects_data:
                return JsonResponse({'status': 'error', 'message': 'Aucun prospect sélectionné'}, status=400)
            
            # Créer l'enregistrement de remise appliquée
            remise_appliquer = RemiseAppliquer.objects.create(
                remise=remise,
                fichie_justificatif=fichier_justificatif if remise.has_to_justify else None,
                is_approuved=False,  # Par défaut, la remise n'est pas approuvée
                is_applicated=False,
            )
            
            # Créer les lignes de remise appliquée pour chaque prospect
            applied_lines = []
            for prospect_data in prospects_data:
                try:
                    prospect = Prospets.objects.get(id=prospect_data['id'])
                    applied_line = RemiseAppliquerLine.objects.create(
                        remise_appliquer=remise_appliquer,
                        prospect=prospect
                    )
                    applied_lines.append(applied_line)
                except Prospets.DoesNotExist:
                    # Si un prospect n'existe pas, on continue avec les autres
                    continue
            
            if not applied_lines:
                # Si aucune ligne n'a pu être créée, supprimer l'enregistrement parent
                remise_appliquer.delete()
                return JsonResponse({'status': 'error', 'message': 'Aucune réduction n\'a pu être appliquée'}, status=400)
            
            return JsonResponse({
                'status': 'success',
                'message': f'Réduction appliquée avec succès à {len(applied_lines)} prospect(s)',
                'data': {
                    'applied_count': len(applied_lines)
                }
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error','message': f'Erreur lors de l\'application de la réduction: {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error','message': 'Méthode non autorisée'}, status=405)


@login_required(login_url="institut_app:login")
def ApiloadRemiseAppliquer(request):
    remises = RemiseAppliquer.objects.all().values('id','remise__label','remise__is_value','remise__montant','remise__taux','is_approuved','is_applicated','created_at')
    data = []
    for remise in remises:
        prospects = list(
            RemiseAppliquerLine.objects.filter(remise_appliquer_id=remise['id']).values('prospect__id','prospect__nom','prospect__prenom'))

        data.append({
            'id': remise['id'],
            'label': remise['remise__label'],
            'remise__is_value': remise['remise__is_value'],
            'remise__montant': remise['remise__montant'],
            'remise__taux': remise['remise__taux'],
            'is_approuved': remise['is_approuved'],
            'is_applicated': remise['is_applicated'],
            'created_at': remise['created_at'].strftime("%Y-%m-%d %H:%M:%S"),
            'prospects': prospects
        })

    return JsonResponse({'liste': data})



@login_required(login_url="institut_app:login")
def ApiLoadRemiseAppliquerDetails(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            remise_id = request.GET.get('id')
            remise_appliquer = RemiseAppliquer.objects.select_related('remise').get(id=remise_id)
            
            # Get prospects associated with this discount
            prospects = RemiseAppliquerLine.objects.filter(remise_appliquer=remise_appliquer).select_related('prospect')
            
            prospects_list = []
            for p in prospects:
                prospect = p.prospect
                formation_label = "-"
                specialite_label = "-"
                promo_label = "-"
                
                if prospect.is_double:
                    # Double diplomation
                    fdv_double = FicheVoeuxDouble.objects.filter(prospect=prospect).select_related('specialite', 'promo').first()
                    if fdv_double:
                        specialite_label = fdv_double.specialite.label if fdv_double.specialite else "-"
                        promo_label = fdv_double.promo.label if fdv_double.promo else "-"
                        formation_label = "Double diplômation"
                else:
                    # Standard fiche de voeux
                    fdv = FicheDeVoeux.objects.filter(prospect=prospect).select_related('specialite__formation', 'promo').first()
                    if fdv:
                        specialite_label = fdv.specialite.label if fdv.specialite else "-"
                        promo_label = fdv.promo.label if fdv.promo else "-"
                        formation_label = fdv.specialite.formation.nom if (fdv.specialite and fdv.specialite.formation) else "-"
                
                prospects_list.append({
                    'id': prospect.id,
                    'nom': prospect.nom,
                    'prenom': prospect.prenom,
                    'date_naissance': prospect.date_naissance.strftime('%d/%m/%Y') if prospect.date_naissance else '-',
                    'statut': prospect.get_statut_display() if prospect.statut else '-',
                    'formation': formation_label,
                    'specialite': specialite_label,
                    'promo': promo_label,
                })
            
            # Format the response data
            data = {
                'id': remise_appliquer.id,
                'remise_name': remise_appliquer.remise.label,
                'taux': str(remise_appliquer.remise.montant) if remise_appliquer.remise.is_value else str(remise_appliquer.remise.taux),
                'is_value': remise_appliquer.remise.is_value,
                'is_approuved': remise_appliquer.is_approuved,
                'created_at': remise_appliquer.created_at.strftime('%d/%m/%Y') if remise_appliquer.created_at else '-',
                'fichie_justificatif': remise_appliquer.fichie_justificatif.url if remise_appliquer.fichie_justificatif else None,
                'prospects': prospects_list
            }
            return JsonResponse({'status': 'success', 'data': data})
        
        except RemiseAppliquer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Réduction non trouvée'}, status=404)
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Paramètre ID manquant'}, status=400)

@login_required(login_url="institut_app:login")
def ApiGetReductionDetails(request):
    if request.method =="GET":
        id_reduction = request.GET.get('id_reduction')

        object = Remises.objects.get(id = id_reduction)

        data = {
            'label' : object.label,
            'description' : object.description,
            'taux' : object.montant if object.is_value else object.taux,
            'is_value' : object.is_value,
            'has_to_justify' : object.has_to_justify,
            'created_at': object.created_at.strftime("%Y-%m-%d"),
        }

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status" : "error", "message" : "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiActivateRemiseAppliquer(request):
    if request.method == "POST":
        discountId = request.POST.get('id')

        remise_obj = RemiseAppliquer.objects.get(id = discountId)
        if remise_obj:
            remise_obj.is_approuved = True
            remise_obj.save()
            return JsonResponse({"status" : "success" , "message" : "La remise a été activée avec succès"})
        else:
            return JsonResponse({"status" : "error" , "message" : "La remise n'existe pas"})
            
    else:
        return JsonResponse({"status" : "error", "message" : "Methode non autoriser"})


@login_required(login_url="institut_app:login")
@module_permission_required('crm', 'delete')
@transaction.atomic
def ApiDeleteRemiseAppliquer(request):
    if request.method == "POST":
        discountId = request.POST.get('id')
        try:
            remise_obj = RemiseAppliquer.objects.get(id=discountId)
            
            # Vérifier si l'un des prospects liés a déjà des paiements enregistrés
            prospect_ids = RemiseAppliquerLine.objects.filter(remise_appliquer=remise_obj).values_list('prospect_id', flat=True)
            if Paiements.objects.filter(prospect_id__in=prospect_ids).exists():
                return JsonResponse({"status": "error", "message": "Impossible de supprimer cette réduction car des paiements ont déjà été enregistrés pour le(s) prospect(s) concerné(s)."})
            
            remise_obj.delete()
            return JsonResponse({"status": "success", "message": "La réduction a été supprimée avec succès."})
        except RemiseAppliquer.DoesNotExist:
            return JsonResponse({"status": "error", "message": "La réduction n'existe pas."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée."}, status=405)