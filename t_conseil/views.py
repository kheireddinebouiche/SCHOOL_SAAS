from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required(login_url='institut_app:login')
def ListeThematique(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/conseil/liste-des-thematiques.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadThematique(request):
    thematique = Thematiques.objects.filter(etat  = "active").values('id', 'label', 'duree', 'prix', 'created_at')
    return JsonResponse(list(thematique), safe=False)

@login_required(login_url='institut_app:login')
def ApiSaveThematique(request):
    label = request.POST.get('label')
    duree = request.POST.get('duree')
    prix = request.POST.get('prix')
    description = request.POST.get('description')

    Thematiques.objects.create(
        label = label,
        duree = duree,
        description = description,
        prix = prix,
    )

    return JsonResponse({'status': 'success', 'message': 'Thématique ajoutée avec succès.'})

@login_required(login_url='institut_app:login')
def ApiLoadThematiqueDetails(request):
    id_thematique = request.GET.get('id_thematique')
    obj = Thematiques.objects.filter(id = id_thematique)
    data =[]
    for i in obj:
        data = {
            'id': i.id,
            'label': i.label,
            'description': i.description,
            'prix': i.prix,
            'duree': i.duree,
        }
    return JsonResponse(data, safe=False)

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

@login_required(login_url="institut_app:login")
def ListeDesDevis(request):
    devis = Devis.objects.all()
    context = {
        "devis" : devis,
    }
    return render(request,'tenant_folder/conseil/liste_des_devis.html', context)

@login_required(login_url='institut_app:login')
def ArchiveThematique(request):
    context = {
        'tenant' : request.tenant
    }

    return render(request, 'tenant_folder/conseil/archive_thematique.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadArchivedThematique(request):
    thematique = Thematiques.objects.filter(etat = "archive").values('id', 'label', 'duree', 'prix', 'created_at')
    return JsonResponse(list(thematique), safe=False)

@login_required(login_url='institut_app:login')
def ApiArchiveThematique(request):
    id_thematique = request.POST.get('id_thematique')
    thematique = Thematiques.objects.get(id=id_thematique)
    thematique.etat = "archive"
    thematique.save()
    return JsonResponse({'status': 'success', 'message': 'Thématique archivée avec succès.'})   
    
@login_required(login_url='institut_app:login')
def ApiActivateThematique(request):
    id_thematique = request.POST.get('id_thematique')
    thematique = Thematiques.objects.get(id=id_thematique)
    thematique.etat = "active"
    thematique.save()
    return JsonResponse({'status': 'success', 'message': 'Thématique activée avec succès.'})

def make_prospect_client(request):
    pass

def ApiUpdateThematique(request):
    pass



@login_required(login_url="institut_app:login")
def ListeProspectConseil(request):
    context ={
        'tenant' : request.tenant,
    }
    return render(request, "tenant_folder/conseil/prospect/liste_des_prospects.html",context)

@login_required(login_url="institut_app:login")
def ApiLoadProspect(request):
    pass

@login_required(login_url="institut_app:login")
def ApiTransformeToClient(request):
    pass