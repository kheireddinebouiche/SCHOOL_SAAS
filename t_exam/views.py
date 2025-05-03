from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .forms import *
from django.db import transaction


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
    session_lines = SessionExamLine.objects.filter(session_id=session_id).values('id', 'groupe')

    
    data = {
        'session': list(session),  
        'session_lines': list(session_lines),
    }

    return JsonResponse(data)
    