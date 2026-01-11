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

    # Calcul des statistiques
    total_count = registres.count()
    in_progress_count = registres.filter(status='enc').count()
    archived_count = registres.filter(status='ter').count()

    # Calcul du taux moyen de présence
    # Le calcul exact dépend de la structure du modèle, mais nous pouvons estimer en fonction
    # des séances effectuées et du nombre d'absences
    total_sessions = 0
    total_absences = 0

    for registre in registres:
        # Pour chaque registre, on va compter les séances et les absences
        lignes_registre = LigneRegistrePresence.objects.filter(registre=registre)
        for ligne in lignes_registre:
            # Compter les séances effectuées pour cette ligne
            suivi_cours_list = SuiviCours.objects.filter(ligne_presence=ligne, is_done=True)
            for seance in suivi_cours_list:
                # Utiliser la méthode nombre_absents du modèle SuiviCours
                absences_dans_seance = seance.nombre_absents()
                total_absences += absences_dans_seance
                total_sessions += 1  # Une séance peut impliquer plusieurs étudiants

    # Pour calculer le taux de présence, nous avons besoin d'avoir plus d'informations
    # Pour l'instant, nous allons estimer basé sur les données disponibles
    # Si nous avons des données d'historique d'absences, comptons le total
    historiques = HistoriqueAbsence.objects.all()
    total_records = 0
    total_presences = 0

    for historique in historiques:
        for entry in historique.historique:
            for data in entry.get("data", []):
                total_records += 1
                etat = data.get("etat", "")
                if etat.upper() == "P":  # Présent
                    total_presences += 1
                # "A" pour absent, "J" pour justifié, etc.

    # Calcul du taux moyen de présence si nous avons des données d'historique
    if total_records > 0:
        average_attendance_rate = (total_presences / total_records) * 100
    else:
        # Si aucune donnée d'historique n'est disponible, nous ne pouvons pas calculer avec précision
        # Utilisons une estimation basée sur les séances effectuées
        total_students_in_registres = 0
        for registre in registres:
            groupe_lines = GroupeLine.objects.filter(groupe=registre.groupe)
            total_students_in_registres += groupe_lines.count()

        if total_sessions > 0 and total_students_in_registres > 0:
            # Estimation: nombre total d'étudiants * nombre de séances - absences
            total_possible_attendances = total_sessions * total_students_in_registres
            if total_possible_attendances > total_absences:
                average_attendance_rate = ((total_possible_attendances - total_absences) / total_possible_attendances) * 100
            else:
                average_attendance_rate = 0
        else:
            average_attendance_rate = 0

    context = {
        'groupes': groupes,
        'registres': registres,
        'total_count': total_count,
        'in_progress_count': in_progress_count,
        'archived_count': archived_count,
        'average_attendance_rate': average_attendance_rate,
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
        return JsonResponse({"status" : "error",'message' : "Méthode non autorisée"})
    

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
def ApiLoadDatas(request):
    if request.method == "GET":
        id_ligne_presence = request.GET.get('id_ligne_presence')

        if not id_ligne_presence:
            return JsonResponse({"status" : "error","message":"Informations manquantes"})
        
        obj = LigneRegistrePresence.objects.get(id = id_ligne_presence)
        student = GroupeLine.objects.filter(groupe = obj.registre.groupe)

        liste = []
        for i in student:
            liste.append({
                "nom" : i.student.nom,
                "prenom" : i.student.prenom,
                "id_student" : i.student.id,
                "matricule_interne" : i.student.matricule_interne,
                "id" : i.id,
            })

        infos = []
        infos.append({
            "module" : obj.module.label,
            "code_module" : obj.module.code,
            "nom_formateur" : obj.teacher.nom,
            "prenom_formateur" : obj.teacher.prenom,
            
        })

        data = {
            'liste' : liste,
            'infos' : infos,
        }

        return JsonResponse(data, safe=False)


    else:
        return JsonResponse({"status" : "error"})

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

            SuiviCours.objects.create(
                is_done = True,
                ligne_presence_id = ligne_id,
                module =ligne.module,
                date_seance = date_obj,
            )

            for record in records:
                student_id = record.get("student_id")
                status = record.get("status", "P")

                etudiant = Prospets.objects.get(id=student_id)
                historique, _ = HistoriqueAbsence.objects.get_or_create(
                    etudiant=etudiant,
                    ligne_presence=ligne
                )

                module_label = ligne.module.label if ligne.module else "N/A"
                module_code  = ligne.module.code if ligne.module.code else "N/A"

                # Appel de la méthode du modèle
                historique.ajouter_entree(date_obj, module_label, module_code, status)

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