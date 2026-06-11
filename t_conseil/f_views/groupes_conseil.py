from institut_app.decorators import module_permission_required
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
from t_conseil.models import Devis, Participant, Thematiques, GroupeConseil, GroupeConseilParticipant, GroupeConseilThematique, Facture, Consultant
from t_formations.models import Formateurs

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
def ListeGroupesConseil(request):
    groupes = GroupeConseil.objects.all().order_by('-created_at')
    context = {
        'liste': groupes,
        'tenant': request.tenant,
        'page_title': "Executive Education - Groupes & Sessions",
    }
    return render(request, 'tenant_folder/conseil/groupes/liste_des_groupes.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'add')
def NouveauGroupeConseil(request):
    clients = Prospets.objects.filter(is_client=True, context='con')
    context = {
        'clients': clients.distinct(),
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/conseil/groupes/nouveau_groupe_conseil.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
def DetailsGroupeConseil(request, pk):
    try:
        groupe = GroupeConseil.objects.get(pk=pk)
    except GroupeConseil.DoesNotExist:
        messages.error(request, "Groupe non trouvé.")
        return redirect('t_conseil:ListeGroupesConseil')

    participants_associes = groupe.participants_groupe.all()
    affectations_thematiques = groupe.affectations_thematiques.all()
    planning_sessions = groupe.planning.all().order_by('date', 'heure_debut')

    # Find the linked standard invoice, if any
    facture = None
    if groupe.devis and hasattr(groupe.devis, 'facture'):
        facture = groupe.devis.facture.filter(type_facture='standard').exclude(etat='annule').first()
    elif groupe.facture:
        facture = groupe.facture

    context = {
        'groupe': groupe,
        'participants_associes': participants_associes,
        'affectations_thematiques': affectations_thematiques,
        'planning_sessions': planning_sessions,
        'facture_liee': facture,
        'formateurs': Formateurs.objects.all(),
        'consultants': Consultant.objects.all(),
        'tenant': request.tenant,
        'context_type': 'con',
    }
    return render(request, 'tenant_folder/conseil/groupes/details_du_groupe.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
def ApiGetClientDevis(request):
    client_id = request.GET.get('client_id')
    if not client_id:
        return JsonResponse({'status': 'error', 'message': 'Client ID manquant'})
    
    devis = Devis.objects.filter(client_id=client_id, etat__in=['accepte', 'envoye']).values('id', 'num_devis', 'date_emission')
    factures = Facture.objects.filter(client_id=client_id, type_facture='standard').exclude(etat='annule').values('id', 'num_facture', 'date_emission', 'devis_source__id', 'etat')
    
    # Check if the client already has active groups
    from django.db.models import Q
    active_groups = GroupeConseil.objects.filter(
        Q(devis__client_id=client_id) | Q(facture__client_id=client_id)
    ).exclude(etat='cloture')
    has_active_group = active_groups.exists()
    active_group_info = None
    if has_active_group:
        g = active_groups.first()
        active_group_info = {
            'id': g.id,
            'nom': g.nom,
            'etat': g.get_etat_display()
        }
    
    return JsonResponse({
        'devis': list(devis),
        'factures': list(factures),
        'has_active_group': has_active_group,
        'active_group_info': active_group_info
    })

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
def ApiGetDevisDetails(request):
    doc_id = request.GET.get('devis_id') # format is either "devis_id" or "facture_id" or just id
    if not doc_id:
        return JsonResponse({'status': 'error', 'message': 'Document ID manquant'})
    
    is_facture = False
    actual_id = doc_id
    if str(doc_id).startswith('devis_'):
        actual_id = str(doc_id).replace('devis_', '')
    elif str(doc_id).startswith('facture_'):
        is_facture = True
        actual_id = str(doc_id).replace('facture_', '')
        
    thematics = []
    participants = []
    
    if is_facture:
        try:
            facture = Facture.objects.get(id=actual_id)
        except Facture.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Facture non trouvée'})
            
        thematics = facture.lignes_facture.filter(thematique__isnull=False).values(
            'thematique__id', 'thematique__label'
        ).distinct()
        
        # Participants might be on facture or its devis_source
        if facture.devis_source:
            parts = Participant.objects.filter(devis=facture.devis_source)
        else:
            parts = Participant.objects.filter(facture=facture)
            
        participants = parts.values('id', 'nom', 'prenom', 'email', 'poste')
        
        client = facture.client
    else:
        try:
            devis = Devis.objects.get(id=actual_id)
        except Devis.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Devis non trouvé'})
            
        thematics = devis.lignes_devis.filter(thematique__isnull=False).values(
            'thematique__id', 'thematique__label'
        ).distinct()
        
        participants = Participant.objects.filter(devis=devis).values(
            'id', 'nom', 'prenom', 'email', 'poste'
        )
        
        client = devis.client
        
    if client.type_prospect == 'particulier':
        participants = list(participants)
        participants.append({
            'id': f"prospect_{client.id}",
            'nom': client.nom,
            'prenom': client.prenom,
            'email': client.email,
            'is_prospect': True
        })

    trainers_list = []
    for f in Formateurs.objects.all():
        trainers_list.append({'id': f"f_{f.id}", 'nom': f.nom, 'prenom': f.prenom, 'type': 'Formateur'})
    for c in Consultant.objects.all():
        trainers_list.append({'id': f"c_{c.id}", 'nom': c.nom, 'prenom': c.prenom, 'type': 'Consultant'})
    
    return JsonResponse({
        'thematics': list(thematics),
        'participants': list(participants),
        'trainers': trainers_list
    }, safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('con', 'add')
@transaction.atomic
def ApiSaveConseilGroupe(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        doc_id = data.get('devis_id')
        
        is_facture = False
        actual_id = doc_id
        if str(doc_id).startswith('devis_'):
            actual_id = str(doc_id).replace('devis_', '')
        elif str(doc_id).startswith('facture_'):
            is_facture = True
            actual_id = str(doc_id).replace('facture_', '')
            
        devis = None
        facture = None
        if is_facture:
            try:
                facture = Facture.objects.get(id=actual_id) 
            except Facture.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Facture introuvable.'})
        else:
            try:
                devis = Devis.objects.get(id=actual_id) 
            except Devis.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Devis introuvable.'})
        
        groupe = GroupeConseil.objects.create(
            nom=data.get('nom'),
            devis=devis,
            facture=facture,
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            created_by=request.user,
            etat='enc'
        )
        
        # Participants
        for p_id in data.get('participants', []):
            if str(p_id).startswith('prospect_'):
                real_id = str(p_id).split('_')[1]
                try:
                    prospect = Prospets.objects.get(id=real_id) 
                except Prospets.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Prospets introuvable.'})
                
                participant, created = Participant.objects.get_or_create(
                    prospect=prospect,
                    devis=devis,
                    facture=facture,
                    defaults={
                        'nom': prospect.nom,
                        'prenom': prospect.prenom,
                        'email': prospect.email,
                        'telephone': prospect.tel_1
                    }
                )
                GroupeConseilParticipant.objects.create(groupe=groupe, participant=participant)
            else:
                try:
                    participant = Participant.objects.get(id=p_id) 
                except Participant.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Participant introuvable.'})
                GroupeConseilParticipant.objects.create(groupe=groupe, participant=participant)
                
        # Thematics
        for assign in data.get('assignments', []):
            try:
                thematique = Thematiques.objects.get(id=assign.get('thematique_id')) 
            except Thematiques.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Thematiques introuvable.'})
            formateur = None
            consultant = None
            
            intervenant_id = assign.get('formateur_id')
            if intervenant_id:
                if str(intervenant_id).startswith('f_'):
                    real_id = str(intervenant_id).replace('f_', '')
                    try:
                        formateur = Formateurs.objects.get(id=real_id) 
                    except Formateurs.DoesNotExist:
                        return JsonResponse({'status': 'error', 'message': 'Formateur introuvable.'})
                elif str(intervenant_id).startswith('c_'):
                    real_id = str(intervenant_id).replace('c_', '')
                    try:
                        consultant = Consultant.objects.get(id=real_id)
                    except Consultant.DoesNotExist:
                        return JsonResponse({'status': 'error', 'message': 'Consultant introuvable.'})
                else:
                    # Rétrocompatibilité au cas où l'ID est brut
                    try:
                        formateur = Formateurs.objects.get(id=intervenant_id)
                    except Formateurs.DoesNotExist:
                        pass
                
            GroupeConseilThematique.objects.create(
                groupe=groupe,
                thematique=thematique,
                formateur=formateur,
                consultant=consultant,
                date_debut=groupe.start_date,
                date_fin=groupe.end_date
            )
            
            
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='CREATE',
            target_model='GroupeConseil',
            target_id=str(groupe.id),
            details=f"Création d'un groupe conseil: {groupe.nom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
            
        messages.success(request, f"Le groupe {groupe.nom} a été créé avec succès.")
        return JsonResponse({'status': 'success', 'message': 'Groupe créé avec succès', 'groupe_id': groupe.id})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'delete')
@transaction.atomic
def ApiDeleteGroupeConseil(request):
    if request.method == "GET":
        id = request.GET.get('id')
        if not id:
            return JsonResponse({"status": "error", "message": "Informations manquantes"})
        
        try:
            groupe = GroupeConseil.objects.get(id=id)
            # Remove state restriction to allow deletion of active/closed groups
            nom_groupe = groupe.nom
            groupe.delete()
            
            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='DELETE',
                target_model='GroupeConseil',
                target_id=str(id),
                details=f"Suppression du groupe conseil: {nom_groupe}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, "Le groupe a été supprimé avec succès")
            return JsonResponse({"status": "success"})
        except GroupeConseil.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Groupe non trouvé"})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'change')
@transaction.atomic
def ApiCloturerGroupeConseil(request):
    id = request.GET.get('id')
    if not id:
        return JsonResponse({"status": "error", "message": "Informations manquantes"})
    
    try:
        groupe = GroupeConseil.objects.get(id=id)
        
        # We allow closing even if the end date hasn't passed
        groupe.etat = 'cloture'
        groupe.save()
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='GroupeConseil',
            target_id=str(groupe.id),
            details=f"Clôture du groupe conseil: {groupe.nom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({"status": "success", "message": "Le groupe a été clôturé avec succès."})
    except GroupeConseil.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Groupe non trouvé."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'change')
@transaction.atomic
def ApiUpdateGroupeSettings(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        groupe_id = data.get('groupe_id')
        lieu = data.get('lieu_formation')
        jours = data.get('jours_travail')
        
        try:
            groupe = GroupeConseil.objects.get(id=groupe_id) 
        except GroupeConseil.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'GroupeConseil introuvable.'})
        groupe.lieu_formation = lieu
        groupe.jours_travail = jours
        groupe.save()
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='GroupeConseil',
            target_id=str(groupe.id),
            details=f"Mise à jour des paramètres du groupe conseil: {groupe.nom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({'status': 'success', 'message': 'Paramètres mis à jour'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'add')
@transaction.atomic
def ApiAddPlanningSession(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        from t_conseil.models import GroupeConseilPlanning, GroupeConseilThematique
        
        try:
            groupe = GroupeConseil.objects.get(id=data.get('groupe_id')) 
        except GroupeConseil.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'GroupeConseil introuvable.'})
        try:
            thematique = Thematiques.objects.get(id=data.get('thematique_id')) 
        except Thematiques.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Thematiques introuvable.'})
        
        # Auto-detect formateur from the group's thematic association
        assoc = GroupeConseilThematique.objects.filter(groupe=groupe, thematique=thematique).first()
        formateur = assoc.formateur if assoc else None
        consultant = assoc.consultant if assoc else None

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
            consultant=consultant,
            date=date_obj,
            heure_debut=time_start_obj,
            heure_fin=time_end_obj,
            note=data.get('note')
        )
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='CREATE',
            target_model='GroupeConseilPlanning',
            target_id=str(session.id),
            details=f"Ajout d'une session de planning au groupe: {groupe.nom} (Date: {date_obj})",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Session ajoutée au planning',
            'session': {
                'id': session.id,
                'date': date_obj.strftime('%d/%m/%Y'),
                'heure': f"{time_start_obj.strftime('%H:%M')} - {time_end_obj.strftime('%H:%M')}",
                'thematique': session.thematique.label,
                'formateur': str(session.consultant) if session.consultant else (str(session.formateur) if session.formateur else "N/A")
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'delete')
@transaction.atomic
def ApiDeletePlanningSession(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        from t_conseil.models import GroupeConseilPlanning
        try:
            session = GroupeConseilPlanning.objects.get(id=data.get('session_id')) 
        except GroupeConseilPlanning.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'GroupeConseilPlanning introuvable.'})
            
        session_info = f"{session.groupe.nom} (Date: {session.date})"
        session.delete()
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='DELETE',
            target_model='GroupeConseilPlanning',
            target_id=str(data.get('session_id')),
            details=f"Suppression d'une session de planning: {session_info}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({'status': 'success', 'message': 'Session supprimée'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
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
            'groupe__facture__client',
            'groupe__facture__entreprise',
            'thematique',
            'formateur',
            'consultant'
        ), 
        id=session_id
    )
    groupe = session.groupe
    participants = groupe.participants_groupe.all().select_related('participant')

    client_logo_path = None
    enterprise_logo_path = None
    
    doc = groupe.devis if groupe.devis else groupe.facture
    
    if doc and doc.client and doc.client.logo_entreprise:
        try:
            client_logo_path = Path(doc.client.logo_entreprise.path).as_uri()
        except ValueError:
            pass

    if doc and doc.entreprise and doc.entreprise.logo:
        try:
            enterprise_logo_path = Path(doc.entreprise.logo.path).as_uri()
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
@module_permission_required('con', 'approuv')
@transaction.atomic
def ApiConfirmParticipantForScolarite(request):
    if request.method == "POST":
        participant_id = request.POST.get('participant_id')
        if not participant_id:
            return JsonResponse({'status': 'error', 'message': 'ID participant manquant'})
        
        participant = get_object_or_404(Participant, id=participant_id)
        participant.is_confirmed_for_scolarite = True
        participant.scolarite_note = request.POST.get('note', '')
        participant.save()
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='Participant',
            target_id=str(participant.id),
            details=f"Confirmation scolarité pour le participant: {participant.nom} {participant.prenom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({'status': 'success', 'message': 'Participant confirmé pour la Scolarité'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'approuv')
