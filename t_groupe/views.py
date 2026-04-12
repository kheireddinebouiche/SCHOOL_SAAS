from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from t_formations.models import *
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from t_conseil.models import Thematiques, Devis, Participant
from t_crm.models import Prospets, UserActionLog
from institut_app.models import Entreprise

@login_required(login_url="insitut_app:login")
@transaction.atomic
def NewGroupe(request):
    form = NewGroupeForms()
    if request.method == "POST":
        form = NewGroupeForms(request.POST)
        if form.is_valid():
            
            groupe = form.save(commit=False)
            groupe.createdy = request.user
            groupe.save()

            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='Groupe',
                target_id=str(groupe.id),
                details=f"Création du groupe {groupe.nom}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

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
        return JsonResponse({"status":"error", "message":"méthode non autorisée"})

@login_required(login_url='institut_app:login')
def ApiSelectSpecialite(request):
    if request.method == 'GET':
        value = request.GET.get('formation')
        if not value:
            return JsonResponse({"status":'error',"message":"Valeurs manquantes"})
        
        liste= Specialites.objects.filter(formation__code=value).values('id','label','version','abr')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status" : "error",'message':"méthode non autorisée"})

@login_required(login_url="institut_app:login")
def ApiListePromo(request):
    if request.method == "GET":
        liste = Promos.objects.filter().values('id','code','begin_year','end_year','session')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error","message" :"méthode non autorisée"})

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
        groupe = Groupe.objects.create(
            nom = id_numero_groupe,
            annee_scolaire = _annee_scolaire,
            promotion = Promos.objects.get(id=id_promotion),
            num_groupe = id_numero_libre,
            min_student = min_student,
            max_student = max_student,
            start_date = start_date,
            end_date = end_date,
            specialite_id = _formSelectSpecialite,
            createdy = request.user,
        )

        UserActionLog.objects.create(
            user=request.user,
            action_type='CREATE',
            target_model='Groupe',
            target_id=str(groupe.id),
            details=f"Création du groupe {groupe.nom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        messages.success(request,"Le groupe a été créé avec succès")
        return JsonResponse({"status":"success"})
    except Exception as e:
        return JsonResponse({"status":"error",'message':str(e)})

@login_required(login_url="insitut_app:login")
def ListeGroupe(request):
    groupes_list = Groupe.objects.all().order_by('-id')
    
    # Pagination
    paginator = Paginator(groupes_list, 10) # 10 groups per page
    page = request.GET.get('page')
    
    try:
        groupes = paginator.page(page)
    except PageNotAnInteger:
        groupes = paginator.page(1)
    except EmptyPage:
        groupes = paginator.page(paginator.num_pages)
        
    context = {
        'liste' : groupes,
        'tenant' : request.tenant,
        'page_title': "Liste des Groupes",
    }
    return render(request,'tenant_folder/formations/groupe/liste_des_groupes.html', context)

@login_required(login_url="insitut_app:login")
def ApiGetGroupeList(request):
    liste = Groupe.objects.all().values('id', 'nom', 'specialite__label', 'promotion__code')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def detailsGroupe(request, pk):
    from t_tresorerie.models import EcheancierPaiementLine,EcheancierPaiement
    from django.core.serializers.json import DjangoJSONEncoder
    from pdf_editor.models import DocumentTemplate
    import json

    groupe = Groupe.objects.get(pk=pk)
    students = GroupeLine.objects.filter(groupe = groupe)

    from t_etudiants.models import StudentTransferRequest
    all_requests = StudentTransferRequest.objects.filter(origin_group=groupe).order_by('-created_at')
    transfer_dict = {}
    for req in all_requests:
        if req.student_id not in transfer_dict:
            transfer_dict[req.student_id] = {
                'status': req.status,
                'status_display': req.get_status_display(),
                'target_specialty': req.target_specialty.label if req.target_specialty else '',
                'target_promo': req.target_promo.code if req.target_promo else '',
                'reason': req.reason or 'Aucun motif renseigné',
                'rejection_reason': req.rejection_reason or '',
                'date': req.created_at.strftime('%d/%m/%Y %H:%M')
            }
    import json
    transfer_data_json = json.dumps(transfer_dict)

    documents = groupe.specialite.formation.documents.all()

    context = {
        'groupe' : groupe,
        'students' : students,
        "specialite" : groupe.specialite,
        "qualification" : groupe.specialite.formation.qualification if groupe.specialite and groupe.specialite.formation else "",
        'transfer_data_json': transfer_data_json,
        "date_debut" : groupe.start_date,
        "date_fin" : groupe.end_date,
        "branche" : groupe.specialite.branche if groupe.specialite else "",
        "entreprise_details" : Entreprise.objects.get(id = groupe.specialite.formation.entite_legal.id) if groupe.specialite and groupe.specialite.formation and groupe.specialite.formation.entite_legal else None,
        "logo_partenaire" : groupe.specialite.formation.partenaire.logo.url if groupe.specialite and groupe.specialite.formation and groupe.specialite.formation.partenaire and groupe.specialite.formation.partenaire.logo else "",
        "documents" : documents,
        #"active_templates": DocumentTemplate.objects.filter(is_active=True), # Filtrer par type si nécessaire, ex: template_type='student_info'
        "active_templates": documents, # Filtrer par type si nécessaire, ex: template_type='student_info'
        "double_students": students.filter(student__is_double = True),
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
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='Groupe',
                target_id=str(groupe.id),
                details=f"Modification du groupe {groupe.nom}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request,"Les informations du groupe ont été modifiées avec succès")
            return redirect("t_groupe:detailsgroupe", pk)
        else:
            messages.error(request,"Une erreur s'est produite lors du traitement de la requête")
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
            return JsonResponse({"status" : "error", "message": "Informations manquantes"})
        obj = Groupe.objects.get(id = id)

        if obj.etat != "brouillon":
            return JsonResponse({"status":"error",'message':'Le groupe est en cours d\'utilisation, vous ne pouvez pas effectuer la suppression'})
        
        groupe_nom = obj.nom
        groupe_id = obj.id
        obj.delete()

        UserActionLog.objects.create(
            user=request.user,
            action_type='DELETE',
            target_model='Groupe',
            target_id=str(groupe_id),
            details=f"Suppression du groupe {groupe_nom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        messages.success(request,"Le groupe a été supprimé avec succès")
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"success",'message':"méthode non autorisée"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateGroupeCode(request):
    if request.method == "POST":
        groupeId  = request.POST.get('groupeId')
        code_partenaire = request.POST.get('code_partenaire')

        groupe = Groupe.objects.get(id = groupeId)
        groupe.code_partenaire = code_partenaire

        groupe.save()

        return JsonResponse({"status" : "success","message" : "Le code du groupe a été changé avec succès"})

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
    messages.success(request, "Le groupe a été clôturé avec succès")
    return redirect('t_groupe:detailsgroupe', pk)

@login_required(login_url="institut_app:login")
def deleteGroupe(request, pk):
    groupe = Groupe.objects.get(id=pk)
    if groupe.etat == "brouillon":
        groupe_nom = groupe.nom
        groupe_id = groupe.id
        groupe.delete()
        
        UserActionLog.objects.create(
            user=request.user,
            action_type='DELETE',
            target_model='Groupe',
            target_id=str(groupe_id),
            details=f"Suppression du groupe {groupe_nom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        messages.success(request, "Groupe supprimé avec succès")
        return redirect('t_groupe:listegroupes')
    else:
        messages.error(request, "Le groupe ne peut pas être supprimé")
        return redirect('t_groupe:listegroupes')

def PrintSuivieCours(request):
    pass

def PrintPvExamen(request):
    pass

@login_required(login_url="institut_app:login")
def ApiCloseGroupInscription(request, pk):
    groupe = Groupe.objects.get(id=pk)
    groupe.etat = 'inscription_terminee'
    groupe.save()
    messages.success(request, f"L'inscription au groupe {groupe.nom} est désormais terminée.")
    return redirect('t_groupe:detailsgroupe', pk=pk)

@login_required(login_url="institut_app:login")
def ApiOpenGroupInscription(request, pk):
    groupe = Groupe.objects.get(id=pk)
    groupe.etat = 'inscription'
    groupe.save()
    messages.success(request, f"L'inscription au groupe {groupe.nom} est désormais réouverte.")
    return redirect('t_groupe:detailsgroupe', pk=pk)
