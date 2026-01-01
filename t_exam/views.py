from django.shortcuts import render
from django.http import JsonResponse
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


@login_required(login_url="institut_app:login")
def ListeSession(request):
    return render(request, 'tenant_folder/exams/liste-session.html')

@transaction.atomic
def NewSession(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                SessionExam.objects.get(code = code)

                return JsonResponse({'statut': False, 'message': "Une session sous le même code existe déja."})
            
            except SessionExam.DoesNotExist:
                
                instance = form.save()
                code = instance.code
                
                return JsonResponse({'statut' : 'success','id' : code})
        else:
            return JsonResponse({'statut' : False, 'message' : "Une erreur c'est produite lors du traitement du formulaire"})
    else:
        form = SessionForm()
        return render(request, 'tenant_folder/exams/template-session-form.html', {'form': form})

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
            'type_session_label': s.get_type_session_display()
        })
    return JsonResponse(data, safe=False)

def ApiDeleteSession(request):
    id = request.GET.get('id')
    obj = SessionExam.objects.get(id = id)
    try:
        obj.delete()

        return JsonResponse({'status' : True, 'message': 'La session à été supprimée avec succès'})
    except IntegrityError as e:
        return JsonResponse({'status' : False, 'message' : str(e)})
    

@login_required(login_url="institut_app:login")
def DetailsSession(request, pk):
    context = {
        'pk' : pk,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/exams/details-session.html', context)

@login_required(login_url="institut_app:login")
def ApiGetSessionDetails(request):
    session_id = request.GET.get("id")
    
    session = SessionExam.objects.filter(id=session_id).values('label','code','date_debut','date_fin','date_fin','created_at')
    session_lines = SessionExamLine.objects.filter(session_id=session_id).values('id', 'groupe__nom','groupe__id','semestre','date_debut','date_fin')

    data = {
        'session': list(session),  
        'session_lines': list(session_lines),
    }

    return JsonResponse(data)

def ApiDeleteGroupeSessionLine(request):
    id = request.GET.get('id')

    obj = SessionExamLine.objects.get(id = id)
    obj.delete()

    return JsonResponse({'status' : 'success', 'message': "Suppréssion effectuer avec succès"})


def ApiUpdateSession(request):
    id = request.POST.get('id')
    label = request.POST.get('label')
    code = request.POST.get('code')
    date_debut = request.POST.get('date_debut')
    date_fin = request.POST.get('date_fin')
    
    if not id:
        return JsonResponse({'status' : 'error', 'message' : "ID session manquant"})
    else:    
        obj = SessionExam.objects.get(id=id)
        obj.label = label
        obj.code = code
        obj.date_debut = date_debut
        obj.date_fin = date_fin
        obj.save()
        return JsonResponse({'status' : 'success', 'message' : 'Les informations de la session on été mis à jours avec succès'})

def ApiCheckLabelDisponibility(request):
    label = request.GET.get('newLabel')

    obj = SessionExam.objects.filter(label = label)
    if obj:
        return JsonResponse({'status' : "success"})
    else:
        return JsonResponse({'status' : "error"})

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
        return JsonResponse({'status' : 'error', 'message' : 'Le groupe est déja planifier'})
    else:

        new_session_line = SessionExamLine(
            groupe = groupe,
            date_debut = date_debut,
            date_fin = date_fin,
            semestre = semestre,
            session = obj
        )

        new_session_line.save()
        return JsonResponse({'status' : 'success', 'message' : 'Le groupe à été planifier'})

def ExamConfiguration(request, pk):
    context = {
        'pk' : pk,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/exams/exams_plannification.html', context)

def ApiGetExamLineDetails(request):
    pass

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

    return JsonResponse({"status": "success","message": "Planifications enregistrées","data": planifications})

