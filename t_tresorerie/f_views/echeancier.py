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
    liste = ModelEcheancier.objects.all().values('id','promo__label','promo__id','promo','promo__begin_year','promo__end_year','nombre_tranche','label','created_at','is_active','is_double_diplomation')
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
def ApiLoadSpecialites(request):
    if request.method == "GET":
        liste = Specialites.objects.all().values('id','label','prix_double_diplomation','version')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status": "error"})

@login_required(login_url="institut_app:login")
def ApiLoadEcheancierDetails(request):
    id = request.GET.get("id")

    if not id:
        return JsonResponse({"status" : "error", "message" : "Informations manquantes"})
    try:
        echeancier = EcheancierPaiement.objects.get(id=id)
        
        # Récupérer les tranches associées
        tranches = EcheancierPaiementLine.objects.filter(echeancier=echeancier).values(
            'id', 'taux', 'value', 'date_echeancier','montant_tranche'
        )
        
        data = {
            'id': echeancier.id,
            'model_label': echeancier.model.label,
            'formation_label': echeancier.formation.nom if echeancier.formation else echeancier.formation_double.label,
            'is_active': echeancier.is_active,
            'type_model' : echeancier.model.is_double_diplomation if echeancier.model.is_double_diplomation else "Modéle standard",
            'created_at': echeancier.created_at,
            'tranches': list(tranches),
            'entite' : echeancier.entite.id if echeancier.entite else None,
            'entite_label' : echeancier.entite.designation if echeancier.entite else None,
            
        }
        
        return JsonResponse({'status': 'success', 'data': data}, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error','message' : str(e)})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSaveEcheancier(request):
    if request.method == 'POST':
        try:
            modele_id = request.POST.get('modele_id')
            formation_id = request.POST.get('formation_id')
            tranches_data = request.POST.get('tranches')
            is_double_diplomation = request.POST.get('is_double_diplomation', 'false') == 'true'
            frais_inscription = request.POST.get('frais_inscription')

            # Convertir les données JSON en objet Python
            import json
            tranches = json.loads(tranches_data)
            modele = ModelEcheancier.objects.get(id = modele_id)

            # Check based on mode - if double diplomation, check against specialites, otherwise formation
            if is_double_diplomation:
                has_already = EcheancierPaiement.objects.filter(formation_double_id=formation_id,model__promo=modele.promo).exists()
            else:
                # Check against formation as before
                has_already = EcheancierPaiement.objects.filter(formation_id=formation_id,model__promo=modele.promo).exists()

            if has_already:
                return JsonResponse({"status": "error-head-already"})

            # Créer l'échéancier principal
            echeancier = EcheancierPaiement.objects.create(model=ModelEcheancier.objects.get(id=modele_id),is_active=True, frais_inscription=frais_inscription)

            # Set formation or specialites based on mode
            if is_double_diplomation :
                echeancier.formation_double = DoubleDiplomation.objects.get(id = formation_id)
            else:
                echeancier.formation = Formation.objects.get(id=formation_id)

            echeancier.save()

            # Créer les lignes d'échéancier
            for tranche in tranches:
                EcheancierPaiementLine.objects.create(
                    echeancier=echeancier,
                    taux=tranche['pourcentage'],
                    value=tranche['libelle'],
                    montant_tranche=tranche['montant_echeance'],
                    date_echeancier=tranche['date'] if tranche['date'] else None,
                    entite_id = tranche['specialite_id'],
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
    if request.method == "POST":
        libelle = request.POST.get('libelle')
        promo = request.POST.get('promo')
        description = request.POST.get('description')
        nbtranche = request.POST.get('nbtranche')
        doubleDiplomation = request.POST.get('doubleDiplomation')

        if doubleDiplomation == "true":
            double = True
        else:
            double = False


        try:
            ModelEcheancier.objects.create(
                label = libelle,
                promo = Promos.objects.get(id = promo),
                nombre_tranche = nbtranche,
                description = description,
                is_double_diplomation = double
            )

            return JsonResponse({"status" : 'success'})
        except:
            return JsonResponse({"status" : "error"})
    else:
        return JsonResponse({"status":"error"})

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
            'double_diplomation' : model.is_double_diplomation,
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
            'id', 'model__label', 'formation__nom', 'is_active', 'is_archived', 'created_at','is_default','formation_double__label','model__is_double_diplomation'
        )
        
        # Ajouter le nombre de tranches pour chaque échéancier
        data = []
        for echeancier in echeanciers:
            echeancier_obj = EcheancierPaiement.objects.get(id=echeancier['id'])
            nombre_tranches = echeancier_obj.echeancierpaiementline_set.count()
            
            data.append({
                'id': echeancier['id'],
                'model_label': echeancier['model__label'],
                'formation_label': (
                    echeancier.get('formation__nom')
                    or echeancier.get('formation_double__label')
                    or ''
                ),
                'is_active': echeancier['is_active'],
                'is_double' : echeancier['model__is_double_diplomation'],
                'is_archived': echeancier['is_archived'],
                'created_at': echeancier['created_at'].strftime('%Y-%m-%d') if echeancier['created_at'] else '',
                'nombre_tranches': nombre_tranches,
                'is_default' : echeancier['is_default']
            })
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
def ApiDeleteEcheancier(request):
    if request.method == "POST":
        echeancierId = request.POST.get('echeancierId')
        obj = EcheancierPaiement.objects.get(id = echeancierId)
        if obj.is_default:
            return JsonResponse({"status" : "error",'message' : "La suppréssion ne peux pas etre effectuer."})
        
        obj.delete()
        return JsonResponse({"status" : "success"})

    else:
        return JsonResponse({"status" : "error"})
    
@login_required(login_url="institut_app:login")
def ApiLoadEntiteLegal(request):
    if request.method == "GET":
        liste = Entreprise.objects.all().values('id','designation')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
def echeancierAppliquer(request):

    return render(request,'tenant_folder/comptabilite/tresorerie/echeancier-configurer.html')

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSetEcheancierDefault(request):
    if request.method == 'POST':
        try:
            echeancier_id = request.POST.get('id')
            
            # Get the echeancier to set as default
            echeancier_to_set = EcheancierPaiement.objects.get(id=echeancier_id)
            
            # Then, set the selected one as default
            echeancier_to_set.is_default = True
            echeancier_to_set.save()
            
            return JsonResponse({"status": "success", "message": "Échéancier défini comme par défaut avec succès"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateEcheancier(request):
    if request.method == 'POST':
        try:
            echeancier_id = request.POST.get('id')
            is_active = request.POST.get('is_active')
            entite = request.POST.get('entite')
            tranche_updates_data = request.POST.get('tranche_updates')
            
            # Convertir les données JSON en objet Python
            import json
            tranche_updates = json.loads(tranche_updates_data)
            
            # Récupérer l'échéancier existant
            echeancier = EcheancierPaiement.objects.get(id=echeancier_id)
            
            # Mettre à jour seulement le statut
            echeancier.is_active = bool(int(is_active))  # Convertir '1'/'0' en booléen
            echeancier.entite = Entreprise.objects.get(id = entite)
            # Sauvegarder les modifications
            echeancier.save()
            
            # Mettre à jour les dates et libellés des tranches
            for update in tranche_updates:
                tranche_id = update['id']
                new_date = update['date']
                new_value = update['value']
                
                # Récupérer la ligne d'échéancier spécifique
                tranche_line = EcheancierPaiementLine.objects.get(id=tranche_id)
                
                # Mettre à jour la date d'échéance et le libellé
                tranche_line.date_echeancier = new_date if new_date else None
                tranche_line.value = new_value
                tranche_line.save()
            
            return JsonResponse({"status": "success", "message": "Échéancier mis à jour avec succès"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
def ApiCheckEcheancierState(request):
    if request.method == "GET":
        id_echeancier = request.GET.get('id_echeancier')
        try:
            due_paiements = DuePaiements.objects.filter(ref_echeancier_id = id_echeancier).exists()
            if due_paiements:
                return JsonResponse({"status" : "has_due_paiement"})
            else:
                return JsonResponse({"stauts" : "success", "message" : "Ne possede pas de paiement en attente"})
        except Exception as e:
            return JsonResponse({"status" : "error", "message" : str(e)})

    else:
        return JsonResponse({"status" : "error"})
    

@login_required(login_url="institut_app:login")
def ApiCheckStateModel(request):
    id_model = request.GET.get('id_model')
    model_obj = ModelEcheancier.objects.get(id = id_model)

    due_paiements = DuePaiements.objects.filter(ref_echeancier__model = model_obj).exists()

    if due_paiements:
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status" :"error"})