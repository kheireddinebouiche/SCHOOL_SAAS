from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django_tenants.utils import get_tenant_model, schema_context
from django.http import JsonResponse
from django.db.models import Q

TenantModel = get_tenant_model()

def listModules(request):
    modules = Modules.objects.all()
    return render(request, 't_formations/modules.html', {'modules': modules})

def listSpecialites(request):
    specialites = Specialites.objects.all()
    context = {
        'liste' : specialites,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/formations/liste_des_specialites.html', context)

def listFormations(request):
    formations = Formation.objects.all()
    context = {
        'liste': formations,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/formations/liste_des_formations.html', context)

def listFraisInscription(request):
    frais = FraisInscription.objects.all()
    return render(request, 't_formations/frais.html', {'frais': frais})

def ListeDesInstituts(request):
    liste = Institut.objects.exclude(Q(schema_name='public') | Q(tenant_type='master'))
    context = {
        'liste' : liste,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/formations/liste_des_instituts.html', context)

@transaction.atomic
def addFormation(request):
    form = NewFormationFormMaster(current_tenant = request.tenant)
    if request.method == 'POST':
        form = NewFormationFormMaster(request.POST, current_tenant =request.tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation ajoutée avec succès')
            return redirect('t_formations:listFormations')
        else:
            messages.error(request, 'Une erreur s\'est produite lors du traitement de la requête')
            return redirect('t_formations:addFormation')

    context = {
        'form' : form,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/formations/nouvelle_formations.html', context)

def ApiCheckIfFormationCompleted(request):
    code = request.GET.get('code_formation')
    if not code:
        return JsonResponse({'error': 'Missing code_formation'}, status=400)

    formation = Formation.objects.filter(code=code).first()
    if not formation:
        return JsonResponse({'error': 'Formation not found'}, status=404)

    specialites = Specialites.objects.filter(formation=formation)

    if not specialites.exists():
        return JsonResponse({'completed': False, 'reason': 'Aucune spécailité trouvée <br> Veuillez ajouter au moins une spécialité.'})

    # Vérifier que chaque spécialité a au moins un module
    for specialite in specialites:
        if not Modules.objects.filter(specialite=specialite).exists():
            return JsonResponse({'completed': False, 'reason': f'<h5>la spécialité {specialite.label} n\'a aucun module </h5><br><br> <p> Veuillez ajouter au moins un module avant de pouvoir synchroniser la formation.</p>'})

    # Si tout est bon
    return JsonResponse({'completed': True})

@transaction.atomic
@login_required(login_url='institut_app:login')
def updateFormation(request, pk):
    if request.tenant.tenant_type == "master":
        formation = Formation.objects.get(pk = pk)
        form = NewFormationFormMaster(instance = formation)
        if request.method == "POST":
            form = NewFormationForm(request.POST, instance=formation)
            if form.is_valid():
                updated_formation = form.save()
                updated_formation.updated = True
                updated_formation.save()

                messages.success(request, 'Les informations de la formation ont été modifier avec succès')
                return redirect('t_formations:listFormations')
            else:
                messages.error(request, 'Une erreur s\'est produite lors du traitement de la requête')
                return redirect('t_formations:updateFormation', pk)
        else:
            context = {
                'form' : form,
                'tenant' : request.tenant
            }
            return render(request, 'tenant_folder/formations/update_formation.html', context)

@transaction.atomic
@login_required(login_url='institut_app:login')
def AddPartenaire(request):
    if request.method == 'POST':
        form = NewPartenaireForm(request.POST, current_tenant=request.tenant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partenaire ajouté avec succès')
            return redirect('t_formations:listPartenaires')
    else:
        form = NewPartenaireForm(current_tenant=request.tenant)

    context = {
        'form': form,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/formations/new_partenaire.html', context)

def detailsPartenaire(request, pk):
    partenaire = Partenaires.objects.get(id=pk)

    context = {
        'partenaire': partenaire,           
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/formations/details_partenaire.html', context)

def ApiGetPartenaireSync(request):
    code = request.GET.get('code_partenaire')
    liste = Institut.objects.exclude(Q(schema_name='public') | Q(tenant_type='master'))
    instituts = []

    for institut in liste:
        with schema_context(institut.schema_name):
            has_partenaire = Partenaires.objects.filter(code=code).exists()

        instituts.append({
            'schema_name': institut.schema_name,
            'has_partenaire': has_partenaire,
        })

    return JsonResponse(instituts, safe=False)

def ApigetFormationSync(request):
    code = request.GET.get('code_formation')
    liste = Institut.objects.exclude(Q(schema_name='public') | Q(tenant_type='master'))
    formation = Formation.objects.get(code=code)

    instituts = []

    for institut in liste:
        with schema_context(institut.schema_name):
            has_formation = Formation.objects.filter(code=code).exists()
            has_partenaire = Partenaires.objects.filter(code=formation.partenaire.code).exists()

        instituts.append({
            'schema_name': institut.schema_name,
            'has_formation': has_formation,
            'has_partenaire': has_partenaire,
        })

    return JsonResponse(instituts, safe=False)


######### methode de syncronisation des formations #############################################
def update_or_create_formation_in_tenant(formation, institut_schema):
    try:
        with schema_context(institut_schema):
            # Chercher si la formation existe déjà dans le schéma
            sync_formation, created = Formation.objects.update_or_create(
                code=formation.code,
                defaults={
                    'nom': formation.nom,
                    'description': formation.description,
                    'duree': formation.duree,
                    'partenaire': formation.partenaire,
                    'type_formation': formation.type_formation,
                    'frais_inscription': formation.frais_inscription,
                    'frais_assurance': formation.frais_assurance,
                }
            )
            return sync_formation
    except IntegrityError:
        raise ValueError("Une erreur d'intégrité s'est produite lors de la mise à jour de la formation.")
    
def update_or_create_specialite_in_tenant(specialite, sync_formation, institut_schema):
    try:
        with schema_context(institut_schema):
            # Chercher si la spécialité existe déjà
            sync_specialite, created = Specialites.objects.update_or_create(
                code=specialite.code,
                formation=sync_formation,
                defaults={
                    'label': specialite.label,
                    'prix': specialite.prix,
                    'duree': specialite.duree,
                    'version': specialite.version,
                    'condition_access': specialite.condition_access,
                    'dossier_inscription': specialite.dossier_inscription,
                }
            )
            return sync_specialite
    except IntegrityError:
        raise ValueError("Une erreur d'intégrité s'est produite lors de la mise à jour de la spécialité.")
    
def update_or_create_module_in_tenant(module, specialite, institut_schema):
    try:
        with schema_context(institut_schema):
            # Chercher si le module existe déjà
            sync_module, created = Modules.objects.update_or_create(
                code=module.code,
                specialite=specialite,
                defaults={
                    'label': module.label,
                    'coef': module.coef,
                    'duree': module.duree,
                }
            )
            return sync_module
    except IntegrityError:
        raise ValueError("Une erreur d'intégrité s'est produite lors de la mise à jour du module.")
######### methode de syncronisation des formations #############################################

##### Synchronisation des formations et spécialités dans un tenant spécifique ##################
def ApiSyncFormation(request):
    code_formation = request.POST.get('code_formation')
    schema_name = request.POST.get('schema_name')

    formation = Formation.objects.get(code=code_formation)
    institut = Institut.objects.get(schema_name=schema_name)

    with schema_context(institut.schema_name):
        sync_formation = update_or_create_formation_in_tenant(formation, institut.schema_name)

    specialites = Specialites.objects.filter(formation=formation)
    for specialite in specialites:
        with schema_context(institut.schema_name):
            sync_specialite = update_or_create_specialite_in_tenant(specialite, sync_formation, institut.schema_name)

    modules = Modules.objects.filter(specialite=specialite)
    for module in modules:
        with schema_context(institut.schema_name):
            update_or_create_module_in_tenant(module, sync_specialite, institut.schema_name)

    return JsonResponse({'status': True, 'message': 'Formation et spécialités synchronisées avec succès'})
##### Synchronisation des formations et spécialités dans un tenant spécifique ##################

##### Synchronisation (Modification et création) des formations et spécialités dans tous les tenants ##################
def ApiSyncUpdateFormation(request):
    code_formation = request.POST.get('code_formation')
    
    formation = Formation.objects.get(code=code_formation)
    liste = Institut.objects.exclude(Q(schema_name='public') | Q(tenant_type='master'))

    formation.updated=False
    formation.save()
    
    for institut in liste:
        with schema_context(institut.schema_name):
            sync_formation = update_or_create_formation_in_tenant(formation, institut.schema_name)

        specialites = Specialites.objects.filter(formation=formation)
        for specialite in specialites:
            with schema_context(institut.schema_name):
                update_or_create_specialite_in_tenant(specialite, sync_formation, institut.schema_name)

        modules = Modules.objects.filter(specialite=specialite)
        for module in modules:
            with schema_context(institut.schema_name):
                update_or_create_module_in_tenant(module, specialite, institut.schema_name)
    return JsonResponse({'status': True, 'message': 'Formation et spécialités ont été mises à jour avec succès dans tous les instituts.'})
##### Synchronisation (Modification et création) des formations et spécialités dans tous les tenants ##################

def ApiCheckFormationState(request):
    code_formation = request.GET.get('code_formation')
    formation = Formation.objects.get(code=code_formation)

    if formation.updated:
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False}) 

def ApiSyncPartenaire(request):

    code_partenaire = request.POST.get('code_partenaire')
    shema_name = request.POST.get('schema_name')
    partenaire  = Partenaires.objects.get(code = code_partenaire)

    institut = Institut.objects.get(schema_name=shema_name)
    with schema_context(institut.schema_name):
        sync_partenaire = Partenaires(
            nom = partenaire.nom,
            code = partenaire.code,
            adresse = partenaire.adresse,

            telephone = partenaire.telephone,
            email = partenaire.email,
            site_web = partenaire.site_web,
            type_partenaire = partenaire.type_partenaire,
        )
        sync_partenaire.save()
        return JsonResponse({'success': True, 'message': 'Partenaire synchronisé avec succès'})
        
def deletePartenaire(request, pk):
    partenaire = Partenaires.objects.get(id=pk)
    partenaire.delete()
    messages.success(request, 'Partenaire supprimé avec succès')
    return redirect('t_formations:listPartenaires')

def ListeDesPartenaires(request):
    liste = Partenaires.objects.all()
    context = {
        'liste' : liste,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/formations/liste_des_partenaires.html', context)

def UpdatePartenaire(request, pk):
    partenaire = Partenaires.objects.get(id=pk)
    form = NewPartenaireForm(instance=partenaire)

    if request.method == "POST":
        form = NewPartenaireForm(request.POST, instance=partenaire)
        if form.is_valid():
            updated_partenaire = form.save()
            if updated_partenaire.type_partenaire == 'etranger':
                instituts = Institut.objects.exclude(Q(schema_name='public') | Q(tenant_type='master'))
                for tenant in instituts:
                    with schema_context(tenant.schema_name):
                        try:
                            partenaire = Partenaires.objects.get(code=updated_partenaire.code)
                            partenaire.nom = updated_partenaire.nom
                            partenaire.adresse = updated_partenaire.adresse
                            partenaire.telephone = updated_partenaire.telephone
                            partenaire.email = updated_partenaire.email
                            partenaire.site_web = updated_partenaire.site_web
                            partenaire.type_partenaire = updated_partenaire.type_partenaire
                            partenaire.save()
                        except Partenaires.DoesNotExist:
                            pass
                messages.success(request, 'Partenaire mis à jour avec succès')
                return redirect('t_formations:listPartenaires')
            else:
                messages.success(request, 'Partenaire mis à jour avec succès')
                return redirect('t_formations:listPartenaires')
        else:
            messages.error(request, 'Une erreur s\'est produite lors du traitement de la requête')
            return redirect('t_formations:UpdatePartenaire', pk)

    context = {
        'form' : form,
        'tenant' : request.tenant,
    }
    return render(request,'tenant_folder/formations/update_partenaire.html',context)

@transaction.atomic
def addSpecialite(request):
    form = NewSpecialiteForm()
    if request.method == 'POST':
        form = NewSpecialiteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Spécialité ajoutée avec succès")
            return redirect('t_formations:listSpecialites')
           
        else:
            errors = " | ".join(["{}: {}".format(field, ", ".join(errors)) for field, errors in form.errors.items()])
            messages.error(request, f"{errors}")
            return redirect('t_formations:addSpecialite')
        
    else:
        context = {
            'form' : form,
            'tenant' : request.tenant,
        }

        return render(request, 'tenant_folder/formations/nouvelle_specialite.html', context)

@transaction.atomic
def updateSpecialite(request,pk):
    specialite = Specialites.objects.get(id = pk)
    form = NewSpecialiteForm(instance=specialite)
    if request.method == "POST":
        form = NewSpecialiteForm(request.POST, instance=specialite)
        if form.is_valid():
            updated_spec = form.save()
            updated_spec.updated_by = request.user
            updated_spec.save()

            formation  = specialite.formation
            formation.updated = True
            formation.save()

            messages.success(request, "Les données de la spécialitée ont été mis à jours avec succès")
            return redirect('t_formations:detailSpecialite', pk)
        else:
            messages.error(request, "Une erreur c'est produite lors du traitement de la réquête")
            return redirect('t_formations:detailSpecialite', pk)
    
    context = {
        'form' : form,
        'tenant' : request.tenant
    }
    return render(request, "tenant_folder/formations/update_specialite.html", context)

def updateFraisInscription(request):
    pass

def deleteFormation(request):
    pass

def deleteSpecialite(request, pk):
    specialite = Specialites.objects.get(id = pk)

    if request.tenant.tenant_type == 'master':

        specialite.delete()
        messages.success(request, 'Spécialité supprimée avec succès')
        return redirect('t_formations:listSpecialites')

    elif specialite.formaton.type_formation == 'etranger':

        messages.error(request, 'Vous ne pouvez pas supprimer cette spécialité')
        return redirect('t_formations:listSpecialites')
    
    else:

        specialite.delete()
        messages.success(request, 'Spécialité supprimée avec succès')
        return redirect('t_formations:listSpecialites')
    
def deleteFraisInscription(request):
    pass

def detailFormation(request, pk):
    formation = Formation.objects.get(id = pk)
    specialite = Specialites.objects.filter(formation = formation)

    context = {
        'formation' : formation,
        'tenant' : request.tenant,
        'specialite' : specialite,
    }
    return render(request, 'tenant_folder/formations/details_formation.html', context)

def detailSpecialite(request, pk):
    object = Specialites.objects.get(id = pk)
    context = {
        'object' : object,
        'tenant' : request.tenant,
    }
    return render(request, "tenant_folder/formations/details_specialite.html", context)

def ApiGetSpecialiteModule(request):
    id = request.GET.get('id')
    modules = Modules.objects.filter(specialite = id, is_archived = False).values('id', 'label','code','coef','duree')

    specialite = Specialites.objects.get(code = id)

    data  = {
       'modules' : list(modules),
       'nb_semestre' : specialite.nb_semestre,
    }

    return JsonResponse(data, safe=False)

def ApiGetRepartitionModule(request):
    id_specialite = request.GET.get('id_specialite')
    object = ProgrammeFormation.objects.filter(specialite = id_specialite).values('id', 'module__label', 'semestre')

    return JsonResponse(list(object), safe=False)

def ApiAffectModuleSemestre(request):
    id_module = request.POST.get('id_module')
    semestre = request.POST.get('semestre')
    id_specialite = request.POST.get('id_specialite')
    try:
        specialite = Specialites.objects.get(code = id_specialite)
        module = Modules.objects.get(id = id_module)

        repartition = ProgrammeFormation(
           
            module = module,
            specialite  = specialite,
            semestre = semestre,
        )
        repartition.save()
        return JsonResponse({'success' : True, 'message' : "Le module à été affecté avec succès"})
    except:
        return JsonResponse({'success' : False, 'message' : "L'affectation du module existe déja"})

def ApiAddModule(request):

    label = request.POST.get('label')
    coef = request.POST.get('coef')
    duree = request.POST.get('duree')
    id = request.POST.get('id')
    code = request.POST.get('code_module')

    specialite = Specialites.objects.get(code = id)
    try:
        new_module = Modules.objects.create(
            label = label,
            coef = coef,
            duree = duree,
            specialite = specialite,
            code = code,
            created_by = request.user,
        )

        new_module.save()
        return JsonResponse({'success' : True})
    except IntegrityError:
        return JsonResponse({'success' : False, 'message' : "Le module existe déja"})

@login_required(login_url='insitut_app:login')
def deleteModule(request):
    id = request.GET.get('id')
    
    obj = Modules.objects.get(id = id)
    obj.is_archived = True
    # obj.updated_by = request.user,
    obj.save()
   
    return JsonResponse({'success' : True, 'message' : "Le module à été supprimé avec succès"})

def archiveModule(request):
    liste = Modules.objects.filter(is_archived = True)
    context = {
        'liste' : liste,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/formations/archive/archive_module.html', context)

def ApiGetModuleDetails(request):
    id = request.GET.get('id')
    obj = Modules.objects.filter(id = id).values('id', 'code', 'label', 'duree', 'coef')
    return JsonResponse(list(obj), safe=False)

@transaction.atomic
def ApiUpdateModule(request):

    id = request.POST.get('id')
    coef = request.POST.get('coef')
    duree = request.POST.get('duree')
    label = request.POST.get('label')
    code = request.POST.get('code')

    module = Modules.objects.get(id= id)
    module.code = code
    module.duree = duree
    module.label = label
    module.coef = coef

    module.save()

    return JsonResponse({'success' : True, 'message' : "Les information du module ont été mis à jours avec succès"})

def archiveFormation(request):
    pass
 
def detailModule(request):
    pass

def detailFraisInscription(request):
    pass

def listPromos(request):
    
    context = {
        
        'tenant' : request.tenant,
    }
    return render(request,'tenant_folder/formations/promos/list_promos.html',context)

def ApiListePromos(request):
    liste= Promos.objects.filter().values('id','label','session','etat')

    for l in liste:
        l_obj = Promos.objects.get(id = l['id'])
        l['etat_label'] = l_obj.get_etat_display()
        l['session_label'] = l_obj.get_session_display()

    return JsonResponse(list(liste), safe=False)

def ApiListeFormation(request):
    liste = Formation.objects.all().values('id', 'nom')
    return JsonResponse(list(liste), safe=False)

def ApiListeSpecialiteByFormation(request):
    id= request.GET.get('id_formation')
    formation_obj = Formation.objects.get(id = id)
    liste = Specialites.objects.filter(formation = formation_obj.code).values('id', 'label','code')
    return JsonResponse(list(liste), safe=False)

def AddPromo(request):
    form = PromoForm()
    if request.method =="POST":
        form = PromoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promo ajoutée avec succès')
            return redirect('t_formations:listPromos')
        else:
            messages.error(request, 'Une erreur c\'est produite lors du traitement de la requête')
            return redirect('t_formations:AddPromo')
    context = {
        'form' : form,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/formations/promos/new_promo.html', context)

def ApiDeletePromo(request):
    id = request.POST.get('id')
    promo = Promos.objects.get(id = id)
    if promo.etat == 'active':
        return JsonResponse({'success' : False, 'message' : 'Vous ne pouvez pas supprimer une promo active'})
    else:
        promo.delete()
        return JsonResponse({'success' : True, 'message' : 'Promo supprimée avec succès'})

def ApiGetPromo(request):
    id = request.GET.get('id')
    promo = Promos.objects.filter(id = id).values('id', 'label', 'session')
    return JsonResponse(list(promo), safe=False)

def ApiUpdatePromo(request):
    id = request.POST.get('id')
    label = request.POST.get('label')
    session = request.POST.get('session')

    if not label or not session:
        return JsonResponse({'success' : False, 'message' : 'Veuillez remplir les champs obligatoires'})
    else:
        promo = Promos.objects.get(id = id)
        promo.label = label
        promo.session = session
        promo.save()
        return JsonResponse({'success' : True, 'message' : 'Promo mis à jours avec succès'})
    
def ApiActivatePromo(request):
    id = request.POST.get('id')
    promo = Promos.objects.get(id = id)
    promo.etat = 'active'
    promo.save()
    return JsonResponse({'success' : True, 'message' : 'Promo activée avec succès'})

def SpecialitePromo(request):
    
    context = {
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/formations/promos/specialite_promo.html', context)

def PageListeModules(request):
    return render(request, 'tenant_folder/formations/modules/modules.html', {'tenant' : request.tenant})

def ApiGetModules(request):
    liste = Modules.objects.all().values('id', 'label', 'coef', 'duree', 'code')
    return JsonResponse(list(liste), safe=False)

def ApiGetModuleDetails(request):
    id = request.GET.get('id')
    
    details = Modules.objects.get(id = id)
    data = {
        'id' : details.id,
        'label' : details.label,
        'coef' : details.coef,
        'duree' : details.duree,
        'code' : details.code,
    }
    
    return JsonResponse(data, safe=False)

@login_required(login_url='intitut_app:login')
def ApiLoadDocuments(request):
    code_formation = request.GET.get('code_formation')
    documents = DossierInscription.objects.filter(formation__code = code_formation).values('id','label')


    return JsonResponse(list(documents), safe=False)

@login_required(login_url="institut_app:login")
def ApiAddDocument(request):
    label = request.POST.get('nom_doc')
    required = request.POST.get('required')
    code_formation = request.POST.get('code_formation')
    
    if required == "false":
        _required = False
    else:
        _required = True

    DossierInscription.objects.create(
        formation = Formation.objects.get(code = code_formation),
        label = label,
        is_required = _required
    )

    return JsonResponse({"status" : "success","message" : "Le document à été ajouter avec succès"})

@login_required(login_url="institu_app:login")
@transaction.atomic
def ApiDeleteDoc(request):
    id_doc = request.POST.get('id_doc')
    if id_doc:
        obj = DossierInscription.objects.get(id = id_doc)
        obj.delete()
        return JsonResponse({'status' : 'success', 'message' : 'Document supprimer avec succès' })
    else:
        return JsonResponse({'status' : 'error', 'message' : 'Une erreur est survenue lors du traitement de la requete' })

    

