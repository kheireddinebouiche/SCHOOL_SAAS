from institut_app.decorators import module_permission_required
from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required

@login_required(login_url='institut_app:login')
@module_permission_required('tre', 'view')
def ListeModelEcheancier(request):
    return render(request,'tenant_folder/comptabilite/tresorerie/gestion_echeancier.html')

@login_required(login_url='institut_app:login')
@module_permission_required('tre', 'view')
def ApiLoadModelEcheancier(request):
    promo_id = request.GET.get('promo_id')
    query = ModelEcheancier.objects.all()
    if promo_id and promo_id != '0':
        query = query.filter(promo_id=promo_id)
        
    liste = query.values('id','promo__label','promo__code','promo__id','promo','promo__begin_year','promo__end_year','nombre_tranche','label','created_at','is_active','is_double_diplomation','has_frais_inscription')
    for i in liste:
        i_obj = ModelEcheancier.objects.get(id = i['id'])
        i['promo_session_label'] = i_obj.promo.get_session_display()
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadPromo(request):
    promo = Promos.objects.all().values('id','label','code','begin_year','end_year','session')
    for i in promo:
        i_obj  = Promos.objects.get(id = i['id'])
        i['session_label'] = i_obj.get_session_display()

    return JsonResponse(list(promo), safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadSpecialites(request):
    if request.method == "GET":
        formation_id = request.GET.get('formation_id')
        query = Specialites.objects.all()
        if formation_id:
            query = query.filter(formation_id=formation_id)
        
        liste = query.values('id','label','prix_double_diplomation','version', 'prix', 'formation_id')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status": "error"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadEcheancierDetails(request):
    try:
        ids_raw = request.GET.get("id")
        if not ids_raw:
             return JsonResponse({"status" : "error", "message" : "Informations manquantes"})
             
        # Pick all IDs to aggregate specialties
        ids = str(ids_raw).split(',')
        echeanciers = EcheancierPaiement.objects.filter(id__in=ids)
        echeancier = echeanciers.first()
        
        if not echeancier:
            return JsonResponse({"status" : "error", "message" : "Échéancier introuvable"})
            
        # Build composite formation label using all specialties
        f_nom = echeancier.formation.nom if echeancier.formation else ""
        specs = []
        for e in echeanciers:
            if e.specialite and e.specialite.label not in specs:
                specs.append(e.specialite.label)
            elif e.formation_double:
                s1 = e.formation_double.specialite1.label if e.formation_double.specialite1 else ""
                s2 = e.formation_double.specialite2.label if e.formation_double.specialite2 else ""
                s_lbl = f"{s1} / {s2}"
                if s_lbl not in specs: specs.append(s_lbl)
                
        if f_nom:
            if specs:
                composite_formation_label = f"{f_nom} ({', '.join(specs)})"
            else:
                composite_formation_label = f_nom
        else:
            composite_formation_label = ", ".join(specs) if specs else ""
        
        # Récupérer les tranches associées au premier (identiques pour le groupe)
        tranches_qs = EcheancierPaiementLine.objects.filter(echeancier=echeancier).order_by('id')
        tranches_list = []
        old_remise_val = float(echeancier.remise or 0)
        old_maj_val = float(echeancier.majoration or 0)
        
        # Priority to stored tarif_formation
        tarif_formation = echeancier.tarif_formation or 0
        
        if not tarif_formation:
            try:
                if echeancier.formation_double:
                    tarif_formation = (echeancier.formation_double.prix_spec1 or 0) + (echeancier.formation_double.prix_spec2 or 0)
                elif echeancier.specialite:
                    tarif_formation = echeancier.specialite.prix_double_diplomation if echeancier.model.is_double_diplomation else echeancier.specialite.prix
                elif echeancier.formation:
                    tarif_formation = echeancier.formation.prix_formation
            except Exception as e:
                print(f"Error calculating tarif: {e}")
                tarif_formation = 0

        # Calculate actual discount amount
        tarif_formation_float = float(tarif_formation)
        remise_val = float(echeancier.remise or 0)
        type_remise = echeancier.type_remise or 'fixe'
        actual_discount = remise_val
        if type_remise == 'pourcentage':
            actual_discount = (tarif_formation_float * remise_val / 100)

        # Calculate actual majoration amount
        majoration_val = float(echeancier.majoration or 0)
        type_majoration = echeancier.type_majoration or 'fixe'
        actual_majoration = majoration_val
        if type_majoration == 'pourcentage':
            actual_majoration = (tarif_formation_float * majoration_val / 100)
            
        total_after_adjustments = max(0, tarif_formation_float - actual_discount + actual_majoration)
            
        for t in tranches_qs:
            t_taux = float(t.taux or 100)
            t_montant = float(t.montant_tranche or 0)
            base_price_net = t_montant * 100.0 / t_taux if t_taux > 0 else 0
            
            inferred_base_price = tarif_formation_float
            if echeancier.formation_double:
                prix1 = float(echeancier.formation_double.prix_spec1 or 0)
                prix2 = float(echeancier.formation_double.prix_spec2 or 0)
                
                disc1 = (prix1 * old_remise_val / 100.0) if type_remise == 'pourcentage' else (old_remise_val / 2.0)
                maj1 = (prix1 * old_maj_val / 100.0) if type_majoration == 'pourcentage' else (old_maj_val / 2.0)
                prix1_net = max(0.0, prix1 - disc1 + maj1)
                
                disc2 = (prix2 * old_remise_val / 100.0) if type_remise == 'pourcentage' else (old_remise_val / 2.0)
                maj2 = (prix2 * old_maj_val / 100.0) if type_majoration == 'pourcentage' else (old_maj_val / 2.0)
                prix2_net = max(0.0, prix2 - disc2 + maj2)
                
                if abs(base_price_net - prix1_net) < abs(base_price_net - prix2_net):
                    inferred_base_price = prix1
                elif abs(base_price_net - prix2_net) < abs(base_price_net - prix1_net):
                    inferred_base_price = prix2
                else:
                    label1 = echeancier.formation_double.specialite1.label if echeancier.formation_double.specialite1 else ""
                    label2 = echeancier.formation_double.specialite2.label if echeancier.formation_double.specialite2 else ""
                    if label1 and label1 in t.value:
                        inferred_base_price = prix1
                    elif label2 and label2 in t.value:
                        inferred_base_price = prix2
                    else:
                        inferred_base_price = prix1 + prix2
            
            tranches_list.append({
                'id': t.id,
                'taux': t.taux,
                'value': t.value,
                'date_echeancier': t.date_echeancier,
                'montant_tranche': t.montant_tranche,
                'entite_id': t.entite_id,
                'base_price': inferred_base_price
            })

        data = {
            'id': echeancier.id,
            'model_label': echeancier.model.label,
            'formation_label': composite_formation_label,
            'formation_nom': f_nom,
            'specialties': specs,
            'is_active': echeancier.is_active,
            'type_model' : "Double Diplomation" if echeancier.model.is_double_diplomation else "Modèle Standard",
            'created_at': echeancier.created_at,
            'tranches': tranches_list,
            'entite' : echeancier.entite.id if echeancier.entite else None,
            'entite_label' : echeancier.entite.designation if echeancier.entite else None,
            'frais_inscription' : str(echeancier.frais_inscription) if echeancier.frais_inscription else "0.00",
            'date_frais_inscription': echeancier.date_frais_inscription.strftime("%Y-%m-%d") if echeancier.date_frais_inscription else "",
            'has_frais_inscription': echeancier.model.has_frais_inscription,
            'has_remise': echeancier.has_remise,
            'type_remise': type_remise,
            'majoration': str(majoration_val),
            'has_majoration': echeancier.has_majoration,
            'type_majoration': type_majoration,
            'tarif_formation': str(tarif_formation),
            'net_total': str(total_after_adjustments),
            'total_after_adjustments': str(total_after_adjustments),
            'prix_spec1': float(echeancier.formation_double.prix_spec1 or 0) if echeancier.formation_double else 0.0,
            'prix_spec2': float(echeancier.formation_double.prix_spec2 or 0) if echeancier.formation_double else 0.0,
            'spec1_label': echeancier.formation_double.specialite1.label if (echeancier.formation_double and echeancier.formation_double.specialite1) else "",
            'spec2_label': echeancier.formation_double.specialite2.label if (echeancier.formation_double and echeancier.formation_double.specialite2) else "",
        }
        
        return JsonResponse({'status': 'success', 'data': data}, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error','message' : str(e)})

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'add')
def ApiSaveEcheancier(request):
    if request.method == 'POST':
        try:
            modele_id = request.POST.get('modele_id')
            formation_id_raw = request.POST.get('formation_id')
            specialite_id_raw = request.POST.get('specialite_id')
            tranches_data = request.POST.get('tranches')
            is_double_diplomation = request.POST.get('is_double_diplomation', 'false') == 'true'
            frais_inscription = request.POST.get('frais_inscription')
            if frais_inscription == '': frais_inscription = None
            date_frais_inscription = request.POST.get('date_frais_inscription')
            if date_frais_inscription == '': date_frais_inscription = None
            remise = request.POST.get('remise', 0)
            type_remise = request.POST.get('type_remise', 'fixe')
            majoration = request.POST.get('majoration', 0)
            type_majoration = request.POST.get('type_majoration', 'fixe')
            entite_id = request.POST.get('entite')

            # Helper to sanitize IDs from potential 'null'/'undefined' strings
            def sanitize_val(val):
                if val == "null" or val == "undefined" or not val or val == "0":
                    return None
                return val

            modele_id = sanitize_val(modele_id)
            formation_id_raw = sanitize_val(formation_id_raw)
            specialite_id_raw = sanitize_val(specialite_id_raw)
            entite_id = sanitize_val(entite_id)

            if not modele_id:
                return JsonResponse({"status": "error", "message": "ID du modèle manquant"})

            # Convertir les données JSON en objet Python
            import json
            tranches = json.loads(tranches_data)
            
            modele = ModelEcheancier.objects.get(id = modele_id)
            libelle = modele.label

            from t_formations.models import Formation, Specialites, DoubleDiplomation

            # Resolve Formation
            formation_obj = None
            if formation_id_raw:
                if str(formation_id_raw).isdigit():
                    formation_obj = Formation.objects.filter(id=formation_id_raw).first()
                if not formation_obj:
                    formation_obj = Formation.objects.filter(code=formation_id_raw).first()

            # Check for multiple specialties (excluding double diplomation mode)
            all_spec_ids = []
            for t in tranches:
                s_id_str = str(t.get('specialite_id') or "")
                if s_id_str:
                    for sid in s_id_str.split(','):
                        if sid.strip() and sid.strip() not in all_spec_ids:
                            all_spec_ids.append(sid.strip())
            
            if len(all_spec_ids) > 1 and not is_double_diplomation:
                # MULTI-SCHEDULE MODE: Create one schedule per specialty
                for s_id in all_spec_ids:
                    spec_obj = None
                    if str(s_id).isdigit():
                        spec_obj = Specialites.objects.filter(id=s_id).first()
                    if not spec_obj:
                        spec_obj = Specialites.objects.filter(code=s_id).first()
                    
                    if not spec_obj: continue

                    # Calculate base price for this specialty
                    current_tarif = spec_obj.prix_double_diplomation if modele.is_double_diplomation else spec_obj.prix
                    
                    label_suffix = f" - {spec_obj.label}"
                    
                    # Check if already exists for this specialty AND model
                    if EcheancierPaiement.objects.filter(formation=formation_obj, specialite=spec_obj, model=modele).exists():
                        continue

                    echeancier = EcheancierPaiement.objects.create(
                        model=modele,
                        formation=formation_obj,
                        specialite=spec_obj,
                        is_active=True,
                        frais_inscription=frais_inscription,
                        date_frais_inscription=date_frais_inscription,
                        remise=remise,
                        type_remise=type_remise,
                        majoration=majoration,
                        type_majoration=type_majoration,
                        has_remise=float(remise or 0) > 0,
                        has_majoration=float(majoration or 0) > 0,
                        tarif_formation=current_tarif,
                        entite_id=entite_id,
                    )
                    
                    # Find tranches that apply to this specialty (either exact match or part of comma-list)
                    for tranche in tranches:
                        t_sid_str = str(tranche.get('specialite_id') or "")
                        if s_id in t_sid_str.split(','):
                            EcheancierPaiementLine.objects.create(
                                echeancier=echeancier,
                                taux=tranche['pourcentage'],
                                value=tranche['libelle'],
                                montant_tranche=tranche['montant_echeance'],
                                date_echeancier=tranche['date'] if tranche['date'] else None,
                                entite_id=tranche.get('entite_id'),
                            )
                return JsonResponse({"status": "success", "message": f"Échéanciers créés pour {len(all_spec_ids)} spécialités"})

            # NORMAL MODE (Single schedule)
            # Resolve Specialty or Double Diplomation
            spec_obj = None
            double_obj = None
            if is_double_diplomation:
                # The frontend might send the DoubleDiplomation ID in either specialite_id or formation_id
                target_double_id = specialite_id_raw or formation_id_raw
                if target_double_id:
                    double_obj = DoubleDiplomation.objects.filter(id=target_double_id).first()
            else:
                if specialite_id_raw:
                    if str(specialite_id_raw).isdigit():
                        spec_obj = Specialites.objects.filter(id=specialite_id_raw).first()
                    if not spec_obj:
                        spec_obj = Specialites.objects.filter(code=specialite_id_raw).first()

            # Check if already exists for this specific model
            if is_double_diplomation:
                has_already = EcheancierPaiement.objects.filter(formation_double=double_obj, model=modele).exists()
            else:
                has_already = EcheancierPaiement.objects.filter(formation=formation_obj, specialite=spec_obj, model=modele).exists()

            if has_already:
                return JsonResponse({"status": "error-head-already"})

            # Calculate base price for normal mode
            tarif_formation = 0
            if is_double_diplomation:
                if double_obj:
                    tarif_formation = (double_obj.prix_spec1 or 0) + (double_obj.prix_spec2 or 0)
            elif spec_obj:
                tarif_formation = spec_obj.prix_double_diplomation if modele.is_double_diplomation else spec_obj.prix
            elif formation_obj:
                # Prioritize specialty price if specialties exist
                first_spec = Specialites.objects.filter(formation=formation_obj).first()
                if first_spec:
                    tarif_formation = first_spec.prix_double_diplomation if modele.is_double_diplomation else first_spec.prix
                else:
                    tarif_formation = formation_obj.prix_formation

            echeancier = EcheancierPaiement.objects.create(
                model=modele,
                formation=formation_obj,
                specialite=spec_obj,
                formation_double=double_obj,
                is_active=True,
                frais_inscription=frais_inscription,
                date_frais_inscription=date_frais_inscription,
                remise=remise,
                type_remise=type_remise,
                majoration=majoration,
                type_majoration=type_majoration,
                has_remise=float(remise or 0) > 0,
                has_majoration=float(majoration or 0) > 0,
                tarif_formation=tarif_formation,
                entite_id=entite_id,
            )

            for tranche in tranches:
                EcheancierPaiementLine.objects.create(
                    echeancier=echeancier,
                    taux=tranche['pourcentage'],
                    value=tranche['libelle'],
                    montant_tranche=tranche['montant_echeance'],
                    date_echeancier=tranche['date'] if tranche['date'] else None,
                    entite_id=tranche.get('entite_id'),
                )

            return JsonResponse({"status": "success", "message": "Échéancier créé avec succès"})
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadFormations(request):
    try:
        formations = Formation.objects.all().values('id', 'nom', 'prix_formation', 'code')
        return JsonResponse(list(formations), safe=False)
    except:
        return JsonResponse({'status': 'error'})

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'add')
def ApiSaveModeleEcheancier(request):
    if request.method == "POST":
        promo = request.POST.get('promo')
        description = request.POST.get('description')
        nbtranche = request.POST.get('nbtranche')
        doubleDiplomation = request.POST.get('doubleDiplomation')

        hasFraisInscription = request.POST.get('hasFraisInscription')

        if doubleDiplomation == "true":
            double = True
        else:
            double = False

        has_frais = hasFraisInscription == "true"

        try:
            promo_obj = Promos.objects.get(id=promo)
            generated_libelle = f"Modèle-{nbtranche}-T-{promo_obj.code or promo_obj.label}"

            ModelEcheancier.objects.create(
                label = generated_libelle,
                promo = promo_obj,
                nombre_tranche = nbtranche,
                description = description,
                is_double_diplomation = double,
                has_frais_inscription = has_frais
            )

            return JsonResponse({"status" : 'success'})
        except Exception as e:
            print(f"Error creating ModelEcheancier: {e}")
            return JsonResponse({"status" : "error"})
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
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
            'has_frais_inscription' : model.has_frais_inscription,
            'created_at': model.created_at.strftime('%d/%m/%Y') if model.created_at else ''
        }

        return JsonResponse({'status':'success','data' : data}, safe=False)
    
    except:
        return JsonResponse({'status':'error'})


