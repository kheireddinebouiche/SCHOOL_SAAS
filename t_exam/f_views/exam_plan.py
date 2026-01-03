from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import ModelBuilltins, BuiltinTypeNote, BuiltinSousNote
from t_formations.models import Formation, Modules
from t_timetable.models import Salle
from t_exam.models import *
from t_groupe.models import Groupe,GroupeLine
from django.db import transaction, IntegrityError
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required(login_url="institut_app:login")
def ApiSavePlannedExam(request):
    if request.method == "POST":
        pass
    else:
        return JsonResponse({"status" : "error"})


@login_required(login_url="institut_app:login")
def ApiLoadDataToPlan(request):
    if request.method == "GET":
        id_groupe = request.GET.get("id_groupe")
        if not id_groupe:
            return JsonResponse({"status":"error","message":"Informations manquante"})


        modules = []
        specialite = Groupe.objects.get(id = id_groupe)
        donnee = Modules.objects.filter(specialite = specialite.specialite)

        for i in donnee:
            modules.append({
                'id' : i.id,
                'label' : i.label,
                'code' : i.code,
            })

        salles = Salle.objects.all().values('id','nom','code')

        data = {
            'modules' : list(modules),
            'salles' : list(salles),
        }

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def get_exam_planifications(request):
    session_line_id = request.GET.get("id")

    plans = ExamPlanification.objects.filter(exam_line__id=session_line_id).order_by('id')

    data = []
    for plan in plans:
        data.append({
            'id' : plan.id,
            "module_id": plan.module.id,
            "module_nom": plan.module.label,
            "type_examen" : plan.get_type_examen_display(),
            "date": plan.date.strftime("%Y-%m-%d") if plan.date else "",
            "heure_debut": plan.heure_debut.strftime("%H:%M") if plan.heure_debut else "",
            "heure_fin": plan.heure_fin.strftime("%H:%M") if plan.heure_fin else "",
            "salle_id": plan.salle.id if plan.salle else '-',
            "salle_nom": plan.salle.nom if plan.salle else '-',
            "passed": plan.passed,
            "statut" : plan.statut,
        })

    return JsonResponse({"status": "success", "planifications": data})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiPlanExam(request):
    if request.method == "POST":
        moduleSelect = request.POST.get('moduleSelect')
        typeExamenSelect = request.POST.get('typeExamenSelect')
        modeExamenSelect = request.POST.get('modeExamenSelect')
        dateExamen = request.POST.get('dateExamen')
        salleSelect = request.POST.get('salleSelect')
        heureDebut = request.POST.get('heureDebut')
        heureFin = request.POST.get('heureFin')
        session_line_id = request.POST.get('session_line_id')

        try:
            # Only get salle if mode is 'exam' (not 'tr' or 'ligne')
            salle = None
            if modeExamenSelect == 'exam' and salleSelect:
                salle = Salle.objects.get(code=salleSelect)
            elif modeExamenSelect in ['tr', 'ligne']:
                # For 'tr' and 'ligne' modes, salle should be None
                salle = None
            else:
                # For 'exam' mode but no salle selected
                if salleSelect:
                    salle = Salle.objects.get(code=salleSelect)
                else:
                    return JsonResponse({"status":"error","message":"Veuillez sélectionner une salle pour le mode examen"})
        except Salle.DoesNotExist:
            return JsonResponse({"status":"error","message":"Salle non trouvée"})

        try:
            exam_planification = ExamPlanification.objects.create(
                exam_line = SessionExamLine.objects.get(id = session_line_id),
                salle = salle,
                date = dateExamen,
                module = Modules.objects.get(id = moduleSelect),
                heure_debut = heureDebut if modeExamenSelect == 'exam' else None,
                heure_fin = heureFin if modeExamenSelect == 'exam' else None,
                type_examen = typeExamenSelect,
                mode_examination = modeExamenSelect,
            )

            return JsonResponse({"status" : "success" , "message" : "Examen planifier avec succès"})
        except Exception as e:
            return JsonResponse({"status":"error",'message':str(e)})
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def PreviewPV(request, pk):
    obj = ExamPlanification.objects.get(id = pk)
    groupe  = SessionExamLine.objects.get(id = obj.exam_line.id)

    modeleBuiltin = ModelBuilltins.objects.get(formation = groupe.groupe.specialite.formation)
    students = GroupeLine.objects.filter(groupe_id = groupe.groupe.id)

    context = {
        'pk' : pk,
        'groupe' : groupe,
        'modele' : modeleBuiltin,
        'students' : students,
    }

    return render(request,'tenant_folder/exams/preview_exam_pv.html',context)

@login_required(login_url="institut_app:login")
@transaction.atomic
def validate_exam(request):
    if request.method == "POST":
        exam_plan_id = request.POST.get('exam_plan_id')
        comment = request.POST.get('comment')
        decision = request.POST.get('decision')
        
        if not exam_plan_id:
            return JsonResponse({"status" : "error", "message" : "Informations manquante"})

        exam_plan = ExamPlanification.objects.get(id=exam_plan_id)

        if decision == "termine":
            exam_plan.passed = True
            exam_plan.statut = "termine"

        elif decision == "nabouti":
            exam_plan.passed = False
            exam_plan.comment = comment
            exam_plan.statut = "nabouti"

        exam_plan.save()
        return JsonResponse({
            "status": "success",
            "message": "Valider avec succès"
        })
    else:
        return JsonResponse({
            "status": "error",
            "message": "Méthode non autorisée"
        })

