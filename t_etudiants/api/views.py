from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_tenants.utils import schema_context
from app.models import Institut
from t_crm.models import Prospets
from t_groupe.models import AffectationGroupe
from t_timetable.models import Timetable, TimetableEntry
from t_exam.models import ExamNote, DeliberationEtudiant
from t_formations.models import Modules
import datetime

def get_tenant_and_student(request):
    institute_code = request.GET.get('institute_code')
    matricule = request.GET.get('matricule')
    
    if not institute_code or not matricule:
        return None, None, JsonResponse({'error': 'institute_code and matricule parameters are required'}, status=400)
        
    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
    except Institut.DoesNotExist:
        return None, None, JsonResponse({'error': 'Institut invalide'}, status=404)
        
    with schema_context(tenant.schema_name):
        try:
            student = Prospets.objects.get(matricule_interne=matricule)
            return tenant, student, None
        except Prospets.DoesNotExist:
            return None, None, JsonResponse({'error': 'Étudiant introuvable'}, status=404)

@csrf_exempt
def get_student_profile_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
    tenant, student, error_response = get_tenant_and_student(request)
    if error_response:
        return error_response
        
    with schema_context(tenant.schema_name):
        affectations = AffectationGroupe.objects.filter(etudiant=student).select_related('specialite', 'groupe__promotion')
        academic_list = []
        for aff in affectations:
            academic_list.append({
                'specialite_id': aff.specialite.id if aff.specialite else None,
                'specialite': aff.specialite.label if aff.specialite else "N/A",
                'groupe': aff.groupe.nom if aff.groupe else "N/A",
                'annee_academique': aff.groupe.annee_scolaire if aff.groupe else "N/A",
                'promotion': str(aff.groupe.promotion) if aff.groupe and aff.groupe.promotion else "N/A",
                'semestre': aff.groupe.get_semestre_display() if aff.groupe else "N/A",
            })
            
        default_academic = academic_list[0] if academic_list else {
            'specialite': "Non affecté",
            'groupe': "Non affecté",
            'annee_academique': "N/A",
            'promotion': "N/A",
            'semestre': "N/A"
        }
            
        return JsonResponse({
            'status': 'success',
            'student': {
                'nom': student.nom,
                'prenom': student.prenom,
                'matricule': student.matricule_interne,
                'email': student.email,
                'telephone': student.telephone,
                'adresse': student.adresse,
                'wilaya': student.wilaya,
                'photo': student.photo.url if student.photo else None,
                'date_naissance': student.date_naissance.strftime('%d/%m/%Y') if student.date_naissance else None,
                'academic': default_academic,
                'academics': academic_list
            }
        })


@csrf_exempt
def get_student_planning_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
    tenant, student, error_response = get_tenant_and_student(request)
    if error_response:
        return error_response
        
    with schema_context(tenant.schema_name):
        affectations = AffectationGroupe.objects.filter(etudiant=student).select_related('groupe')
        if not affectations.exists():
            return JsonResponse({'status': 'success', 'planning': []})
            
        # Determine the latest (current) academic year
        years = [aff.groupe.annee_scolaire for aff in affectations if aff.groupe and aff.groupe.annee_scolaire]
        latest_year = max(years) if years else None
        
        # Filter groups to only include the ones in the latest academic year
        if latest_year:
            groups = [aff.groupe for aff in affectations if aff.groupe and aff.groupe.annee_scolaire == latest_year]
        else:
            groups = [aff.groupe for aff in affectations if aff.groupe]
            
        if not groups:
            return JsonResponse({'status': 'success', 'planning': []})
            
        # Get timetables of the groups
        timetables = Timetable.objects.filter(groupe__in=groups, is_validated=True)
        if not timetables.exists():
            timetables = Timetable.objects.filter(groupe__in=groups) # fallback to unvalidated if none validated
            
        if not timetables.exists():
            return JsonResponse({'status': 'success', 'planning': []})
            
        entries = TimetableEntry.objects.filter(timetable__in=timetables).select_related('cours', 'salle', 'formateur')
        
        planning_list = []
        for entry in entries:
            # Map day to consistent string
            day_str = entry.jour or ""
            
            planning_list.append({
                'timeStart': entry.heure_debut.strftime("%H:%M") if entry.heure_debut else "",
                'timeEnd': entry.heure_fin.strftime("%H:%M") if entry.heure_fin else "",
                'title': entry.cours.label if entry.cours else "Cours inconnu",
                'professor': f"{entry.formateur.nom} {entry.formateur.prenom}" if entry.formateur else "Enseignant non assigné",
                'room': entry.salle.nom if entry.salle else "N/A",
                'day': day_str,
                'status': 'upcoming' # simple status default, frontend can refine based on time
            })
            
        return JsonResponse({
            'status': 'success',
            'planning': planning_list
        })

