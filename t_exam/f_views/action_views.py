from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
import logging
from ..models import CommisionResult, Commissions, Prospets, Modules
from django.db import transaction
from t_etudiants.models import HistoriqueAbsence

@login_required(login_url="institut_app:login")
@csrf_exempt
@transaction.atomic
def examen_action(request):
    
    if request.method == 'POST':
        
        data = json.loads(request.body)
        student_id = data.get('student_id')
        commission_id = data.get('commission_id')  # This might be derived from the group context
        comment = data.get('comment', '')
        historiqueAbs = data.get('historiqueAbsence')

        # Validate required parameters
        if not student_id:
            return JsonResponse({'status': 'error','message': 'Student ID is required'}, status=400)

        if not commission_id:
            return JsonResponse({'status': 'error','message': 'Commission ID is required'}, status=400)

        student = Prospets.objects.get(id=student_id)
        commission = Commissions.objects.get(id=commission_id)

        HistoriqueAbsence.objects.filter(id__in=historiqueAbs).update(etat=True)

        # Create or update the CommissionResult record
        result, created = CommisionResult.objects.get_or_create(
            commission=commission,
            etudiants=student,
            defaults={
                'result': 'exam',
                'commentaire': comment
            }
        )

        if not created:
            result.result = 'exam'
            result.commentaire = comment
            result.save()

        return JsonResponse({'status': 'success','message': f'Action "Examen" enregistrée pour {student.prenom} {student.nom}','result_id': result.id})

    return JsonResponse({'status': 'error','message': 'Method not allowed'}, status=405)

@login_required(login_url="institut_app:login")
@transaction.atomic
@csrf_exempt
def rachat_action(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        commission_id = data.get('commission_id')
        selected_modules = data.get('modules', [])
        comment = data.get('comment', '')
        historique_ids = data.get('historiqueIds')

        student = Prospets.objects.get(id=student_id)
        commission = Commissions.objects.get(id=commission_id)

        HistoriqueAbsence.objects.filter(id__in=historique_ids).update(etat=True)

        modules = list(Modules.objects.filter(code__in=selected_modules))  
        result, created = CommisionResult.objects.get_or_create(
            commission=commission,
            etudiants=student,
            defaults={'result': 'rach','commentaire': comment}
        )
        if not created:
            result.result = 'rach'
            result.commentaire = comment
            result.save()

        result.modules.clear()
        result.modules.add(*modules)
        return JsonResponse({'status': 'success','message': f'Action "Rachat" enregistrée pour {student.prenom} {student.nom} ({len(modules)} module(s) sélectionné(s))','result_id': result.id,'module_count': len(modules)})
    
    
    return JsonResponse({'status': 'error','message': 'Method not allowed'}, status=405)

@login_required(login_url="institut_app:login")
@transaction.atomic
@csrf_exempt
def ajourne_action(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        student_id = data.get('student_id')
        commission_id = data.get('commission_id')
        comment = data.get('comment', '')
        historiqueAbs = data.get('historiqueAbs')

        
        if not student_id:
            return JsonResponse({'status': 'error','message': 'Student ID is required'}, status=400)

        if not commission_id:
            return JsonResponse({'status': 'error','message': 'Commission ID is required'}, status=400)

        student = Prospets.objects.get(id=student_id)
        commission = Commissions.objects.get(id=commission_id)
       
        HistoriqueAbsence.objects.filter(id__in=historiqueAbs).update(etat=True)

        result, created = CommisionResult.objects.get_or_create(
            commission=commission,
            etudiants=student,
            defaults={
                'result': 'ajou',
                'commentaire': comment
            }
        )

        if not created:
            # Update the existing record
            result.result = 'ajou'
            result.commentaire = comment
            result.save()

        return JsonResponse({'status': 'success','message': f'Action "Ajourné" enregistrée pour {student.prenom} {student.nom}','result_id': result.id})

    return JsonResponse({'status': 'error','message': 'Method not allowed'}, status=405)