import os

content = """
from t_timetable.models import TimetableEntry

@login_required(login_url="institut_app:login")
def ChargeHoraireFormateur(request):
    formateurs = Formateurs.objects.all()
    formateur_id = request.GET.get('formateur_id')
    mode_calcul = request.GET.get('mode', 'standard')
    
    selected_formateur = None
    workload_data = []
    totaux = {'hebdo': 0, 'mensuel_standard': 0, 'mensuel_reel': 0, 'semestre': 0}

    if formateur_id:
        try:
            selected_formateur = Formateurs.objects.get(id=formateur_id)
            entries = TimetableEntry.objects.filter(formateur=selected_formateur)
            
            # Group by (groupe, semestre)
            grouped = {}
            for entry in entries:
                key = (entry.timetable.groupe.nom if entry.timetable and entry.timetable.groupe else 'Inconnu', entry.timetable.semestre if entry.timetable else '')
                if key not in grouped:
                    grouped[key] = {
                        'lundi': 0, 'mardi': 0, 'mercredi': 0, 'jeudi': 0, 
                        'vendredi': 0, 'samedi': 0, 'dimanche': 0
                    }
                
                # Calculate hours
                if entry.heure_debut and entry.heure_fin:
                    t1 = entry.heure_debut
                    t2 = entry.heure_fin
                    dt1 = datetime.combine(datetime.today(), t1)
                    dt2 = datetime.combine(datetime.today(), t2)
                    duration = (dt2 - dt1).total_seconds() / 3600.0
                    
                    jour_lower = entry.jour.lower() if entry.jour else ''
                    if 'lun' in jour_lower: grouped[key]['lundi'] += duration
                    elif 'mar' in jour_lower: grouped[key]['mardi'] += duration
                    elif 'mer' in jour_lower: grouped[key]['mercredi'] += duration
                    elif 'jeu' in jour_lower: grouped[key]['jeudi'] += duration
                    elif 'ven' in jour_lower: grouped[key]['vendredi'] += duration
                    elif 'sam' in jour_lower: grouped[key]['samedi'] += duration
                    elif 'dim' in jour_lower: grouped[key]['dimanche'] += duration
            
            for (groupe, semestre), stats in grouped.items():
                total_hebdo = sum(stats.values())
                
                row = {
                    'groupe': groupe,
                    'semestre': f"Semestre {semestre}" if semestre.isdigit() else semestre,
                    'jour_stats': {k: round(v, 2) for k, v in stats.items()},
                    'total_hebdomadaire': round(total_hebdo, 2),
                    'mensuel_standard': round(total_hebdo * 4, 2),
                    'mensuel_reel': round(total_hebdo * 4.33, 2),
                    'semestre_total': round(total_hebdo * 14, 2)
                }
                workload_data.append(row)
                
                totaux['hebdo'] += total_hebdo
                
            totaux['mensuel_standard'] = round(totaux['hebdo'] * 4, 2)
            totaux['mensuel_reel'] = round(totaux['hebdo'] * 4.33, 2)
            totaux['semestre'] = round(totaux['hebdo'] * 14, 2)
            totaux['hebdo'] = round(totaux['hebdo'], 2)
                
        except Formateurs.DoesNotExist:
            pass
            
    context = {
        'formateurs': formateurs,
        'selected_formateur': selected_formateur,
        'mode_calcul': mode_calcul,
        'totaux': totaux,
        'workload_data': workload_data
    }
    
    return render(request, 'tenant_folder/formateur/charge_horaire.html', context)
"""

with open(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_formations\f_views\formateurs.py', 'a', encoding='utf-8') as f:
    f.write(content)