@csrf_exempt
def get_student_notes_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
    tenant, student, error_response = get_tenant_and_student(request)
    if error_response:
        return error_response
        
    with schema_context(tenant.schema_name):
        # Fetch all affectations to build enrolled formations
        affectations = AffectationGroupe.objects.filter(etudiant=student).select_related('specialite__formation')
        formations_data = {}
        for aff in affectations:
            spec = aff.specialite
            if not spec:
                continue
            formation = spec.formation
            formations_data[spec.id] = {
                'specialite_id': spec.id,
                'specialite_code': spec.code or "",
                'specialite_label': spec.label or "",
                'formation_code': formation.code if formation else "",
                'formation_label': formation.nom if formation else (spec.label or ""),
                'nb_semestre': int(spec.nb_semestre) if spec.nb_semestre and spec.nb_semestre.isdigit() else 2,
                'semesters': {},
                'summary': {}
            }
            
        # Fetch all notes for the student
        exam_notes = ExamNote.objects.filter(etudiant=student).select_related(
            'pv__exam_planification__module__specialite__formation',
            'pv__exam_planification__exam_line',
            'type_note__bloc'
        )
        
        # Group notes by specialty, semester and module
        for note in exam_notes:
            planification = note.pv.exam_planification
            if not planification or not planification.module:
                continue
                
            module = planification.module
            spec = module.specialite
            if not spec:
                continue
                
            spec_id = spec.id
            if spec_id not in formations_data:
                formation = spec.formation
                formations_data[spec_id] = {
                    'specialite_id': spec.id,
                    'specialite_code': spec.code or "",
                    'specialite_label': spec.label or "",
                    'formation_code': formation.code if formation else "",
                    'formation_label': formation.nom if formation else (spec.label or ""),
                    'nb_semestre': int(spec.nb_semestre) if spec.nb_semestre and spec.nb_semestre.isdigit() else 2,
                    'semesters': {},
                    'summary': {}
                }
                
            semestre_code = planification.exam_line.semestre if planification.exam_line else '1'
            semester_key = f"S{semestre_code}"
            
            if semester_key not in formations_data[spec_id]['semesters']:
                formations_data[spec_id]['semesters'][semester_key] = {}
                
            module_id = module.id
            if module_id not in formations_data[spec_id]['semesters'][semester_key]:
                formations_data[spec_id]['semesters'][semester_key][module_id] = {
                    'title': module.label or module.code,
                    'ue': note.type_note.bloc.label if note.type_note and note.type_note.bloc else "UE",
                    'ects': module.coef or 4,
                    'status': 'pending',
                    'grades': {}
                }
                
            type_code = note.type_note.code.upper() if note.type_note else ""
            type_libelle = note.type_note.libelle.upper() if note.type_note else ""
            
            valeur = note.valeur
            max_note = note.type_note.max_note if note.type_note else None
            
            # Robust scaling
            if valeur is not None:
                if max_note is None or max_note == 0:
                    if valeur > 20.0:
                        max_note = 40.0
                    else:
                        max_note = 20.0
                
                if max_note != 20.0:
                    valeur = round((valeur / max_note) * 20.0, 2)
            
            if 'CC' in type_code or 'CONTINU' in type_libelle:
                formations_data[spec_id]['semesters'][semester_key][module_id]['grades']['cc'] = valeur
            elif 'FINAL' in type_code or 'EXAM' in type_libelle:
                formations_data[spec_id]['semesters'][semester_key][module_id]['grades']['final'] = valeur
            elif 'MOY' in type_code or 'AVG' in type_code or 'MOYENNE' in type_libelle:
                formations_data[spec_id]['semesters'][semester_key][module_id]['grades']['average'] = valeur
                
        # Format the grouped data into the expected list structure
        formatted_formations = []
        for spec_id, f_data in formations_data.items():
            semesters_dict = f_data['semesters']
            formatted_semesters = {}
            
            # Initialize semesters up to nb_semestre to ensure they exist
            for i in range(1, f_data['nb_semestre'] + 1):
                formatted_semesters[f"S{i}"] = []
                
            for sem, modules_dict in semesters_dict.items():
                if sem not in formatted_semesters:
                    formatted_semesters[sem] = []
                for mod_id, mod_info in modules_dict.items():
                    grades = mod_info['grades']
                    
                    if 'cc' in grades and 'final' in grades:
                        if grades['cc'] is not None and grades['final'] is not None:
                            grades['average'] = round((grades['cc'] + grades['final']) / 2, 2)
                    elif 'average' not in grades and 'cc' in grades and 'final' in grades:
                        if grades['cc'] is not None and grades['final'] is not None:
                            grades['average'] = round((grades['cc'] + grades['final']) / 2, 2)
                            
                    avg = grades.get('average')
                    if avg is not None:
                        mod_info['status'] = 'valid' if avg >= 10 else 'pending'
                    else:
                        mod_info['status'] = 'pending'
                        
                    formatted_semesters[sem].append(mod_info)
            
            f_data['semesters'] = formatted_semesters
            
            # Calculate dynamic overall average from modules for this formation
            all_module_averages = []
            ects_acquis = 0
            for sem, modules_list in formatted_semesters.items():
                for m in modules_list:
                    avg = m['grades'].get('average')
                    if avg is not None:
                        all_module_averages.append(avg)
                    if m['status'] == 'valid':
                        ects_acquis += m['ects']
                        
            deliberations = DeliberationEtudiant.objects.filter(
                etudiant=student,
                session_line__groupe__specialite_id=spec_id
            )
            delib_averages = [d.moyenne_semestre for d in deliberations if d.moyenne_semestre is not None]
            
            if all_module_averages:
                overall_average = round(sum(all_module_averages) / len(all_module_averages), 2)
            elif delib_averages:
                overall_average = round(sum(delib_averages) / len(delib_averages), 2)
            else:
                overall_average = 14.5
                
            f_data['summary'] = {
                'moyenne_generale': overall_average,
                'ects_acquis': ects_acquis,
                'ects_total': 30 * f_data['nb_semestre'],
                'rang_promotion': "N/A",
                'status': "Admis" if overall_average >= 10 else "En attente"
            }
            
            formatted_formations.append(f_data)
            
        # Backward compatibility for single-degree view
        default_semesters = formatted_formations[0]['semesters'] if formatted_formations else {}
        default_summary = formatted_formations[0]['summary'] if formatted_formations else {
            'moyenne_generale': 14.5,
            'ects_acquis': 0,
            'ects_total': 60,
            'rang_promotion': "N/A",
            'status': "En attente"
        }
        
        return JsonResponse({
            'status': 'success',
            'formations': formatted_formations,
            'semesters': default_semesters,
            'summary': default_summary
        })


