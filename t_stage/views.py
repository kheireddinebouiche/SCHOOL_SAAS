from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Stage, FocusGroup, SeanceFocusGroup, PresentationProgressive, ConseilValidation, DecisionConseil
from t_crm.models import Prospets
from t_groupe.models import Groupe
from t_formations.models import Formateurs
from django.utils import timezone

@login_required
def stage_dashboard(request):
    """Tableau de bord général des stages."""
    stages = Stage.objects.all().order_by('-created_at')
    focus_groups = FocusGroup.objects.all()
    return render(request, 't_stage/dashboard.html', {
        'stages': stages,
        'focus_groups': focus_groups,
    })

@login_required
def list_stages(request):
    """Liste filtrée des stages."""
    stages = Stage.objects.all()
    # Logique de filtrage par groupe ou encadrant à ajouter ici
    return render(request, 't_stage/list_stages.html', {'stages': stages})

@login_required
def focus_group_detail(request, pk):
    """Détail d'un Focus Group et ses séances."""
    fg = get_object_or_404(FocusGroup, pk=pk)
    seances = fg.seances.all().order_by('-date_seance')
    return render(request, 't_stage/focus_group_detail.html', {
        'focus_group': fg,
        'seances': seances
    })

@login_required
def progressive_presentation_form(request, stage_id):
    """Enregistrement d'une présentation progressive (P1, P2 ou P3)."""
    stage = get_object_or_404(Stage, pk=stage_id)
    if request.method == 'POST':
        etape = int(request.POST.get('etape'))
        taux = int(request.POST.get('taux_avancement_declare'))
        
        # Création ou mise à jour de la présentation
        PresentationProgressive.objects.update_or_create(
            stage=stage,
            etape=etape,
            defaults={
                'date_presentation': timezone.now().date(),
                'taux_avancement_declare': taux,
                'observations': request.POST.get('observations'),
                'validee': True # Validation auto par défaut pour la simu
            }
        )
        
        # Mise à jour de l'avancement global du stage basé sur le maximum des présentations
        from django.db.models import Max
        max_taux = stage.presentations.aggregate(Max('taux_avancement_declare'))['taux_avancement_declare__max'] or 0
        stage.taux_avancement = max_taux
        stage.save()
            
        return redirect('t_stage:presentation_form', stage_id=stage.id)
    
    # Get existing presentations for history/edit list
    presentations = PresentationProgressive.objects.filter(stage=stage).order_by('etape')
    completed_steps = presentations.values_list('etape', flat=True)

    # Autocorrection de l'avancement global si incohérent
    from django.db.models import Max
    actual_max = presentations.aggregate(Max('taux_avancement_declare'))['taux_avancement_declare__max'] or 0
    if stage.taux_avancement != actual_max:
        stage.taux_avancement = actual_max
        stage.save()

    # Get session history for this stage
    sessions = stage.seances_discussion.all().order_by('-date_seance')

    return render(request, 't_stage/presentation_form.html', {
        'stage': stage, 
        'presentations': presentations,
        'completed_steps': completed_steps,
        'sessions': sessions
    })

@login_required
def delete_presentation(request, pk):
    """Suppression d'une présentation progressive."""
    presentation = get_object_or_404(PresentationProgressive, pk=pk)
    stage = presentation.stage
    presentation.delete()
    
    # Recalculer l'avancement global
    from django.db.models import Max
    max_taux = stage.presentations.aggregate(Max('taux_avancement_declare'))['taux_avancement_declare__max'] or 0
    stage.taux_avancement = max_taux
    stage.save()
    
    return redirect('t_stage:presentation_form', stage_id=stage.id)