@login_required(login_url="institut_app:login")
def GeneratePv(request, pk):
    obj = ExamPlanification.objects.get(id=pk)
    groupe = SessionExamLine.objects.get(id=obj.exam_line.id)

    modeleBuiltin = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)
    students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id)

    # Get or create the PvExamen record
    pv_examen, created = PvExamen.objects.get_or_create(exam_planification=obj)

    # If this is the first time creating the PV, create the ExamTypeNote records based on BuiltinTypeNote
    if created:
        for builtin_type_note in modeleBuiltin.types_notes.all().order_by('ordre'):
            exam_type_note = ExamTypeNote.objects.create(
                pv=pv_examen,
                code=builtin_type_note.code,
                libelle=builtin_type_note.libelle,
                max_note=builtin_type_note.max_note,
                has_sous_notes=builtin_type_note.has_sous_notes,
                nb_sous_notes=builtin_type_note.nb_sous_notes,
                ordre=builtin_type_note.ordre
            )

            # Create ExamNote records for each student for this type of note
            for student_line in students:
                exam_note = ExamNote.objects.create(
                    pv=pv_examen,
                    etudiant=student_line.student,
                    type_note=exam_type_note,
                    valeur=None
                )

                # If this type note has sous-notes, create them
                if builtin_type_note.has_sous_notes and builtin_type_note.nb_sous_notes > 0:
                    for builtin_sous_note in builtin_type_note.sous_notes.all().order_by('ordre'):
                        ExamSousNote.objects.create(
                            note=exam_note,
                            valeur=0.0  # Use 0.0 instead of None to avoid NOT NULL constraint
                        )

    # Get the builtin model to match the IDs used in the template
    modele_builtins = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)

    # Filter type notes based on exam type
    exam_type = obj.type_examen  # Get the actual type, not the display value
    if exam_type == 'normal':
        # For normal exam, show all types where both is_rattrapage and is_rachat are False
        filtered_types_notes = modele_builtins.types_notes.filter(is_rattrapage=False, is_rachat=False).order_by('ordre')
    elif exam_type == 'rattrage':
        # For rattrapage exam, show only types where is_rattrapage is True
        filtered_types_notes = modele_builtins.types_notes.filter(is_rattrapage=True).order_by('ordre')
    elif exam_type == 'rachat':
        # For rachat exam, show only types where is_rachat is True
        filtered_types_notes = modele_builtins.types_notes.filter(is_rachat=True).order_by('ordre')
    else:
        # Default case: show all type notes
        filtered_types_notes = modele_builtins.types_notes.all().order_by('ordre')

    # Create a mapping between builtin type note IDs and exam type note objects
    builtin_to_exam_mapping = {}
    for exam_type_note in pv_examen.exam_types_notes.all():
        # Find the corresponding builtin type note by code
        builtin_type_note = modele_builtins.types_notes.filter(code=exam_type_note.code).first()
        if builtin_type_note:
            builtin_to_exam_mapping[builtin_type_note.id] = exam_type_note

    # Debug: Print the mapping and data structure
    print("DEBUG - Builtin to Exam mapping:", {builtin_id: exam_note.id for builtin_id, exam_note in builtin_to_exam_mapping.items()})

    # Prepare data for the template - use builtin IDs as keys to match template
    student_notes_data = {}
    for student_line in students:
        student_notes_data[student_line.student.id] = {}
        for builtin_type_note in filtered_types_notes:  # Use filtered types instead of all
            print(f"DEBUG - Processing builtin_type_note id: {builtin_type_note.id}, code: {builtin_type_note.code}")

            # Get the corresponding exam type note
            exam_type_note = builtin_to_exam_mapping.get(builtin_type_note.id)
            if exam_type_note:
                print(f"DEBUG - Found corresponding exam_type_note id: {exam_type_note.id}")

                exam_note = ExamNote.objects.filter(
                    pv=pv_examen,
                    etudiant=student_line.student,
                    type_note=exam_type_note
                ).first()

                if exam_note:
                    sous_notes_list = list(exam_note.sous_notes.all())
                    print(f"DEBUG - Found exam_note with value: {exam_note.valeur}, sous_notes count: {len(sous_notes_list)}")

                    student_notes_data[student_line.student.id][builtin_type_note.id] = {
                        'value': exam_note.valeur if exam_note.valeur is None else float(exam_note.valeur),
                        'sous_notes': [{'valeur': float(sn.valeur) if sn.valeur is not None else None} for sn in sous_notes_list] if exam_type_note.has_sous_notes else []
                    }
                else:
                    print(f"DEBUG - No exam_note found for student {student_line.student.id} and type {exam_type_note.id}")
                    # If no exam note exists yet, create empty data structure
                    student_notes_data[student_line.student.id][builtin_type_note.id] = {
                        'value': None,
                        'sous_notes': []
                    }
            else:
                print(f"DEBUG - No corresponding exam_type_note found for builtin_type_note id: {builtin_type_note.id}")

    context = {
        'pk': pk,
        'groupe': groupe,
        'modele': modeleBuiltin,
        'filtered_types_notes': filtered_types_notes,  # Pass the filtered types
        'students': students,
        'pv_examen': pv_examen,
        'student_notes_data': student_notes_data,
    }

    return render(request, 'tenant_folder/exams/preview_exam_pv.html', context)