@csrf_exempt
def get_student_attendance_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
    tenant, student, error_response = get_tenant_and_student(request)
    if error_response:
        return error_response
        
    with schema_context(tenant.schema_name):
        from t_etudiants.models import HistoriqueAbsence, LigneRegistrePresence
        
        affectations = AffectationGroupe.objects.filter(etudiant=student).select_related('specialite__formation')
        formations_data = {}
        for aff in affectations:
            spec = aff.specialite
            if not spec:
                continue
            formation = spec.formation
            formations_data[spec.id] = {
                'specialite_id': spec.id,
                'specialite_code': spec.code or "",
                'specialite_label': spec.label or "",
                'formation_code': formation.code if formation else "",
                'formation_label': formation.nom if formation else (spec.label or ""),
                'modules': {}
            }
            
            # Pre-populate all modules for this specialty
            all_modules = Modules.objects.filter(specialite_id=spec.id)
            for mod in all_modules:
                formations_data[spec.id]['modules'][mod.id] = {
                    'module_id': mod.id,
                    'module_code': mod.code or "",
                    'module_label': mod.label or "",
                    'sessions': []
                }
                
        # Fetch student attendance histories
        absences = HistoriqueAbsence.objects.filter(etudiant=student).select_related('ligne_presence__module')
        
        for abs_record in absences:
            ligne = abs_record.ligne_presence
            if not ligne or not ligne.module:
                continue
                
            module = ligne.module
            spec = module.specialite
            if not spec:
                continue
                
            spec_id = spec.id
            # If student has records for a specialty they aren't active in, add it dynamically
            if spec_id not in formations_data:
                formation = spec.formation
                formations_data[spec_id] = {
                    'specialite_id': spec.id,
                    'specialite_code': spec.code or "",
                    'specialite_label': spec.label or "",
                    'formation_code': formation.code if formation else "",
                    'formation_label': formation.nom if formation else (spec.label or ""),
                    'modules': {}
                }
                
            module_id = module.id
            if module_id not in formations_data[spec_id]['modules']:
                formations_data[spec_id]['modules'][module_id] = {
                    'module_id': module_id,
                    'module_code': module.code or "",
                    'module_label': module.label or "",
                    'sessions': []
                }
                
            # Parse history
            historique_list = abs_record.historique or []
            for entry in historique_list:
                session_date = entry.get('date') # DD/MM/YYYY
                for data_item in entry.get('data', []):
                    item_code = data_item.get('code')
                    item_module = data_item.get('module')
                    
                    if (item_code and item_code == module.code) or (item_module and item_module == module.label):
                        etat = str(data_item.get('etat', 'P')).upper()
                        reason = data_item.get('reason') or data_item.get('motif') or ""
                        
                        formations_data[spec_id]['modules'][module_id]['sessions'].append({
                            'date': session_date,
                            'status': etat,
                            'reason': reason
                        })
                        
        # Helper to sort dates
        def parse_date(date_str):
            try:
                return datetime.datetime.strptime(date_str, "%d/%m/%Y")
            except:
                return datetime.datetime.min
                
        # Format the response
        formatted_formations = []
        for spec_id, f_data in formations_data.items():
            modules_list = []
            for mod_id, mod_data in f_data['modules'].items():
                mod_data['sessions'].sort(key=lambda x: parse_date(x['date']))
                modules_list.append(mod_data)
            
            # Sort modules by label or code
            modules_list.sort(key=lambda x: x['module_label'])
            f_data['modules'] = modules_list
            formatted_formations.append(f_data)
            
        return JsonResponse({
            'status': 'success',
            'formations': formatted_formations
        })