@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiUpdateModeleEcheancier(request):
    echeancierId = request.POST.get('id')
    promo = request.POST.get('promo')
    description = request.POST.get('description')
    nbtranche = request.POST.get('nbtranche')
    doubleDiplomation = request.POST.get('doubleDiplomation')
    hasFraisInscription = request.POST.get('hasFraisInscription')

    modelEcheance = ModelEcheancier.objects.get(id = echeancierId)

    try:
        promo_obj = Promos.objects.get(id=promo)
        generated_libelle = f"Modèle-{nbtranche}-T-{promo_obj.code or promo_obj.label}"

        modelEcheance.label = generated_libelle
        modelEcheance.promo = promo_obj
        modelEcheance.description = description
        modelEcheance.nombre_tranche = nbtranche
        modelEcheance.is_double_diplomation = doubleDiplomation == "true"
        modelEcheance.has_frais_inscription = hasFraisInscription == "true"

        modelEcheance.save()

        return JsonResponse({"status": "success"})
    except Exception as e:
        print(f"Error updating ModelEcheancier: {e}")
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'delete')
def ApiDeleteModeleEcheancier(request):
    if request.method == "POST":
        echeancierId = request.POST.get('echeancierId')
        try:
            model = ModelEcheancier.objects.get(id=echeancierId)
            model.delete()
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error"})


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def CreeEcheancier(request):
    return render(request,'tenant_folder/comptabilite/tresorerie/creer-un-echeancier.html')

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'change')
def ListeEcheanciersConfigures(request):
    return render(request,'tenant_folder/comptabilite/tresorerie/echeancier-configurer.html')

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'change')
def ApiLoadEcheanciersConfigures(request):
    try:
        echeanciers = EcheancierPaiement.objects.all().order_by('-id').values(
            'id', 'model__label', 'formation__nom', 'formation__prix_formation', 'specialite__label', 'specialite__prix', 'specialite__prix_double_diplomation', 'is_active', 'is_archived', 'created_at','is_default','formation_double__label','formation_double__prix','formation_double__prix_spec1','formation_double__prix_spec2','model__is_double_diplomation', 'frais_inscription', 'remise', 'type_remise', 'majoration', 'type_majoration', 'tarif_formation',
            'model__promo_id', 'model__promo__label', 'formation_double__specialite1__label', 'formation_double__specialite2__label'
        )
        
        # Use a dictionary to group by (model, formation, and tranches signature)
        grouped_data = {}
        
        for echeancier in echeanciers:
            # Determine base price first for grouping
            prix = echeancier.get('tarif_formation') or 0
            base_label = ""
            
            if not prix:
                if echeancier.get('specialite__label'):
                    if echeancier['model__is_double_diplomation']:
                        prix = echeancier.get('specialite__prix_double_diplomation') or 0
                    else:
                        prix = echeancier.get('specialite__prix') or 0
                elif echeancier.get('formation__nom'):
                    prix = echeancier.get('formation__prix_formation') or 0
                elif echeancier.get('formation_double__label'):
                    prix = (echeancier.get('formation_double__prix_spec1') or 0) + (echeancier.get('formation_double__prix_spec2') or 0)
            
            if echeancier.get('specialite__label'):
                base_label = echeancier['specialite__label']
            elif echeancier.get('formation__nom'):
                base_label = echeancier['formation__nom']
            elif echeancier.get('formation_double__label'):
                spec1 = echeancier.get('formation_double__specialite1__label') or "Spécialité 1"
                spec2 = echeancier.get('formation_double__specialite2__label') or "Spécialité 2"
                base_label = f"{spec1} / {spec2}"
            
            # Create a signature for the tranches
            lines = EcheancierPaiementLine.objects.filter(echeancier_id=echeancier['id']).order_by('id')
            tranches_sig = "|".join([f"{l.value}-{l.taux}-{l.montant_tranche}" for l in lines])
            
            # Key for grouping: Model + Promo + Formation + Signature + Price + Base Tarif
            key = (
                echeancier['model__label'],
                echeancier['model__promo_id'],
                echeancier['formation__nom'] or '',
                str(echeancier['frais_inscription'] or '0.00'),
                str(echeancier['remise'] or '0.00'),
                echeancier['type_remise'],
                str(echeancier['majoration'] or '0.00'),
                echeancier['type_majoration'],
                str(prix), # Include base price in grouping
                tranches_sig
            )
            
            spec_label = f"{base_label}" if base_label else ""
            
            # Compute final price
            prix_float = float(prix)
            remise_val = float(echeancier['remise'] or 0)
            actual_remise = (prix_float * remise_val / 100) if echeancier['type_remise'] == 'pourcentage' else remise_val
            
            majoration_val = float(echeancier['majoration'] or 0)
            actual_majoration = (prix_float * majoration_val / 100) if echeancier['type_majoration'] == 'pourcentage' else majoration_val
            
            tarif_final = max(0, prix_float - actual_remise + actual_majoration)
            
            if key not in grouped_data:
                grouped_data[key] = {
                    'ids': [echeancier['id']],
                    'model_label': echeancier['model__label'],
                    'promo_id': echeancier['model__promo_id'],
                    'promo_label': echeancier['model__promo__label'],
                    'formation_nom': echeancier['formation__nom'] or '',
                    'specialties': [spec_label] if spec_label else [],
                    'is_active': echeancier['is_active'],
                    'is_double': echeancier['model__is_double_diplomation'],
                    'is_archived': echeancier['is_archived'],
                    'created_at': echeancier['created_at'].strftime('%Y-%m-%d') if echeancier['created_at'] else '',
                    'nombre_tranches': lines.count(),
                    'is_default': echeancier['is_default'],
                    'frais_inscription': echeancier['frais_inscription'],
                    'remise': echeancier['remise'],
                    'type_remise': echeancier['type_remise'],
                    'majoration': echeancier['majoration'],
                    'type_majoration': echeancier['type_majoration'],
                    'tarif_formation': prix,
                    'tarif_final': tarif_final,
                    'spec1': echeancier.get('formation_double__specialite1__label'),
                    'spec2': echeancier.get('formation_double__specialite2__label')
                }
            else:
                grouped_data[key]['ids'].append(echeancier['id'])
                if spec_label and spec_label not in grouped_data[key]['specialties']:
                    grouped_data[key]['specialties'].append(spec_label)
                # If any in group is default, mark as default (though usually they should be all or none)
                if echeancier['is_default']:
                    grouped_data[key]['is_default'] = True

        data = []
        for key, group in grouped_data.items():
            f_nom = group['formation_nom']
            # If no formation name (e.g. double diplome), use the first specialty
            if not f_nom and group['specialties']:
                f_nom = group['specialties'][0]
                
            # Filter out the formation name from the list of specialties for the tooltip
            filtered_specs = [s for s in group['specialties'] if s != f_nom]
            
            data.append({
                'id': ",".join(map(str, group['ids'])), # Comma-separated IDs
                'model_label': group['model_label'],
                'promo_id': group['promo_id'],
                'promo_label': group['promo_label'],
                'formation_nom': f_nom,
                'spec1': group.get('spec1'),
                'spec2': group.get('spec2'),
                'specialties_list': ", ".join(filtered_specs) if filtered_specs else "",
                'is_active': group['is_active'],
                'is_double': group['is_double'],
                'is_archived': group['is_archived'],
                'created_at': group['created_at'],
                'nombre_tranches': group['nombre_tranches'],
                'is_default': group['is_default'],
                'frais_inscription': group['frais_inscription'],
                'remise': group['remise'],
                'type_remise': group['type_remise'],
                'majoration': group['majoration'],
                'type_majoration': group['type_majoration'],
                'tarif_formation': group['tarif_formation']
            })
        
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'delete')
def ApiDeleteEcheancier(request):
    if request.method == "POST":
        ids_raw = request.POST.get('echeancierId')
        if not ids_raw:
            return JsonResponse({"status": "error", "message": "ID manquant"})
            
        ids = str(ids_raw).split(',')
        deleted_count = 0
        
        for eid in ids:
            try:
                obj = EcheancierPaiement.objects.filter(id=eid).first()
                if obj and not obj.is_default:
                    obj.delete()
                    deleted_count += 1
            except:
                continue
                
        return JsonResponse({"status": "success", "message": f"{deleted_count} échéancier(s) supprimé(s)"})

    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'delete')
