from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from t_etudiants.models import *
from django.db.models import Count, Q


@login_required(login_url="institut_app:login")
def PageSuivieCours(request):
    seances = (LigneRegistrePresence.objects
               .filter()
               .annotate(
                    total=Count('seance_module'),
                    faites=Count('seance_module', filter=Q(seance_module__is_done=True))
                )
            )
    groupes = Groupe.objects.all()

    context = {
        'seances' : seances,
        'groupes' : groupes,
    }

    return render(request, 'tenant_folder/timetable/avancement/suivie_cours.html', context)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAddSeance(request):
    if request.method == "POST":

        is_complete = request.POST.get('is_complete')
        reason = request.POST.get('reason')
        lignePresenceId = request.POST.get('lignePresenceId')
        date = request.POST.get('date')

        if not is_complete and not reason and not lignePresenceId and not date:
            return JsonResponse({"status":"error",'message':"Informations manquantes"})
        
        obj = LigneRegistrePresence.objects.get(id = lignePresenceId)

        SuiviCours.objects.update_or_create(
            
             module = obj.module,
                date_seance = date,
                ligne_presence_id = lignePresenceId,
            defaults={
               'is_done' : False,
            'observation' : reason,
            }
        )
        return JsonResponse({"status":"success", "message":"Informations enregistrer avec succès"})

    else:
        return JsonResponse({"status":"error",'message':"Methode non autoriser"})

@login_required(login_url="institut_app:login")
def ApiHistoriqueCours(request):
    if request.method =="GET":
        moduleId = request.GET.get('moduleId')
        seanceLigne = request.GET.get('seanceLigne')

        if not moduleId and not seanceLigne:
            return JsonResponse({"status":"error",'message':"Informations manquantes"})
        
        liste = SuiviCours.objects.filter(
            module_id=moduleId,
            ligne_presence_id=seanceLigne
        )

        resultats = []
        for item in liste:
            resultats.append({
                "id": item.id,
                "date_seance": item.date_seance.strftime("%d/%m/%Y") if item.date_seance else None,
                "is_done": item.is_done,
                "observation": item.observation,
                "nb_absents": item.nombre_absents(), 
                "ligne_presence" : item.ligne_presence.id,
            })

        return JsonResponse(resultats, safe=False)
    else:
        return JsonResponse({"status":"error",'message':"Methode non autoriser"})
