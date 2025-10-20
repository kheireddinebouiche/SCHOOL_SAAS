from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from django.db.models import Avg



@login_required(login_url="institut_app:login")
def ListeDesSalles(request):
    salles = Salle.objects.all()
    avg_capacity = salles.aggregate(Avg('capacite'))['capacite__avg']
    
    # Count rooms by type
    salles_td_count = salles.filter(type_salle='TD').count()
    salles_tp_count = salles.filter(type_salle='TP').count()
    
    context = {
        'salles' : salles,
        'avg_capacity': avg_capacity,
        'salles_td_count': salles_td_count,
        'salles_tp_count': salles_tp_count
    }
    return render(request, 'tenant_folder/timetable/liste_des_salles.html', context)


@login_required(login_url="institut_app:login")
def CreerSalle(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        code = request.POST.get('code')
        capacite = request.POST.get('capacite')
        type_salle = request.POST.get('type_salle')
        equipements = request.POST.get('equipements', '')
        
        # Check if code already exists and generate a unique one if necessary
        original_code = code
        counter = 1
        while Salle.objects.filter(code=code).exists():
            code = f"{original_code}{counter}"
            counter += 1
        
        # Create new Salle
        try:
            salle = Salle.objects.create(
                nom=nom,
                code=code,
                capacite=int(capacite),
                type_salle=type_salle,
                equipements=equipements
            )
            messages.success(request, 'Salle créée avec succès!')
            return JsonResponse({'success': True, 'message': 'Salle créée avec succès!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Erreur lors de la création de la salle: {str(e)}'})
    else:
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
def EditerSalle(request, salle_id):
    salle = Salle.objects.get(id=salle_id)
    if request.method == 'POST':
        salle.nom = request.POST.get('nom')
        code = request.POST.get('code')
        
        # Check if the new code is different and if it already exists
        if salle.code != code:
            if Salle.objects.filter(code=code).exclude(id=salle_id).exists():
                messages.error(request, 'Le code de la salle existe déjà!')
                context = {
                    'salle': salle
                }
                return render(request, 'tenant_folder/timetable/modifier_salle.html', context)
            salle.code = code
        
        salle.capacite = int(request.POST.get('capacite'))
        salle.type_salle = request.POST.get('type_salle')
        salle.equipements = request.POST.get('equipements', '')
        salle.save()
        messages.success(request, 'Salle modifiée avec succès!')
        return redirect('t_timetable:ListeDesSalles')
    
    context = {
        'salle': salle
    }
    return render(request, 'tenant_folder/timetable/modifier_salle.html', context)


@login_required(login_url="institut_app:login")
def SupprimerSalle(request, salle_id):
    salle = Salle.objects.get(id=salle_id)
    salle.delete()
    messages.success(request, 'Salle supprimée avec succès!')
    return redirect('t_timetable:ListeDesSalles')


@login_required(login_url="institut_app:login")
def get_salle_data(request, salle_id):
    try:
        salle = Salle.objects.get(id=salle_id)
        data = {
            'success': True,
            'room': {
                'id': salle.id,
                'nom': salle.nom,
                'code': salle.code,
                'capacite': salle.capacite,
                'type_salle': salle.type_salle,
                'equipements': salle.equipements or '',
                'date_creation': salle.date_creation.strftime('%Y-%m-%d')
            }
        }
        return JsonResponse(data)
    except Salle.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Salle non trouvée'})


@login_required(login_url="institut_app:login")
def EditerSalle(request, salle_id):
    if request.method == 'POST':
        salle = Salle.objects.get(id=salle_id)
        salle.nom = request.POST.get('nom')
        code = request.POST.get('code')
        
        # Check if the new code is different and if it already exists
        if salle.code != code:
            if Salle.objects.filter(code=code).exclude(id=salle_id).exists():
                return JsonResponse({'success': False, 'message': 'Le code de la salle existe déjà!'})
            salle.code = code
        
        salle.capacite = int(request.POST.get('capacite'))
        salle.type_salle = request.POST.get('type_salle')
        salle.equipements = request.POST.get('equipements', '')
        salle.save()
        messages.success(request, 'Salle modifiée avec succès!')
        return JsonResponse({'success': True, 'message': 'Salle modifiée avec succès!'})