def ApiBulkDeleteEcheanciers(request):
    if request.method == "POST":
        try:
            ids_json = request.POST.get('ids')
            import json
            ids = json.loads(ids_json)
            
            # Filter out default schedules and delete the rest
            deleted_count = 0
            for eid in ids:
                try:
                    obj = EcheancierPaiement.objects.filter(id=eid).first()
                    if obj and not obj.is_default:
                        obj.delete()
                        deleted_count += 1
                except Exception as e:
                    continue
            
            return JsonResponse({"status": "success", "message": f"{deleted_count} échéanciers supprimés avec succès"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})
    
@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadEntiteLegal(request):
    if request.method == "GET":
        liste = Entreprise.objects.all().values('id','designation')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def echeancierAppliquer(request):

    return render(request,'tenant_folder/comptabilite/tresorerie/echeancier-configurer.html')

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'view')
def ApiSetEcheancierDefault(request):
    if request.method == 'POST':
        try:
            ids_raw = request.POST.get('id')
            if not ids_raw:
                return JsonResponse({"status": "error", "message": "ID manquant"})
            
            ids = str(ids_raw).split(',')
            
            # Use the first one to find the formation/promo
            first_obj = EcheancierPaiement.objects.filter(id=ids[0]).first()
            if first_obj:
                # Set all others for this formation/promo to NOT default
                EcheancierPaiement.objects.filter(
                    formation=first_obj.formation, 
                    model__promo=first_obj.model.promo
                ).update(is_default=False)

            # Now set the selected ones to default
            updated_count = EcheancierPaiement.objects.filter(id__in=ids).update(is_default=True)
            
            return JsonResponse({"status": "success", "message": f"{updated_count} échéancier(s) défini(s) par défaut avec succès"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'change')
def ApiToggleEcheancierAvailability(request):
    if request.method == 'POST':
        try:
            ids_raw = request.POST.get('id')
            available = request.POST.get('available') == 'true'
            if not ids_raw:
                return JsonResponse({"status": "error", "message": "ID manquant"})
            
            ids = str(ids_raw).split(',')
            EcheancierPaiement.objects.filter(id__in=ids).update(is_active=available)
            
            msg = "disponible" if available else "indisponible"
            return JsonResponse({"status": "success", "message": f"Échéancier(s) rendu(s) {msg} avec succès"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiUpdateEcheancier(request):
    if request.method == 'POST':
        try:
            def clean_decimal(val):
                if not val: return None
                cleaned = str(val).replace('\xa0', '').replace(' ', '').replace(',', '.')
                return cleaned if cleaned != '' else None
                
            ids_raw = request.POST.get('id')
            if not ids_raw:
                return JsonResponse({"status": "error", "message": "ID manquant"})
            
            ids = str(ids_raw).split(',')
            
            is_active_val = request.POST.get('is_active') == '1'
            entite_id = request.POST.get('entite')
            frais_inscription = clean_decimal(request.POST.get('frais_inscription'))
            date_frais_inscription = request.POST.get('date_frais_inscription')
            if date_frais_inscription == '': date_frais_inscription = None
            entite_id = request.POST.get('entite')
            remise = clean_decimal(request.POST.get('remise'))
            type_remise = request.POST.get('type_remise')
            majoration = clean_decimal(request.POST.get('majoration'))
            type_majoration = request.POST.get('type_majoration')
            tranche_updates_json = request.POST.get('tranche_updates')
            import json
            tranche_updates = json.loads(tranche_updates_json)
            
            for eid in ids:
                echeancier = EcheancierPaiement.objects.filter(id=eid).first()
                if not echeancier:
                    continue
                
                old_remise_val_db = float(echeancier.remise or 0)
                old_maj_val_db = float(echeancier.majoration or 0)
                
                echeancier.is_active = is_active_val
                if entite_id and entite_id != "0":
                    echeancier.entite_id = entite_id
                if frais_inscription is not None:
                    echeancier.frais_inscription = frais_inscription
                elif 'frais_inscription' in request.POST:
                    echeancier.frais_inscription = None
                
                if date_frais_inscription:
                    echeancier.date_frais_inscription = date_frais_inscription
                elif 'date_frais_inscription' in request.POST:
                    echeancier.date_frais_inscription = None

                if remise is not None:
                    echeancier.remise = remise
                    echeancier.has_remise = float(remise or 0) > 0
                elif 'remise' in request.POST:
                    echeancier.remise = None
                    echeancier.has_remise = False
                    
                if type_remise:
                    echeancier.type_remise = type_remise
                    
                if majoration is not None:
                    echeancier.majoration = majoration
                    echeancier.has_majoration = float(majoration or 0) > 0
                elif 'majoration' in request.POST:
                    echeancier.majoration = None
                    echeancier.has_majoration = False
                    
                if type_majoration:
                    echeancier.type_majoration = type_majoration
                echeancier.save()
                
                # Recalculate tranches amounts if needed
                tarif = float(echeancier.tarif_formation or 0)
                remise_val = float(echeancier.remise or 0)
                maj_val = float(echeancier.majoration or 0)
                
                actual_discount = (tarif * remise_val / 100) if echeancier.type_remise == 'pourcentage' else remise_val
                actual_majoration = (tarif * maj_val / 100) if echeancier.type_majoration == 'pourcentage' else maj_val
                net_total = tarif - actual_discount + actual_majoration
                
                # Identify tranches to delete
                update_t_ids = [u.get('id') for u in tranche_updates if u.get('id')]
                EcheancierPaiementLine.objects.filter(echeancier=echeancier).exclude(id__in=update_t_ids).delete()
                
                # Update tranches by matching ID to prevent duplication or mismatch
                for update in tranche_updates:
                    t_id = update.get('id')
                    if t_id:
                        tranche_obj = EcheancierPaiementLine.objects.filter(id=t_id, echeancier=echeancier).first()
                        if not tranche_obj:
                            continue
                        
                        tranche_obj.value = update.get('value')
                        if update.get('date'):
                            tranche_obj.date_echeancier = update.get('date')
                        
                        taux_custom = clean_decimal(update.get('taux'))
                        if taux_custom is not None:
                            try:
                                tranche_obj.taux = float(taux_custom)
                            except ValueError:
                                pass
                        
                        # Recalculate montant_tranche
                        taux = float(tranche_obj.taux or 0)
                        tranche_obj.montant_tranche = (net_total * taux / 100.0)
                        
                        montant_custom = clean_decimal(update.get('montant'))
                        if montant_custom is not None:
                            try:
                                tranche_obj.montant_tranche = float(montant_custom)
                            except ValueError:
                                pass
                        
                        
                        # Update tranche entity
                        t_entite_id = update.get('entite_id')
                        if t_entite_id and t_entite_id != "0":
                            tranche_obj.entite_id = t_entite_id
                        else:
                            tranche_obj.entite = None
                            
                        tranche_obj.save()

            return JsonResponse({"status": "success", "message": f"{len(ids)} échéancier(s) mis à jour avec succès"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
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
@module_permission_required('tre', 'view')
def ApiCheckStateModel(request):
    id_model = request.GET.get('id_model')
    model_obj = ModelEcheancier.objects.get(id = id_model)

    due_paiements = DuePaiements.objects.filter(ref_echeancier__model = model_obj).exists()

    if due_paiements:
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status" :"error"})