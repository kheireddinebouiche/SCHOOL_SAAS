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
from datetime import datetime, timedelta

@login_required(login_url="institut_app:login")
def PageSuivieCours(request):
    return render(request, 'tenant_folder/timetable/avancement/suivie_cours.html')

@login_required(login_url="institut_app:login")
def ApiGetCours(request):
    seances = (LigneRegistrePresence.objects
               .filter()
               .annotate(
                    total=Count('seance_module'),
                    faites=Count('seance_module', filter=Q(seance_module__is_done=True))
                )
            ).values('id','module__id','module__label','module__code','module__duree','registre__groupe__nom','registre__groupe__annee_scolaire','registre__semestre','total','faites')
    
    groupes = Groupe.objects.all().values('id','nom')

    context = {
        'seances' : list(seances),
        'groupes' : list(groupes),
    }

    return JsonResponse(context, safe=False)



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

        SuiviCours.objects.create(
            module = obj.module,
            date_seance = date,
            ligne_presence_id = lignePresenceId,
            is_done=False,
            observation = reason,
           
        )
        return JsonResponse({"status":"success", "message":"Informations enregistrer avec succès"})

    else:
        return JsonResponse({"status":"error",'message':"Methode non autoriser"})

@login_required(login_url="institut_app:login")
def ApiHistoriqueCours(request):
    if request.method == "GET":
        moduleId = request.GET.get('moduleId')
        seanceLigne = request.GET.get('seanceLigne')

        if not moduleId or not seanceLigne:
            return JsonResponse({"status": "error", "message": "Informations manquantes"})

        # Liste des suivis du module pour cette ligne
        liste = SuiviCours.objects.filter(module_id=moduleId, ligne_presence_id=seanceLigne)

        # Informations du module
        module = LigneRegistrePresence.objects.filter(
            id=seanceLigne,
            module_id=moduleId
        ).values(
            'id',
            'teacher__nom',
            'teacher__prenom',
            'registre__groupe__nom',
            'registre__semestre',
            'module__duree',
            'module__label'
        ).first()

        # Suivis marqués comme effectués
        suivis_faits = SuiviCours.objects.filter(module_id=moduleId, is_done=True, ligne_presence_id=seanceLigne)
        cours_total = SuiviCours.objects.filter(module_id=moduleId, ligne_presence_id=seanceLigne)


        entries = TimetableEntry.objects.filter(
            cours_id=moduleId,
            timetable__groupe__in=suivis_faits.values_list('ligne_presence__registre__groupe', flat=True)
        ).distinct()

        total_duree = timedelta()
        for entry in entries:
            if entry.heure_debut and entry.heure_fin:
                debut = datetime.combine(datetime.today(), entry.heure_debut)
                fin = datetime.combine(datetime.today(), entry.heure_fin)
                total_duree += (fin - debut)

        
        if entries.exists():
            duree_seance = total_duree / entries.count()
            heures_effectuees = round((duree_seance.total_seconds() / 3600) * suivis_faits.count(), 2)
        else:
            heures_effectuees = 0.0

        duree_totale_module = module.get('module__duree', 0) if module else 0
        if duree_totale_module and duree_totale_module > 0:
            taux_progression = round((heures_effectuees / duree_totale_module) * 100, 2)
        else:
            taux_progression = 0.0

        resultats = []
        for item in liste:
            resultats.append({
                "id": item.id,
                "date_seance": item.date_seance.strftime("%d/%m/%Y") if item.date_seance else None,
                "is_done": item.is_done,
                "observation": item.observation,
                "cours": getattr(item, 'cours', ''),
                "nb_absents": item.nombre_absents(),
                "ligne_presence": item.ligne_presence.id,
            })

        absence = HistoriqueAbsence.objects.filter(ligne_presence_id=seanceLigne)
        total_absences = 0

        for i in absence:
            historique = i.historique or []
            for entry in historique:
                for d in entry.get('data', []):
                    if d.get('etat') == 'A':
                        total_absences += 1

        data = {
            'resultats': resultats,
            'module': module,
            'heures_effectuees': heures_effectuees,
            'cours_effectuer': suivis_faits.count(),
            'cours_total': cours_total.count(),
            'taux_progression': taux_progression,
            'total_absences': total_absences,
        }

        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})



@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateSeanceNotes(request):
    if request.method == "POST":
        seance_id = request.POST.get('seance_id')
        notes = request.POST.get('notes')
        
        if not seance_id or not notes:
            return JsonResponse({"status": "error", "message": "Informations manquantes"})
        
        try:
            seance = SuiviCours.objects.get(id=seance_id)
            seance.cours = notes
            seance.save()
            return JsonResponse({"status": "success", "message": "Notes mises à jour avec succès"})
        except SuiviCours.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Séance non trouvée"})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})