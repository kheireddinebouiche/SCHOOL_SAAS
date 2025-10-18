from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from ..models import *
from django.contrib.auth.decorators import login_required
from ..forms import *
from t_crm.models import NotesProcpects, RendezVous
from django.db import transaction
from t_formations.models import *
from t_groupe.models import GroupeLine, Group
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from django.shortcuts import get_object_or_404



@login_required(login_url="institut_app:login")
def RegistrePage(request):

    groupes = Groupe.objects.all()
    registres = RegistrePresence.objects.all()

    context = {
        'groupes' : groupes,
        'registres' : registres,
    }
    return render(request, 'tenant_folder/presences/registres.html', context)


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSaveRegistreGroupe(request):
    registerName = request.POST.get('registerName')
    semester = request.POST.get('semester')
    group = request.POST.get('group')


    try:
        RegistrePresence.objects.create(
            label = registerName,
            semestre = semester,
            groupe_id = group,
        )

        return JsonResponse({"status" : "success"})
    except:
        return JsonResponse({"status" : "error"})
    

@login_required(login_url="institut_app:login")
def DetailsRegistrePresence(request, pk):
    registre = RegistrePresence.objects.get(id= pk)

    modules = ProgrammeFormation.objects.filter(specialite = registre.groupe.specialite, semestre = registre.semestre)
    enseignants = Employees.objects.filter(is_teacher = True)
    listes = LigneRegistrePresence.objects.filter(registre = registre)

    context = {
        'registre' : registre,
        'modules' : modules,
        'enseignants' : enseignants,
        'listes' : listes,
    }

    return render(request, 'tenant_folder/presences/details_registre.html', context)

@login_required(login_url="institut_app:login")
def liste_registres(request):
    if request.method == "POST":
        module_id = request.POST.get('module_id')
        teacher_id = request.POST.get('teacher_id')
        hours = request.POST.get('hours')
        type = request.POST.get('type')
        room = request.POST.get('room')
        registre_id = request.POST.get('registre_id')

        print(module_id,teacher_id,hours,type,room,registre_id)
        try:
            LigneRegistrePresence.objects.create(
                module_id = module_id,
                teacher_id = teacher_id,
                hours = hours,
                type = type,
                room = room,
                registre_id = registre_id
            )
            return JsonResponse({"status" : "success"})
        
        except Exception as e:
            error_message = str(e)
        
            return JsonResponse({ "status": "error","message": "Une erreur s'est produite lors du traitement de la requête","error": error_message})
    else:
        return JsonResponse({"status" : "error",'message' : "Methode non autoriser"})
    

@login_required(login_url="institut_app:login")
def DetailsListePresence(request, pk):
    object = LigneRegistrePresence.objects.get(id = pk)

    student = GroupeLine.objects.filter(groupe = object.registre.groupe)

    context =  {
        'etudiants' : student,
        'ligne_presence' : object,
        'pk' : pk,
    }
    return render(request, 'tenant_folder/presences/details_ligne_presence.html', context)

@login_required(login_url="institut_app:login")
@csrf_exempt
def ApiAjouterHistoriqueAbsence(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.POST.get("data"))
            ligne_id = payload.get("ligne_presence")
            date_str = payload.get("date")
            records = payload.get("records", [])

            ligne = LigneRegistrePresence.objects.get(id=ligne_id)
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            for record in records:
                student_id = record.get("student_id")
                status = record.get("status", "P")

                etudiant = Prospets.objects.get(id=student_id)
                historique, _ = HistoriqueAbsence.objects.get_or_create(
                    etudiant=etudiant,
                    ligne_presence=ligne
                )

                module_label = ligne.module.label if ligne.module else "N/A"
                heure = ligne.hours.strftime("%H") if ligne.hours else "00"

                # Appel de la méthode du modèle
                historique.ajouter_entree(date_obj, module_label, heure, status)

            return JsonResponse({"status": "success", "message": "Historique mis à jour avec succès"})
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
def ApiGetHistoriqueEtudiant(request, pk, id_ligne):
    try:
        historique_obj = get_object_or_404(HistoriqueAbsence, etudiant_id=pk, ligne_presence_id=id_ligne)
        data = historique_obj.historique or []
        return JsonResponse({"status": "success", "historique": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
def ListeDesEtudiants(request):
    liste = Prospets.objects.filter(statut = "convertit")
    context = {
        'etudiants' : liste
    }
    return render(request, 'tenant_folder/presences/liste_des_etudiants.html', context)