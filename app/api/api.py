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