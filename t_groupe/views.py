from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.db import transaction

@transaction.atomic
def NewGroupe(request):
    form = NewGroupeForms()
    if request.method == "POST":
        form = NewGroupeForms(request.POST)
        if form.is_valid():
            
            designation = form.cleaned_data.get('nom')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            description = form.cleaned_data.get('description')
            min_student = form.cleaned_data.get('min_student')
            max_student = form.cleaned_data.get('max_student')
            specialite = form.cleaned_data.get('specialite')

            groupe = Groupe.objects.create(
                nom = designation,start_date = start_date, end_date = end_date, description = description,
                min_student = min_student,max_student = max_student, specialite = specialite, createdy = request.user

            )

            groupe.save()

            messages.success(request, "Groupe enregistré avec succès")
            return redirect('t_groupe:listegroupes')
        
    context = {
        'form' : form,
        'tenant' : request.tenant,
    }

    return render(request,'tenant_folder/formations/groupe/nouveau_groupe.html', context)

def ListeGroupe(request):
    groupes = Groupe.objects.all()
    context = {
        'liste' : groupes,
        'tenant' : request.tenant,
    }
    return render(request,'tenant_folder/formations/groupe/liste_des_groupes.html', context)

def detailsGroupe(request, pk):
    groupe = Groupe.objects.get(pk=pk)
    students = GroupeLine.objects.filter(groupe = groupe)
    context = {
        'groupe' : groupe,
        'students' : students,
        'tenant' : request.tenant,
    }
    return render(request,'tenant_folder/formations/groupe/details_du_groupe.html', context)
