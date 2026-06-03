from institut_app.decorators import module_permission_required
from django.shortcuts import render
from django.http import JsonResponse, Http404
from .models import *
from .forms import *
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils import timezone
from t_etudiants.models import *
from t_timetable.models import Salle
from t_groupe.models import *
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from t_crm.models import UserActionLog


@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def ListeSession(request):
    return render(request, 'tenant_folder/exams/liste-session.html')

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('exa', 'add')
def NewSession(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                SessionExam.objects.get(code = code)

                return JsonResponse({'statut': False, 'message': "Une session sous le même code existe déjà."})
            
            except SessionExam.DoesNotExist:
                
                instance = form.save()
                code = instance.code
                
                UserActionLog.objects.create(
                    user=request.user,
                    action_type='CREATE',
                    target_model='SessionExamen',
                    target_id=str(instance.id),
                    details=f"Création de la session d'examen code: {instance.code}, libellé: {instance.label}",
                    ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
                )
                
                return JsonResponse({'statut' : 'success','id' : code})
        else:
            return JsonResponse({'statut' : False, 'message' : "Une erreur s'est produite lors du traitement du formulaire"})
    else:
        form = SessionForm()
        return render(request, 'tenant_folder/exams/template-session-form.html', {'form': form})

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def ApiListSession(request):
    session = SessionExam.objects.all()
    data = []
    for s in session:
        data.append({
            'id': s.id,
            'code': s.code,
            'label': s.label,
            'date_debut': s.date_debut,
            'date_fin': s.date_fin,
            'type_session': s.type_session,
            'status' : s.status,
            'type_session_label': s.get_type_session_display()
        })
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def ApiGetSessionDetailsById(request):
    session_id = request.GET.get("id")

    try:
        session = SessionExam.objects.get(id=session_id)
        data = {
            'id': session.id,
            'code': session.code,
            'label': session.label,
            'date_debut': session.date_debut,
            'date_fin': session.date_fin,
            'type_session': session.type_session,
            'type_session_label': session.get_type_session_display()
        }
        return JsonResponse({'status': 'success', 'data': data})
    except SessionExam.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Session non trouvée'})

@module_permission_required('exa', 'delete')
def ApiDeleteSession(request):
    id = request.GET.get('id')
    obj = SessionExam.objects.get(id = id)
    try:
        UserActionLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action_type='DELETE',
            target_model='SessionExamen',
            target_id=str(obj.id),
            details=f"Suppression de la session d'examen code: {obj.code}, libellé: {obj.label}",
            ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        )
        obj.delete()

        return JsonResponse({'status' : True, 'message': 'La session a été supprimée avec succès'})
    except IntegrityError as e:
        return JsonResponse({'status' : False, 'message' : str(e)})
    

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def DetailsSession(request, pk):
    context = {
        'pk' : pk,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/exams/details-session.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def ApiGetSessionDetails(request):
    session_id = request.GET.get("id")
    
    session = SessionExam.objects.filter(id=session_id).values('label','code','date_debut','date_fin','date_fin','created_at')
    session_lines = SessionExamLine.objects.filter(session_id=session_id).values('id', 'groupe__nom','groupe__id','semestre','date_debut','date_fin','status')

    data = {
        'session': list(session),  
        'session_lines': list(session_lines),
    }

    return JsonResponse(data)

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'delete')
def ApiDeleteGroupeSessionLine(request):
    id = request.GET.get('id')

    obj = SessionExamLine.objects.get(id = id)
    
    UserActionLog.objects.create(
        user=request.user,
        action_type='DELETE',
        target_model='SessionExamLine',
        target_id=str(obj.id),
        details=f"Suppression de la planification du groupe {obj.groupe.nom} de la session d'examen {obj.session.label}",
        ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
    )
    
    obj.delete()

    return JsonResponse({'status' : 'success', 'message': "Suppression effectuée avec succès"})

