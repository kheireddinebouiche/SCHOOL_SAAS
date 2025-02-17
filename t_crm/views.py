from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages

def listeVisiteurs(request):
    liste = Visiteurs.objects.all()
    return render(request, 'tenant_folder/crm/liste_visiteurs.html', {'liste': liste})

def nouveauVisiteur(request):
    form = VisiteurForm()
    if request.method == 'POST':
        form = VisiteurForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visiteur ajouté avec succès')
            return redirect('t_crm:liste_visiteurs')
    else:
        context = {
            'form' : form,
        }
        return render(request, 'tenant_folder/crm/nouveau_visiteur.html', context)

def modifierVisiteur(request, id):
    pass

def supprimerVisiteur(request, id):
    pass

def detailsVisiteur(request, pk):
    obj = Visiteurs.objects.get(id = pk)
    return render(request,'tenant_folder/crm/details_visiteur.html')
