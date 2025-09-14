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
from django.utils.dateformat import format


@login_required(login_url="institut_app:login")
def ListeRemiseApplique(request):
    return render(request,"tenant_folder/crm/remises/liste_remise_appliquer.html")

@login_required(login_url="institut_app:login")
def AipLoadRemise(request):
    remises = Remises.objects.filter(is_enabled= True).values('id','label','taux','has_to_justify')
    return JsonResponse(list(remises), safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadProspectParticulier(request):
    prospect = Prospets.objects.filter(type_prospect = 'particulier',statut='prinscrit' ).values('id','nom','prenom','date_naissance','statut')

    for i in prospect:
        i_obj = Prospets.objects.get(id= i['id'])
        i['statut_label'] = i_obj.get_statut_display()

    return JsonResponse(list(prospect), safe=False)
 

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
                is_approuved=False  # Par défaut, la remise n'est pas approuvée
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
    liste = RemiseAppliquer.objects.all().values('id','remise__label','is_approuved','created_at')
    return JsonResponse(list(liste), safe=False)


@login_required(login_url="institut_app:login")
def ApiLoadRemiseAppliquerDetails(request):
    if request.method == 'GET' and 'id' in request.GET:
        try:
            remise_id = request.GET.get('id')
            remise_appliquer = RemiseAppliquer.objects.select_related('remise').get(id=remise_id)
            
            # Get prospects associated with this discount
            prospects = RemiseAppliquerLine.objects.filter(remise_appliquer=remise_appliquer).select_related('prospect')
            
            # Format the response data
            data = {
                'id': remise_appliquer.id,
                'remise_name': remise_appliquer.remise.label,
                'taux': str(remise_appliquer.remise.taux),
                'is_approuved': remise_appliquer.is_approuved,
                'created_at': remise_appliquer.created_at.strftime('%d/%m/%Y') if remise_appliquer.created_at else '-',
                'fichie_justificatif': remise_appliquer.fichie_justificatif.url if remise_appliquer.fichie_justificatif else None,
                'prospects': [
                    {
                        'id': p.prospect.id,
                        'nom': p.prospect.nom,
                        'prenom': p.prospect.prenom,
                        'date_naissance': p.prospect.date_naissance.strftime('%d/%m/%Y') if p.prospect.date_naissance else '-',
                        'statut': p.prospect.get_statut_display() if p.prospect.statut else '-'
                    }
                    for p in prospects
                ]
            }
            
            return JsonResponse({'status': 'success', 'data': data})
        except RemiseAppliquer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Réduction non trouvée'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Paramètre ID manquant'}, status=400)