@login_required(login_url="institut_app:login")
def GeneratePvModal(request, pk):
    obj = ExamPlanification.objects.get(id=pk)
    groupe = SessionExamLine.objects.get(id=obj.exam_line.id)

    modeleBuiltin = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)

    # Get students from the group
    all_students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id)

    # Get the commission results for the session if it exists
    commission_results = {}
    if groupe.session.commission:
        commission_results = {
            result.etudiants.id: result.result
            for result in CommisionResult.objects.filter(
                commission=groupe.session.commission,
                modules__id=obj.module.id  # Filter by the current module
            ).distinct()
        }

    # Filter students based on commission results and exam type
    exam_type = obj.type_examen
    filtered_students = []

    for student_line in all_students:
        student_id = student_line.student.id
        commission_result = commission_results.get(student_id, None)

        # Apply filtering based on exam type and commission result
        if exam_type == 'normal':
            # For normal exam, show ALL students regardless of commission result
            # But handle their status differently in the template
            filtered_students.append(student_line)
        elif exam_type == 'rachat':
            # For rachat exam, show students with 'rach' result
            if commission_result == 'rach':
                filtered_students.append(student_line)
        elif exam_type == 'rattrage':
            # For rattrapage exam, show students with 'ajou' result
            if commission_result == 'ajou':
                filtered_students.append(student_line)
        else:
            # Default: show all students
            filtered_students.append(student_line)

    students = filtered_students

    session = groupe.session.get_type_session_display()
    date_debut = groupe.session.date_debut.date()
    date_fin = groupe.session.date_fin.date()
    module = obj.module.label
    note_eliminatoire = obj.module.n_elimate

    # Get or create the PvExamen record
    pv_examen, created = PvExamen.objects.get_or_create(exam_planification=obj)

    # If this is the first time creating the PV, create the ExamTypeNote records based on BuiltinTypeNote
    if created:
        for builtin_type_note in modeleBuiltin.types_notes.all().order_by('ordre'):
            exam_type_note = ExamTypeNote.objects.create(
                pv=pv_examen,
                code=builtin_type_note.code,
                libelle=builtin_type_note.libelle,
                max_note=builtin_type_note.max_note,
                has_sous_notes=builtin_type_note.has_sous_notes,
                nb_sous_notes=builtin_type_note.nb_sous_notes,
                ordre=builtin_type_note.ordre
            )

            # Create ExamNote records for each student for this type of note
            for student_line in students:
                exam_note = ExamNote.objects.create(
                    pv=pv_examen,
                    etudiant=student_line.student,
                    type_note=exam_type_note,
                    valeur=None
                )

                # If this type note has sous-notes, create them
                if builtin_type_note.has_sous_notes and builtin_type_note.nb_sous_notes > 0:
                    for builtin_sous_note in builtin_type_note.sous_notes.all().order_by('ordre'):
                        ExamSousNote.objects.create(
                            note=exam_note,
                            valeur=0.0  # Use 0.0 instead of None to avoid NOT NULL constraint
                        )

    # Get the builtin model to match the IDs used in the template
    modele_builtins = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)

    # Filter type notes based on exam type
    exam_type = obj.type_examen  # Get the actual type, not the display value
    if exam_type == 'normal':
        # For normal exam, show all types where both is_rattrapage and is_rachat are False
        filtered_types_notes = modele_builtins.types_notes.filter(is_rattrapage=False, is_rachat=False).order_by('ordre')
    elif exam_type == 'rattrage':
        # For rattrapage exam, show only types where is_rattrapage is True
        filtered_types_notes = modele_builtins.types_notes.filter(is_rattrapage=True).order_by('ordre')
    elif exam_type == 'rachat':
        # For rachat exam, show only types where is_rachat is True
        filtered_types_notes = modele_builtins.types_notes.filter(is_rachat=True).order_by('ordre')
    else:
        # Default case: show all type notes
        filtered_types_notes = modele_builtins.types_notes.all().order_by('ordre')

    # Create a mapping between builtin type note IDs and exam type note objects
    builtin_to_exam_mapping = {}
    for exam_type_note in pv_examen.exam_types_notes.all():
        # Find the corresponding builtin type note by code
        builtin_type_note = modele_builtins.types_notes.filter(code=exam_type_note.code).first()
        if builtin_type_note:
            builtin_to_exam_mapping[builtin_type_note.id] = exam_type_note

    # Prepare data for the template - use builtin IDs as keys to match template
    student_notes_data = {}
    for student_line in students:
        student_notes_data[student_line.student.id] = {}
        for builtin_type_note in filtered_types_notes:  # Use filtered types instead of all
            # Get the corresponding exam type note
            exam_type_note = builtin_to_exam_mapping.get(builtin_type_note.id)
            if exam_type_note:
                exam_note = ExamNote.objects.filter(
                    pv=pv_examen,
                    etudiant=student_line.student,
                    type_note=exam_type_note
                ).first()

                if exam_note:
                    sous_notes_list = list(exam_note.sous_notes.all())

                    student_notes_data[student_line.student.id][builtin_type_note.id] = {
                        'value': exam_note.valeur if exam_note.valeur is None else float(exam_note.valeur),
                        'sous_notes': [{'valeur': float(sn.valeur) if sn.valeur is not None else None} for sn in sous_notes_list] if exam_type_note.has_sous_notes else []
                    }
                else:
                    # If no exam note exists yet, create empty data structure
                    student_notes_data[student_line.student.id][builtin_type_note.id] = {
                        'value': None,
                        'sous_notes': []
                    }

    # Récupérer les décisions existantes pour ce PV
    decisions_existantes = {}
    for decision in ExamDecisionEtudiant.objects.filter(pv=pv_examen):
        decisions_existantes[decision.etudiant.id] = {
            'statut': decision.statut,
            'moyenne': decision.moyenne
        }

    # Pass commission results to template for special handling
    context = {
        'pk': pk,
        'groupe': groupe,
        'modele': modeleBuiltin,
        'filtered_types_notes': filtered_types_notes,  # Pass the filtered types
        'students': students,
        'pv_examen': pv_examen,
        'student_notes_data': student_notes_data,
        'session' : f"{session} - {date_debut}/{date_fin}",
        "module" : module,
        'note_eliminatoire' : note_eliminatoire,
        'decisions_existantes': decisions_existantes,
        'commission_results': commission_results,  # Pass commission results to template
        'exam_planification': obj,  # Pass the exam planification object to template
    }

    return render(request, 'tenant_folder/exams/preview_exam_pv_modal.html', context)

