from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url="insitut_app:login")
@transaction.atomic
def NewGroupe(request):
    form = NewGroupeForms()
    if request.method == "POST":
        form = NewGroupeForms(request.POST)
        if form.is_valid():
            
            form.save()

            messages.success(request, "Groupe enregistré avec succès")
            return redirect('t_groupe:listegroupes')
        
    context = {
        'form' : form,
        'tenant' : request.tenant,
    }

    return render(request,'tenant_folder/formations/groupe/nouveau_groupe.html', context)

@login_required(login_url="insitut_app:login")
def ListeGroupe(request):
    groupes = Groupe.objects.all()
    context = {
        'liste' : groupes,
        'tenant' : request.tenant,
    }
    return render(request,'tenant_folder/formations/groupe/liste_des_groupes.html', context)

@login_required(login_url="insitut_app:login")
def ApiGetGroupeList(request):
    liste = Groupe.objects.all().values('id','nom')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def detailsGroupe(request, pk):
    groupe = Groupe.objects.get(pk=pk)
    students = GroupeLine.objects.filter(groupe = groupe)
    context = {
        'groupe' : groupe,
        'students' : students,
        "specialite" : groupe.specialite,
        'tenant' : request.tenant,
    }
    return render(request,'tenant_folder/formations/groupe/details_du_groupe.html', context)

@login_required(login_url="insitut_app:login")
@transaction.atomic
def UpdateGroupe(request, pk):
    groupe = Groupe.objects.get(id = pk)
    form = NewGroupeForms(instance=groupe)
    if request.method == "POST":
        form = NewGroupeForms(request.POST, instance=groupe)
        if form.is_valid():
            form.save()
            messages.success(request,"Les informations du groupe on été modifier avec succès")
            return redirect("t_groupe:detailsgroupe", pk)
        else:
            messages.error(request,"Une erreur c'est produite lors du traitement de la requete")
            return redirect("t_groupe:UpdateGroupe", pk)
        
    context = {
        'form': form,
        'groupe' : groupe,
        'tenant' : request.tenant
    }
    return render(request,"tenant_folder/formations/groupe/update_groupe.html", context)

@login_required(login_url="institut_app:login")
def makeGroupeBrouillon(request, pk):
    groupe = Groupe.objects.get(id = pk)
    groupe.etat = "brouillon"
    groupe.save()
    messages.success(request, "Le groupe est en mode brouillon")
    return redirect('t_groupe:detailsgroupe', pk)

@login_required(login_url="insitut_app:login")
@transaction.atomic
def validateGroupe(request, pk):
    groupe = Groupe.objects.get(id = pk)
    groupe.etat = "inscription"
    groupe.save()
    messages.success(request, "Le début des inscription est programmé")
    return redirect('t_groupe:detailsgroupe', pk)

@login_required(login_url="insitut_app:login")
@transaction.atomic
def closeGroupe(request, pk):
    groupe = Groupe.objects.get(id = pk)
    groupe.etat = "cloture"
    groupe.save()
    messages.success(request, "Le groupe a été cloturé avec suucès")
    return redirect('t_groupe:detailsgroupe', pk)

def deleteGroupe(request, pk):
    groupe = Groupe.objects.get(pk=pk)
    groupe.delete()
    messages.success(request, "Groupe supprimé avec succès")
    return redirect('t_groupe:listegroupes')

def PrintSuivieCours(request):
    pass

def PrintPvExamen(request):
    pass