@login_required
def validation_council(request):
    """Gestion du conseil de validation de fin de stage."""
    if request.method == 'POST':
        date_conseil = request.POST.get('date_conseil')
        observations = request.POST.get('observations')
        if date_conseil:
            ConseilValidation.objects.create(
                date_conseil=date_conseil,
                observations_generales=observations
            )
            # On peut ajouter un message de succès ici si nécessaire
            return redirect('t_stage:validation_council')

    # Sélectionner les stages qui ne sont pas encore soutenus/annulés
    stages = Stage.objects.exclude(statut__in=['soutenu', 'annule']).order_by('date_debut')
    conseils = ConseilValidation.objects.all().order_by('-date_conseil')
    return render(request, 't_stage/council.html', {
        't_stage_list': stages,
        'conseils': conseils
    })

@login_required
def quick_decision(request):
    """Enregistrement rapide d'une décision depuis le tableau de bord."""
    if request.method == 'POST':
        stage_id = request.POST.get('stage_id')
        council_id = request.POST.get('council_id')
        decision_statut = request.POST.get('decision')
        commentaire = request.POST.get('commentaire')
        taux_final = request.POST.get('taux_final')

        stage = get_object_or_404(Stage, pk=stage_id)
        
        # Determine council: specific ID or latest open one
        if council_id:
            council = get_object_or_404(ConseilValidation, pk=council_id)
        else:
            # Fallback to latest
            council = ConseilValidation.objects.all().order_by('-date_conseil').first()
        
        if council:
            DecisionConseil.objects.create(
                conseil=council,
                stage=stage,
                decision=decision_statut,
                taux_final=taux_final,
                commentaire=commentaire
            )
            
            # Update stage status if needed (e.g. soutenable -> soutenu or just marked as validated)
            # For simplicity, we just record the decision here.
            
    return redirect('t_stage:validation_council')

@login_required
def launch_stage(request):
    """Lancement/Planification d'un nouveau stage."""
    if request.method == 'POST':
        etudiants_ids = request.POST.getlist('etudiants')
        encadrant_id = request.POST.get('encadrant')
        focus_group_id = request.POST.get('focus_group')
        # Groupe id for the stage context, optional
        groupe_id = request.POST.get('groupe_filtre') 
        
        stage = Stage.objects.create(
            encadrant_id=encadrant_id,
            groupe_id=groupe_id if groupe_id else None,
            sujet=request.POST.get('sujet'),
            date_debut=request.POST.get('date_debut'),
            date_fin=request.POST.get('date_fin'),
            statut='en_cours'
        )
        
        if etudiants_ids:
            stage.etudiants.set(etudiants_ids)
        
        if focus_group_id:
            fg = get_object_or_404(FocusGroup, pk=focus_group_id)
            fg.stages.add(stage)
            
        return redirect('t_stage:stage_dashboard')

    context = {
        'etudiants': Prospets.objects.all(), # Fallback if no group selected or initial load
        'encadrants': Formateurs.objects.all(),
        'focus_groups': FocusGroup.objects.all(),
        'groupes': Groupe.objects.all().order_by('nom'),
    }
    return render(request, 't_stage/stage_form.html', context)

@login_required
def edit_stage(request, stage_id):
    """Modification d'un stage existant."""
    stage = get_object_or_404(Stage, pk=stage_id)
    
    if request.method == 'POST':
        etudiants_ids = request.POST.getlist('etudiants')
        encadrant_id = request.POST.get('encadrant')
        focus_group_id = request.POST.get('focus_group')
        groupe_id = request.POST.get('groupe_filtre')
        
        stage.encadrant_id = encadrant_id
        if groupe_id:
            stage.groupe_id = groupe_id
        stage.sujet = request.POST.get('sujet')
        stage.date_debut = request.POST.get('date_debut')
        stage.date_fin = request.POST.get('date_fin')
        stage.save()
        
        if etudiants_ids:
            stage.etudiants.set(etudiants_ids)
            
        # Update Focus Group if changed
        # Remove from old FGs or handle logic if one stage can have multiple FGs? 
        # Model says ManyToMany from FocusGroup to Stage (related_name='stages')
        # Here we assume user selects ONE FG in the form to "move" it or "assign" it.
        # Ideally we clear old ones and set new one if we treat it as single choice in UI.
        if focus_group_id:
            # simple approach: remove from all other FGs, add to this one
            for fg in FocusGroup.objects.filter(stages=stage):
                fg.stages.remove(stage)
            new_fg = get_object_or_404(FocusGroup, pk=focus_group_id)
            new_fg.stages.add(stage)
        elif 'focus_group' in request.POST: # If explicitly cleared
             for fg in FocusGroup.objects.filter(stages=stage):
                fg.stages.remove(stage)

        return redirect('t_stage:stage_dashboard')

    # Prepare context with existing data
    selected_etudiants = stage.etudiants.all()
    # Find current focus group if any
    current_fg = FocusGroup.objects.filter(stages=stage).first()

    context = {
        'stage': stage,
        'etudiants': Prospets.objects.all(),
        'encadrants': Formateurs.objects.all(),
        'focus_groups': FocusGroup.objects.all(),
        'groupes': Groupe.objects.all().order_by('nom'),
        'selected_etudiants_ids': [e.id for e in selected_etudiants],
        'current_fg_id': current_fg.id if current_fg else None
    }
    return render(request, 't_stage/stage_form.html', context)

