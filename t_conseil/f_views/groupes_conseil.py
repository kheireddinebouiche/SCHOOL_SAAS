import json
import os
from datetime import datetime
from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from t_crm.models import Prospets
from t_conseil.models import Devis, Participant, Thematiques, GroupeConseil, GroupeConseilParticipant, GroupeConseilThematique
from t_formations.models import Formateurs

@login_required(login_url="institut_app:login")
def ListeGroupesConseil(request):
    groupes = GroupeConseil.objects.all().order_by('-created_at')
    context = {
        'liste': groupes,
        'tenant': request.tenant,
        'page_title': "Executive Education - Groupes & Sessions",
    }
    return render(request, 'tenant_folder/conseil/groupes/liste_des_groupes.html', context)

@login_required(login_url="institut_app:login")
def NouveauGroupeConseil(request):
    clients = Prospets.objects.filter(is_client=True, context='con')
    context = {
        'clients': clients.distinct(),
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/conseil/groupes/nouveau_groupe_conseil.html', context)

@login_required(login_url="institut_app:login")
def DetailsGroupeConseil(request, pk):
    try:
        groupe = GroupeConseil.objects.get(pk=pk)
    except GroupeConseil.DoesNotExist:
        messages.error(request, "Groupe non trouvé.")
        return redirect('t_conseil:ListeGroupesConseil')

    participants_associes = groupe.participants_groupe.all()
    affectations_thematiques = groupe.affectations_thematiques.all()
    planning_sessions = groupe.planning.all().order_by('date', 'heure_debut')

    context = {
        'groupe': groupe,
        'participants_associes': participants_associes,
        'affectations_thematiques': affectations_thematiques,
        'planning_sessions': planning_sessions,
        'tenant': request.tenant,
        'context_type': 'con',
    }
    return render(request, 'tenant_folder/conseil/groupes/details_du_groupe.html', context)

@login_required(login_url="institut_app:login")
def ApiGetClientDevis(request):
    client_id = request.GET.get('client_id')
    if not client_id:
        return JsonResponse({'status': 'error', 'message': 'Client ID manquant'})
    
    devis = Devis.objects.filter(client_id=client_id, etat='accepte').values('id', 'num_devis', 'date_emission')
    return JsonResponse(list(devis), safe=False)

@login_required(login_url="institut_app:login")
def ApiGetDevisDetails(request):
    devis_id = request.GET.get('devis_id')
    if not devis_id:
        return JsonResponse({'status': 'error', 'message': 'Devis ID manquant'})
    
    try:
        devis = Devis.objects.get(id=devis_id)
    except Devis.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Devis non trouvé'})
    
    thematics = devis.lignes_devis.filter(thematique__isnull=False).values(
        'thematique__id', 'thematique__label'
    ).distinct()
    
    participants = Participant.objects.filter(devis=devis).values(
        'id', 'nom', 'prenom', 'email', 'poste'
    )
    
    if devis.client.type_prospect == 'particulier':
        participants = list(participants)
        participants.append({
            'id': f"prospect_{devis.client.id}",
            'nom': devis.client.nom,
            'prenom': devis.client.prenom,
            'email': devis.client.email,
            'is_prospect': True
        })

    trainers = Formateurs.objects.all().values('id', 'nom', 'prenom')
    
    return JsonResponse({
        'thematics': list(thematics),
        'participants': list(participants),
        'trainers': list(trainers)
    }, safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSaveConseilGroupe(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        
        devis = Devis.objects.get(id=data['devis_id'])
        
        groupe = GroupeConseil.objects.create(
            nom=data.get('nom'),
            devis=devis,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            created_by=request.user,
            etat='enc'
        )
        
        # Participants
        for p_id in data.get('participants', []):
            if str(p_id).startswith('prospect_'):
                real_id = p_id.split('_')[1]
                prospect = Prospets.objects.get(id=real_id)
                
                participant, created = Participant.objects.get_or_create(
                    prospect=prospect,
                    devis=devis,
                    defaults={
                        'nom': prospect.nom,
                        'prenom': prospect.prenom,
                        'email': prospect.email,
                        'telephone': prospect.tel_1
                    }
                )
                GroupeConseilParticipant.objects.create(groupe=groupe, participant=participant)
            else:
                participant = Participant.objects.get(id=p_id)
                GroupeConseilParticipant.objects.create(groupe=groupe, participant=participant)
                
        # Thematics
        for assign in data.get('assignments', []):
            thematique = Thematiques.objects.get(id=assign['thematique_id'])
            formateur = None
            if assign.get('formateur_id'):
                formateur = Formateurs.objects.get(id=assign['formateur_id'])
                
            GroupeConseilThematique.objects.create(
                groupe=groupe,
                thematique=thematique,
                formateur=formateur,
                date_debut=groupe.start_date,
                date_fin=groupe.end_date
            )
            
        messages.success(request, f"Le groupe {groupe.nom} a été créé avec succès.")
        return JsonResponse({'status': 'success', 'message': 'Groupe créé avec succès', 'groupe_id': groupe.id})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
def ApiDeleteGroupeConseil(request):
    if request.method == "GET":
        id = request.GET.get('id')
        if not id:
            return JsonResponse({"status": "error", "message": "Informations manquantes"})
        
        try:
            groupe = GroupeConseil.objects.get(id=id)
            if groupe.etat != "brouillon":
                return JsonResponse({"status": "error", "message": "Le groupe est en cours d'utilisation, vous ne pouvez pas effectuer la suppression"})
            
            groupe.delete()
            messages.success(request, "Le groupe a été supprimé avec succès")
            return JsonResponse({"status": "success"})
        except GroupeConseil.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Groupe non trouvé"})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
def ApiUpdateGroupeSettings(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        groupe_id = data.get('groupe_id')
        lieu = data.get('lieu_formation')
        jours = data.get('jours_travail')
        
        groupe = GroupeConseil.objects.get(id=groupe_id)
        groupe.lieu_formation = lieu
        groupe.jours_travail = jours
        groupe.save()
        
        return JsonResponse({'status': 'success', 'message': 'Paramètres mis à jour'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
def ApiAddPlanningSession(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        from t_conseil.models import GroupeConseilPlanning, GroupeConseilThematique
        
        groupe = GroupeConseil.objects.get(id=data.get('groupe_id'))
        thematique = Thematiques.objects.get(id=data.get('thematique_id'))
        
        # Auto-detect formateur from the group's thematic association
        assoc = GroupeConseilThematique.objects.filter(groupe=groupe, thematique=thematique).first()
        formateur = assoc.formateur if assoc else None

        try:
            date_obj = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
            time_start_obj = datetime.strptime(data.get('heure_debut'), '%H:%M').time()
            time_end_obj = datetime.strptime(data.get('heure_fin'), '%H:%M').time()
        except Exception as parse_e:
            return JsonResponse({'status': 'error', 'message': f"Format de date ou d'heure invalide : {str(parse_e)}"})

        # Check for overlaps
        overlaps = GroupeConseilPlanning.objects.filter(
            groupe=groupe,
            date=date_obj,
            heure_debut__lt=time_end_obj,
            heure_fin__gt=time_start_obj
        ).exists()

        if overlaps:
            return JsonResponse({
                'status': 'error', 
                'message': f"Une séance est déjà planifiée sur ce créneau le {date_obj.strftime('%d/%m/%Y')}."
            })
            
        session = GroupeConseilPlanning.objects.create(
            groupe=groupe,
            thematique=thematique,
            formateur=formateur,
            date=date_obj,
            heure_debut=time_start_obj,
            heure_fin=time_end_obj,
            note=data.get('note')
        )
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Session ajoutée au planning',
            'session': {
                'id': session.id,
                'date': date_obj.strftime('%d/%m/%Y'),
                'heure': f"{time_start_obj.strftime('%H:%M')} - {time_end_obj.strftime('%H:%M')}",
                'thematique': session.thematique.label,
                'formateur': str(session.formateur) if session.formateur else "N/A"
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
def ApiDeletePlanningSession(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        from t_conseil.models import GroupeConseilPlanning
        session = GroupeConseilPlanning.objects.get(id=data.get('session_id'))
        session.delete()
        return JsonResponse({'status': 'success', 'message': 'Session supprimée'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
def SessionAttendancePDF(request, session_id):
    from django.shortcuts import get_object_or_404
    from t_conseil.models import GroupeConseilPlanning
    from django.template.loader import render_to_string
    from weasyprint import HTML
    from django.utils import timezone
    from django.http import HttpResponse

    session = get_object_or_404(
        GroupeConseilPlanning.objects.select_related(
            'groupe__devis__client', 
            'groupe__devis__entreprise',
            'thematique',
            'formateur'
        ), 
        id=session_id
    )
    groupe = session.groupe
    participants = groupe.participants_groupe.all().select_related('participant')

    client_logo_path = None
    if groupe.devis.client.logo_entreprise:
        try:
            client_logo_path = Path(groupe.devis.client.logo_entreprise.path).as_uri()
        except ValueError:
            pass

    enterprise_logo_path = None
    if groupe.devis.entreprise and groupe.devis.entreprise.logo:
        try:
            enterprise_logo_path = Path(groupe.devis.entreprise.logo.path).as_uri()
        except ValueError:
            pass

    html_string = render_to_string('tenant_folder/conseil/groupes/pdf_attendance_sheet.html', {
        'session': session,
        'groupe': groupe,
        'participants': participants,
        'tenant': request.tenant,
        'now': timezone.now(),
        'client_logo_path': client_logo_path,
        'enterprise_logo_path': enterprise_logo_path,
    }, request=request)

    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    filename = f"Emargement_{groupe.nom}_{session.date.strftime('%d-%m-%Y')}.pdf"
    response['Content-Disposition'] = f'inline; filename="{filename}"'
    
    return response

@login_required(login_url="institut_app:login")
def ApiConfirmParticipantForScolarite(request):
    if request.method == "POST":
        participant_id = request.POST.get('participant_id')
        if not participant_id:
            return JsonResponse({'status': 'error', 'message': 'ID participant manquant'})
        
        participant = get_object_or_404(Participant, id=participant_id)
        participant.is_confirmed_for_scolarite = True
        participant.scolarite_note = request.POST.get('note', '')
        participant.save()
        
        return JsonResponse({'status': 'success', 'message': 'Participant confirmé pour la Scolarité'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
def ApiCancelParticipantConfirmationForScolarite(request):
    if request.method == "POST":
        participant_id = request.POST.get('participant_id')
        if not participant_id:
            return JsonResponse({'status': 'error', 'message': 'ID participant manquant'})
        
        participant = get_object_or_404(Participant, id=participant_id)
        participant.is_confirmed_for_scolarite = False
        participant.scolarite_note = None
        participant.save()
        
        return JsonResponse({'status': 'success', 'message': 'Confirmation annulée avec succès'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
