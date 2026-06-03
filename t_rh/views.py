from institut_app.decorators import module_permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .utils import calculate_leave_duration
from django.http import JsonResponse, HttpResponse

from .forms import *
from .models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Q, Avg
import json


def remplacer_tags(contenu, employe, contrat):
    tags = {
        '[date_debut]': f"<strong>{contrat.date_embauche.strftime('%d/%m/%Y') if contrat.date_embauche else ''}</strong>",
        '[nom_employe]': f"<strong>{employe.nom}</strong>",
        '[prenom_employe]': f"<strong>{employe.prenom}</strong>",
        '[poste]': f"<strong>{contrat.poste.label}</strong>",
        '[periode_essai]': f"<strong>{contrat.periode_essai}</strong>",
    }

    for tag, valeur in tags.items():
        contenu = contenu.replace(tag, valeur)

    return contenu

def view_contrat(request, pk):
    employe = Employees.objects.get(id=pk)
    contrat = Contrats.objects.get(employee=employe)
    articles = ArticlesContratStandard.objects.filter(type_contrat=contrat.type_contrat)

    articles_personnalises = []
    for article in articles:
        contenu_remplace = remplacer_tags(article.contenu, employe,contrat)
        article.contenu_remplace = contenu_remplace  
        articles_personnalises.append(article)

    context = {
        'employe': employe,
        'contrat': contrat,
        'articles': articles_personnalises,
    }
    return render(request, 'tenant_folder/rh/contrats/contrat_template.html', context)

# def view_contrat(request, pk):

#     employe = Employees.objects.get(id = pk)
#     contrat = Contrats.objects.get(employee = employe)
#     articles = ArticlesContratStandard.objects.filter(type_contrat = contrat.type_contrat)
#     context = {
#         'employe' : employe,
#         'contrat' : contrat,
#         'articles' : articles,
#     }
#     return render(request, 'tenant_folder/rh/contrats/contrat_template.html', context)

@module_permission_required('rh', 'view')
def listeEmployes(request):
    liste = Employees.objects.prefetch_related('contrats').all()
   
    context = {
        'liste' : liste,
    }
    return render(request,"tenant_folder/rh/liste_des_employee.html", context)

@transaction.atomic
@module_permission_required('rh', 'add')
def nouveauEmploye(request):
    form = NouveauEmploye()
    if request.method == 'POST':
        form = NouveauEmploye(request.POST)
        if form.is_valid():
            emp = form.save()
            messages.success(request, 'Employé ajouté avec succès')
            return redirect('t_rh:detailsEmploye', emp.id)
    
    context = {
        'form' : form,
        'tenant' : request.tenant
    }

    return render(request, 'tenant_folder/rh/nouveau_employe.html', context)

@module_permission_required('rh', 'view')
def detailsEmploye(request, pk):
    employe = Employees.objects.prefetch_related('contrats').get(id = pk)
    # Get active contract (the one with the latest date_embauche)
    active_contract = employe.contrats.order_by('-date_embauche').first()
    
    primes = []
    payroll_id = None
    if active_contract:
        from t_ressource_humaine.models import Contrat as PayrollContrat, RubriqueContrat
        payroll_contract = PayrollContrat.objects.filter(employee=employe).first()
        if payroll_contract:
            payroll_id = payroll_contract.id
            primes = RubriqueContrat.objects.filter(contrat=payroll_contract, actif=True).select_related('rubrique')

    from pdf_editor.models import DocumentTemplate
    templates_contrat = DocumentTemplate.objects.filter(template_type='contract', is_active=True)

    context = {
        'employe' : employe,
        'contrats' : employe.contrats.all(),
        'active_contract': active_contract,
        'primes': primes,
        'payroll_id': payroll_id,
        'templates_contrat': templates_contrat,
    }
    return render(request,'tenant_folder/rh/details_employe.html', context)

