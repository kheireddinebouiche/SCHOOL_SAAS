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
    session = SessionExam.objects.all().values('id','code','label','date_debut','date_fin')
    
    return JsonResponse(list(session), safe=False)

def ApiDeleteSession(request):
    id = request.GET.get('id')
    obj = SessionExam.objects.get(id = id)
    obj.delete()
    return JsonResponse({'status' : True, 'message': 'La session à été supprimée avec succès'})


    