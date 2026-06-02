from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from ..form import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django_tenants.utils import schema_context
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from asgiref.sync import async_to_sync, sync_to_async
from t_crm.models import Prospets

def verify_institute(request):
    code = request.GET.get('code')
    try:
        institut = Institut.objects.get(code_tenant=code, is_active=True)
        
        if not getattr(institut, 'is_portail_active', True):
            return JsonResponse({'error': "L'institut a désactivé l'accès à la plateforme"}, status=403)
            
        return JsonResponse({'name': institut.nom,'status': 'success'})
        
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut non trouvé'}, status=404)


def verify_student(request):
    institute_code = request.GET.get('institute_code')
    matricule = request.GET.get('matricule')

    if not institute_code or not matricule:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)

    try:
        # 1. Trouver l'institut dans le schéma public
        tenant = Institut.objects.get(code_tenant=institute_code)
        
        if not getattr(tenant, 'is_portail_active', True):
            return JsonResponse({'error': "L'institut a désactivé l'accès à la plateforme"}, status=403)
            
        # 2. Basculer dans le schéma de cet institut
        with schema_context(tenant.schema_name):
            # 3. Chercher l'étudiant par son matricule interne
            student = Prospets.objects.get(matricule_interne=matricule)
            
            return JsonResponse({
                'nom': student.nom,
                'prenom': student.prenom,
                'matricule': student.matricule_interne,
                'status': 'success'
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Prospets.DoesNotExist:
        return JsonResponse({'error': 'Matricule étudiant inconnu dans cet établissement'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from django.views.decorators.csrf import csrf_exempt
import json
from t_groupe.models import AffectationGroupe

@csrf_exempt # Pour permettre l'appel depuis le frontend sans token CSRF pour le moment
def login_student(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            institute_code = data.get('institute_code')
            matricule = data.get('matricule')
            password = data.get('password')

            # 1. Trouver l'institut
            tenant = Institut.objects.get(code_tenant=institute_code)
            
            if not getattr(tenant, 'is_portail_active', True):
                return JsonResponse({'error': "L'institut a désactivé l'accès à la plateforme"}, status=403)
                
            with schema_context(tenant.schema_name):
                # 2. Trouver l'étudiant
                student = Prospets.objects.get(matricule_interne=matricule)
                
                # 3. Vérifier le mot de passe (comparaison directe selon votre modèle)
                if student.password == password:
                    affectation = AffectationGroupe.objects.filter(etudiant=student).first()
                        
                    academic_data = {
                        'specialite': "Non affecté",
                        'groupe': "Non affecté",
                        'annee_academique': "N/A",
                        'promotion': "N/A",
                        'semestre': "N/A"
                    }
   
                    if affectation:
                        academic_data.update({
                            'specialite': affectation.specialite.label if affectation.specialite else "N/A",
                            'groupe': affectation.groupe.nom if affectation.groupe else "N/A",
                            'annee_academique': affectation.groupe.annee_scolaire if affectation.groupe else "N/A",
                            'promotion': str(affectation.groupe.promotion) if affectation.groupe and affectation.groupe.promotion else "N/A",
                            'semestre': affectation.groupe.get_semestre_display() if affectation.groupe else "N/A",
                        })

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
                            # Ajout des infos académiques
                            'academic': academic_data 
                        }
                    })
                else:
                    return JsonResponse({'error': 'Mot de passe incorrect'}, status=401)

        except Institut.DoesNotExist:
            return JsonResponse({'error': 'Institut invalide'}, status=404)
        except Prospets.DoesNotExist:
            return JsonResponse({'error': 'Étudiant introuvable'}, status=404)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

from t_formations.models import Formateurs

def verify_formateur(request):
    institute_code = request.GET.get('institute_code')
    email = request.GET.get('email')

    if not institute_code or not email:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)

    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        
        with schema_context(tenant.schema_name):
            formateur = Formateurs.objects.get(email=email)
            
            return JsonResponse({
                'nom': formateur.nom,
                'prenom': formateur.prenom,
                'email': formateur.email,
                'status': 'success'
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Formateurs.DoesNotExist:
        return JsonResponse({'error': 'Formateur inconnu dans cet établissement'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def login_formateur(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            institute_code = data.get('institute_code')
            email = data.get('email')
            password = data.get('password')

            tenant = Institut.objects.get(code_tenant=institute_code)
            
            with schema_context(tenant.schema_name):
                formateur = Formateurs.objects.get(email=email)
                
                if formateur.password == password and formateur.password:
                    return JsonResponse({
                        'status': 'success',
                        'instructor': {
                            'id': formateur.id,
                            'nom': formateur.nom,
                            'prenom': formateur.prenom,
                            'email': formateur.email,
                            'telephone': formateur.telephone,
                            'diplome': formateur.diplome,
                            'dispo': formateur.dispo,
                        }
                    })
                else:
                    return JsonResponse({'error': 'Mot de passe incorrect'}, status=401)

        except Institut.DoesNotExist:
            return JsonResponse({'error': 'Institut invalide'}, status=404)
        except Formateurs.DoesNotExist:
            return JsonResponse({'error': 'Formateur introuvable'}, status=404)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


from t_groupe.models import EnseignantModule

def get_instructor_assignments_api(request):
    institute_code = request.GET.get('institute_code')
    instructor_id = request.GET.get('instructor_id')

    if not institute_code or not instructor_id:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)

    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        with schema_context(tenant.schema_name):
            # Fetch module assignments for this trainer
            assignments = EnseignantModule.objects.filter(formateur_id=instructor_id).select_related('module')
            
            # Fetch formateur dispo
            formateur = Formateurs.objects.get(id=instructor_id)
            
            data = []
            for assignment in assignments:
                data.append({
                    'id': assignment.id,
                    'module_id': assignment.module.id,
                    'module_code': assignment.module.code,
                    'module_label': assignment.module.label,
                    'specialite': assignment.module.specialite.label if assignment.module.specialite else 'N/A'
                })
                
            return JsonResponse({
                'status': 'success',
                'assignments': data,
                'dispo': formateur.dispo
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def submit_instructor_dispo_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            institute_code = data.get('institute_code')
            instructor_id = data.get('instructor_id')
            disponibilites = data.get('disponibilites', [])

            if not institute_code or not instructor_id:
                return JsonResponse({'error': 'Paramètres manquants'}, status=400)

            tenant = Institut.objects.get(code_tenant=institute_code)
            
            if not getattr(tenant, 'is_portail_active', True):
                return JsonResponse({'error': "L'institut a désactivé l'accès à la plateforme"}, status=403)
                
            with schema_context(tenant.schema_name):
                formateur = Formateurs.objects.get(id=instructor_id)
                
                # Update dispo json
                if not isinstance(formateur.dispo, dict):
                    formateur.dispo = {}
                
                formateur.dispo['disponibilites'] = disponibilites
                formateur.dispo['demande_dispo'] = False
                formateur.save()

                return JsonResponse({'status': 'success', 'dispo': formateur.dispo})
                
        except Institut.DoesNotExist:
            return JsonResponse({'error': 'Institut invalide'}, status=404)
        except Formateurs.DoesNotExist:
            return JsonResponse({'error': 'Formateur introuvable'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

from t_timetable.models import TimetableEntry
import datetime

def get_instructor_notifications_api(request):
    institute_code = request.GET.get('institute_code')
    email = request.GET.get('email')
    
    if not institute_code or not email:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)
        
    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        
        if not getattr(tenant, 'is_portail_active', True):
            return JsonResponse({'error': "L'institut a désactivé l'accès à la plateforme"}, status=403)
            
        with schema_context(tenant.schema_name):
            formateur = Formateurs.objects.get(email=email)
            
            notifications = []
            
            # Check for dispo request
            if isinstance(formateur.dispo, dict) and formateur.dispo.get('demande_dispo'):
                notifications.append({
                    'id': f"dispo_{formateur.id}",
                    'title': "Disponibilités requises",
                    'desc': "L'administration vous invite à configurer ou confirmer vos disponibilités pour la planification des cours.",
                    'time': "Aujourd'hui",
                    'category': "urgent",
                    'icon': "notification_important",
                    'badge': "Action requise",
                    'action_url': "/disponibilites",
                    'date_raw': datetime.datetime.now().isoformat()
                })
                
            return JsonResponse({
                'status': 'success',
                'notifications': notifications
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Formateurs.DoesNotExist:
        return JsonResponse({'error': 'Formateur introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_instructor_planning_api(request):
    institute_code = request.GET.get('institute_code')
    instructor_id = request.GET.get('instructor_id')
    
    if not institute_code or not instructor_id:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)
        
    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        with schema_context(tenant.schema_name):
            formateur = Formateurs.objects.get(id=instructor_id)
            
            sessions = TimetableEntry.objects.filter(
                formateur=formateur,
                timetable__status__in=['enc', 'val']
            ).select_related('cours', 'salle', 'timetable__groupe').order_by('jour', 'heure_debut')
            
            planning = []
            for s in sessions:
                planning.append({
                    'timeStart': s.heure_debut.strftime("%H:%M") if s.heure_debut else "",
                    'timeEnd': s.heure_fin.strftime("%H:%M") if s.heure_fin else "",
                    'title': f"{s.cours.label} ({s.timetable.groupe.nom})" if s.cours and s.timetable.groupe else (s.cours.label if s.cours else "N/A"),
                    'professor': f"{formateur.nom} {formateur.prenom}",
                    'room': s.salle.nom if s.salle else "N/A",
                    'day': s.jour or "",
                    'status': 'upcoming'
                })
                
            return JsonResponse({
                'status': 'success',
                'planning': planning
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Formateurs.DoesNotExist:
        return JsonResponse({'error': 'Formateur introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from t_groupe.models import Groupe, GroupeLine

def get_instructor_groups_api(request):
    institute_code = request.GET.get('institute_code')
    instructor_id = request.GET.get('instructor_id')
    
    if not institute_code or not instructor_id:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)
        
    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        with schema_context(tenant.schema_name):
            formateur = Formateurs.objects.get(id=instructor_id)
            
            # Fetch groups where this trainer has active timetable sessions
            from t_timetable.models import TimetableEntry
            groups_ids = TimetableEntry.objects.filter(
                formateur=formateur,
                timetable__status__in=['enc', 'val']
            ).values_list('timetable__groupe_id', flat=True).distinct()
            
            groups = Groupe.objects.filter(id__in=groups_ids).select_related('specialite', 'promotion')
            
            data = []
            for g in groups:
                student_count = GroupeLine.objects.filter(groupe=g).count()
                data.append({
                    'id': g.id,
                    'nom': g.nom,
                    'specialite': g.specialite.label if g.specialite else "N/A",
                    'promotion': g.promotion.label if g.promotion and hasattr(g.promotion, 'label') else (g.promotion.nom if g.promotion and hasattr(g.promotion, 'nom') else "N/A"),
                    'annee_scolaire': g.annee_scolaire,
                    'student_count': student_count,
                    'etat': g.etat
                })
                
            return JsonResponse({
                'status': 'success',
                'groups': data
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Formateurs.DoesNotExist:
        return JsonResponse({'error': 'Formateur introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


from t_etudiants.models import LigneRegistrePresence, RegistrePresence, SuiviCours, HistoriqueAbsence
import datetime

def get_instructor_registers_api(request):
    institute_code = request.GET.get('institute_code')
    instructor_id = request.GET.get('instructor_id')
    
    if not institute_code or not instructor_id:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)
        
    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        with schema_context(tenant.schema_name):
            formateur = Formateurs.objects.get(id=instructor_id)
            
            # Fetch active registers lines for this instructor
            lignes = LigneRegistrePresence.objects.filter(
                teacher=formateur,
                registre__status='enc'
            ).select_related('module', 'registre__groupe', 'registre__groupe__promotion')
            
            data = []
            for ligne in lignes:
                g = ligne.registre.groupe
                promo_label = g.promotion.label if g.promotion and hasattr(g.promotion, 'label') else (g.promotion.nom if g.promotion and hasattr(g.promotion, 'nom') else "N/A")
                data.append({
                    'id': ligne.id,
                    'module_label': ligne.module.label if ligne.module else "N/A",
                    'module_code': ligne.module.code if ligne.module else "N/A",
                    'groupe_nom': g.nom if g else "N/A",
                    'promotion': promo_label,
                    'registre_label': ligne.registre.label if ligne.registre else "N/A",
                    'jour': ligne.jour,
                    'heure_debut': ligne.heure_debut,
                    'heure_fin': ligne.heure_fin
                })
                
            return JsonResponse({
                'status': 'success',
                'registres': data
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Formateurs.DoesNotExist:
        return JsonResponse({'error': 'Formateur introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_register_students_api(request):
    institute_code = request.GET.get('institute_code')
    ligne_id = request.GET.get('ligne_id')
    date_str = request.GET.get('date') # Format: YYYY-MM-DD
    
    if not institute_code or not ligne_id:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)
        
    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        with schema_context(tenant.schema_name):
            ligne = LigneRegistrePresence.objects.select_related('registre__groupe', 'module').get(id=ligne_id)
            students = GroupeLine.objects.filter(groupe=ligne.registre.groupe).select_related('student')
            
            # Check if a session already exists for this date
            session_exists = False
            observation = ""
            existing_attendance = {}
            
            historiques = HistoriqueAbsence.objects.filter(ligne_presence=ligne)
            module_code = ligne.module.code if ligne.module else ""
            
            full_history = {}
            for h in historiques:
                student_id = h.etudiant_id
                full_history[student_id] = []
                if h.historique:
                    for entry in h.historique:
                        date_entry = entry.get('date')
                        for d in entry.get('data', []):
                            if d.get('code') == module_code:
                                status = d.get('etat')
                                full_history[student_id].append({'date': date_entry, 'status': status})
            
            if date_str:
                try:
                    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    date_str_fr = date_obj.strftime("%d/%m/%Y")
                    
                    seance = SuiviCours.objects.filter(ligne_presence=ligne, date_seance=date_obj).first()
                    if seance:
                        session_exists = True
                        observation = seance.observation or ""
                        
                    for student_id, history_list in full_history.items():
                        for h_item in history_list:
                            if h_item['date'] == date_str_fr:
                                existing_attendance[student_id] = h_item['status']
                                            
                except Exception as ex:
                    pass
            
            data = []
            for s in students:
                student_id = s.student.id
                status = existing_attendance.get(student_id, 'P') # Default to Present if no record
                
                student_history = full_history.get(student_id, [])
                total_sessions = len(student_history)
                present_sessions = sum(1 for h in student_history if h['status'] == 'P')
                rate = round((present_sessions / total_sessions) * 100) if total_sessions > 0 else 100
                
                data.append({
                    'id': student_id,
                    'nom': s.student.nom,
                    'prenom': s.student.prenom,
                    'matricule': s.student.matricule_interne,
                    'status': status,
                    'history': student_history,
                    'rate': rate
                })
                
            return JsonResponse({
                'status': 'success',
                'students': data,
                'session_exists': session_exists,
                'observation': observation
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except LigneRegistrePresence.DoesNotExist:
        return JsonResponse({'error': 'Registre introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def submit_instructor_attendance_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
        
    try:
        payload = json.loads(request.body)
        institute_code = payload.get('institute_code')
        ligne_id = payload.get('ligne_id')
        date_str = payload.get('date') # Format: YYYY-MM-DD
        observation = payload.get('observation', '')
        records = payload.get('records', [])
        
        if not institute_code or not ligne_id or not date_str:
             return JsonResponse({'error': 'Paramètres manquants'}, status=400)
             
        tenant = Institut.objects.get(code_tenant=institute_code)
        with schema_context(tenant.schema_name):
            ligne = LigneRegistrePresence.objects.get(id=ligne_id)
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Create or update SuiviCours
            seance, created = SuiviCours.objects.get_or_create(
                ligne_presence_id=ligne_id,
                date_seance=date_obj,
                defaults={
                    'is_done': True,
                    'module': ligne.module,
                    'observation': observation
                }
            )
            
            if not created:
                seance.observation = observation
                seance.save()

            for record in records:
                student_id = record.get('student_id')
                status = record.get('status', 'P')
                
                etudiant = Prospets.objects.get(id=student_id)
                historique, _ = HistoriqueAbsence.objects.get_or_create(
                    etudiant=etudiant,
                    ligne_presence=ligne
                )
                
                module_label = ligne.module.label if ligne.module else "N/A"
                module_code  = ligne.module.code if ligne.module else "N/A"
                
                date_str_fr = date_obj.strftime("%d/%m/%Y")
                if historique.historique is None:
                    historique.historique = []
                    
                existing_date = next((item for item in historique.historique if item["date"] == date_str_fr), None)
                
                if existing_date:
                    existing_module = next((d for d in existing_date["data"] if d["code"] == module_code), None)
                    if existing_module:
                        existing_module["etat"] = status
                    else:
                        existing_date["data"].append({"module": module_label, "code": module_code, "etat": status})
                else:
                    historique.historique.append({
                        "date": date_str_fr,
                        "data": [{"module": module_label, "code": module_code, "etat": status}]
                    })
                    
                historique.save()

            return JsonResponse({'status': 'success', 'message': 'Présences enregistrées avec succès'})
            
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_instructor_exams_api(request):
    institute_code = request.GET.get('institute_code')
    instructor_id = request.GET.get('instructor_id')

    if not institute_code or not instructor_id:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)

    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        
        with schema_context(tenant.schema_name):
            from t_exam.models import ExamPlanification
            
            # Fetch exams where the instructor teaches the module and the exam is 'termine'
            exam_planifications = ExamPlanification.objects.filter(
                module__affect_module__formateur_id=instructor_id,
                statut='termine'
            ).select_related('exam_line__groupe', 'module', 'salle').distinct()
            
            exams_data = []
            for plan in exam_planifications:
                exams_data.append({
                    'id': plan.id,
                    'module': {
                        'id': plan.module.id,
                        'label': plan.module.label,
                        'code': plan.module.code,
                    },
                    'groupe': {
                        'id': plan.exam_line.groupe.id if plan.exam_line and plan.exam_line.groupe else None,
                        'nom': plan.exam_line.groupe.nom if plan.exam_line and plan.exam_line.groupe else "N/A",
                    },
                    'date': plan.date.strftime("%Y-%m-%d") if plan.date else "",
                    'type_examen': plan.get_type_examen_display(),
                    'mode_examination': plan.mode_examination,
                    'passed': plan.passed
                })
                
            return JsonResponse({
                'status': 'success',
                'exams': exams_data
            })
            
    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_instructor_pv_api(request):
    institute_code = request.GET.get('institute_code')
    exam_plan_id = request.GET.get('exam_plan_id')

    if not institute_code or not exam_plan_id:
        return JsonResponse({'error': 'Paramètres manquants'}, status=400)

    try:
        tenant = Institut.objects.get(code_tenant=institute_code)
        
        with schema_context(tenant.schema_name):
            from t_exam.models import ExamPlanification, PvExamen, ExamTypeNote, ExamNote, ModelBuilltins
            from t_groupe.models import GroupeLine
            
            exam_plan = ExamPlanification.objects.get(id=exam_plan_id)
            
            # Fetch or generate PV
            pv_examen, created = PvExamen.objects.get_or_create(exam_planification=exam_plan)
            
            groupe = exam_plan.exam_line
            modele_builtins = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)
            students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id).select_related('student')
            
            if created:
                for builtin_type_note in modele_builtins.types_notes.all().order_by('ordre'):
                    exam_type_note = ExamTypeNote.objects.create(
                        pv=pv_examen,
                        code=builtin_type_note.code,
                        libelle=builtin_type_note.libelle,
                        max_note=builtin_type_note.max_note,
                        has_sous_notes=builtin_type_note.has_sous_notes,
                        nb_sous_notes=builtin_type_note.nb_sous_notes,
                        ordre=builtin_type_note.ordre,
                        coefficient=builtin_type_note.coefficient,
                        is_calculee=builtin_type_note.is_calculee,
                        type_calcul=builtin_type_note.type_calcul
                    )

                    for student_line in students:
                        exam_note = ExamNote.objects.create(
                            pv=pv_examen,
                            etudiant=student_line.student,
                            type_note=exam_type_note,
                            valeur=None
                        )
                        if builtin_type_note.has_sous_notes and builtin_type_note.nb_sous_notes > 0:
                            from t_exam.models import ExamSousNote
                            for _ in range(builtin_type_note.nb_sous_notes):
                                ExamSousNote.objects.create(
                                    note=exam_note,
                                    valeur=0.0
                                )

            # Filter logic adapted from view
            exam_type = exam_plan.type_examen
            if exam_type == 'normal':
                filtered_types = modele_builtins.types_notes.filter(is_rattrapage=False, is_rachat=False).order_by('ordre')
            elif exam_type == 'rattrage':
                filtered_types = modele_builtins.types_notes.filter(is_rattrapage=True).order_by('ordre')
            elif exam_type == 'rachat':
                filtered_types = modele_builtins.types_notes.filter(is_rachat=True).order_by('ordre')
            else:
                filtered_types = modele_builtins.types_notes.all().order_by('ordre')

            # Build columns list
            types_notes_data = []
            for btn in filtered_types:
                note_dict = {
                    'id': btn.id, 
                    'code': btn.code,
                    'libelle': btn.libelle,
                    'max_note': btn.max_note,
                    'is_calculee': btn.is_calculee,
                    'has_sous_notes': btn.has_sous_notes,
                    'nb_sous_notes': btn.nb_sous_notes,
                    'sous_notes_config': []
                }
                
                if btn.has_sous_notes and btn.nb_sous_notes > 0:
                    for sn in btn.sous_notes.all().order_by('ordre'):
                        note_dict['sous_notes_config'].append({
                            'id': sn.id,
                            'label': sn.label,
                            'max_note': sn.max_note
                        })
                        
                types_notes_data.append(note_dict)
                
            # Mapping from builtin ID to exam type note object
            builtin_to_exam_mapping = {}
            for exam_type_note in pv_examen.exam_types_notes.all():
                btn = modele_builtins.types_notes.filter(code=exam_type_note.code).first()
                if btn:
                    builtin_to_exam_mapping[btn.id] = exam_type_note
                    
            # Build students data
            students_data = []
            for student_line in students:
                student = student_line.student
                student_notes = {}
                
                for btn in filtered_types:
                    etn = builtin_to_exam_mapping.get(btn.id)
                    if etn:
                        exam_note = ExamNote.objects.filter(
                            pv=pv_examen,
                            etudiant=student,
                            type_note=etn
                        ).first()
                        if exam_note:
                            note_data = {'valeur': exam_note.valeur}
                            if etn.has_sous_notes and etn.nb_sous_notes > 0:
                                sous_notes_dict = {}
                                sous_notes_list = list(exam_note.sous_notes.all().order_by('id'))
                                for idx, sn in enumerate(sous_notes_list):
                                    if idx < etn.nb_sous_notes:
                                        sous_notes_dict[str(idx)] = sn.valeur
                                note_data['sous_notes'] = sous_notes_dict
                            student_notes[str(btn.id)] = note_data
                            
                students_data.append({
                    'id': student.id,
                    'nom': student.nom,
                    'prenom': student.prenom,
                    'matricule': student.matricule_interne,
                    'notes': student_notes
                })
                
            return JsonResponse({
                'status': 'success',
                'pv_id': pv_examen.id,
                'est_valide': pv_examen.est_valide,
                'types_notes': types_notes_data,
                'students': students_data
            })

    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def submit_instructor_notes_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        institute_code = data.get('institute_code')
        exam_plan_id = data.get('exam_plan_id')
        notes_data = data.get('notes') 

        if not institute_code or not exam_plan_id or notes_data is None:
            return JsonResponse({'error': 'Paramètres manquants'}, status=400)

        tenant = Institut.objects.get(code_tenant=institute_code)
        
        with schema_context(tenant.schema_name):
            from t_exam.models import ExamPlanification, PvExamen, ExamNote, ModelBuilltins
            from t_crm.models import Prospets
            
            exam_plan = ExamPlanification.objects.get(id=exam_plan_id)
            pv_examen = PvExamen.objects.get(exam_planification=exam_plan)
            
            if pv_examen.est_valide:
                return JsonResponse({'error': 'PV déjà validé, modification impossible'}, status=400)
                
            groupe = exam_plan.exam_line
            modele_builtins = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)
            
            builtin_to_exam_mapping = {}
            for exam_type_note in pv_examen.exam_types_notes.all():
                btn = modele_builtins.types_notes.filter(code=exam_type_note.code).first()
                if btn:
                    builtin_to_exam_mapping[str(btn.id)] = exam_type_note
            
            for item in notes_data:
                student_id = item.get('student_id')
                note_type_id = str(item.get('note_type_id'))
                valeur = item.get('valeur')
                
                if valeur == '':
                    valeur = None
                elif valeur is not None:
                    try:
                        valeur = float(valeur)
                    except ValueError:
                        valeur = None
                    
                etn = builtin_to_exam_mapping.get(note_type_id)
                if etn and not etn.is_calculee:
                    student = Prospets.objects.get(id=student_id)
                    exam_note, _ = ExamNote.objects.get_or_create(
                        pv=pv_examen,
                        etudiant=student,
                        type_note=etn
                    )
                    
                    if etn.has_sous_notes and etn.nb_sous_notes > 0:
                        sous_notes_data = item.get('sous_notes', {})
                        from t_exam.models import ExamSousNote
                        existing_sous_notes = list(exam_note.sous_notes.all().order_by('id'))
                        
                        for i in range(etn.nb_sous_notes):
                            sn_val_str = sous_notes_data.get(str(i), '')
                            sn_val = 0.0
                            if sn_val_str != '' and sn_val_str is not None:
                                try:
                                    sn_val = float(sn_val_str)
                                except ValueError:
                                    sn_val = 0.0
                            
                            if i < len(existing_sous_notes):
                                sn_obj = existing_sous_notes[i]
                                sn_obj.valeur = sn_val
                                sn_obj.save()
                            else:
                                ExamSousNote.objects.create(
                                    note=exam_note,
                                    valeur=sn_val
                                )
                        
                        exam_note.calculer_valeur()
                    else:
                        if valeur is not None and etn.max_note and valeur > etn.max_note:
                            valeur = etn.max_note
                            
                        exam_note.valeur = valeur
                        exam_note.save()
                    
            pv_examen.recalculer_notes_calculees()
            pv_examen.soumis_par_formateur = True
            pv_examen.save()
            
            return JsonResponse({'status': 'success', 'message': 'Notes enregistrées avec succès'})

    except Institut.DoesNotExist:
        return JsonResponse({'error': 'Institut invalide'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)