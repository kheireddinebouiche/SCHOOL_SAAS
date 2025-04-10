from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction

def listeEmployes(request):
    liste = Employees.objects.prefetch_related('contrats').all()
   
    context = {
        'liste' : liste,
    }
    return render(request,"tenant_folder/rh/liste_des_employee.html", context)

@transaction.atomic
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

def detailsEmploye(request, pk):
    employe = Employees.objects.prefetch_related('contrats').get(id = pk)
    context = {
        'employe' : employe,
        'contrats' : employe.contrats.all(),
    }
    return render(request,'tenant_folder/rh/details_employe.html', context)

@transaction.atomic
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

def listeServices(request):

    context = {
        
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/rh/services/liste_des_services.html', context)

def ApiListeServices(request):
    liste = Services.objects.filter().values('id','label', 'description','created_at')
    return JsonResponse(list(liste), safe=False)

def ApiAddService(request):
    label = request.POST.get('label')
    description = request.POST.get('description')

    if label and description:
        service = Services(label=label, description=description)
        service.save()
        return JsonResponse({'status': 'success', 'message':"Service ajouté avec succès"})
    else:
        return JsonResponse({'status': 'error', 'message':"Erreur lors de l'ajout du service"})

def ApiGetService(request):
    id = request.GET.get('id')
    service = Services.objects.filter(id=id).values('id','label', 'description')
    return JsonResponse(list(service), safe=False)

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

def ApiDeleteService(request):
    id = request.POST.get('id')
    if id:
        service = Services.objects.get(id=id)
        service.delete()
        return JsonResponse({'status': 'success', 'message':"Service supprimé avec succès"})
    else:
        return JsonResponse({'status': 'error', 'message':"Erreur lors de la suppression du service"})

@transaction.atomic
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

def listeArticlesContrat(request):
    liste = ArticlesContratStandard.objects.all()
    context = {
        'liste' : liste,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/rh/contrats/liste_des_articles.html', context)

def listeTypeContrat(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/rh/contrats/liste_des_types_contrat.html', context)

def ApiListeTypeContrat(request):
    liste = TypesContrat.objects.all().values('id','label','description','created_at')
    return JsonResponse(list(liste), safe=False)

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

def ApiDeleteTypeContrat(request):
    id = request.GET.get('id')

    type = TypesContrat.objects.get(id = id)
    contrat = Contrats.objects.filter(type_contrat = type)

    if contrat.count() > 0:
        return JsonResponse({'status' : "error", 'message' : "Suppression impossible ! <br> Le type de contrat est relié a un ou plusieurs contrat."}) 
    else:
        type.delete()
        return JsonResponse({'status' : 'success', "message" : "La suppression est effectué avec succès."})

def ClausesTypeContrat(request, pk):
    type = TypesContrat.objects.get(id= pk)
    context = {
        'type' : type,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/rh/contrats/type_contrat_articles.html', context)

def ApiGetClauseStandardOfType(request):
    id = request.GET.get('id')
    type = TypesContrat.objects.get(id=id)
    liste = ArticlesContratStandard.objects.filter(type_contrat = type).values('id', 'titre','contenu','created_at')
    return JsonResponse(list(liste), safe=False)

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

def ApiDeleteClause(request):
    id = request.GET.get('id')
    obj = ArticlesContratStandard.objects.get(id = id)
    obj.delete()
    return JsonResponse({'status' : 'success', 'message' : "La clause à été supprimé avec succès"})

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

def ListeCategorieContrat(request):
    context = {
        'tenant' : request.tenant
    }
    return render(request,'tenant_folder/rh/contrats/liste_categorie_contrat.html', context)

def ApiListCategorie(request):
    liste = CategoriesContrat.objects.filter().values('id', 'label', 'entite_legal','entite_legal__designation', 'description')
    return JsonResponse(list(liste), safe=False)

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

def ApiGetDefaultValueForContrat(request):
    entreprises = list(Entreprise.objects.filter().values('id', 'designation'))
    services = list(Services.objects.values('id', 'label'))
    postes = list(Posts.objects.filter().values('id','label'))
    return JsonResponse({'entreprises': entreprises, 'services': services, 'postes' : postes}, safe=False)

def detailsCategorie(request, pk):
    cate = CategoriesContrat.objects.get(id = pk)
    context = {
        'categorie' : cate, 
    }
    return render(request,'tenant_folder/rh/contrats/details_categorie_contrat.html', context)

def ApiGetListeTypeContratByCategorie(request):
    id = request.GET.get('id_categorie')
    liste = TypesContrat.objects.filter(categorie = id).values('id','label','description','created_at')
    return JsonResponse(list(liste), safe=False)

def ApiGetCategorieContrat(request):
    id_entite = request.GET.get('id_entite')
    entite = Entreprise.objects.get(id = id_entite)
    categories = CategoriesContrat.objects.filter(entite_legal = entite).values('id', 'label')
    return JsonResponse(list(categories), safe=False)


def ApiGetTypeContrat(request):
    id_categorie = request.GET.get('id_categorie')
    categorie = CategoriesContrat.objects.get(id = id_categorie)
    types = TypesContrat.objects.filter(categorie = categorie).values('id', 'label')
    return JsonResponse(list(types), safe=False)

def ApiCreateContrat(request):
    id_employe = request.POST.get('id_employe')
    id_type_contrat = request.POST.get('type_contrat')
    id_service  = request.POST.get('service')
    id_poste = request.POST.get('posts')
    date_embauche = request.POST.get('date_embauche')
    periode_essaie = request.POST.get('periode_essaie')
    duree_essaie = request.POST.get('duree_essaie')
    duree_contrat = request.POST.get('duree_contrat')
    
    if(periode_essaie == "1"):
        has_essaie = True
    else:
        has_essaie = False

    employe = Employees.objects.get(id = id_employe)
    service = Services.objects.get(id = id_service)
    poste = Posts.objects.get(id = id_poste)
    type_contrat = TypesContrat.objects.get(id = id_type_contrat)

    new_contrat = Contrats(
        service = service,
        employee = employe,
        date_embauche = date_embauche,
        periode_essai = duree_essaie,
        has_essai = has_essaie,
        poste = poste,
        type_contrat = type_contrat,
        duree = duree_contrat
    )
    new_contrat.save()

    employe.has_contract = True
    employe.save()

    return JsonResponse({"status" : "success", 'message' : "Le contrat à été crée avec succès"})

def ApiGetListContratForEmploye(request):
    id_employe = request.GET.get('id_employe')
    employe = Employees.objects.get(id = id_employe)
    liste = Contrats.objects.filter(employee = employe).values('id','type_contrat__label','poste__label','date_embauche','duree','created_at')


    return JsonResponse(list(liste), safe=False)

def ApiListePostes(request):
    liste = Posts.objects.filter().values('id', 'label', 'description')
    return JsonResponse(list(liste), safe=False)

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


def ListeDesPostes(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/rh/postes/liste_des_postes.html', context)

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
    }
    return render(request, 'tenant_folder/rh/postes/update_poste.html', context)


def ApiUpdateCategorie(request):
    pass

def ApiDeleteCategorie(request):
    pass


def modifierArticleContrat(request):
    pass

def detailsArticleContrat(request):
    pass

def supprimerArticleContrat(request):
    pass

def ApiGetEntite(request):
    liste = Entreprise.objects.all().values('id','designation')
    return JsonResponse(list(liste),safe=False)