@csrf_exempt
def get_student_finances_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
    tenant, student, error_response = get_tenant_and_student(request)
    if error_response:
        return error_response
        
    with schema_context(tenant.schema_name):
        from t_tresorerie.models import DuePaiements, Paiements
        from t_groupe.models import AffectationGroupe
        
        # Helper to format dates in French
        def format_french_date(date_obj):
            if not date_obj:
                return "N/A"
            months = {
                1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
                5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
                9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
            }
            return f"{date_obj.day} {months.get(date_obj.month, '')} {date_obj.year}"
            
        affectations = AffectationGroupe.objects.filter(etudiant=student).select_related('specialite__formation', 'groupe__promotion')
        formations_data = {}
        promo_to_spec = {}
        
        for aff in affectations:
            spec = aff.specialite
            if not spec:
                continue
            formation = spec.formation
            formations_data[spec.id] = {
                'specialite_id': spec.id,
                'specialite_code': spec.code or "",
                'specialite_label': spec.label or "",
                'formation_code': formation.code if formation else "",
                'formation_label': formation.nom if formation else (spec.label or ""),
                'annee_academique': aff.groupe.annee_scolaire if aff.groupe else "N/A",
                'installments': [],
                'total_amount': 0.0,
                'total_paid': 0.0,
                'total_remaining': 0.0,
                'status_ok': True,
                'next_due_date': None,
                'next_due_amount': 0.0
            }
            if aff.groupe and aff.groupe.promotion:
                promo_to_spec[aff.groupe.promotion.id] = spec.id
            
        default_spec_id = list(formations_data.keys())[0] if formations_data else None
        
        due_qs = DuePaiements.objects.filter(client=student, is_annulated=False).select_related('promo')
        
        for due in due_qs:
            spec_id = None
            if due.promo:
                spec_id = promo_to_spec.get(due.promo.id)
                if not spec_id:
                    from t_groupe.models import Groupe
                    groupe = Groupe.objects.filter(promotion=due.promo).first()
                    if groupe and groupe.specialite:
                        spec_id = groupe.specialite.id
                
            if not spec_id or spec_id not in formations_data:
                if default_spec_id:
                    spec_id = default_spec_id
                else:
                    from t_groupe.models import Groupe
                    groupe = Groupe.objects.filter(promotion=due.promo).first() if due.promo else None
                    spec = groupe.specialite if (groupe and groupe.specialite) else None
                    formation = spec.formation if spec else None
                    spec_id = spec.id if spec else 9999
                    formations_data[spec_id] = {
                        'specialite_id': spec_id,
                        'specialite_code': spec.code if spec else "GEN",
                        'specialite_label': spec.label if spec else "Général",
                        'formation_code': formation.code if formation else "GEN",
                        'formation_label': formation.nom if formation else "Situation générale",
                        'annee_academique': due.promo.annee_scolaire if due.promo else "N/A",
                        'installments': [],
                        'total_amount': 0.0,
                        'total_paid': 0.0,
                        'total_remaining': 0.0,
                        'status_ok': True,
                        'next_due_date': None,
                        'next_due_amount': 0.0
                    }
                    if not default_spec_id:
                        default_spec_id = spec_id
            
            is_paid = due.is_done or (due.montant_restant is not None and due.montant_restant <= 0)
            
            import datetime
            today = datetime.date.today()
            
            status = 'paid'
            if not is_paid:
                if due.date_echeance and due.date_echeance < today:
                    status = 'due'
                else:
                    status = 'future'
                    
            amount = float(due.montant_due or 0)
            remaining = float(due.montant_restant or 0)
            paid = amount - remaining
            
            formations_data[spec_id]['installments'].append({
                'id': due.id,
                'name': due.label or "Tranche",
                'date': format_french_date(due.date_echeance),
                'date_raw': due.date_echeance.isoformat() if due.date_echeance else "",
                'amount': amount,
                'remaining': remaining,
                'paid': paid,
                'status': status
            })
            
            formations_data[spec_id]['total_amount'] += amount
            formations_data[spec_id]['total_remaining'] += remaining
            formations_data[spec_id]['total_paid'] += paid
            
            if status == 'due':
                formations_data[spec_id]['status_ok'] = False
                
        # Handle payments without due_paiements (direct payments / admission / registration fees)
        unlinked_payments = Paiements.objects.filter(prospect=student, due_paiements__isnull=True)
        for p in unlinked_payments:
            if default_spec_id:
                amount_paid = float(p.montant_paye or 0)
                formations_data[default_spec_id]['total_paid'] += amount_paid
                if formations_data[default_spec_id]['total_remaining'] >= amount_paid:
                    formations_data[default_spec_id]['total_remaining'] -= amount_paid
                else:
                    formations_data[default_spec_id]['total_remaining'] = 0.0
                    
                formations_data[default_spec_id]['installments'].insert(0, {
                    'id': f"p-{p.id}",
                    'name': p.paiement_label or "Frais d'inscription / Admission",
                    'date': format_french_date(p.date_paiement),
                    'date_raw': p.date_paiement.isoformat() if p.date_paiement else "",
                    'amount': amount_paid,
                    'remaining': 0.0,
                    'paid': amount_paid,
                    'status': 'paid'
                })
                
        # Format list and calculate next due payment
        formatted_formations = []
        for spec_id, f_data in formations_data.items():
            # Sort installments by date
            f_data['installments'].sort(key=lambda x: x['date_raw'] or '9999-12-31')
            
            next_unpaid = None
            for inst in f_data['installments']:
                if inst['status'] in ['due', 'future']:
                    next_unpaid = inst
                    break
                    
            if next_unpaid:
                f_data['next_due_date'] = next_unpaid['date']
                f_data['next_due_amount'] = next_unpaid['remaining']
                
            f_data['total_amount'] = round(f_data['total_amount'], 2)
            f_data['total_paid'] = round(f_data['total_paid'], 2)
            f_data['total_remaining'] = round(f_data['total_remaining'], 2)
            
            formatted_formations.append(f_data)
            
        return JsonResponse({
            'status': 'success',
            'formations': formatted_formations
        })