@transaction.atomic
def ApiCancelParticipantConfirmationForScolarite(request):
    if request.method == "POST":
        participant_id = request.POST.get('participant_id')
        if not participant_id:
            return JsonResponse({'status': 'error', 'message': 'ID participant manquant'})
        
        participant = get_object_or_404(Participant, id=participant_id)
        participant.is_confirmed_for_scolarite = False
        participant.scolarite_note = None
        participant.save()
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='Participant',
            target_id=str(participant.id),
            details=f"Annulation confirmation scolarité pour le participant: {participant.nom} {participant.prenom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({'status': 'success', 'message': 'Confirmation annulée avec succès'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'approuv')
def ApiUpdateSessionReport(request):
    import json
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
        
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        realisee = data.get('realisee', False)
        resume_seance = data.get('resume_seance', '')
        
        session = GroupeConseilPlanning.objects.get(id=session_id)
        session.realisee = realisee
        session.resume_seance = resume_seance
        session.save()
        
        return JsonResponse({'status': 'success', 'message': 'Compte rendu enregistré avec succès'})
    except GroupeConseilPlanning.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Session introuvable'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'change')
@transaction.atomic
def ApiUpdateThematiqueIntervenant(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})
        
    try:
        data = json.loads(request.body)
        affectation_id = data.get('affectation_id')
        intervenant_id = data.get('intervenant_id')
        
        try:
            affectation = GroupeConseilThematique.objects.get(id=affectation_id)
        except GroupeConseilThematique.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Affectation introuvable.'})
            
        formateur = None
        consultant = None
        
        if intervenant_id:
            if str(intervenant_id).startswith('f_'):
                real_id = str(intervenant_id).replace('f_', '')
                try:
                    formateur = Formateurs.objects.get(id=real_id) 
                except Formateurs.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Formateur introuvable.'})
            elif str(intervenant_id).startswith('c_'):
                real_id = str(intervenant_id).replace('c_', '')
                try:
                    consultant = Consultant.objects.get(id=real_id)
                except Consultant.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Consultant introuvable.'})
            else:
                # Rétrocompatibilité
                try:
                    formateur = Formateurs.objects.get(id=intervenant_id)
                except Formateurs.DoesNotExist:
                    pass
                    
        affectation.formateur = formateur
        affectation.consultant = consultant
        affectation.save()
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='GroupeConseilThematique',
            target_id=str(affectation.id),
            details=f"Modification de l'intervenant pour la thématique: {affectation.thematique.label}",
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return JsonResponse({'status': 'success', 'message': 'Intervenant mis à jour avec succès'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