@transaction.atomic
@module_permission_required('rh', 'change')
def updateEmploye(request,pk):
    emp = Employees.objects.get(id = pk)
    form = NouveauEmploye(instance=emp)
    if request.method == "POST":
        form = NouveauEmploye(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            messages.success(request,"Les informations de l'employe ont été mis à jours.")
            return redirect('t_rh:detailsEmploye', pk)
    
    context = {
        'form' : form,
        'tenant' : request.tenant,
    }
    return render(request, "tenant_folder/rh/update_employe.html", context)

@transaction.atomic
@module_permission_required('rh', 'add')
def nouveauService(request):
    form = NouveauService()
    if request.method == 'POST':
        form = NouveauService(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service ajouté avec succès')
            return redirect('t_rh:liste_services')
    
    context = {
        'form' : form,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/rh/services/nouveau_service.html', context)

@module_permission_required('rh', 'view')
def listeServices(request):

    context = {
        
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/rh/services/liste_des_services.html', context)

@module_permission_required('rh', 'view')
def ApiListeServices(request):
    liste = Services.objects.filter().values('id','label', 'description','created_at')
    return JsonResponse(list(liste), safe=False)

@module_permission_required('rh', 'add')
def ApiAddService(request):
    label = request.POST.get('label')
    description = request.POST.get('description')

    if label and description:
        service = Services(label=label, description=description)
        service.save()
        return JsonResponse({'status': 'success', 'message':"Service ajouté avec succès"})
    else:
        return JsonResponse({'status': 'error', 'message':"Erreur lors de l'ajout du service"})

@module_permission_required('rh', 'view')
def ApiGetService(request):
    id = request.GET.get('id')
    service = Services.objects.filter(id=id).values('id','label', 'description')
    return JsonResponse(list(service), safe=False)

@module_permission_required('rh', 'change')
def ApiUpdateService(request):
    id = request.POST.get('id')
    label = request.POST.get('label')
    description = request.POST.get('description')

    if id and label and description:
        service = Services.objects.get(id=id)
        service.label = label
        service.description = description
        service.save()
        return JsonResponse({'status': 'success', 'message':"Service mis à jour avec succès"})
    else:
        return JsonResponse({'status': 'error', 'message':"Erreur lors de la mise à jour du service"})

@module_permission_required('rh', 'delete')
def ApiDeleteService(request):
    id = request.POST.get('id')
    if id:
        service = Services.objects.get(id=id)
        service.delete()
        return JsonResponse({'status': 'success', 'message':"Service supprimé avec succès"})
    else:
        return JsonResponse({'status': 'error', 'message':"Erreur lors de la suppression du service"})

@transaction.atomic
@module_permission_required('rh', 'add')
def NouveauArticleContrat(request):
    form = ArticlesContratStandard()
    if request.method == 'POST':
        form = ArticlesContratStandard(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article ajouté avec succès')
            return redirect('t_rh:liste_articles_contrat')
    context = {
        'form' : form,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/rh/contrats/nouveau_article.html', context)

@module_permission_required('rh', 'view')
def listeArticlesContrat(request):
    liste = ArticlesContratStandard.objects.all()
    context = {
        'liste' : liste,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/rh/contrats/liste_des_articles.html', context)

@module_permission_required('rh', 'view')
def listeTypeContrat(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/rh/contrats/liste_des_types_contrat.html', context)

@module_permission_required('rh', 'view')
def ApiListeTypeContrat(request):
    liste = TypesContrat.objects.all().values('id','label','description','created_at')
    return JsonResponse(list(liste), safe=False)

@module_permission_required('rh', 'add')
def ApiAddTypeContrat(request):
    label = request.POST.get('label')
    description = request.POST.get('description')
    categorie = request.POST.get('id_categorie')

    if label and categorie:
        cat = CategoriesContrat.objects.get(id = categorie)
        type_contrat = TypesContrat(label=label, description=description, categorie = cat)
        type_contrat.save()
        return JsonResponse({'status': 'success', 'message':"Type de contrat ajouté avec succès"})
    else:
        return JsonResponse({'status': 'error', 'message':"Le champ label est requis"})
    
@module_permission_required('rh', 'change')
def ApiUpdateTypeContrat(request):
    id = request.POST.get('id')
    label = request.POST.get('label')
    description = request.POST.get('description')

    if id and label and description:
        obj = TypesContrat.objects.get(id = id)
        
        obj.label = label
        obj.description = description
        obj.save()
        return JsonResponse({'status': 'success', 'message':"Type de contrat mis à jour avec succès"})
    else:
        return JsonResponse({'status' : 'error', 'message' : "Veuillez saisir les champs requis"})

@module_permission_required('rh', 'delete')
def ApiDeleteTypeContrat(request):
    id = request.GET.get('id')

    type = TypesContrat.objects.get(id = id)
    contrat = Contrats.objects.filter(type_contrat = type)

    if contrat.count() > 0:
        return JsonResponse({'status' : "error", 'message' : "Suppression impossible ! <br> Le type de contrat est relié a un ou plusieurs contrat."}) 
    else:
        type.delete()
        return JsonResponse({'status' : 'success', "message" : "La suppression est effectué avec succès."})

@module_permission_required('rh', 'view')
def ClausesTypeContrat(request, pk):
    type = TypesContrat.objects.get(id= pk)
    context = {
        'type' : type,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/rh/contrats/type_contrat_articles.html', context)

@module_permission_required('rh', 'view')
def ApiGetClauseStandardOfType(request):
    id = request.GET.get('id')
    type = TypesContrat.objects.get(id=id)
    liste = ArticlesContratStandard.objects.filter(type_contrat = type).values('id', 'titre','contenu','created_at')
    return JsonResponse(list(liste), safe=False)

@module_permission_required('rh', 'add')
def ApiAddNewClause(request):
    titre = request.POST.get('titre')
    contenu = request.POST.get('contenu')
    id = request.POST.get('id')

    if titre and contenu and id:
        type_contrat = TypesContrat.objects.get(id = id)
        obj = ArticlesContratStandard(
            type_contrat = type_contrat,
            titre = titre,
            contenu = contenu
        )
        obj.save()
        return JsonResponse({'status' : 'success', 'message' : "Opération effectuer avec succès"})
    else:
        return JsonResponse({'status' : "error", "message" : "Tous les champs sont requis."})

@module_permission_required('rh', 'delete')
def ApiDeleteClause(request):
    id = request.GET.get('id')
    obj = ArticlesContratStandard.objects.get(id = id)
    obj.delete()
    return JsonResponse({'status' : 'success', 'message' : "La clause à été supprimé avec succès"})

@module_permission_required('rh', 'change')
def ApiUpdateClause(request):
    id = request.POST.get('id')
    titre = request.POST.get('update_titre')
    contenu = request.POST.get('update_contenu')
    if id or titre or contenu:
        obj = ArticlesContratStandard.objects.get(id=id)
        obj.titre = titre
        obj.contenu = contenu
        obj.save()
        return JsonResponse({'status' : 'success', 'message' : "Les informations ont été modifier avec succès."})
    else:
        return JsonResponse({'status' : 'error', 'message' : "Tous les champs sont requis"})

@module_permission_required('rh', 'view')
def ListeCategorieContrat(request):
    context = {
        'tenant' : request.tenant
    }
    return render(request,'tenant_folder/rh/contrats/liste_categorie_contrat.html', context)

@module_permission_required('rh', 'view')
def ApiListCategorie(request):
    liste = CategoriesContrat.objects.filter().values('id', 'label', 'entite_legal','entite_legal__designation', 'description')
    return JsonResponse(list(liste), safe=False)

@module_permission_required('rh', 'add')
def ApiAddCategorieContrat(request):
    label = request.POST.get('label')
    description = request.POST.get('description')
    entite = request.POST.get('entite')

    if label and entite:
        obj_ent = Entreprise.objects.get(id = entite)

        new_cat = CategoriesContrat(
            label = label,
            description = description,
            entite_legal = obj_ent,
        )
        new_cat.save()
        return JsonResponse({'status': "success", 'message' : "La catégorie à été crée avec succès"})
    else:
        return JsonResponse({'status' : "error", 'message': "Champs requis manquants, veuillez completer les champs"})

@module_permission_required('rh', 'view')
def ApiGetDefaultValueForContrat(request):
    entreprises = list(Entreprise.objects.filter().values('id', 'designation'))
    services = list(Services.objects.values('id', 'label'))
    postes = list(Posts.objects.filter().values('id','label'))
    return JsonResponse({'entreprises': entreprises, 'services': services, 'postes' : postes}, safe=False)

@module_permission_required('rh', 'view')
def detailsCategorie(request, pk):
    cate = CategoriesContrat.objects.get(id = pk)
    context = {
        'categorie' : cate, 
    }
    return render(request,'tenant_folder/rh/contrats/details_categorie_contrat.html', context)

@module_permission_required('rh', 'view')
def ApiGetListeTypeContratByCategorie(request):
    id = request.GET.get('id_categorie')
    liste = TypesContrat.objects.filter(categorie = id).values('id','label','description','created_at')
    return JsonResponse(list(liste), safe=False)

@module_permission_required('rh', 'view')
def ApiGetCategorieContrat(request):
    id_entite = request.GET.get('id_entite')
    entite = Entreprise.objects.get(id = id_entite)
    categories = CategoriesContrat.objects.filter(entite_legal = entite).values('id', 'label')
    return JsonResponse(list(categories), safe=False)

@module_permission_required('rh', 'view')
def ApiGetTypeContrat(request):
    id_categorie = request.GET.get('id_categorie')
    types = TypesContrat.objects.filter(categorie=id_categorie)
    data = []
    for t in types:
        data.append({
            'id': t.id,
            'label': t.label
        })
    return JsonResponse(data, safe=False)

@module_permission_required('rh', 'view')
def ApiGetRubriquesOfType(request):
    id_type = request.GET.get('id')
    from t_ressource_humaine.models import Rubrique
    # Get rubriques explicitly linked to this type
    eligible = Rubrique.objects.filter(eligible_types=id_type, actif=True).values(
        'id', 'libelle', 'type_rubrique', 'mode_calcul', 'valeur_defaut'
    )
    # Get global rubriques (not linked to any specific type)
    globals = Rubrique.objects.filter(eligible_types__isnull=True, actif=True).values(
        'id', 'libelle', 'type_rubrique', 'mode_calcul', 'valeur_defaut'
    )
    return JsonResponse({
        'eligible': list(eligible), 
        'globals': list(globals)
    }, safe=False)

@module_permission_required('rh', 'add')
def ApiCreateContrat(request):
    import json
    id_employe = request.POST.get('id_employe')
    id_type_contrat = request.POST.get('type_contrat')
    date_embauche = request.POST.get('date_embauche')
    duree_contrat = request.POST.get('duree_contrat')
    id_service = request.POST.get('service')
    id_poste = request.POST.get('posts')
    has_essaie = request.POST.get('periode_essaie')
    duree_essaie = request.POST.get('duree_essaie')
    salaire_base_raw = request.POST.get('salaire_base')
    salaire_base = float(salaire_base_raw) if salaire_base_raw and salaire_base_raw.strip() else 0
    
    # Primes/Rubriques overrides
    rubriques_json = request.POST.get('rubriques_data')
    rubriques_data = []
    if rubriques_json:
        try:
            rubriques_data = json.loads(rubriques_json)
        except:
            pass

    employe = Employees.objects.get(id=id_employe)
    type_contrat = TypesContrat.objects.get(id=id_type_contrat)
    service = Services.objects.get(id=id_service)
    poste = Posts.objects.get(id=id_poste)

    new_contrat = Contrats(
        service = service,
        employee = employe,
        date_embauche = date_embauche,
        periode_essai = duree_essaie,
        has_essai = has_essaie,
        poste = poste,
        type_contrat = type_contrat,
        duree = duree_contrat,
        salaire_base = salaire_base
    )
    new_contrat.save()

    # --- Sync with Payroll Engine (t_ressource_humaine) ---
    from t_ressource_humaine.models import Contrat as PayrollContrat, Rubrique, RubriqueContrat
    
    payroll_contract, created = PayrollContrat.objects.get_or_create(
        employee=employe,
        defaults={
            'date_debut': date_embauche,
            'salaire_base': salaire_base,
            'actif': True
        }
    )
    
    if not created:
        payroll_contract.date_debut = date_embauche
        payroll_contract.salaire_base = salaire_base
        payroll_contract.save()

    # Apply Rubriques
    # If we have custom data from the form, use it
    if rubriques_data:
        for r_item in rubriques_data:
            rubrique_obj = Rubrique.objects.get(id=r_item['id'])
            # Create or update RubriqueContrat
            rc, created_rc = RubriqueContrat.objects.get_or_create(
                contrat=payroll_contract,
                rubrique=rubrique_obj,
                defaults={
                    'valeur': r_item['valeur'],
                    'actif': r_item['actif']
                }
            )
            if not created_rc:
                rc.valeur = r_item['valeur']
                rc.actif = r_item['actif']
                rc.save()
    else:
        # Fallback to default logic if no specific data provided
        eligible_rubriques = Rubrique.objects.filter(eligible_types=type_contrat, actif=True)
        global_rubriques = Rubrique.objects.filter(eligible_types__isnull=True, actif=True)
        all_eligible = (eligible_rubriques | global_rubriques).distinct()
        
        for r in all_eligible:
            RubriqueContrat.objects.get_or_create(
                contrat=payroll_contract,
                rubrique=r,
                defaults={'valeur': r.valeur_defaut, 'actif': True}
            )

    employe.has_contract = True
    employe.save()

    return JsonResponse({"status" : "success", 'message' : "Le contrat a été créé et les rubriques de paie ont été associées."})

@module_permission_required('rh', 'view')
def ApiGetListContratForEmploye(request):
    id_employe = request.GET.get('id_employe')
    employe = get_object_or_404(Employees, id=id_employe)
    
    # Get the payroll contract associated with this employee
    from t_ressource_humaine.models import Contrat as PayrollContrat
    payroll_contract = PayrollContrat.objects.filter(employee=employe).first()
    payroll_id = payroll_contract.id if payroll_contract else None

    contrats = Contrats.objects.filter(employee=employe).values(
        'id', 'type_contrat__label', 'poste__label', 'date_embauche', 'duree', 'created_at'
    )
    
    # Convert to list and inject payroll_id
    liste = list(contrats)
    for c in liste:
        c['payroll_id'] = payroll_id
        
    return JsonResponse(liste, safe=False)

@module_permission_required('rh', 'view')
def ApiGetCategorieContratDetails(request):
    id = request.GET.get('id')

    obj = CategoriesContrat.objects.get(id = id)

    data = {
        'id' : obj.id,
        'label'  :obj.label,
        'entite_id' : obj.entite_legal.id,
        'entite' : obj.entite_legal.designation,
        'description' : obj.description
    }

    return JsonResponse(data, safe=False)

@module_permission_required('rh', 'change')
def ApiUpdateCategorieGroupe(request):
    update_label = request.POST.get('update_label')
    update_description = request.POST.get('update_description')
    update_entite = request.POST.get('update_entite')
    categorieId = request.POST.get('id_cat')

   
    try:
        obj = CategoriesContrat.objects.get(id = categorieId)
    
        obj.label = update_label
        obj.description = update_description
        obj.entite_legal = Entreprise.objects.get(id = update_entite)
        obj.save()

        return JsonResponse({"status" : 'success', "message" : "Les informations ont été mis à jours"})
    except:
        return JsonResponse({'status' : "error", "message" : "Une erreur est survenue lors du traitement de la réquete"})

@module_permission_required('rh', 'view')
def ApiGetDetailsOfContract(request):
    id = request.GET.get('id')
    obj = get_object_or_404(Contrats, id=id)
    
    from t_ressource_humaine.models import Contrat as PayrollContrat, RubriqueContrat
    payroll_contract = PayrollContrat.objects.filter(employee=obj.employee).first()
    
    primes = []
    if payroll_contract:
        rcs = RubriqueContrat.objects.filter(contrat=payroll_contract, actif=True).select_related('rubrique')
        for rc in rcs:
            primes.append({
                'libelle': rc.rubrique.libelle,
                'valeur': float(rc.valeur),
                'mode': rc.rubrique.get_mode_calcul_display(),
                'type': rc.rubrique.type_rubrique
            })

    data = {
        'id': obj.id,
        'employee_nom': obj.employee.nom,
        'employee_prenom': obj.employee.prenom,
        'type_contrat': obj.type_contrat.label if obj.type_contrat else '-',
        'categorie_contrat': obj.type_contrat.categorie.label if obj.type_contrat and obj.type_contrat.categorie else '-',
        'employeur': obj.type_contrat.categorie.entite_legal.designation if obj.type_contrat and obj.type_contrat.categorie and obj.type_contrat.categorie.entite_legal else '-',
        'service': obj.service.label if obj.service else '-',
        'poste': obj.poste.label if obj.poste else '-',
        'duree': obj.duree or 'Indéterminée',
        'date_embauche': obj.date_embauche.strftime('%d/%m/%Y') if obj.date_embauche else '-',
        'salaire_base': float(payroll_contract.salaire_base) if payroll_contract else 0,
        'primes': primes
    }
    return JsonResponse(data, safe=False)

@module_permission_required('rh', 'view')
def ApiListePostes(request):
    liste = Posts.objects.filter().values('id', 'label', 'description')
    return JsonResponse(list(liste), safe=False)

@module_permission_required('rh', 'add')
def ApiAddPoste(request):
    poste = request.POST.get('poste')
    description = request.POST.get('description')

    new_poste = Posts(
        label = poste,
        description = description
    )
    new_poste.save()
    messages.success(request, 'Le poste à été ajouté avec succès')
    return JsonResponse({'status' : "success", "message" : "Le poste à été ajouter avec suucès",'id' : new_poste.id})

@module_permission_required('rh', 'view')
def ListeDesPostes(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/rh/postes/liste_des_postes.html', context)

@module_permission_required('rh', 'change')
def UpdatePoste(request, pk):
    poste = Posts.objects.get(id = pk)
    form = NouveauPoste(instance=poste)
    if request.method == 'POST':
        form = NouveauPoste(request.POST, instance=poste)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le poste à été mis à jour avec succès')
            return redirect('t_rh:updatePoste', pk)
    
    context = {
        'form' : form,
        'tenant' : request.tenant,
        'pk' : pk
    }
    return render(request, 'tenant_folder/rh/postes/update_poste.html', context)

@module_permission_required('rh', 'view')
def ApiGetPostDetails(request):
    id=  request.GET.get('id')
    obj = Posts.objects.get(id = id)

    data= {
        'id' : obj.id,
        'label' : obj.label,
        'description' : obj.description
    }

    return JsonResponse(data, safe=False)

@module_permission_required('rh', 'view')
def ApiGetListPostTaches(request):
    id = request.GET.get('postId')
    liste = TachesPoste.objects.filter(poste = Posts.objects.get(id=id))

    data = []
    for tache in liste:
        data.append({
            'id' : tache.id,
            'label' : tache.label,
        })

    return JsonResponse(data, safe=False)

@module_permission_required('rh', 'change')
def ApiUpdateCategorie(request):
    pass

@module_permission_required('rh', 'delete')
def ApiDeleteCategorie(request):
    pass


@module_permission_required('rh', 'change')
def modifierArticleContrat(request):
    pass

@module_permission_required('rh', 'view')
def detailsArticleContrat(request):
    pass

@module_permission_required('rh', 'delete')
def supprimerArticleContrat(request):
    pass

@module_permission_required('rh', 'view')
def ApiGetEntite(request):
    liste = Entreprise.objects.all().values('id','designation')
    return JsonResponse(list(liste),safe=False)

@module_permission_required('rh', 'view')
def listeDesContrats(request):
    contrats = Contrats.objects.select_related('employee', 'type_contrat', 'poste').all().order_by('-created_at')
    from pdf_editor.models import DocumentTemplate
    templates_contrat = DocumentTemplate.objects.filter(template_type='contract', is_active=True)
    context = {
        'liste': contrats,
        'templates_contrat': templates_contrat,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/rh/contrats/liste_des_contrats.html', context)

@module_permission_required('rh', 'view')
def imprimerContrat(request, contrat_id, template_id):
    from pdf_editor.models import DocumentTemplate, DocumentGeneration
    from django.template import Template, Context
    from django.utils import timezone
    from django.shortcuts import get_object_or_404, redirect
    
    contrat = get_object_or_404(Contrats, id=contrat_id)
    template_obj = get_object_or_404(DocumentTemplate, id=template_id, is_active=True)
    
    context_data = {
        'employe': contrat.employee,
        'contrat': contrat,
        'entreprise': 'SALDAE SYSTEMS',
        'current_user': request.user.get_full_name() or request.user.username,
        'date_impression': timezone.now().strftime('%d/%m/%Y'),
    }
    
    try:
        from pdf_editor.utils import render_template_with_context
        rendered_content, error = render_template_with_context(template_obj.content, context_data)
        
        if error:
            messages.error(request, f"Erreur lors du rendu du contrat: {error}")
            return redirect('t_rh:liste_des_contrats')
        
        doc_gen = DocumentGeneration.objects.create(
            template=template_obj,
            context_data={'type': 'impression_contrat', 'contrat_id': contrat.id},
            rendered_content=rendered_content,
            generated_by=request.user
        )
        
        return redirect('pdf_editor:document-export', pk=doc_gen.pk)
    except Exception as e:
        messages.error(request, f"Erreur lors de la génération du contrat: {str(e)}")
        return redirect('t_rh:liste_des_contrats')

@module_permission_required('rh', 'view')
def imprimerAttestation(request, employe_id, template_id):
    """Generate attestation document via pdf_editor."""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from django.utils import timezone
    from pdf_editor.models import DocumentTemplate, DocumentGeneration
    from pdf_editor.utils import render_template_with_context
    employe = get_object_or_404(Employees, id=employe_id)
    template_obj = get_object_or_404(DocumentTemplate, id=template_id, is_active=True)
    context_data = {
        'employe': employe,
        'company': 'SALDAE SYSTEMS',
        'current_user': request.user.get_full_name() or request.user.username,
        'date_impression': timezone.now().strftime('%d/%m/%Y'),
    }
    rendered_content, error = render_template_with_context(template_obj.content, context_data)
    if error:
        messages.error(request, f"Erreur lors du rendu de l'attestation: {error}")
        return redirect('t_rh:detailsEmploye', employe_id)
    doc_gen = DocumentGeneration.objects.create(
        template=template_obj,
        context_data={'type': 'attestation', 'employe_id': employe.id},
        rendered_content=rendered_content,
        generated_by=request.user,
    )
    return redirect('pdf_editor:document-export', pk=doc_gen.pk)

@module_permission_required('rh', 'view')
def imprimerBadge(request, employe_id, template_id):
    """Generate badge document via pdf_editor."""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from django.utils import timezone
    from pdf_editor.models import DocumentTemplate, DocumentGeneration
    from pdf_editor.utils import render_template_with_context
    employe = get_object_or_404(Employees, id=employe_id)
    template_obj = get_object_or_404(DocumentTemplate, id=template_id, is_active=True)
    context_data = {
        'employe': employe,
        'company': 'SALDAE SYSTEMS',
        'current_user': request.user.get_full_name() or request.user.username,
        'date_impression': timezone.now().strftime('%d/%m/%Y'),
    }
    rendered_content, error = render_template_with_context(template_obj.content, context_data)
    if error:
        messages.error(request, f"Erreur lors du rendu du badge: {error}")
        return redirect('t_rh:detailsEmploye', employe_id)
    doc_gen = DocumentGeneration.objects.create(
        template=template_obj,
        context_data={'type': 'badge', 'employe_id': employe.id},
        rendered_content=rendered_content,
        generated_by=request.user,
    )
    return redirect('pdf_editor:document-export', pk=doc_gen.pk)

@module_permission_required('rh', 'add')
def nouveauContrat(request):
    employes = Employees.objects.all().order_by('nom', 'prenom')
    context = {
        'employes': employes,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/rh/contrats/nouveau_contrat.html', context)

@module_permission_required('rh', 'view')
def listePresences(request):
    # Get filtering parameters
    date_str = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
    service_id = request.GET.get('service')
    
    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Base queryset for employees
    employees = Employees.objects.filter(etat="en cours", is_teacher=False)


    
    # Apply service filter if selected
    if service_id:
        employees = employees.filter(contrats__service_id=service_id).distinct()

    # Get existing presences for this date
    presences = {p.employee_id: p for p in Presence.objects.filter(date=date_obj)}
    
    # Calculate KPIs
    total_staff = employees.count()
    present_count = 0
    absent_count = 0
    late_count = 0
    half_day_count = 0
    not_marked_count = 0

    for emp in employees:
        p = presences.get(emp.id)
        emp.presence = p
        if p:
            if p.status == 'present': present_count += 1
            elif p.status == 'absent': absent_count += 1
            elif p.status == 'late': late_count += 1
            elif p.status == 'half_day': half_day_count += 1
        else:
            not_marked_count += 1
    
    # Get all services for the filter dropdown
    from .models import Services
    services = Services.objects.all()

    attendance_stats = {
        'total': total_staff,
        'present': present_count,
        'absent': absent_count,
        'late': late_count,
        'half_day': half_day_count,
        'not_marked': not_marked_count,
        'rate': round((present_count + late_count + half_day_count) / total_staff * 100, 1) if total_staff > 0 else 0
    }

    context = {
        'employees': employees,
        'services': services,
        'date_selected': date_str,
        'service_selected': service_id,
        'attendance_stats': attendance_stats,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/rh/presences/liste_presences.html', context)

@module_permission_required('rh', 'view')
def fichesMensuelles(request):
    import calendar
    from django.db.models import Count, Q
    
    # Get month/year from params or default to current
    today = datetime.now()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    service_id = request.GET.get('service')

    # Base queryset for active employees
    employees = Employees.objects.filter(etat="en cours", is_teacher=False)
    if service_id:
        employees = employees.filter(contrats__service_id=service_id).distinct()

    # Aggregate presence counts for each employee in the selected month
    # Using conditional aggregation for performance
    attendance_data = Presence.objects.filter(
        date__year=year,
        date__month=month
    ).values('employee_id').annotate(
        present_days=Count('id', filter=Q(status='present')),
        absent_days=Count('id', filter=Q(status='absent')),
        late_days=Count('id', filter=Q(status='late')),
        half_days=Count('id', filter=Q(status='half_day')),
        total_marked=Count('id')
    )

    # Convert to map for easy lookup
    stats_map = {item['employee_id']: item for item in attendance_data}

    # Prepare report list
    report = []
    for emp in employees:
        stats = stats_map.get(emp.id, {
            'present_days': 0,
            'absent_days': 0,
            'late_days': 0,
            'half_days': 0,
            'total_marked': 0
        })
        
        # Calculate working days in month (approximation or based on marking)
        # Here we use the number of distinct dates marked in the system for this month
        # or simply the count of present/absent/etc.
        
        report.append({
            'employee': emp,
            'stats': stats,
            'service': emp.contrats.last().service.label if emp.contrats.exists() and emp.contrats.last().service else "N/A"
        })

    # Services for filter
    from .models import Services
    services = Services.objects.all()

    # Years for filter (last 5 years)
    years = range(today.year, today.year - 5, -1)
    months = [
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ]

    context = {
        'report': report,
        'services': services,
        'months': months,
        'years': years,
        'selected_month': month,
        'selected_year': year,
        'selected_service': service_id,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/rh/presences/fiches_mensuelles.html', context)


@transaction.atomic
@module_permission_required('rh', 'add')
def ApiMarkPresence(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        status = request.POST.get('status')
        date_str = request.POST.get('date')
        
        if not employee_id or not status or not date_str:
            return JsonResponse({'status': 'error', 'message': 'Paramètres manquants'})
            
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        employee = Employees.objects.get(id=employee_id)
        
        presence, created = Presence.objects.update_or_create(
            employee=employee,
            date=date_obj,
            defaults={'status': status}
        )
        
        return JsonResponse({'status': 'success', 'message': f'Présence mise à jour pour {employee}'})
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@module_permission_required('rh', 'view')
def listeConges(request):
    conges = Conges.objects.all().order_by('-created_at')
    context = {
        'conges': conges,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/rh/conges/liste_conges.html', context)

@module_permission_required('rh', 'add')
def demandeConge(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        type_conge = request.POST.get('type_conge')
        date_debut_str = request.POST.get('date_debut')
        date_fin_str = request.POST.get('date_fin')
        motif = request.POST.get('motif')
        
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin_str, '%Y-%m-%d').date()
        
        employee = get_object_or_404(Employees, id=employee_id)

        if not employee.has_contract:
            messages.error(request, "Erreur: L'employé ne possède pas de contrat actif, il n'a donc pas droit aux congés.")
            return redirect('t_rh:demande_conge')
        
        # Validation: Date de début ne peut pas être avant la date de recrutement
        if employee.date_recrutement and date_debut < employee.date_recrutement:
            messages.error(request, f"Erreur: L'employé a été recruté le {employee.date_recrutement.strftime('%d/%m/%Y')}. Le congé ne peut pas commencer avant.")
            return redirect('t_rh:demande_conge')

        # Check for overlapping requests
        overlapping = Conges.objects.filter(
            employee=employee,
            status__in=[Conges.StatusConge.EN_ATTENTE, Conges.StatusConge.VALIDE],
            date_debut__lte=date_fin,
            date_fin__gte=date_debut
        ).exists()
        
        if overlapping:
            messages.error(request, "Erreur: Une demande de congé existe déjà pour cette période.")
            return redirect('t_rh:demande_conge')

        # Logic for duration calculation
        # Special leaves and Recuperation are in working days (excluding Fri/Sat)
        is_working_days = type_conge in [Conges.TypeConge.EXCEPTIONNEL, Conges.TypeConge.RECUPERATION]
        duree = calculate_leave_duration(date_debut, date_fin, is_working_days=is_working_days)
        
        # Validation du solde pour les congés annuels
        if type_conge == Conges.TypeConge.ANNUEL:
            if duree > employee.solde_conge:
                messages.error(request, f"Erreur: Solde de congé insuffisant. Demandé: {duree} jours, Solde disponible: {employee.solde_conge} jours.")
                return redirect('t_rh:demande_conge')
        
        
        Conges.objects.create(
            employee_id=employee_id,
            type_conge=type_conge,
            date_debut=date_debut,
            date_fin=date_fin,
            duree=duree,
            motif=motif,
            status=Conges.StatusConge.EN_ATTENTE
        )

        messages.success(request, "Demande de congé enregistrée.")
        return redirect('t_rh:liste_conges')
    
    employees = Employees.objects.filter(etat="en cours")
    context = {
        'employees': employees,
        'types_conge': Conges.TypeConge.choices,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/rh/conges/demande_conge.html', context)

@module_permission_required('rh', 'approuv')
def validerConge(request, pk):
    conge = get_object_or_404(Conges, pk=pk)
    action = request.POST.get('action') # 'valider' or 'refuser'
    
    if action == 'valider':
        conge.status = Conges.StatusConge.VALIDE
        conge.valide_par = request.user
        
        # Deduct from balance if it's annual leave
        if conge.type_conge == Conges.TypeConge.ANNUEL:
            employee = conge.employee
            employee.solde_conge -= conge.duree
            employee.save()
            
        messages.success(request, f"Congé validé pour {conge.employee}.")
    elif action == 'refuser':
        conge.status = Conges.StatusConge.REFUSE
        conge.commentaire_rh = request.POST.get('commentaire')
        messages.warning(request, f"Congé refusé pour {conge.employee}.")
        
    conge.save()
    return redirect('t_rh:liste_conges')

from .payroll_utils import get_monthly_payroll_variables
from t_ressource_humaine.logic import PaieEngine
from t_ressource_humaine.models import Rubrique, FichePaie, LignePaie, ParametresPaie, Contrat as PaieContrat

from .reporting_paie import generate_payroll_journal_csv, generate_bank_transfer_csv

@module_permission_required('rh', 'view')
def assistantPaie(request):
    month = int(request.GET.get('month', timezone.now().month))
    year = int(request.GET.get('year', timezone.now().year))
    action = request.GET.get('action')
    
    employees = Employees.objects.filter(etat='en cours', has_contract=True)
    
    payroll_data = []
    for emp in employees:
        contrat_rh = emp.contrats.first()
        if not contrat_rh:
            continue
            
        vars = get_monthly_payroll_variables(emp, month, year)
        res = PaieEngine.calculer_paie(
            contrat_rh, 
            jours_travailles=vars['jours_travailles'],
            heures_absence=vars['absences_jours'] * 8,
        )
        
        payroll_data.append({
            'employee': emp,
            'variables': vars,
            'result': res
        })
    
    # Handle Exports
    if action == 'export_journal':
        csv_content = generate_payroll_journal_csv(payroll_data, month, year)
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Journal_Paie_{month}_{year}.csv"'
        return response
        
    if action == 'export_virement':
        csv_content = generate_bank_transfer_csv(payroll_data)
        response = HttpResponse(csv_content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="Ordre_Virement_{month}_{year}.csv"'
        return response
        
    if action == 'valider':
        from t_ressource_humaine.models import FichePaie, LignePaie, Contrat, Rubrique
        from django.db import transaction
        
        with transaction.atomic():
            for data in payroll_data:
                contrat_rh = data['contrat_obj'] # The t_rh.Contrats object
                
                # Check if a FichePaie already exists for this month/year/contrat
                # We need a t_ressource_humaine.Contrat link. 
                # If it doesn't exist, we skip or create one.
                # For now, let's assume we map t_rh.Contrats to a temporary or persistent RH Contrat
                
                # Retrieve or create the corresponding Contrat in t_ressource_humaine
                rh_contrat, _ = Contrat.objects.get_or_create(
                    employee=data['employee'],
                    defaults={
                        'entreprise': Entreprise.objects.first(),
                        'date_debut': contrat_rh.date_debut or '2020-01-01',
                        'salaire_base': Decimal(getattr(contrat_rh, 'salaire_base', 0) or 0),
                        'prime_panier': Decimal(getattr(contrat_rh, 'prime_panier', 0) or 0),
                        'prime_transport': Decimal(getattr(contrat_rh, 'prime_transport', 0) or 0),
                    }
                )
                
                fiche, created = FichePaie.objects.update_or_create(
                    contrat=rh_contrat,
                    mois=month,
                    annee=year,
                    defaults={
                        'entreprise': Entreprise.objects.first(),
                        'jours_travailles': data['variables']['jours_travailles'],
                        'heures_absence': data['variables']['absences_heures'],
                        'salaire_base_calcule': data['result']['salaire_base_calcule'],
                        'montant_ss': data['result']['montant_ss'],
                        'base_ss': data['result']['base_ss'],
                        'salaire_imposable': data['result']['salaire_imposable'],
                        'irg': data['result']['irg'],
                        'net_a_payer': data['result']['net_a_payer'],
                        'prime_panier': data['result']['prime_panier'],
                        'prime_transport': data['result']['prime_transport'],
                    }
                )
        
        return redirect('t_rh:liste_fiches_paie')

    context = {
        'month': month,
        'year': year,
        'payroll_data': payroll_data,
        'months_choices': [
            (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
            (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
            (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
        ]
    }
    return render(request, 'tenant_folder/rh/paie/assistant_paie.html', context)



from t_ressource_humaine.models import TrancheIRG

@module_permission_required('rh', 'change')
def configFiscalite(request):
    # Retrieve the legal entity for the current tenant
    entreprise = Entreprise.objects.first()
    config = ParametresPaie.get_config(entreprise=entreprise)

    tranches = TrancheIRG.objects.all().order_by('min_montant')
    
    if request.method == 'POST':
        # Update global settings
        taux_ss_input = Decimal(request.POST.get('taux_ss', 9))
        config.taux_ss = taux_ss_input / Decimal('100')
        config.seuil_exoneration_irg = Decimal(request.POST.get('seuil_irg', 30000))
        config.save()
        return redirect('t_rh:config_fiscalite')

        
    context = {
        'config': config,
        'tranches': tranches,
    }
    return render(request, 'tenant_folder/rh/paie/config_fiscalite.html', context)

from t_ressource_humaine.models import FichePaie

@module_permission_required('rh', 'view')
def listeFichesPaie(request):
    fiches = FichePaie.objects.filter(contrat__employee__isnull=False).order_by('-annee', '-mois', 'contrat__employee__nom')
    
    # Filter by month/year if provided
    month = request.GET.get('month')
    year = request.GET.get('year')
    if month:
        fiches = fiches.filter(mois=month)
    if year:
        fiches = fiches.filter(annee=year)
        
    context = {
        'fiches': fiches,
        'months_choices': [
            (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
            (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
            (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
        ]
    }
    return render(request, 'tenant_folder/rh/paie/liste_fiches_paie.html', context)

@module_permission_required('rh', 'view')
def detailFichePaie(request, pk):
    fiche = get_object_or_404(FichePaie, pk=pk)
    context = {
        'fiche': fiche,
        'entreprise': Entreprise.objects.first(),
    }
    return render(request, 'tenant_folder/rh/paie/fiche_paie_detail.html', context)

@module_permission_required('rh', 'view')
def hubConfigRH(request):



    context = {
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/rh/hub_config_rh.html', context)

@module_permission_required('rh', 'change')
def configRH(request):

    config, created = HRConfig.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        config.heure_debut_standard = request.POST.get('heure_debut')
        config.heure_fin_standard = request.POST.get('heure_fin')
        config.quota_annuel_conge = request.POST.get('quota_conge')
        config.taux_heure_sup_standard = request.POST.get('taux_hs')
        config.save()
        messages.success(request, "Configuration RH mise à jour.")
        return redirect('t_rh:config_rh')
        
    context = {
        'config': config,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/rh/config_rh.html', context)

@module_permission_required('rh', 'view')
def dashboardRH(request):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    
    # --- 1. Top Cards Metrics ---
    total_active = Employees.objects.filter(etat="en cours").count()
    total_departments = Services.objects.count()
    
    # Absences today
    absences_today = Presence.objects.filter(date=today, status='absent').count()
    absence_rate = (absences_today / total_active * 100) if total_active > 0 else 0
    
    # On leave today
    on_leave_today = Conges.objects.filter(
        status=Conges.StatusConge.VALIDE,
        date_debut__lte=today,
        date_fin__gte=today
    ).count()

    # --- 2. Service Distribution (Pie Chart) ---
    services_data = Services.objects.annotate(
        emp_count=Count('contrats', filter=Q(contrats__employee__etat="en cours"))
    ).values('label', 'emp_count')
    
    service_labels = [s['label'] for s in services_data]
    service_counts = [s['emp_count'] for s in services_data]

    # --- 3. Gender Distribution (Pie Chart) ---
    gender_data = Employees.objects.filter(etat="en cours").values('genre').annotate(count=Count('id'))
    gender_labels = []
    gender_counts = []
    for g in gender_data:
        label = "Homme" if g['genre'] == 'M' else "Femme" if g['genre'] == 'F' else "Non défini"
        gender_labels.append(label)
        gender_counts.append(g['count'])

    # --- 4. Payroll Evolution (Line Chart - Last 6 Months) ---
    payroll_trend = []
    for i in range(5, -1, -1):
        target_date = today - timedelta(days=i*30)
        m = target_date.month
        y = target_date.year
        
        total_net = FichePaie.objects.filter(mois=m, annee=y).aggregate(total=Sum('net_a_payer'))['total'] or 0
        month_name = target_date.strftime('%b %Y')
        payroll_trend.append({'month': month_name, 'total': float(total_net)})
    
    payroll_labels = [p['month'] for p in payroll_trend]
    payroll_values = [p['total'] for p in payroll_trend]

    # --- 5. Upcoming Alerts ---
    # Contracts expiring in next 30 days
    expiry_limit = today + timedelta(days=30)
    expiring_contracts = Contrats.objects.filter(
        date_fin__gte=today,
        date_fin__lte=expiry_limit
    ).select_related('employee', 'type_contrat')
    
    # Probation periods ending soon
    probation_ends = Employees.objects.filter(
        date_fin_probation__gte=today,
        date_fin_probation__lte=expiry_limit,
        etat="en cours"
    )
    
    # Birthdays this month
    birthdays = Employees.objects.filter(
        date_naissance__month=today.month,
        etat="en cours"
    )

    context = {
        'total_active': total_active,
        'total_departments': total_departments,
        'absence_rate': round(absence_rate, 1),
        'on_leave_today': on_leave_today,
        
        # Charts Data (JSON for JS)
        'service_labels': json.dumps(service_labels),
        'service_counts': json.dumps(service_counts),
        'gender_labels': json.dumps(gender_labels),
        'gender_counts': json.dumps(gender_counts),
        'payroll_labels': json.dumps(payroll_labels),
        'payroll_values': json.dumps(payroll_values),
        
        # Lists
        'expiring_contracts': expiring_contracts,
        'probation_ends': probation_ends,
        'birthdays': birthdays,
        'tenant': request.tenant,
    }
    
    return render(request, 'tenant_folder/rh/dashboard_rh.html', context)