@csrf_exempt
def get_student_notifications_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
    tenant, student, error_response = get_tenant_and_student(request)
    if error_response:
        return error_response
        
    with schema_context(tenant.schema_name):
        from t_tresorerie.models import DuePaiements, Paiements
        from t_etudiants.models import HistoriqueAbsence
        from t_exam.models import ExamNote
        import datetime
        
        notifications_list = []
        
        # Helper to format dates and compute human readable time diffs
        def format_time_diff(date_obj):
            if not date_obj:
                return ""
            if isinstance(date_obj, datetime.datetime):
                date_val = date_obj.date()
            else:
                date_val = date_obj
                
            today = datetime.date.today()
            diff = today - date_val
            if diff.days == 0:
                return "Aujourd'hui"
            elif diff.days == 1:
                return "Hier"
            elif diff.days < 7:
                return f"Il y a {diff.days} jours"
            else:
                months = {
                    1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
                    5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
                    9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
                }
                return f"{date_val.day} {months.get(date_val.month, '')} {date_val.year}"

        # 1. Absences & Justifications (HistoriqueAbsence)
        absences = HistoriqueAbsence.objects.filter(etudiant=student).select_related('ligne_presence__module')
        for abs_record in absences:
            module_label = abs_record.ligne_presence.module.label if (abs_record.ligne_presence and abs_record.ligne_presence.module) else "Module"
            historique_list = abs_record.historique or []
            for entry in historique_list:
                date_str = entry.get('date') # DD/MM/YYYY
                
                try:
                    date_val = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
                except:
                    date_val = datetime.date.today()
                    
                for data_item in entry.get('data', []):
                    etat = str(data_item.get('etat', 'P')).upper()
                    reason = data_item.get('reason') or data_item.get('motif') or ""
                    
                    if etat == 'A':
                        notifications_list.append({
                            'id': f"abs-{date_str}-{module_label}-absent",
                            'title': "Absence signalée",
                            'desc': f"Vous avez été marqué(e) absent(e) au cours de '{module_label}' le {date_str}.",
                            'time': format_time_diff(date_val),
                            'date_raw': date_val.isoformat(),
                            'category': 'urgent',
                            'icon': 'warning',
                            'iconBg': 'bg-error-container',
                            'iconColor': 'text-error',
                            'badge': 'ABSENCE',
                            'badgeBg': 'bg-error-container',
                            'badgeColor': 'text-error'
                        })
                    elif etat == 'J':
                        notifications_list.append({
                            'id': f"abs-{date_str}-{module_label}-justified",
                            'title': "Absence justifiée",
                            'desc': f"Votre absence au cours de '{module_label}' le {date_str} a été validée. Motif : {reason or 'Justifié'}.",
                            'time': format_time_diff(date_val),
                            'date_raw': date_val.isoformat(),
                            'category': 'academic',
                            'icon': 'task_alt',
                            'iconBg': 'bg-secondary-container',
                            'iconColor': 'text-on-secondary-container',
                            'badge': 'JUSTIFIÉ',
                            'badgeBg': 'bg-secondary-container',
                            'badgeColor': 'text-on-secondary-container'
                        })

        # 2. Exam Notes (ExamNote)
        exam_notes = ExamNote.objects.filter(etudiant=student).select_related('pv__exam_planification__module')
        for note in exam_notes:
            plan = note.pv.exam_planification if (note.pv and note.pv.exam_planification) else None
            if not plan or not plan.module:
                continue
            module_label = plan.module.label or plan.module.code
            valeur = note.valeur
            if valeur is not None:
                max_note = note.type_note.max_note if note.type_note else 20.0
                if max_note is None or max_note == 0:
                    max_note = 40.0 if valeur > 20.0 else 20.0
                if max_note != 20.0:
                    valeur = round((valeur / max_note) * 20.0, 2)
                    
                note_date = datetime.date.today()
                notifications_list.append({
                    'id': f"note-{note.id}",
                    'title': "Nouvelle note publiée",
                    'desc': f"Votre résultat pour le module '{module_label}' a été saisi. Note : {valeur}/20.",
                    'time': format_time_diff(note_date),
                    'date_raw': note_date.isoformat(),
                    'category': 'academic',
                    'icon': 'edit_square',
                    'iconBg': 'bg-primary-container',
                    'iconColor': 'text-on-primary-container',
                    'badge': 'NOTE',
                    'badgeBg': 'bg-secondary-container',
                    'badgeColor': 'text-on-secondary-container'
                })

        # 3. Due Payments (DuePaiements)
        due_qs = DuePaiements.objects.filter(client=student, is_annulated=False)
        today = datetime.date.today()
        for due in due_qs:
            is_paid = due.is_done or (due.montant_restant is not None and due.montant_restant <= 0)
            if not is_paid:
                amount = float(due.montant_due or 0)
                date_str = due.date_echeance.strftime('%d/%m/%Y') if due.date_echeance else "N/A"
                if due.date_echeance and due.date_echeance < today:
                    notifications_list.append({
                        'id': f"due-{due.id}-late",
                        'title': "Paiement en retard",
                        'desc': f"La tranche '{due.label}' de {amount:,.2f} DA est en retard depuis le {date_str}.",
                        'time': format_time_diff(due.date_echeance),
                        'date_raw': due.date_echeance.isoformat(),
                        'category': 'urgent',
                        'icon': 'gavel',
                        'iconBg': 'bg-error-container',
                        'iconColor': 'text-error',
                        'badge': 'RETARD',
                        'badgeBg': 'bg-error-container',
                        'badgeColor': 'text-error'
                    })
                else:
                    notifications_list.append({
                        'id': f"due-{due.id}-future",
                        'title': "Échéance de paiement à venir",
                        'desc': f"La tranche '{due.label}' de {amount:,.2f} DA arrive à échéance le {date_str}.",
                        'time': format_time_diff(due.date_echeance),
                        'date_raw': due.date_echeance.isoformat() if due.date_echeance else "",
                        'category': 'finance',
                        'icon': 'receipt_long',
                        'iconBg': 'bg-secondary-container',
                        'iconColor': 'text-on-secondary-container',
                        'badge': 'À PAYER',
                        'badgeBg': 'bg-surface-container-high',
                        'badgeColor': 'text-primary'
                    })

        # 4. Payments Made (Paiements)
        payments = Paiements.objects.filter(prospect=student)
        for p in payments:
            amount = float(p.montant_paye or 0)
            date_str = p.date_paiement.strftime('%d/%m/%Y') if p.date_paiement else "N/A"
            notifications_list.append({
                'id': f"pay-{p.id}",
                'title': "Versement enregistré",
                'desc': f"Votre versement de {amount:,.2f} DA pour '{p.paiement_label or 'Frais de formation'}' a été enregistré le {date_str}.",
                'time': format_time_diff(p.date_paiement),
                'date_raw': p.date_paiement.isoformat() if p.date_paiement else "",
                'category': 'finance',
                'icon': 'payments',
                'iconBg': 'bg-secondary-container',
                'iconColor': 'text-on-secondary-container',
                'badge': 'PAYÉ',
                'badgeBg': 'bg-secondary-container',
                'badgeColor': 'text-on-secondary-container'
            })

        # Sort notifications by date_raw (newest first)
        notifications_list.sort(key=lambda x: x['date_raw'] or '', reverse=True)

        return JsonResponse({
            'status': 'success',
            'notifications': notifications_list
        })
        })
