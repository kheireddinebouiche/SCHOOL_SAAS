from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required

@login_required(login_url='institut_app:login')
def ListeModelEcheancier(request):
    return render(request,'tenant_folder/comptabilite/tresorerie/gestion_echeancier.html')

@login_required(login_url='institut_app:login')
def ApiLoadModelEcheancier(request):
    liste = ModelEcheancier.objects.all().values('id','promo__label','promo__id','promo','promo__begin_year','promo__end_year','nombre_tranche','label','created_at','is_active')
    for i in liste:
        i_obj = ModelEcheancier.objects.get(id = i['id'])
        i['promo_session_label'] = i_obj.promo.get_session_display()
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadPromo(request):
    promo = Promos.objects.all().values('id','label','code','begin_year','end_year','session')
    for i in promo:
        i_obj  = Promos.objects.get(id = i['id'])
        i['session_label'] = i_obj.get_session_display()

    return JsonResponse(list(promo), safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadEcheancierDetails(request):
    id = request.GET.get("id")
    try:
        echeancier = EcheancierPaiement.objects.get(id=id)
        
        # Récupérer les tranches associées
        tranches = EcheancierPaiementLine.objects.filter(echeancier=echeancier).values(
            'id', 'taux', 'value', 'date_echeancier','montant_tranche'
        )
        
        data = {
            'id': echeancier.id,
            'model_label': echeancier.model.label,
            'formation_label': echeancier.formation.nom,
            'is_active': echeancier.is_active,
            'created_at': echeancier.created_at,
            'tranches': list(tranches)
        }
        
        return JsonResponse({'status': 'success', 'data': data}, safe=False)
    except:
        return JsonResponse({'status': 'error'})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSaveEcheancier(request):
    if request.method == 'POST':
        try:
            modele_id = request.POST.get('modele_id')
            formation_id = request.POST.get('formation_id')
            tranches_data = request.POST.get('tranches')
            
            # Convertir les données JSON en objet Python
            import json
            tranches = json.loads(tranches_data)
            
            # Créer l'échéancier principal
            echeancier = EcheancierPaiement.objects.create(
                model=ModelEcheancier.objects.get(id=modele_id),
                formation=Formation.objects.get(id=formation_id),
                is_active=True
            )
            
            # Créer les lignes d'échéancier
            for tranche in tranches:
                EcheancierPaiementLine.objects.create(
                    echeancier=echeancier,
                    taux=tranche['pourcentage'],
                    value=tranche['libelle'],
                    montant_tranche = tranche['montant_echeance'],
                    date_echeancier=tranche['date'] if tranche['date'] else None
                )
            
            return JsonResponse({"status": "success", "message": "Échéancier créé avec succès"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
def ApiLoadFormations(request):
    try:
        formations = Formation.objects.all().values('id', 'nom', 'prix_formation')
        return JsonResponse(list(formations), safe=False)
    except:
        return JsonResponse({'status': 'error'})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSaveModeleEcheancier(request):
    libelle = request.POST.get('libelle')
    promo = request.POST.get('promo')
    description = request.POST.get('description')
    nbtranche = request.POST.get('nbtranche')
    try:
        ModelEcheancier.objects.create(
            label = libelle,
            promo = Promos.objects.get(id = promo),
            nombre_tranche = nbtranche,
            description = description
        )

        return JsonResponse({"status" : 'success'})
    except:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
def ApiLoadModeleEcheancierDetails(request):
    id = request.GET.get("id")
    try:
        model  = ModelEcheancier.objects.get(id = id)
        
        # Récupérer les informations de la promo
        promo_label = ""
        if model.promo:
            promo_label = f"{model.promo.code} / {model.promo.get_session_display()} - {model.promo.begin_year}-{model.promo.end_year}"
        
        data={
            'id' : model.id,
            'label': model.label,
            'promo_label': promo_label,
            'promo_id': model.promo.id if model.promo else None,
            'nombre_tranche': model.nombre_tranche,
            'description': model.description,
            'is_active': model.is_active,
            'created_at': model.created_at.strftime('%d/%m/%Y') if model.created_at else ''
        }

        return JsonResponse({'status':'success','data' : data}, safe=False)
    
    except:
        return JsonResponse({'status':'error'})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateModeleEcheancier(request):
    echeancierId = request.POST.get('id')
    libelle = request.POST.get('libelle')
    promo = request.POST.get('promo')
    description = request.POST.get('description')
    nbtranche = request.POST.get('nbtranche')

    modelEcheance = ModelEcheancier.objects.get(id = echeancierId)

    modelEcheance.label = libelle
    modelEcheance.promo = Promos.objects.get(id = promo)
    modelEcheance.description = description
    modelEcheance.nombre_tranche = nbtranche

    try:
        modelEcheance.save()

        return JsonResponse({"status": "success"})
    except:
        return JsonResponse({"status": "error"})


@login_required(login_url="institut_app:login")
def CreeEcheancier(request):
    return render(request,'tenant_folder/comptabilite/tresorerie/creer-un-echeancier.html')

@login_required(login_url="institut_app:login")
def ListeEcheanciersConfigures(request):
    return render(request,'tenant_folder/comptabilite/tresorerie/echeancier-configurer.html')

@login_required(login_url="institut_app:login")
def ApiLoadEcheanciersConfigures(request):
    try:
        echeanciers = EcheancierPaiement.objects.all().values(
            'id', 'model__label', 'formation__nom', 'is_active', 'is_archived', 'created_at','is_default',
        )
        
        # Ajouter le nombre de tranches pour chaque échéancier
        data = []
        for echeancier in echeanciers:
            echeancier_obj = EcheancierPaiement.objects.get(id=echeancier['id'])
            nombre_tranches = echeancier_obj.echeancierpaiementline_set.count()
            
            data.append({
                'id': echeancier['id'],
                'model_label': echeancier['model__label'],
                'formation_label': echeancier['formation__nom'],
                'is_active': echeancier['is_active'],
                'is_archived': echeancier['is_archived'],
                'created_at': echeancier['created_at'].strftime('%Y-%m-%d') if echeancier['created_at'] else '',
                'nombre_tranches': nombre_tranches,
                'is_default' : echeancier['is_default']
            })
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
def echeancierAppliquer(request):

    return render(request,'tenant_folder/comptabilite/tresorerie/echeancier-configurer.html')