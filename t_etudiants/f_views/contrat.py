from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from ..models import *
from django.contrib.auth.decorators import login_required
from ..forms import *
from t_crm.models import NotesProcpects, RendezVous
from django.db import transaction
from t_formations.models import *
from t_groupe.models import GroupeLine, Group
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json
from django.shortcuts import get_object_or_404



@login_required(login_url="institut_app:login")
def PageModeleContrat(request):
    formations = Formation.objects.all()
    context = {
        'formations' : formations
    }
    return render(request, 'tenant_folder/student/contrat/liste-model.html',context)


@login_required(login_url="institut_app:login")
def ApiLoadModelesContrat(request):
    modeles = ModelContrat.objects.all().select_related('formation')
    data = []
    for modele in modeles:
        # Statut mapping
        status_labels = {
            'act': 'Actif',
            'att': 'En attente', 
            'ina': 'Inactif'
        }
        status_label = status_labels.get(modele.status, modele.status)
        
        data.append({
            'id': modele.id,
            'nom': modele.label or '',
            'type_contrat': modele.formation.nom if modele.formation else 'N/A',
            'annee_scolaire': modele.annee_scolaire or '',
            'statut': modele.status,
            'statut_label': status_label,
            'date_creation': modele.created_at.strftime('%d/%m/%Y') if modele.created_at else '',
            'date_modification': modele.updated_at.strftime('%d/%m/%Y') if modele.updated_at else ''
        })
    return JsonResponse(data, safe=False)


@login_required(login_url="institut_app:login")
def ApiDeleteModeleContrat(request):
    if request.method == 'POST':
        try:
            modele_id = request.POST.get('id_modele')
            modele = get_object_or_404(ModelContrat, id=modele_id)
            modele.delete()
            return JsonResponse({'status': 'success', 'message': 'Modèle de contrat supprimé avec succès'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
def ApiUpdateModeleContrat(request):
    if request.method == 'POST':
        try:
            modele_id = request.POST.get('id_modele')
            modele = get_object_or_404(ModelContrat, id=modele_id)
            
            # Mettre à jour les champs
            if 'nom' in request.POST:
                modele.label = request.POST.get('nom')
            if 'formation_id' in request.POST:
                formation_id = request.POST.get('formation_id')
                if formation_id:
                    modele.formation = Formation.objects.get(id=formation_id)
            if 'statut' in request.POST:
                modele.status = request.POST.get('statut')
            
            modele.save()
            return JsonResponse({'status': 'success', 'message': 'Modèle de contrat mis à jour avec succès'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
def ApiCreateModeleContrat(request):
    if request.method == 'POST':
        try:
            nom = request.POST.get('nom')
            formation_id = request.POST.get('formation_id')
            annee_scolaire = request.POST.get('annee_scolaire')
            statut = request.POST.get('statut', request.POST.get('status', 'att'))  # Par défaut: en attente, avec fallback sur 'status'
            
            # Créer le nouveau modèle de contrat
            modele = ModelContrat.objects.create(
                label=nom,
                annee_scolaire=annee_scolaire,
                status=statut
            )
            
            # Associer la formation si fournie
            if formation_id:
                formation = Formation.objects.get(id=formation_id)
                modele.formation = formation
            
            modele.save()
            return JsonResponse({'status': 'success', 'message': 'Modèle de contrat créé avec succès'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
def ApiUpdateModeleContrat(request):
    if request.method == 'POST':
        try:
            modele_id = request.POST.get('id_modele')
            modele = get_object_or_404(ModelContrat, id=modele_id)
            
            # Mettre à jour les champs
            if 'nom' in request.POST:
                modele.label = request.POST.get('nom')
            if 'formation_id' in request.POST:
                formation_id = request.POST.get('formation_id')
                if formation_id:
                    modele.formation = Formation.objects.get(id=formation_id)
            if 'annee_scolaire' in request.POST:
                modele.annee_scolaire = request.POST.get('annee_scolaire')
            if 'statut' in request.POST:
                modele.status = request.POST.get('statut')
            elif 'status' in request.POST:
                modele.status = request.POST.get('status')
            
            modele.save()
            return JsonResponse({'status': 'success', 'message': 'Modèle de contrat mis à jour avec succès'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
def ApiLoadArticlesContrat(request):
    modele_id = request.GET.get('modele_id')
    try:
        articles = ClauseContrat.objects.filter(modele_id=modele_id)
        data = []
        for article in articles:
            data.append({
                'id': article.id,
                'article': article.article or '',
                'created_at': article.created_at.strftime('%d/%m/%Y') if article.created_at else '',
                'updated_at': article.updated_at.strftime('%d/%m/%Y') if article.updated_at else ''
            })
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url="institut_app:login")
def ApiCreateArticleContrat(request):
    if request.method == 'POST':
        try:
            modele_id = request.POST.get('modele_id')
            article_text = request.POST.get('article')
            
            modele = get_object_or_404(ModelContrat, id=modele_id)
            
            clause = ClauseContrat.objects.create(
                modele=modele,
                article=article_text
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Article ajouté avec succès',
                'data': {
                    'id': clause.id,
                    'article': clause.article or '',
                    'created_at': clause.created_at.strftime('%d/%m/%Y'),
                    'updated_at': clause.updated_at.strftime('%d/%m/%Y')
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
def ApiUpdateArticleContrat(request):
    if request.method == 'POST':
        try:
            article_id = request.POST.get('article_id')
            article_text = request.POST.get('article')
            
            clause = get_object_or_404(ClauseContrat, id=article_id)
            clause.article = article_text
            clause.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Article mis à jour avec succès',
                'data': {
                    'id': clause.id,
                    'article': clause.article or '',
                    'created_at': clause.created_at.strftime('%d/%m/%Y'),
                    'updated_at': clause.updated_at.strftime('%d/%m/%Y')
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
def ApiDeleteArticleContrat(request):
    if request.method == 'POST':
        try:
            article_id = request.POST.get('article_id')
            
            clause = get_object_or_404(ClauseContrat, id=article_id)
            clause.delete()
            
            return JsonResponse({'status': 'success', 'message': 'Article supprimé avec succès'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})