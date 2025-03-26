from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import *
from .models import *
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
    liste = Services.objects.filter().values('id','label', 'description')
    return JsonResponse(list(liste), safe=False)

@transaction.atomic
def NouveauArticleContrat(request):
    form = NouvelleArticleContrat()
    if request.method == 'POST':
        form = NouvelleArticleContrat(request.POST)
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
    liste = ArticlesContrat.objects.all()
    context = {
        'liste' : liste,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/rh/contrats/liste_des_articles.html', context)

def modifierArticleContrat(request):
    pass

def detailsArticleContrat(request):
    pass

def supprimerArticleContrat(request):
    pass