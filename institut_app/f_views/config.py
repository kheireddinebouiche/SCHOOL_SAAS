from decimal import Decimal
from institut_app.decorators import superuser_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import GlobalConfiguration
from django.views.decorators.csrf import csrf_exempt

@login_required
@superuser_required
def general_settings_view(request):
    """
    Renders the general configuration page.
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    config = GlobalConfiguration.get_solo()
    context = {
        'config': config,
        'tenant': request.tenant,
        'users': User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    }
    return render(request, 'tenant_folder/configuration/general_settings.html', context)

from django.db import models

@csrf_exempt
@login_required
@superuser_required
def api_update_global_settings(request):
    """
    API endpoint to update global settings via AJAX.
    """
    if request.method == 'POST':
        setting_name = request.POST.get('setting_name')
        setting_value = request.POST.get('setting_value')
        
        config = GlobalConfiguration.get_solo()
        
        if '__' in setting_name:
            field_name, key_name = setting_name.split('__', 1)
            if hasattr(config, field_name):
                field = config._meta.get_field(field_name)
                if isinstance(field, models.JSONField):
                    current_val = getattr(config, field_name) or {}
                    current_val[key_name] = str(setting_value).lower() == 'true'
                    setattr(config, field_name, current_val)
                    config.save()
                    
                    from t_crm.models import UserActionLog
                    UserActionLog.objects.create(
                        user=request.user,
                        action_type='UPDATE',
                        target_model='GlobalConfiguration',
                        target_id=str(config.id),
                        details=f"Mise à jour du paramètre global {field_name}[{key_name}] = {current_val[key_name]}",
                        ip_address=request.META.get('REMOTE_ADDR')
                    )
                    return JsonResponse({'status': 'success', 'message': 'Paramètre mis à jour avec succès.'})

        if hasattr(config, setting_name):
            # Get the field type to handle conversion
            field = config._meta.get_field(setting_name)
            
            if isinstance(field, models.BooleanField):
                val = str(setting_value).lower() == 'true'
            elif isinstance(field, (models.IntegerField, models.PositiveIntegerField)):
                try:
                    val = int(setting_value) if setting_value else 0
                except (ValueError, TypeError):
                    return JsonResponse({'status': 'error', 'message': 'Valeur numérique invalide.'}, status=400)
            elif isinstance(field, models.ManyToManyField):
                import json
                try:
                    val_list = json.loads(setting_value)
                    getattr(config, setting_name).set(val_list)
                    
                    from t_crm.models import UserActionLog
                    UserActionLog.objects.create(
                        user=request.user,
                        action_type='UPDATE',
                        target_model='GlobalConfiguration',
                        target_id=str(config.id),
                        details=f"Mise à jour du paramètre global (relation multiple) {setting_name}",
                        ip_address=request.META.get('REMOTE_ADDR')
                    )

                    return JsonResponse({'status': 'success', 'message': 'Paramètre mis à jour avec succès.'})
                except Exception as e:
                    return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            elif isinstance(field, models.JSONField):
                import json
                try:
                    val = json.loads(setting_value)
                except Exception:
                    val = setting_value
            else:
                val = setting_value
                
            setattr(config, setting_name, val)
            config.save()
            
            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='GlobalConfiguration',
                target_id=str(config.id),
                details=f"Mise à jour du paramètre global {setting_name} = {val}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({'status': 'success', 'message': 'Paramètre mis à jour avec succès.'})
        
        return JsonResponse({'status': 'error', 'message': 'Paramètre non trouvé.'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@csrf_exempt
@login_required
@superuser_required
def api_update_tenant_settings(request):
    """
    API endpoint to update Institut (tenant) details.
    """
    if request.method == 'POST':
        tenant = request.tenant
        nom = request.POST.get('nom')
        adresse = request.POST.get('adresse')
        telephone = request.POST.get('telephone')
        
        if nom:
            tenant.nom = nom
        if adresse is not None:
            tenant.adresse = adresse
        if telephone is not None:
            tenant.telephone = telephone
            
        tenant.save()
        
        from t_crm.models import UserActionLog
        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='Institut',
            target_id=str(tenant.id),
            details=f"Mise à jour des informations de l'établissement {tenant.nom}",
            ip_address=request.META.get('REMOTE_ADDR')
        )

        return JsonResponse({
            'status': 'success', 
            'message': 'Détails de l\'établissement mis à jour avec succès.'
        })
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@login_required
@superuser_required
def ConfigurationDashboardView(request):
    """
    Renders the main Configuration Dashboard with KPIs and quick links.
    """
    from django.contrib.auth import get_user_model
    from t_crm.models import UserActionLog
    from institut_app.models import Role
    from django.utils import timezone
    from datetime import timedelta

    User = get_user_model()
    
    # KPIs
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_roles = Role.objects.count()
    
    # Active sessions proxy (users with a session key, or you can use your active_sessions logic if it exists)
    # Let's count recent actions as proxy for activity if true sessions are hard to query here
    recent_actions = UserActionLog.objects.order_by('-created_at')[:5]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_roles': total_roles,
        'recent_actions': recent_actions,
        'tenant': request.tenant,
    }

    return render(request, 'tenant_folder/configuration/dashboard.html', context)

from django.db.models import Q
from t_crm.models import Prospets, NotesProcpects, RendezVous, RelancesProspet, Derogations, DemandeInscription, FicheDeVoeux, FicheVoeuxDouble, RemiseAppliquerLine
from t_tresorerie.models import EcheancierPaiement, EcheancierSpecial, Paiements, Rembourssements, DuePaiements, ClientPaiementsRequest
from t_groupe.models import GroupeLine
from t_exam.models import ExamNote
from django.http import JsonResponse

@login_required
@superuser_required
def GestionDonneesPage(request):
    prospects = Prospets.objects.all().order_by('-created_at')
    
    from saas_admin_app.models import SaaSGlobalConfiguration
    config = SaaSGlobalConfiguration.get_solo()
    
    # Si aucun mot de passe n'est défini, on considère que c'est toujours déverrouillé
    is_unlocked = True
    if config.gestion_donnees_password:
        is_unlocked = request.session.get('gestion_donnees_unlocked', False)
        
    context = {
        'tenant': request.tenant,
        'prospects': prospects,
        'is_unlocked': is_unlocked
    }
    return render(request, 'tenant_folder/configuration/gestion_donnees.html', context)

@login_required
@superuser_required
def ApiUnlockGestionDonnees(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        from saas_admin_app.models import SaaSGlobalConfiguration
        config = SaaSGlobalConfiguration.get_solo()
        
        if config.gestion_donnees_password and password == config.gestion_donnees_password:
            request.session['gestion_donnees_unlocked'] = True
            return JsonResponse({'status': 'success', 'message': 'Accès déverrouillé'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Mot de passe incorrect'})
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@login_required
@superuser_required
def ApiSearchProspects(request):
    q = request.GET.get('q', '')
    query = Q(nom__icontains=q) | Q(prenom__icontains=q) | Q(nin__icontains=q) | Q(email__icontains=q)
    prospects = Prospets.objects.filter(query)[:20]
    
    results = []
    for p in prospects:
        results.append({
            'id': p.id,
            'text': f"{p.nom or ''} {p.prenom or ''} - {p.nin or ''}"
        })
    return JsonResponse({'results': results})

@login_required
@superuser_required
def ApiProspectHistory(request, prospect_id):
    try:
        p = Prospets.objects.get(id=prospect_id)
    except Prospets.DoesNotExist:
        return JsonResponse({'error': 'Prospect not found'}, status=404)

    # CRM
    notes = NotesProcpects.objects.filter(prospect=p).order_by('-created_at')
    rendezvous = RendezVous.objects.filter(prospect=p).order_by('-created_at')
    relances = RelancesProspet.objects.filter(prospect=p).order_by('-date_relance')
    derogations = Derogations.objects.filter(demandeur=p).order_by('-created_at')

    # SCOLARITE
    demandes = DemandeInscription.objects.filter(visiteur__nom=p.nom, visiteur__prenom=p.prenom) if hasattr(p, 'nom') else []
    
    voeux_std = FicheDeVoeux.objects.filter(prospect=p)
    voeux_dbl = FicheVoeuxDouble.objects.filter(prospect=p)

    groupes_affecte = []
    try:
        lines = GroupeLine.objects.filter(student=p)
        for l in lines:
            if l.groupe:
                groupes_affecte.append({'nom': l.groupe.label})
    except Exception:
        pass

    examens = []
    try:
        notes_ex = ExamNote.objects.filter(etudiant=p)
        for n in notes_ex:
            examens.append({
                'module': n.type_note.label if hasattr(n, 'type_note') and n.type_note else 'Examen',
                'date': n.created_at.strftime('%d/%m/%Y') if hasattr(n, 'created_at') else '',
                'note': str(n.valeur) if hasattr(n, 'valeur') else ''
            })
    except Exception:
        pass

    # TRESORERIE
    ech_data = []
    try:
        dues = DuePaiements.objects.filter(client=p)
        for d in dues:
            ech_data.append({
                'type': d.label if d.label else 'Echéance',
                'details': 'Montant dû',
                'montant': str(d.montant_due) if hasattr(d, 'montant_due') and d.montant_due else '0',
                'restant': str(d.montant_restant) if hasattr(d, 'montant_restant') and d.montant_restant else '0',
                'date': d.date_echeance.strftime('%d/%m/%Y') if hasattr(d, 'date_echeance') and d.date_echeance else ''
            })
        ech_sp = EcheancierSpecial.objects.filter(prospect=p)
        for e in ech_sp:
            ech_data.append({
                'type': 'Spécial',
                'details': 'Echéancier Spécial',
                'montant': '0',
                'restant': '0',
                'date': ''
            })
    except Exception:
        pass

    paiements_data = []
    try:
        payms = Paiements.objects.filter(prospect=p).order_by('-date_paiement')
        for p_obj in payms:
            paiements_data.append({
                'id': p_obj.id,
                'is_refund': False,
                'montant': str(p_obj.montant_paye) if hasattr(p_obj, 'montant_paye') else '0',
                'date': p_obj.date_paiement.strftime('%d/%m/%Y') if hasattr(p_obj, 'date_paiement') and p_obj.date_paiement else '',
                'reference': p_obj.num if hasattr(p_obj, 'num') and p_obj.num else (p_obj.paiement_label if hasattr(p_obj, 'paiement_label') else '')
            })
    except Exception:
        pass
        
    try:
        remb = Rembourssements.objects.filter(client=p)
        for r_obj in remb:
            paiements_data.append({
                'is_refund': True,
                'montant': str(r_obj.allowed_amount) if hasattr(r_obj, 'allowed_amount') and r_obj.allowed_amount else '0',
                'date': r_obj.created_at.strftime('%d/%m/%Y') if hasattr(r_obj, 'created_at') else '',
                'reference': r_obj.motif_rembourssement if hasattr(r_obj, 'motif_rembourssement') else 'Remboursement'
            })
    except Exception:
        pass
        
    remises_data = []
    try:
        rem_lines = RemiseAppliquerLine.objects.filter(prospect=p)
        for rl in rem_lines:
            remises_data.append({
                'remise_label': rl.remise_appliquer.remise.label if rl.remise_appliquer and rl.remise_appliquer.remise else 'Remise',
                'date': rl.created_at.strftime('%d/%m/%Y'),
                'is_applicated': rl.remise_appliquer.is_applicated if rl.remise_appliquer else False
            })
    except Exception:
        pass

    data = {
        'base': {
            'nom': p.nom,
            'prenom': p.prenom,
            'email': p.email,
            'telephone': p.telephone,
            'indic': p.indic,
            'nin': p.nin,
            'statut': p.get_statut_display() if hasattr(p, 'get_statut_display') else p.statut,
            'etat': p.get_etat_display() if hasattr(p, 'get_etat_display') else p.etat,
        },
        'crm': {
            'notes': [{'date': n.created_at.strftime('%d/%m/%Y'), 'note': n.note, 'tag': n.tage} for n in notes],
            'rendezvous': [{'date': r.date_rendez_vous.strftime('%d/%m/%Y') if r.date_rendez_vous else r.created_at.strftime('%d/%m/%Y'), 'type': r.get_type_display(), 'statut': r.get_statut_display()} for r in rendezvous],
            'relances': [{'date': r.date_relance.strftime('%d/%m/%Y') if hasattr(r, 'date_relance') and r.date_relance else '', 'canal': r.get_canal_display(), 'objet': r.objet} for r in relances],
            'derogations': [{'date': d.created_at.strftime('%d/%m/%Y'), 'type': d.type, 'motif': d.motif, 'statut': d.get_statut_display()} for d in derogations],
        },
        'scolarite': {
            'demandes': [{'date': d.created_at.strftime('%d/%m/%Y'), 'formation': d.formation.label if d.formation else '', 'specialite': d.specialite.label if d.specialite else '', 'etat': d.get_etat_display()} for d in demandes],
            'voeux': [{'type': 'Standard', 'specialite': v.specialite.label if v.specialite else '', 'is_confirmed': v.is_confirmed} for v in voeux_std] + 
                     [{'type': 'Double Diplomation', 'specialite': v.specialite.label if hasattr(v, 'specialite') and v.specialite else '', 'is_confirmed': v.is_confirmed} for v in voeux_dbl],
            'groupes': groupes_affecte,
            'examens': examens,
        },
        'tresorerie': {
            'echeanciers': ech_data,
            'paiements': paiements_data,
            'remises': remises_data
        }
    }
    return JsonResponse(data)

def api_reset_prospect(request, prospect_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Non autorisé'}, status=403)
        
    try:
        p = Prospets.objects.get(id=prospect_id)
        
        # 1. Scolarité (Voeux, Inscriptions, Groupes, Exams)
        FicheDeVoeux.objects.filter(prospect=p).update(is_confirmed=False)
        FicheVoeuxDouble.objects.filter(prospect=p).update(is_confirmed=False)
        DemandeInscription.objects.filter(visiteur__nom=p.nom, visiteur__prenom=p.prenom).delete()
        GroupeLine.objects.filter(student=p).delete()
        ExamNote.objects.filter(etudiant=p).delete()
        
        # 2. Trésorerie
        DuePaiements.objects.filter(client=p).delete()
        ClientPaiementsRequest.objects.filter(client=p).delete()
        EcheancierSpecial.objects.filter(prospect=p).delete()
        Paiements.objects.filter(prospect=p).delete()
        Rembourssements.objects.filter(client=p).delete()
        RemiseAppliquerLine.objects.filter(prospect=p).delete()
        
        # 3. CRM Dérogations
        Derogations.objects.filter(demandeur=p).delete()
        
        # 4. Reset Prospect
        p.statut = 'visiteur'
        p.etat = 'en_attente'
        p.save()
        
        return JsonResponse({'status': 'success', 'message': 'Le prospect a été réinitialisé avec succès.'})
    except Prospets.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Prospect introuvable'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@csrf_exempt
def api_delete_paiement(request, paiement_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Non autorisé'}, status=403)
        
    if request.method == 'POST':
        try:
            paiement = Paiements.objects.get(id=paiement_id)
            
            # Reset montant due if linked
            if paiement.due_paiements:
                due = paiement.due_paiements
                if paiement.montant_paye:
                    due.montant_restant = Decimal(str(due.montant_restant)) + Decimal(str(paiement.montant_paye))
                    if due.montant_restant > 0:
                        due.is_done = False
                due.save()
            
            paiement.delete()
            return JsonResponse({'status': 'success', 'message': 'Le paiement a été supprimé et le montant dû réinitialisé.'})
        except Paiements.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paiement introuvable'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
