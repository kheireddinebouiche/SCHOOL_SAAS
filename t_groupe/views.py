from django.shortcuts import render, redirect
from .models import *
from .forms import *
from t_formations.models import *
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

@login_required(login_url="institut_app:login")
def ApiGetFormation(request):
    if request.method =="GET":
        liste = Formation.objects.all().values('code','nom','code')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error", "message":"methode non autoriser"})

@login_required(login_url='institut_app:login')
def ApiSelectSpecialite(request):
    if request.method == 'GET':
        value = request.GET.get('formation')
        if not value:
            return JsonResponse({"status":'error',"message":"Valeurs manquante"})
        
        liste= Specialites.objects.filter(formation__code=value).values('id','label','version','abr')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status" : "error",'message':"methode non autoriser"})

@login_required(login_url="institut_app:login")
def ApiListePromo(request):
    if request.method == "GET":
        liste = Promos.objects.filter().values('id','code','begin_year','end_year','session')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error","message" :"Methode non autoriser"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiCreateGroupe(request):
   
    _formSelectSpecialite = request.POST.get('_formSelectSpecialite')
    id_numero_groupe = request.POST.get('id_numero_groupe')
    id_numero_libre = request.POST.get('id_numero_libre')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    _annee_scolaire = request.POST.get('_annee_scolaire')
    id_promotion = request.POST.get('id_promotion')
    min_student = request.POST.get('min_student')
    max_student = request.POST.get('max_student')
    print(id_promotion)
    try:
        Groupe.objects.create(
            nom = id_numero_groupe,
            annee_scolaire = _annee_scolaire,
            promotion = Promos.objects.get(code=id_promotion),
            num_groupe = id_numero_libre,
            min_student = min_student,
            max_student = max_student,
            start_date = start_date,
            end_date = end_date,
            specialite_id = _formSelectSpecialite,
        )
        messages.success(request,"Le groupe à été crée avec succès")
        return JsonResponse({"status":"success"})
    except:
        return JsonResponse({"status":"error",'message':"Une erreur c'est produite lors du traitement"})

    

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
    from t_tresorerie.models import EcheancierPaiementLine,EcheancierPaiement
    from django.core.serializers.json import DjangoJSONEncoder
    import json

    groupe = Groupe.objects.get(pk=pk)
    students = GroupeLine.objects.filter(groupe = groupe)

    echeancier_line = EcheancierPaiementLine.objects.filter(echeancier__formation = groupe.specialite.formation).values('value','date_echeancier', 'montant_tranche')
    echeancier = EcheancierPaiement.objects.get(formation = groupe.specialite.formation)
    dossier_inscription = DossierInscription.objects.filter(formation = groupe.specialite.formation).values('label')
    montant_formation = groupe.specialite.formation.prix_formation
    documents = groupe.specialite.formation.documents.all()

    context = {
        'groupe' : groupe,
        'students' : students,
        "specialite" : groupe.specialite,
        'echeancier_line' : json.dumps(list(echeancier_line),cls=DjangoJSONEncoder),
        'frais_inscription' : echeancier.frais_inscription,
        "qualification" : groupe.specialite.formation.qualification,
        "date_debut" : groupe.start_date,
        "date_fin" : groupe.end_date,
        "branche" : groupe.specialite.branche,
        'dossier_inscription' : json.dumps(list(dossier_inscription), cls=DjangoJSONEncoder),
        "entreprise_details" : Entreprise.objects.get(id = groupe.specialite.formation.entite_legal.id),
        "logo_partenaire" : groupe.specialite.formation.partenaire.logo.url if groupe.specialite.formation.partenaire.logo else "",
        "documents" : documents,
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
@transaction.atomic
def ApiDeleteGroupe(request):
    if request.method == "GET":
        id = request.GET.get('id')
        if not id:
            return JsonResponse({"status" : "error", "message": "Information manquante"})
        obj = Groupe.objects.get(id = id)

        if obj.etat != "brouillon":
            return JsonResponse({"status":"error",'message':'Le groupe est en cours d\'utilisation, vous ne pouvez pas effectuer la suppression'})
        obj.delete()
        messages.success(request,"Le groupe à été supprimer avec succès")
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"success",'message':"methode non autoriser"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateGroupeCode(request):
    if request.method == "POST":
        groupeId  = request.POST.get('groupeId')
        code_partenaire = request.POST.get('code_partenaire')

        groupe = Groupe.objects.get(id = groupeId)
        groupe.code_partenaire = code_partenaire

        groupe.save()

        return JsonResponse({"status" : "success","message" : "Le code du groupe à été changer avec succès"})

    else:
        return JsonResponse({"status" : "erreur"})

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

@login_required(login_url="institut_app:login")
def deleteGroupe(request, pk):
    groupe = Groupe.objects.get(id=pk)
    if groupe.etat == "brouillon":
        groupe.delete()
        messages.success(request, "Groupe supprimé avec succès")
        return redirect('t_groupe:listegroupes')
    else:
        messages.error(request, "Le groupe ne peux pas etre supprimer")
        return redirect('t_groupe:listegroupes')

def PrintSuivieCours(request):
    pass

def PrintPvExamen(request):
    pass