@login_required(login_url="institut_app:login")
def ShowPvModal(request, pk):
    obj = ExamPlanification.objects.get(id = pk)
    groupe  = SessionExamLine.objects.get(id = obj.exam_line.id)

    exam_type = obj.type_examen  # Get the actual type, not the display value
    exam_type_display = obj.get_type_examen_display()

    modeleBuiltin = ModelBuilltins.objects.get(formation = groupe.groupe.specialite.formation)

    # Filter type notes based on exam type
    if exam_type == 'normal':
        # For normal exam, show all types where both is_rattrapage and is_rachat are False
        filtered_types_notes = modeleBuiltin.types_notes.filter(is_rattrapage=False, is_rachat=False).order_by('ordre')
    elif exam_type == 'rattrage':
        # For rattrapage exam, show only types where is_rattrapage is True
        filtered_types_notes = modeleBuiltin.types_notes.filter(is_rattrapage=True).order_by('ordre')
    elif exam_type == 'rachat':
        # For rachat exam, show only types where is_rachat is True
        filtered_types_notes = modeleBuiltin.types_notes.filter(is_rachat=True).order_by('ordre')
    else:
        # Default case: show all type notes
        filtered_types_notes = modeleBuiltin.types_notes.all().order_by('ordre')

    students = GroupeLine.objects.filter(groupe_id = groupe.groupe.id)

    groupe_nom = groupe.groupe.nom
    module = obj.module.label
    context = {
        'pk' : pk,
        'groupe' : groupe,
        'modele' : modeleBuiltin,
        'filtered_types_notes': filtered_types_notes,  # Pass the filtered types
        'students' : students,
        'groupe_nom' : groupe_nom,
        'exam_type' : exam_type_display,
        'module' : module,
    }
    return render(request,'tenant_folder/exams/print_pv_examn_modal.html',context)

def TestExamResults(request, pk):
    """
    Test function that returns the submitted data as JSON without saving to database
    """
    if request.method == 'POST':
        try:
            # Simply return the POST data as JSON
            result_data = {
                "status": "success",
                "message": "Données reçues avec succès",
                "received_data": dict(request.POST)
            }
            return JsonResponse(result_data)
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Erreur: {str(e)}"
            })
    else:
        return JsonResponse({
            "status": "error",
            "message": "Méthode non autorisée"
        })

@login_required(login_url="institut_app:login")
def get_calculated_results(request, pk):
    """
    API pour récupérer les résultats calculés avec les moyennes des sous-notes
    """
    
    exam_plan = ExamPlanification.objects.get(id=pk)
    pv_examen = PvExamen.objects.get(exam_planification=exam_plan)

    # Récupérer les étudiants
    groupe = SessionExamLine.objects.get(id=exam_plan.exam_line.id)
    students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id)

    # Récupérer les types de notes
    exam_type_notes = pv_examen.exam_types_notes.all().order_by('ordre')

    # Préparer les données
    results_data = []
    for student_line in students:
        student_data = {
            'id': student_line.student.id,
            'nom': student_line.student.nom,
            'prenom': student_line.student.prenom,
            'notes': []
        }

        for exam_type_note in exam_type_notes:
            # Récupérer la note principale pour cet étudiant et ce type de note
            exam_note = ExamNote.objects.filter(
                pv=pv_examen,
                etudiant=student_line.student,
                type_note=exam_type_note
            ).first()

            note_data = {
                'type_note_id': exam_type_note.id,
                'type_note_libelle': exam_type_note.libelle,
                'type_note_max': exam_type_note.max_note,
                'has_sous_notes': exam_type_note.has_sous_notes,
                'nb_sous_notes': exam_type_note.nb_sous_notes,
                'valeur': exam_note.valeur if exam_note else None,
                'sous_notes': []
            }

            # Si ce type de note a des sous-notes, les récupérer
            if exam_type_note.has_sous_notes and exam_type_note.nb_sous_notes > 0:
                if exam_note:
                    sous_notes = exam_note.sous_notes.all()
                    for sous_note in sous_notes:
                        note_data['sous_notes'].append({
                            'valeur': sous_note.valeur
                        })

            student_data['notes'].append(note_data)

        results_data.append(student_data)

    return JsonResponse({
        "status": "success",
        "results_data": results_data
    })

