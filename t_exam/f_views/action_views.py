from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json
import logging
from ..models import CommisionResult, Commissions, Prospets, Modules


@login_required
@csrf_exempt
def examen_action(request):
    """
    View to handle Examen action for a student
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            commission_id = data.get('commission_id')  # This might be derived from the group context
            comment = data.get('comment', '')

            # Validate required parameters
            if not student_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Student ID is required'
                }, status=400)

            if not commission_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Commission ID is required'
                }, status=400)

            # Get the Prospets object directly since the CommisionResult model references Prospets
            try:
                student = Prospets.objects.get(id=student_id)
            except Prospets.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Prospets with ID {student_id} does not exist'
                }, status=400)

            # Get commission
            try:
                commission = Commissions.objects.get(id=commission_id)
            except Commissions.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Commission with ID {commission_id} does not exist'
                }, status=400)

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
                # Update the existing record
                result.result = 'exam'
                result.commentaire = comment
                result.save()

            return JsonResponse({
                'status': 'success',
                'message': f'Action "Examen" enregistrée pour {student.prenom} {student.nom}',
                'result_id': result.id
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            # Log the detailed error for debugging
            logging.exception("Error in examen_action")
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)


@login_required
@csrf_exempt
def rachat_action(request):
    """
    View to handle Rachat action for a student with selected modules
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            commission_id = data.get('commission_id')
            selected_modules = data.get('modules', [])
            comment = data.get('comment', '')

            
            student = Prospets.objects.get(id=student_id)
            commission = Commissions.objects.get(id=commission_id)
            

            # Get module objects
            modules = list(Modules.objects.filter(id__in=selected_modules))
            # Verify all requested modules exist
            if len(modules) != len(selected_modules) and selected_modules:
                requested_ids = set(selected_modules)
                found_ids = set([m.id for m in modules])
                missing_ids = requested_ids - found_ids
                return JsonResponse({
                    'status': 'error',
                    'message': f'Some modules do not exist: {list(missing_ids)}'
                }, status=400)

            # Create or update the CommissionResult record
            result, created = CommisionResult.objects.get_or_create(
                commission=commission,
                etudiants=student,
                defaults={
                    'result': 'rach',
                    'commentaire': comment
                }
            )

            if not created:
                # Update the existing record
                result.result = 'rach'
                result.commentaire = comment
                result.save()

            # Clear existing modules and add the new ones
            result.modules.clear()
            result.modules.add(*modules)

            return JsonResponse({
                'status': 'success',
                'message': f'Action "Rachat" enregistrée pour {student.prenom} {student.nom} ({len(modules)} module(s) sélectionné(s))',
                'result_id': result.id,
                'module_count': len(modules)
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            # Log the detailed error for debugging
            logging.exception("Error in rachat_action")
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)


@login_required
@csrf_exempt
def ajourne_action(request):
    """
    View to handle Ajourné action for a student
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            commission_id = data.get('commission_id')
            comment = data.get('comment', '')

            # Validate required parameters
            if not student_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Student ID is required'
                }, status=400)

            if not commission_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Commission ID is required'
                }, status=400)

            # Get the Prospets object directly since the CommisionResult model references Prospets
            try:
                student = Prospets.objects.get(id=student_id)
            except Prospets.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Prospets with ID {student_id} does not exist'
                }, status=400)

            # Get commission
            try:
                commission = Commissions.objects.get(id=commission_id)
            except Commissions.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Commission with ID {commission_id} does not exist'
                }, status=400)

            # Create or update the CommissionResult record
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

            return JsonResponse({
                'status': 'success',
                'message': f'Action "Ajourné" enregistrée pour {student.prenom} {student.nom}',
                'result_id': result.id
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)