@module_permission_required('exa', 'change')
def ApiUpdateSession(request):
    id = request.POST.get('id')
    label = request.POST.get('label')
    code = request.POST.get('code')
    date_debut = request.POST.get('date_debut')
    date_fin = request.POST.get('date_fin')
    type_session = request.POST.get('type_session')

    if not id:
        return JsonResponse({'status' : 'error', 'message' : "ID session manquant"})
    else:
        obj = SessionExam.objects.get(id=id)
        obj.label = label
        obj.code = code
        obj.date_debut = date_debut
        obj.date_fin = date_fin
        if type_session:  # Only update if type_session is provided
            obj.type_session = type_session
        obj.save()

        UserActionLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action_type='UPDATE',
            target_model='SessionExamen',
            target_id=str(obj.id),
            details=f"Mise à jour de la session d'examen code: {obj.code}, libellé: {obj.label}",
            ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        )

        return JsonResponse({'status' : 'success', 'message' : 'Les informations de la session ont été mises à jour avec succès'})

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def ApiGetSessionLineDetails(request):
    id = request.GET.get('id')

    if not id:
        return JsonResponse({'status': 'error', 'message': 'ID manquant'})

    try:
        session_line = SessionExamLine.objects.get(id=id)
        data = {
            'id': session_line.id,
            'semestre': session_line.semestre,
            'date_debut': session_line.date_debut.strftime('%Y-%m-%d') if session_line.date_debut else '',
            'date_fin': session_line.date_fin.strftime('%Y-%m-%d') if session_line.date_fin else '',
        }
        return JsonResponse({'status': 'success', 'data': data})
    except SessionExamLine.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Ligne de session non trouvée'})

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'change')
def ApiUpdateGroupeSessionLine(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        semestre = request.POST.get('semestre')
        date_debut = request.POST.get('date_debut')
        date_fin = request.POST.get('date_fin')

        if not id:
            return JsonResponse({'status': 'error', 'message': 'ID manquant'})

        try:
            session_line = SessionExamLine.objects.get(id=id)
            session_line.semestre = semestre
            session_line.date_debut = date_debut
            session_line.date_fin = date_fin
            session_line.save()

            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='SessionExamLine',
                target_id=str(session_line.id),
                details=f"Mise à jour de la planification du groupe {session_line.groupe.nom} (Semestre: {semestre}, Début: {date_debut}, Fin: {date_fin}) dans la session d'examen {session_line.session.label}",
                ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
            )

            return JsonResponse({'status': 'success', 'message': 'Les informations du groupe de session ont été mises à jour avec succès'})
        except SessionExamLine.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ligne de session non trouvée'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def ApiGetExamPlanificationDetails(request):
    exam_plan_id = request.GET.get('id')

    if not exam_plan_id:
        return JsonResponse({'status': 'error', 'message': 'ID manquant'})

    try:
        exam_plan = ExamPlanification.objects.select_related('module', 'salle').get(id=exam_plan_id)
        data = {
            'id': exam_plan.id,
            'module_id': exam_plan.module.id,
            'module_nom': exam_plan.module.label,
            'type_examen': exam_plan.type_examen,
            'type_examen_label': exam_plan.get_type_examen_display(),
            'mode_examination': exam_plan.mode_examination,
            'date': exam_plan.date.strftime('%Y-%m-%d') if exam_plan.date else '',
            'salle_id': exam_plan.salle.id if exam_plan.salle else '',
            'salle_nom': exam_plan.salle.nom if exam_plan.salle else '',
            'heure_debut': exam_plan.heure_debut.strftime('%H:%M') if exam_plan.heure_debut else '',
            'heure_fin': exam_plan.heure_fin.strftime('%H:%M') if exam_plan.heure_fin else '',
        }
        return JsonResponse({'status': 'success', 'data': data})
    except ExamPlanification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Planification d\'examen non trouvée'})

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'change')
def ApiUpdateExamPlanification(request):
    if request.method == 'POST':
        exam_plan_id = request.POST.get('exam_planification_id')
        mode_examen = request.POST.get('mode_examen')
        date = request.POST.get('date')
        salle_id = request.POST.get('salle')
        heure_debut = request.POST.get('heure_debut')
        heure_fin = request.POST.get('heure_fin')

        if not exam_plan_id:
            return JsonResponse({'status': 'error', 'message': 'ID de planification manquant'})

        try:
            exam_plan = ExamPlanification.objects.get(id=exam_plan_id)

            if mode_examen:
                exam_plan.mode_examination = mode_examen
            if date:
                exam_plan.date = date
            if salle_id:
                exam_plan.salle = Salle.objects.get(id=salle_id)
            if heure_debut:
                exam_plan.heure_debut = heure_debut
            if heure_fin:
                exam_plan.heure_fin = heure_fin

            exam_plan.save()

            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='ExamPlanification',
                target_id=str(exam_plan.id),
                details=f"Mise à jour de la planification de l'examen du module {exam_plan.module.label} (Date: {date}, Salle: {exam_plan.salle.nom if exam_plan.salle else 'N/A'}, Horaires: {heure_debut} - {heure_fin})",
                ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
            )

            return JsonResponse({'status': 'success', 'message': 'La planification d\'examen a été mise à jour avec succès'})
        except ExamPlanification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Planification d\'examen non trouvée'})
        except Salle.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Salle non trouvée'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@module_permission_required('exa', 'view')