@login_required(login_url="institut_app:login")
@transaction.atomic
def validate_pv_exam(request):
    """
    Vue pour valider le PV d'examen et enregistrer les décisions des étudiants
    """
    if request.method == "POST":
        try:
            exam_plan_id = request.POST.get('exam_plan_id')
            decisions_json = request.POST.get('decisions')

            if not exam_plan_id:
                return JsonResponse({"status": "error", "message": "ID de l'examen manquant"})

            if not decisions_json:
                return JsonResponse({"status": "error", "message": "Aucune décision fournie"})

            # Récupérer l'objet d'examen planifié
            exam_plan = ExamPlanification.objects.get(id=exam_plan_id)

            # Récupérer ou créer le PV d'examen
            pv_examen, created = PvExamen.objects.get_or_create(exam_planification=exam_plan)

            # Parser les décisions
            try:
                decisions = json.loads(decisions_json)
            except json.JSONDecodeError:
                return JsonResponse({"status": "error", "message": "Format JSON invalide pour les décisions"})

            # Enregistrer les décisions pour chaque étudiant
            for student_id, decision_data in decisions.items():
                try:
                    student_id = int(student_id)
                    statut = decision_data.get('statut')
                    moyenne = decision_data.get('moyenne')

                    if statut:  # Vérifier que le statut existe
                        # Récupérer l'étudiant
                        etudiant = Prospets.objects.get(id=student_id)

                        # Créer ou mettre à jour la décision
                        decision_etudiant, created = ExamDecisionEtudiant.objects.update_or_create(
                            pv=pv_examen,
                            etudiant=etudiant,
                            defaults={
                                'statut': statut,
                                'moyenne': moyenne
                            }
                        )
                except (ValueError, Prospets.DoesNotExist):
                    # Si l'étudiant n'existe pas, continuer avec les autres
                    continue

            # Valider le PV d'examen
            pv_examen.est_valide = True
            pv_examen.date_validation = timezone.now()
            pv_examen.save()

            return JsonResponse({
                "status": "success",
                "message": "PV d'examen validé et décisions enregistrées avec succès"
            })

        except ExamPlanification.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Examen planifié non trouvé"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Erreur lors de la validation: {str(e)}"})

    return JsonResponse({
        "status": "error",
        "message": "Méthode non autorisée"
    })


@login_required(login_url="institut_app:login")
def ApiListPvExamen(request):
    if request.method == "GET":
        # Get status filter from request parameters
        status_filter = request.GET.get('status', 'validated')  # Default to validated only

        # Build the query based on the status filter
        if status_filter == 'validated':
            # Only get validated exam planifications
            exam_planifications = ExamPlanification.objects.select_related(
                'exam_line',
                'exam_line__groupe',
                'module',
                'salle'
            ).filter(
                passed=True  # Only get validated exam planifications
            ).all()
        elif status_filter == 'pending':
            # Only get pending exam planifications
            exam_planifications = ExamPlanification.objects.select_related(
                'exam_line',
                'exam_line__groupe',
                'module',
                'salle'
            ).filter(
                passed=False  # Only get pending exam planifications
            ).all()
        else:
            # Get all exam planifications
            exam_planifications = ExamPlanification.objects.select_related(
                'exam_line',
                'exam_line__groupe',
                'module',
                'salle'
            ).all()

        # Prepare PV data
        pv_data = []
        for plan in exam_planifications:
            # Try to get the related PV - since it's OneToOne, we access it directly
            # We need to handle the case where PV doesn't exist
            try:
                pv_obj = PvExamen.objects.select_related('exam_planification').get(exam_planification=plan)
                pv_exists = True
            except PvExamen.DoesNotExist:
                pv_obj = None
                pv_exists = False

            pv_data.append({
                'id': pv_obj.id if pv_obj else None,
                'exam_planification': {
                    'id': plan.id,
                    'module': {
                        'id': plan.module.id,
                        'label': plan.module.label,
                        'code': plan.module.code,
                    },
                    'exam_line': {
                        'id': plan.exam_line.id,
                        'groupe': {
                            'id': plan.exam_line.groupe.id,
                            'nom': plan.exam_line.groupe.nom,
                        },
                        'semestre': plan.exam_line.semestre,
                    },
                    'date': plan.date.strftime("%Y-%m-%d") if plan.date else "",
                    'heure_debut': plan.heure_debut.strftime("%H:%M") if plan.heure_debut else "",
                    'heure_fin': plan.heure_fin.strftime("%H:%M") if plan.heure_fin else "",
                    'salle': {
                        'id': plan.salle.id if plan.salle else None,
                        'nom': plan.salle.nom if plan.salle else "Non spécifié",
                    } if plan.salle else {'id': None, 'nom': "Non spécifié"},
                    'type_examen': plan.get_type_examen_display(),
                    'mode_examination': plan.mode_examination,
                    'statut': plan.statut,
                    'passed': plan.passed,
                    'comment': plan.comment,
                },
                'pv_exists': pv_exists,
                'est_valide': pv_obj.est_valide if pv_obj else False,
                'date_validation': pv_obj.date_validation.strftime("%Y-%m-%d %H:%M") if pv_obj and pv_obj.date_validation else "",
            })

        # Get unique groups from the exam planifications
        groups_data = []
        group_ids = set()
        for plan in exam_planifications:
            if plan.exam_line and plan.exam_line.groupe and plan.exam_line.groupe.id not in group_ids:
                group_ids.add(plan.exam_line.groupe.id)
                groups_data.append({
                    'id': plan.exam_line.groupe.id,
                    'nom': plan.exam_line.groupe.nom,
                })

        # Return structured data as expected by the template
        response_data = {
            'pvs': pv_data,
            'groups': groups_data,
        }

        return JsonResponse(response_data)

    else:
        return JsonResponse({"status": "error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeletePvExamen(request):
    """
    API pour supprimer un PV d'examen et remettre le statut passed de l'exam planification à False
    """
    if request.method == "POST":
        try:
            pv_id = request.POST.get('pv_id')
            exam_planification_id = request.POST.get('exam_planification_id')

            # Récupérer le PV et la planification
            pv = PvExamen.objects.get(id=pv_id)
            exam_plan = ExamPlanification.objects.get(id=exam_planification_id)

            # Supprimer le PV
            pv.delete()

            # Mettre à jour le statut passed à False
            exam_plan.passed = False
            exam_plan.save()

            return JsonResponse({
                "status": "success",
                "message": "PV supprimé avec succès et examen marqué comme non validé"
            })
        except PvExamen.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "PV non trouvé"
            })
        except ExamPlanification.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Planification d'examen non trouvée"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
    else:
        return JsonResponse({
            "status": "error",
            "message": "Méthode non autorisée"
        })