@login_required
def ajax_get_students_by_group(request):
    """Renvoie la liste des étudiants d'un groupe spécifique (JSON)."""
    groupe_id = request.GET.get('groupe_id')
    students = []
    if groupe_id:
        # Assuming GroupeLine links students to groups
        from t_groupe.models import GroupeLine
        lines = GroupeLine.objects.filter(groupe_id=groupe_id).select_related('student')
        for line in lines:
            students.append({
                'id': line.student.id,
                'nom': str(line.student)
            })
    return JsonResponse({'students': students})

@login_required
def list_focus_groups(request):
    """Liste de tous les Focus Groups."""
    focus_groups = FocusGroup.objects.all().order_by('nom')
    encadrants = Formateurs.objects.all()
    return render(request, 't_stage/list_focus_groups.html', {
        'focus_groups': focus_groups,
        'encadrants': encadrants
    })

@login_required
def create_focus_group(request):
    """Création d'un nouveau Focus Group (POST only via Modal)."""
    if request.method == 'POST':
        nom = request.POST.get('nom')
        encadrant_id = request.POST.get('encadrant')
        thematique = request.POST.get('thematique')
        
        fg = FocusGroup.objects.create(
            nom=nom,
            encadrant_id=encadrant_id,
            thematique=thematique
        )
        return redirect('t_stage:focus_group_detail', pk=fg.pk)
    
    return redirect('t_stage:list_focus_groups')

@login_required
def add_seance(request, fg_id):
    """Enregistrement d'une séance pour un Focus Group."""
    fg = get_object_or_404(FocusGroup, pk=fg_id)
    if request.method == 'POST':
        date_seance = request.POST.get('date_seance')
        duree = request.POST.get('duree')
        compte_rendu = request.POST.get('compte_rendu')
        stages_ids = request.POST.getlist('stages')
        
        seance = SeanceFocusGroup.objects.create(
            focus_group=fg,
            date_seance=date_seance,
            duree_heures=duree,
            compte_rendu=compte_rendu
        )
        if stages_ids:
            seance.stages.set(stages_ids)
            
        return redirect('t_stage:focus_group_detail', pk=fg.pk)
    
    return render(request, 't_stage/seance_form.html', {'focus_group': fg})

@login_required
def council_detail(request, pk):
    """Vue détaillée pour gérer un conseil de validation spécifique."""
    conseil = get_object_or_404(ConseilValidation, pk=pk)
    # Pour l'instant, simple affichage des décisions existantes
    return render(request, 't_stage/council_detail.html', {'conseil': conseil})

@login_required
def print_sessions(request, fg_id):
    """Génération de l'état imprimable des séances d'un Focus Group."""
    focus_group = get_object_or_404(FocusGroup, pk=fg_id)
    seances = focus_group.seances.all().order_by('date_seance')
    
    return render(request, 't_stage/print_sessions.html', {
        'focus_group': focus_group,
        'seances': seances,
        'print_date': timezone.now()
    })