def ApiCheckAvailability(request):
    label = request.GET.get('label')
    code = request.GET.get('code')
    
    if label:
        exists = SessionExam.objects.filter(label__iexact=label).exists()
        return JsonResponse({'exists': exists, 'type': 'label'})
    
    if code:
        exists = SessionExam.objects.filter(code__iexact=code).exists()
        return JsonResponse({'exists': exists, 'type': 'code'})
    
    return JsonResponse({'error': 'No parameters provided'}, status=400)

@module_permission_required('exa', 'add')
def ApiPlaneExam(request):
    groupe = request.POST.get('groupe')
    session = request.POST.get('session')
    semestre = request.POST.get('semestre')
    date_debut = request.POST.get('date_debut')
    date_fin = request.POST.get('date_fin')

    obj = SessionExam.objects.get(id=session)
    groupe = Groupe.objects.get(id = groupe)

    find_groupe = SessionExamLine.objects.filter(groupe = groupe, semestre=semestre).exists()

    if find_groupe:
        return JsonResponse({'status' : 'error', 'message' : 'Le groupe est déjà planifié'})
    else:

        new_session_line = SessionExamLine(
            groupe = groupe,
            date_debut = date_debut,
            date_fin = date_fin,
            semestre = semestre,
            session = obj
        )

        new_session_line.save()

        UserActionLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action_type='CREATE',
            target_model='SessionExamLine',
            target_id=str(new_session_line.id),
            details=f"Planification du groupe {groupe.nom} pour la session d'examen {obj.label} (Semestre: {semestre}, Début: {date_debut}, Fin: {date_fin})",
            ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        )

        return JsonResponse({'status' : 'success', 'message' : 'Le groupe a été planifié'})

@module_permission_required('exa', 'change')
def ExamConfiguration(request, pk):
    try:
        SessionExamLine.objects.get(id=pk)
    except SessionExamLine.DoesNotExist:
        raise Http404("La planification demandée n'existe pas.")
    context = {
        'pk' : pk,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/exams/exams_plannification.html', context)

@module_permission_required('exa', 'view')
def ApiGetExamLineDetails(request):
    pass

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'add')
def ApiLoadDatasForPlanExam(request):
    id = request.GET.get('id')
    obj = SessionExamLine.objects.get(id = id)
    modules = Modules.objects.filter(specialite = obj.groupe.specialite).values('id','label')
    salles = Salle.objects.all().values('id','nom')

    data = {
        'modules' : list(modules),
        'salles' : list(salles)
    }

    return JsonResponse(data, safe=False)

@transaction.atomic
@module_permission_required('exa', 'add')
def save_exam_plan(request):
    
    session_line_id = request.POST.get("session_id")
    modules = request.POST.getlist("module[]")
    dates = request.POST.getlist("date[]")
    heures_debut = request.POST.getlist("heure_debut[]")
    heures_fin = request.POST.getlist("heure_fin[]")
    salles = request.POST.getlist("salle[]")

    if not session_line_id:
        return JsonResponse({"status" : "error", "message" : "Informations manquantes"})
    
    obj = SessionExamLine.objects.get(id =session_line_id )

    planifications = []
    erreurs = []

    for i in range(len(modules)):
        try:
            # Conversion date
            date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
            
            # Récupérer module et salle
            module_obj = Modules.objects.get(id=modules[i])
            salle_obj = Salle.objects.get(id=salles[i])
            
            # Création planification
            plan, created = ExamPlanification.objects.update_or_create(
                #exam_line=obj,
                module=module_obj,
                defaults={
                    'date':date_obj,
                    'heure_debut':heures_debut[i],
                    'heure_fin':heures_fin[i],
                    'salle':salle_obj
                }
                
            )
            
            # Ajouter à la liste des planifications créées
            planifications.append({
                "module": plan.module.label,
                "date": plan.date.strftime("%Y-%m-%d"),
                "heure_debut": str(plan.heure_debut),
                "heure_fin": str(plan.heure_fin),
                "salle": plan.salle.nom
            })
            
        except Exception as e:
            # Stocker l'erreur avec l'index ou les données concernées
            erreurs.append({
                "index": i,
                "module_id": modules[i] if i < len(modules) else None,
                "salle_id": salles[i] if i < len(salles) else None,
                "error": str(e)
            })

    # À la fin, tu peux afficher ou logger les erreurs
    if erreurs:
        for err in erreurs:
            print(f"Erreur à l'index {err['index']}: {err['error']}")

    if planifications:
        modules_list = ", ".join([p["module"] for p in planifications])
        details_str = f"Planification enregistrée pour {len(planifications)} module(s) ({modules_list}) du groupe {obj.groupe.nom} pour la session d'examen {obj.session.label}."
        
        UserActionLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action_type='CREATE',
            target_model='SessionExamLine',
            target_id=str(obj.id),
            details=details_str,
            ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        )

    return JsonResponse({"status": "success","message": "Planifications enregistrées","data": planifications})

