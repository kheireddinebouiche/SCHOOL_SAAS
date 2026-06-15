import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from institut_app.decorators import *
from t_conseil.models import Consultant

from django.db.models import Prefetch
from t_conseil.models import GroupeConseilThematique, GroupeConseilPlanning

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
def ListeConsultants(request):
    consultants = Consultant.objects.all().prefetch_related(
        Prefetch('groupeconseilthematique_set', queryset=GroupeConseilThematique.objects.select_related('groupe', 'thematique').order_by('-date_debut'), to_attr='thematiques_history'),
        Prefetch('groupeconseilplanning_set', queryset=GroupeConseilPlanning.objects.select_related('groupe', 'thematique').order_by('-date', '-heure_debut'), to_attr='plannings_history')
    ).order_by('-created_at')
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'add':
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            email = request.POST.get('email')
            telephone = request.POST.get('telephone')
            specialite = request.POST.get('specialite')
            
            Consultant.objects.create(
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                specialite=specialite
            )
            return redirect('t_conseil:ListeConsultants')
            
        elif action == 'edit':
            c_id = request.POST.get('consultant_id')
            consultant = get_object_or_404(Consultant, id=c_id)
            
            consultant.nom = request.POST.get('nom')
            consultant.prenom = request.POST.get('prenom')
            consultant.email = request.POST.get('email')
            consultant.telephone = request.POST.get('telephone')
            consultant.specialite = request.POST.get('specialite')
            consultant.save()
            return redirect('t_conseil:ListeConsultants')
            
        elif action == 'delete':
            c_id = request.POST.get('consultant_id')
            consultant = get_object_or_404(Consultant, id=c_id)
            consultant.delete()
            return redirect('t_conseil:ListeConsultants')
            
    context = {
        'consultants': consultants,
        'page_title': 'Consultants (Executive Education)',
    }
    return render(request, 'tenant_folder/conseil/consultants/liste_consultants.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
def HistoriqueConsultant(request, consultant_id):
    consultant = get_object_or_404(
        Consultant.objects.prefetch_related(
            Prefetch('groupeconseilthematique_set', queryset=GroupeConseilThematique.objects.select_related('groupe', 'thematique').order_by('-date_debut'), to_attr='thematiques_history'),
            Prefetch('groupeconseilplanning_set', queryset=GroupeConseilPlanning.objects.select_related('groupe', 'thematique').order_by('-date', '-heure_debut'), to_attr='plannings_history')
        ),
        id=consultant_id
    )
    
    context = {
        'consultant': consultant,
        'page_title': f'Historique Consultant - {consultant.prenom} {consultant.nom}',
    }
    return render(request, 'tenant_folder/conseil/consultants/historique_consultant.html', context)