@login_required(login_url="institut_app:login")    
def exams_results(request):
    """
    Vue pour afficher la liste des PVs d'examens
    """
    return render(request, 'tenant_folder/exams/exams_results.html')

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeleteExamPlanification(request):
    """
    API pour supprimer une planification d'examen
    """
    if request.method == "POST":
        try:
            exam_planification_id = request.POST.get('exam_planification_id')

            # Récupérer la planification d'examen
            exam_plan = ExamPlanification.objects.get(id=exam_planification_id)

            # Vérifier s'il y a un PV associé
            pv_examen = PvExamen.objects.filter(exam_planification=exam_plan).first()

            if pv_examen:
                # Si un PV existe et est validé, on ne peut pas supprimer
                if pv_examen.est_valide:
                    return JsonResponse({
                        "status": "error",
                        "message": "Impossible de supprimer cette planification : un PV est déjà validé pour cet examen."
                    })
                # Sinon, supprimer le PV associé
                pv_examen.delete()

            # Supprimer la planification d'examen
            exam_plan.delete()

            return JsonResponse({
                "status": "success",
                "message": "Planification d'examen supprimée avec succès"
            })
        except ExamPlanification.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "Planification d'examen non trouvée"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
    else:
        return JsonResponse({
            "status": "error",
            "message": "Méthode non autorisée"
        })

