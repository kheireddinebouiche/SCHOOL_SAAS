from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='institut_app:login')
def ListeThematique(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/conseil/liste-des-thematiques.html', context)


@login_required(login_url='institut_app:login')
def AddNewDevis(request):
    form = NewDevisForms()
    if request.method == "POST":
        form = NewDevisForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Devis ajouté avec succès.")
            return redirect('t_conseil:configure-devis', pk=form.instance.num_devis)
        else:
            messages.error(request, "Erreur lors de l'ajout du devis.")
            return redirect('t_conseil:AddNewDevis')

    context = {
        'form' : form,
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/conseil/nouveau-devis.html', context)

@login_required(login_url='institut_app:login')
def configure_devis(request, pk):
    if pk is None:
        return redirect('t_conseil:AddNewDevis')
    else:
        devis = Devis.objects.get(num_devis=pk)
        lignes_devis = devis.lignes_devis.all()

        context = {
            'tenant' : request.tenant,
            'devis' : devis,
            'lignes_devis' : lignes_devis
        }

        return render(request, 'tenant_folder/conseil/configure-devis.html', context)
    

def make_prospect_client(request):
    pass