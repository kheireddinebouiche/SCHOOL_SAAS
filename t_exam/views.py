from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import *
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def ListeSession(request):
    return render(request, 'tenant_folder/exams/liste-session.html', {'tenant' : request.tenant})

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
    obj.delete()
    return JsonResponse({'status' : True, 'message': 'La session à été supprimée avec succès'})

def DetailsSession(request, pk):
    context = {
        'pk' : pk,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/exams/details-session.html', context)

def ApiGetSessionDetails(request):
    session_id = request.GET.get("id")
    
    session = SessionExam.objects.filter(id=session_id).values('label','code','date_debut','date_fin','date_fin','created_at')
    session_lines = SessionExamLine.objects.filter(session_id=session_id).values('id', 'groupe__nom','semestre','date_debut','date_fin')

    data = {
        'session': list(session),  
        'session_lines': list(session_lines),
    }

    return JsonResponse(data)

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
    salles = SalleClasse.objects.all().values('id','label')

    data = {
        'modules' : list(modules),
        'salles' : list(salles)
    }

    return JsonResponse(data, safe=False)

def get_exam_planifications(request):
    session_line_id = request.GET.get("id")
    
    plans = ExamPlanification.objects.filter(exam_line__id=session_line_id)

    data = []
    for plan in plans:
        data.append({
            "module_id": plan.module.id,
            "module_nom": plan.module.label,
            "date": plan.date.strftime("%Y-%m-%d") if plan.date else "",
            "heure_debut": plan.heure_debut.strftime("%H:%M") if plan.heure_debut else "",
            "heure_fin": plan.heure_fin.strftime("%H:%M") if plan.heure_fin else "",
            "salle_id": plan.salle.id,
            "salle_nom": plan.salle.label
        })

    return JsonResponse({"status": "success", "planifications": data})

@csrf_exempt 
def save_exam_plan(request):
    if request.method == "POST":
        

        session_line_id = request.POST.get("session_line_id")
        modules = request.POST.getlist("module[]")
        dates = request.POST.getlist("date[]")
        heures_debut = request.POST.getlist("heure_debut[]")
        heures_fin = request.POST.getlist("heure_fin[]")
        salles = request.POST.getlist("salle[]")

        obj = SessionExamLine.objects.get(id =session_line_id )

        planifications = []

        for i in range(len(modules)):
            date_obj = datetime.strptime(dates[i], "%Y-%m-%d")

            plan, created  = ExamPlanification.objects.update_or_create(
                exam_line=obj,
                module = Modules.objects.get(id=modules[i]),
                defaults={
                    'date': date_obj,
                    'heure_debut': heures_debut[i],
                    'heure_fin': heures_fin[i],
                    'salle': SalleClasse.objects.get(id=salles[i]),
                }
            )
            planifications.append({
                "module": plan.module.label,
                "date": plan.date.strftime("%Y-%m-%d"),
                "heure_debut": str(plan.heure_debut),
                "heure_fin": str(plan.heure_fin),
                "salle": plan.salle.label
            })

        return JsonResponse({
            "status": "success",
            "message": "Planifications enregistrées",
            "data": planifications
        })

    return JsonResponse({"status": "error", "message": "Méthode non autorisée"}, status=405)

def ModelBuilltinPage(request):
    return render(request,'tenant_folder/exams/model-builtins.html',{'tenant' : request.tenant})

def ApiListModeleBuilltins(request):
    obj = ModelBuilltins.objects.all().values('id','label','formation__nom','is_default')
    return JsonResponse(list(obj), safe=False)

def NewModelBuilltin(request):
    if request.method == "POST":
        form = BuilltinForm(request.POST)
        if form.is_valid():  
            instance =  form.save()
            id = instance.id
            return JsonResponse({'statut' : 'success','id': id})
        else:
            return JsonResponse({'statut' : False, 'message' : "Une erreur c'est produite lors du traitement du formulaire"})
    else:
        form = BuilltinForm()
        return render(request, 'tenant_folder/exams/template-modele-builtins.html', {'form': form})
    
def ApiLoadTypeNote(request):
    id = request.GET.get('id')
    modele = ModelBuilltins.objects.get(id=id)
    listeTypeNote = TypeNote.objects.filter(model_builtins = modele).values('id','label', 'eval','affichage','model_builtins__id')

    return JsonResponse(list(listeTypeNote), safe=False)

    
def ApiDeleteModelBuitltin(request):
    id = request.GET.get('id')
    obj = ModelBuilltins.objects.get(id = id)
    obj.delete()

    return JsonResponse({'status' : 'success', 'message' : 'Le modéle de builltin a été supprimer avec succès .'})

@transaction.atomic
def ApiAddNewType(request):
    label = request.POST.get('label')
    evaluation = request.POST.get('evaluation')
    affichage = request.POST.get('affichage')
    id_model = request.POST.get('id')

    obj = ModelBuilltins.objects.get(id=id_model)

    new_type_note = TypeNote(
        label = label,
        eval = evaluation,
        affichage = affichage,
        model_builtins = obj,
    )

    new_type_note.save()
    return JsonResponse({'status' : 'success', 'message':"Le type de note a été ajouter avec succès"})

def ApiDeleteTypeNote(request):
    id = request.GET.get('id')

    obj = TypeNote.objects.get(id = id)
    obj.delete()

    return JsonResponse({'status' : 'success', 'message' : "Le type de note à été supprimer avec succès."})

def ApiGetTypeNoteDetails(request):
    id = request.GET.get('id')
    obj = TypeNote.objects.get(id = id)

    data = {
        'label' : obj.label,
        'eval' : obj.eval,
        'affichage' : obj.affichage
    }

    return JsonResponse(data, safe=False)

def ApiUpdateTypeNote(request):
    pass