@login_required(login_url="institut_app:login")
def SaveExamResults(request, pk):
    if request.method == 'POST':
        try:
            # Get the exam planification and associated PV
            exam_plan = ExamPlanification.objects.get(id=pk)
            pv_examen = PvExamen.objects.get(exam_planification=exam_plan)

            # Check if PV is already validated
            if pv_examen.est_valide:
                return JsonResponse({
                    "status": "error",
                    "message": "PV déjà validé, modification impossible"
                })

            # Get all students for this exam
            groupe = SessionExamLine.objects.get(id=exam_plan.exam_line.id)
            students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id)

            # Get the builtin model to match the IDs used in the template
            modele_builtins = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)

            # Create a mapping between builtin type note IDs and exam type note objects
            builtin_to_exam_mapping = {}
            for exam_type_note in pv_examen.exam_types_notes.all():
                # Find the corresponding builtin type note by code
                builtin_type_note = modele_builtins.types_notes.filter(code=exam_type_note.code).first()
                if builtin_type_note:
                    builtin_to_exam_mapping[builtin_type_note.id] = exam_type_note

            # Debug: Print the expected field names to check
            print("DEBUG - Expected field patterns:")
            for student_line in students:
                student = student_line.student
                for builtin_type_note in modele_builtins.types_notes.all().order_by('ordre'):
                    exam_type_note = builtin_to_exam_mapping.get(builtin_type_note.id)
                    if exam_type_note and exam_type_note.has_sous_notes and exam_type_note.nb_sous_notes > 0:
                        for i in range(exam_type_note.nb_sous_notes):
                            expected_name = f'sous_note_{student.id}_{builtin_type_note.id}_{i}'
                            actual_value = request.POST.get(expected_name)
                            print(f"  Expected: {expected_name}, Actual value: {actual_value}")
                    elif exam_type_note:
                        expected_name = f'note_{student.id}_{builtin_type_note.id}'
                        actual_value = request.POST.get(expected_name)
                        print(f"  Expected: {expected_name}, Actual value: {actual_value}")

            # Initialize counters for visualization
            processed_data = {
                'students_processed': 0,
                'notes_updated': 0,
                'sous_notes_updated': 0,
                'sous_notes_created': 0,
                'errors': [],
                'details': [],
                'debug_info': {
                    'total_post_fields': len(request.POST),
                    'received_fields': dict(request.POST),
                    'mapping_info': {builtin_id: exam_note.id for builtin_id, exam_note in builtin_to_exam_mapping.items()}
                }
            }

            # Process the submitted notes
            for student_line in students:
                student = student_line.student
                student_details = {
                    'student_id': student.id,
                    'student_name': f"{student.nom} {student.prenom}",
                    'notes': []
                }

                # Process each type of note using the builtin model to match template
                for builtin_type_note in modele_builtins.types_notes.all().order_by('ordre'):
                    exam_type_note = builtin_to_exam_mapping.get(builtin_type_note.id)
                    if not exam_type_note:
                        continue  # Skip if no corresponding exam type note

                    type_note_details = {
                        'type_note_id': exam_type_note.id,
                        'type_note_label': exam_type_note.libelle
                    }

                    if exam_type_note.has_sous_notes and exam_type_note.nb_sous_notes > 0:
                        # Process sous-notes
                        try:
                            exam_note, created = ExamNote.objects.get_or_create(
                                pv=pv_examen,
                                etudiant=student,
                                type_note=exam_type_note
                            )
                        except Exception as e:
                            processed_data['errors'].append({
                                'student_id': student.id,
                                'type_note_id': exam_type_note.id,
                                'error': f"Failed to create/get exam note: {str(e)}"
                            })
                            continue

                        # Get all existing sous-notes for this exam note
                        try:
                            existing_sous_notes = list(exam_note.sous_notes.all())
                        except Exception as e:
                            processed_data['errors'].append({
                                'student_id': student.id,
                                'type_note_id': exam_type_note.id,
                                'error': f"Failed to get sous-notes: {str(e)}"
                            })
                            continue

                        # Process each sous-note based on form input - use builtin_type_note.id for field lookup
                        for i in range(exam_type_note.nb_sous_notes):
                            sous_note_value = request.POST.get(f'sous_note_{student.id}_{builtin_type_note.id}_{i}')

                            # Update or create the sous-note at index i
                            if i < len(existing_sous_notes):
                                # Update existing sous-note
                                sous_note = existing_sous_notes[i]
                                if sous_note_value and sous_note_value.strip() != '':
                                    try:
                                        old_value = sous_note.valeur
                                        sous_note.valeur = float(sous_note_value)
                                        sous_note.save()
                                        processed_data['sous_notes_updated'] += 1
                                        type_note_details.setdefault('sous_notes', []).append({
                                            'id': sous_note.id,
                                            'index': i,
                                            'old_value': old_value,
                                            'new_value': float(sous_note_value),
                                            'status': 'updated'
                                        })
                                    except ValueError:
                                        # Handle invalid value - skip to avoid NULL constraint
                                        type_note_details.setdefault('sous_notes', []).append({
                                            'id': sous_note.id,
                                            'index': i,
                                            'value': sous_note_value,
                                            'status': 'invalid_value_skipped'
                                        })
                                        continue
                                    except IntegrityError as e:
                                        # Handle database constraint errors
                                        print(f"Database error updating sous-note {i} for student {student.id}: {str(e)}")
                                        processed_data['errors'].append({
                                            'student_id': student.id,
                                            'type_note_id': exam_type_note.id,
                                            'sous_note_index': i,
                                            'error': str(e)
                                        })
                                        type_note_details.setdefault('sous_notes', []).append({
                                            'id': sous_note.id,
                                            'index': i,
                                            'value': sous_note_value,
                                            'status': 'database_error',
                                            'error': str(e)
                                        })
                                        continue
                                    except Exception as e:
                                        # Log the error for debugging
                                        print(f"Error updating sous-note {i} for student {student.id}: {str(e)}")
                                        processed_data['errors'].append({
                                            'student_id': student.id,
                                            'type_note_id': exam_type_note.id,
                                            'sous_note_index': i,
                                            'error': str(e)
                                        })
                                        type_note_details.setdefault('sous_notes', []).append({
                                            'id': sous_note.id,
                                            'index': i,
                                            'value': sous_note_value,
                                            'status': 'error',
                                            'error': str(e)
                                        })
                                        continue
                                else:
                                    type_note_details.setdefault('sous_notes', []).append({
                                        'id': sous_note.id,
                                        'index': i,
                                        'value': sous_note_value,
                                        'status': 'no_value_provided'
                                    })
                            else:
                                # Create new sous-note if it doesn't exist yet
                                valeur = 0.0
                                if sous_note_value and sous_note_value.strip() != '':
                                    try:
                                        valeur = float(sous_note_value)
                                    except ValueError:
                                        # Handle invalid value - use default 0.0
                                        type_note_details.setdefault('sous_notes', []).append({
                                            'index': i,
                                            'value': sous_note_value,
                                            'status': 'invalid_value_used_default'
                                        })
                                        pass

                                try:
                                    new_sous_note = ExamSousNote.objects.create(
                                        note=exam_note,
                                        valeur=valeur
                                    )
                                    processed_data['sous_notes_created'] += 1
                                    type_note_details.setdefault('sous_notes', []).append({
                                        'id': new_sous_note.id,
                                        'index': i,
                                        'value': valeur,
                                        'status': 'created'
                                    })
                                except IntegrityError as e:
                                    # Handle database constraint errors
                                    print(f"Database error creating sous-note {i} for student {student.id}: {str(e)}")
                                    processed_data['errors'].append({
                                        'student_id': student.id,
                                        'type_note_id': exam_type_note.id,
                                        'sous_note_index': i,
                                        'error': str(e)
                                    })
                                    type_note_details.setdefault('sous_notes', []).append({
                                        'index': i,
                                        'value': valeur,
                                        'status': 'database_error',
                                        'error': str(e)
                                    })
                                    continue
                                except Exception as e:
                                    # Log the error for debugging
                                    print(f"Error creating sous-note {i} for student {student.id}: {str(e)}")
                                    processed_data['errors'].append({
                                        'student_id': student.id,
                                        'type_note_id': exam_type_note.id,
                                        'sous_note_index': i,
                                        'error': str(e)
                                    })
                                    type_note_details.setdefault('sous_notes', []).append({
                                        'index': i,
                                        'value': valeur,
                                        'status': 'error',
                                        'error': str(e)
                                    })
                                    continue

                        # After updating sous-notes, recalculate the main note value
                        try:
                            exam_note.calculer_valeur()
                        except Exception as e:
                            processed_data['errors'].append({
                                'student_id': student.id,
                                'type_note_id': exam_type_note.id,
                                'error': f"Failed to calculate note value: {str(e)}"
                            })
                    else:
                        # Process main note - use builtin_type_note.id for field lookup
                        note_value = request.POST.get(f'note_{student.id}_{builtin_type_note.id}')
                        if note_value and note_value.strip() != '':
                            try:
                                note_value_float = float(note_value)
                                exam_note, created = ExamNote.objects.get_or_create(
                                    pv=pv_examen,
                                    etudiant=student,
                                    type_note=exam_type_note
                                )
                                old_value = exam_note.valeur
                                exam_note.valeur = note_value_float
                                exam_note.save()
                                processed_data['notes_updated'] += 1
                                type_note_details['note_value'] = {
                                    'old_value': old_value,
                                    'new_value': note_value_float,
                                    'status': 'updated'
                                }
                            except ValueError:
                                # Handle invalid value
                                type_note_details['note_value'] = {
                                    'value': note_value,
                                    'status': 'invalid_value_skipped'
                                }
                                pass
                            except IntegrityError as e:
                                # Handle database constraint errors
                                print(f"Database error processing note for student {student.id}, type {exam_type_note.id}: {str(e)}")
                                processed_data['errors'].append({
                                    'student_id': student.id,
                                    'type_note_id': exam_type_note.id,
                                    'error': str(e)
                                })
                                type_note_details['note_value'] = {
                                    'value': note_value,
                                    'status': 'database_error',
                                    'error': str(e)
                                }
                                continue
                            except Exception as e:
                                # Log the error for debugging
                                print(f"Error processing note for student {student.id}, type {exam_type_note.id}: {str(e)}")
                                processed_data['errors'].append({
                                    'student_id': student.id,
                                    'type_note_id': exam_type_note.id,
                                    'error': str(e)
                                })
                                type_note_details['note_value'] = {
                                    'value': note_value,
                                    'status': 'error',
                                    'error': str(e)
                                }
                                continue

                    student_details['notes'].append(type_note_details)

                processed_data['details'].append(student_details)
                processed_data['students_processed'] += 1

            return JsonResponse({
                "status": "success",
                "message": f"Résultats sauvegardés partiellement. {processed_data['notes_updated']} notes mises à jour, {processed_data['sous_notes_updated']} sous-notes mises à jour, {processed_data['sous_notes_created']} sous-notes créées. {len(processed_data['errors'])} erreurs rencontrées.",
                "processed_data": processed_data
            })
        except PvExamen.DoesNotExist:
            return JsonResponse({
                "status": "error",
                "message": "PV d'examen non trouvé"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": f"Erreur lors de la sauvegarde: {str(e)}"
            })
    else:
        return JsonResponse({
            "status": "error",
            "message": "Méthode non autorisée"
        })

def GetExamHistory(request, pk):
    """
    Function to retrieve the history of exam results for a given exam planification
    """
    try:
        exam_plan = ExamPlanification.objects.get(id=pk)
        pv_examen = PvExamen.objects.get(exam_planification=exam_plan)

        # Get all students for this exam
        groupe = SessionExamLine.objects.get(id=exam_plan.exam_line.id)
        students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id)

        history_data = {
            'exam_plan': {
                'id': exam_plan.id,
                'module': exam_plan.module.label,
                'date': exam_plan.date.strftime("%Y-%m-%d") if exam_plan.date else "",
                'type_examen': exam_plan.get_type_examen_display(),
            },
            'students': []
        }

        for student_line in students:
            student_data = {
                'student_id': student_line.student.id,
                'student_name': f"{student_line.student.nom} {student_line.student.prenom}",
                'notes': []
            }

            # Get all exam notes for this student
            exam_notes = ExamNote.objects.filter(
                pv=pv_examen,
                etudiant=student_line.student
            ).select_related('type_note')

            for exam_note in exam_notes:
                note_data = {
                    'type_note_id': exam_note.type_note.id,
                    'type_note_label': exam_note.type_note.libelle,
                    'note_value': exam_note.valeur,
                    'has_sous_notes': exam_note.type_note.has_sous_notes,
                    'sous_notes': []
                }

                if exam_note.type_note.has_sous_notes:
                    sous_notes = ExamSousNote.objects.filter(note=exam_note)
                    for sous_note in sous_notes:
                        note_data['sous_notes'].append({
                            'id': sous_note.id,
                            'valeur': sous_note.valeur
                        })

                student_data['notes'].append(note_data)

            history_data['students'].append(student_data)

        return JsonResponse({
            "status": "success",
            "history_data": history_data
        })
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Erreur lors de la récupération de l'historique: {str(e)}"
        })

@login_required(login_url="institut_app:login")
def ShowPv(request, pk):
    obj = ExamPlanification.objects.get(id = pk)
    groupe  = SessionExamLine.objects.get(id = obj.exam_line.id)

    exam_type = obj.type_examen  # Get the actual type, not the display value
    exam_type_display = obj.get_type_examen_display()

    modeleBuiltin = ModelBuilltins.objects.get(formation = groupe.groupe.specialite.formation)

    # Filter type notes based on exam type
    if exam_type == 'normal':
        # For normal exam, show all types where both is_rattrapage and is_rachat are False
        filtered_types_notes = modeleBuiltin.types_notes.filter(is_rattrapage=False, is_rachat=False).order_by('ordre')
    elif exam_type == 'rattrage':
        # For rattrapage exam, show only types where is_rattrapage is True
        filtered_types_notes = modeleBuiltin.types_notes.filter(is_rattrapage=True).order_by('ordre')
    elif exam_type == 'rachat':
        # For rachat exam, show only types where is_rachat is True
        filtered_types_notes = modeleBuiltin.types_notes.filter(is_rachat=True).order_by('ordre')
    else:
        # Default case: show all type notes
        filtered_types_notes = modeleBuiltin.types_notes.all().order_by('ordre')

    students = GroupeLine.objects.filter(groupe_id = groupe.groupe.id)

    groupe_nom = groupe.groupe.nom
    module = obj.module.label
    context = {
        'pk' : pk,
        'groupe' : groupe,
        'modele' : modeleBuiltin,
        'filtered_types_notes': filtered_types_notes,  # Pass the filtered types
        'students' : students,
        'groupe_nom' : groupe_nom,
        'exam_type' : exam_type_display,
        'module' : module,
    }
    return render(request,'tenant_folder/exams/print_pv_examn.html',context)

