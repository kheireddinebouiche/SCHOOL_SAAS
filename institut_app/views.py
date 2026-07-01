from institut_app.decorators import superuser_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from decimal import Decimal, InvalidOperation
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django_tenants.utils import schema_context
from .form import *
from .models import Profile
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.db import transaction
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from t_crm.models import *
from t_exam.models import *
from t_tresorerie.models import DuePaiements
from t_formations.models import Promos
from t_groupe.models import Groupe, GroupeLine
from t_timetable.models import Timetable, TimetableEntry, Salle
from t_rh.models import Employees, Contrats, Services, Posts
from t_ressource_humaine.models import FichePaie
from .models import UserSession, Profile
from django.contrib.sessions.models import Session
from django.utils import timezone
import datetime
from datetime import datetime, timedelta
from django.db.models import Count, Sum
from t_tresorerie.models import DuePaiements, Paiements, Depenses, ClientPaiementsRequest
import calendar
from django.db.models.functions import TruncMonth
from .decorators import ajax_required, module_permission_required, role_required
from .utils_notifications import send_notification_to_user


@login_required(login_url='institut_app:login')
def crm_dashboard(request):
    # KPIs
    total_prospects = Prospets.objects.count()
    
    # Nouveaux prospects cette semaine
    one_week_ago = datetime.now() - timedelta(days=7)
    new_prospects_this_week = Prospets.objects.filter(created_at__gte=one_week_ago).count()
    
    # Rappels en attente
    pending_reminders = RendezVous.objects.filter(statut='en_attente').count()
    
    # Taux de conversion (prospects convertis en visiteurs)
    converted_prospects = Prospets.objects.filter(statut='convertit').count()
    conversion_rate = (converted_prospects / total_prospects * 100) if total_prospects > 0 else 0
    
    # Derniers rappels
    recent_reminders = RendezVous.objects.filter(archived=False).select_related('prospect').order_by('-created_at')[:5]
    
    # Répartition des prospects par canal
    prospects_by_channel = Prospets.objects.values('canal').annotate(count=Count('canal')).order_by('-count')
    
    # Calcul du taux de conversion par canal
    channel_conversion_data = []
    for channel in prospects_by_channel:
        canal = channel['canal']
        total = channel['count']
        converted = Prospets.objects.filter(canal=canal, statut='convertit').count()
        conversion_rate = (converted / total * 100) if total > 0 else 0
        channel_conversion_data.append({
            'canal': canal,
            'count': total,
            'conversion_rate': round(conversion_rate, 2)
        })
    
    # Répartition des prospects par statut - version avec données factices pour test
    prospects_by_status = Prospets.objects.values('statut').annotate(count=Count('statut')).order_by('-count')
    
    # Ajout des labels pour l'affichage
    status_labels = {
        'visiteur': 'Visiteur',
        'prinscrit': 'Pré-inscrit',
        'instance': 'Instance',
        'convertit': 'Converti'
    }
    
    prospects_by_status_with_labels = []
    for status in prospects_by_status:
        status_code = status['statut']
        count = status['count']
        label = status_labels.get(status_code, status_code)
        prospects_by_status_with_labels.append({
            'status': status_code,
            'label': label,
            'count': count
        })
    
    # Si aucune donnée n'est disponible, utiliser des données factices pour test
    if not prospects_by_status_with_labels:
        prospects_by_status_with_labels = [
            {'status': 'visiteur', 'label': 'Visiteur', 'count': 150},
            {'status': 'prinscrit', 'label': 'Pré-inscrit', 'count': 80},
            {'status': 'instance', 'label': 'Instance', 'count': 45},
            {'status': 'convertit', 'label': 'Converti', 'count': 30}
        ]
        total_prospects = 305
        
    # Répartition des prospects par source (lead_source)
    prospects_by_lead_source = Prospets.objects.values('canal').annotate(count=Count('canal')).order_by('-count')
    
    # Ajout des labels pour l'affichage des sources
    lead_source_labels = {
        'viste': 'Visite',
        'appel': 'Appel',
        'prospectus': 'Prospectus'
    }
    
    lead_source_data = []
    for source in prospects_by_lead_source:
        source_code = source['canal']
        count = source['count']
        # Only include sources that have a count > 0
        if count > 0 and source_code is not None:
            label = lead_source_labels.get(source_code, source_code)
            lead_source_data.append({
                'source': source_code,
                'label': label,
                'count': count
            })
    
    # Répartition des prospects par promotion (à partir des fiches de voeux)
    prospects_by_promo = FicheDeVoeux.objects.values('promo__label').annotate(
        count=Count('prospect', distinct=True)
    ).order_by('-count')
    
    # Répartition des prospects par spécialité (à partir des fiches de voeux)
    prospects_by_speciality = FicheDeVoeux.objects.values('specialite__label').annotate(
        count=Count('prospect', distinct=True)
    ).order_by('-count')
    
    # --- Statistiques Fiche de Voeux & Double Diplomation ---
    
    # 1. Fiche de Voeux Simple
    # Group by Specialite, Promo, and Status
    fiche_voeux_stats = FicheDeVoeux.objects.values(
        'specialite__label', 
        'promo__label', 
        'is_confirmed'
    ).annotate(
        count=Count('id')
    ).order_by('specialite__label', 'promo__label')
    
    # 2. Fiche de Voeux Double
    # Group by Specialite (Double Diplomation), Promo, and Status
    fiche_voeux_double_stats = FicheVoeuxDouble.objects.values(
        'specialite__label', 
        'promo__label', 
        'is_confirmed'
    ).annotate(
        count=Count('id')
    ).order_by('specialite__label', 'promo__label')

    # Données pour le graphique des prospects par période (derniers 7 jours)
    from django.db.models.functions import TruncDate

    # Calcul des prospects par jour pour les 7 derniers jours
    seven_days_ago = datetime.now() - timedelta(days=6)  # 7 jours incluant aujourd'hui
    prospects_by_date = Prospets.objects.filter(
        created_at__gte=seven_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Création des données pour le graphique
    chart_dates = []
    chart_counts = []

    # Remplir les dates manquantes avec 0
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).date()
        chart_dates.append(date.strftime('%b %d'))  # Format 'Jan 01'

        # Trouver le compte pour cette date ou 0 si non trouvé
        count = 0
        for item in prospects_by_date:
            if item['date'] == date:
                count = item['count']
                break
        chart_counts.append(count)

    # Données pour le graphique des rappels
    reminders_by_date = RendezVous.objects.filter(
        created_at__gte=seven_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    reminder_counts = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).date()

        # Trouver le compte pour cette date ou 0 si non trouvé
        count = 0
        for item in reminders_by_date:
            if item['date'] == date:
                count = item['count']
                break
        reminder_counts.append(count)

    context = {
        'tenant': request.tenant,
        'total_prospects': total_prospects,
        'new_prospects_this_week': new_prospects_this_week,
        'pending_reminders': pending_reminders,
        'conversion_rate': round(conversion_rate, 2),
        'recent_reminders': recent_reminders,
        'channel_conversion_data': channel_conversion_data,
        'prospects_by_status': prospects_by_status_with_labels,
        'lead_source_data': lead_source_data,
        'prospects_by_promo': prospects_by_promo,
        'prospects_by_speciality': prospects_by_speciality,
        'chart_dates': chart_dates,
        'chart_counts': chart_counts,
        'chart_counts': chart_counts,
        'reminder_counts': reminder_counts,
        'fiche_voeux_stats': fiche_voeux_stats,
        'fiche_voeux_double_stats': fiche_voeux_double_stats,
    }
    
    return render(request, 'tenant_folder/dashboard/crm_dashboard.html', context)

@login_required(login_url='institut_app:login')
def rh_dashboard(request):
    # KPIs de base
    total_employees = Employees.objects.count()
    active_employees = Employees.objects.filter(etat='en cours').count()
    total_contracts = Contrats.objects.count()
    total_services = Services.objects.count()

    # Répartition par genre
    gender_stats = Employees.objects.values('genre').annotate(count=Count('genre'))
    gender_labels = []
    gender_counts = []
    gender_map = {'M': 'Masculin', 'F': 'Féminin'}
    for stat in gender_stats:
        if stat['genre']:
            gender_labels.append(gender_map.get(stat['genre'], stat['genre']))
            gender_counts.append(stat['count'])

    # Répartition par situation familiale
    family_stats = Employees.objects.values('situation_familiale').annotate(count=Count('situation_familiale'))
    family_labels = []
    family_counts = []
    family_map = {'C': 'Célibataire', 'M': 'Marié(e)', 'D': 'Divorcé(e)', 'V': 'Veuf(ve)'}
    for stat in family_stats:
        if stat['situation_familiale']:
            family_labels.append(family_map.get(stat['situation_familiale'], stat['situation_familiale']))
            family_counts.append(stat['count'])

    # Recrutements récents (30 derniers jours)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_hires = Employees.objects.filter(created_at__gte=thirty_days_ago).order_by('-created_at')[:5]

    # Contrats arrivant à échéance (dans les 30 prochains jours)
    next_month = timezone.now().date() + timedelta(days=30)
    expiring_contracts = Contrats.objects.filter(date_fin__gte=timezone.now().date(), date_fin__lte=next_month).select_related('employee')

    context = {
        'tenant': request.tenant,
        'total_employees': total_employees,
        'active_employees': active_employees,
        'total_contracts': total_contracts,
        'total_services': total_services,
        'gender_labels': json.dumps(gender_labels),
        'gender_counts': json.dumps(gender_counts),
        'family_labels': json.dumps(family_labels),
        'family_counts': json.dumps(family_counts),
        'recent_hires': recent_hires,
        'expiring_contracts': expiring_contracts,
    }
    
    return render(request, 'tenant_folder/dashboard/rh_dashboard.html', context)

def default_dashboard(request):
    pass

@login_required(login_url="institut_app:login")
@module_permission_required('tre','view')
@module_permission_required('tre','add')
@role_required('tre', ['Administrateur','Manager','Utilisateur','Superviseur'])
def FinanceDashboard(request):
    # 1. Unpaid Dues by Promo
    # Try fetching promo from the echeancier model if direct promo is null
    unpaid_dues_by_promo = DuePaiements.objects.filter(is_done=False).values('ref_echeancier__model__promo__label').annotate(
        promo_label=models.F('ref_echeancier__model__promo__label'),
        total_amount=Sum('montant_restant')
    ).order_by('-total_amount')

    # Calculate total unpaid
    total_unpaid = DuePaiements.objects.filter(is_done=False).aggregate(Sum('montant_restant'))['montant_restant__sum'] or 0

    # 2. Monthly Financial Analysis (Revenue vs Expenses)
    # Get last 6 months
    today = datetime.now()
    monthly_stats = []
    current_month_date = today
    for i in range(6):
        month_start = datetime(current_month_date.year, current_month_date.month, 1)
        # End of month
        if month_start.month == 12:
            next_month_start = datetime(month_start.year + 1, 1, 1)
        else:
            next_month_start = datetime(month_start.year, month_start.month + 1, 1)
        month_end = next_month_start - timedelta(days=1)
        
        # Ensure we use aware datetimes if needed or just handle as is (depends on project settings)
        # But here we just need the range.
        
        # Revenue: Sum of Paiements in this month
        revenue = Paiements.objects.filter(
            date_paiement__gte=month_start, 
            date_paiement__lte=month_end
        ).aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
        
        # Expenses: Sum of Depenses in this month
        expenses = Depenses.objects.filter(
            date_paiement__gte=month_start,
            date_paiement__lte=month_end
        ).aggregate(Sum('montant_ttc'))['montant_ttc__sum'] or 0
        
        profit = revenue - expenses
        margin = (profit / revenue * 100) if revenue > 0 else 0
        
        monthly_stats.append({
            'period': month_start.strftime('%b %Y'),
            'revenue': float(revenue),
            'expenses': float(expenses),
            'profit': float(profit),
            'margin': float(margin),
            'is_positive': profit >= 0
        })
        # Move to previous month
        current_month_date = month_start - timedelta(days=1)

    # Reverse to chronological order (past to present)
    monthly_stats.reverse()

    # 3. Full Payment Situation (History)
    # Aggregate Paiements by Year-Month
    payment_qs = Paiements.objects.annotate(
        month=TruncMonth('date_paiement')
    ).values('month').annotate(
        total_revenue=Sum('montant_paye'),
        count=Count('id')
    ).order_by('-month')

    # Aggregate Depenses by Year-Month
    expense_qs = Depenses.objects.annotate(
        month=TruncMonth('date_paiement')
    ).values('month').annotate(
        total_expense=Sum('montant_ttc')
    ).order_by('-month')
    
    # Merge data
    history_map = {}
    
    for p in payment_qs:
        m = p['month']
        if m: # filter out None dates if any
            key = m.strftime('%Y-%m')
            history_map[key] = {
                'date': m,
                'revenue': p['total_revenue'] or 0,
                'count': p['count'],
                'expense': 0
            }
            
    for e in expense_qs:
        m = e['month']
        if m:
            key = m.strftime('%Y-%m')
            if key not in history_map:
                history_map[key] = {
                    'date': m,
                    'revenue': 0,
                    'count': 0,
                    'expense': 0
                }
            history_map[key]['expense'] = e['total_expense'] or 0
    
    # Convert to list and calculate result
    payment_history = []
    for key, val in history_map.items():
        val['result'] = val['revenue'] - val['expense']
        val['is_positive'] = val['result'] >= 0
        payment_history.append(val)
        
    # Sort by date descending
    payment_history.sort(key=lambda x: x['date'], reverse=True)

    context = {
        'tenant': request.tenant,
        'unpaid_dues_by_promo': unpaid_dues_by_promo,
        'total_unpaid': total_unpaid,
        'monthly_stats': monthly_stats,
        'payment_history': payment_history,
    }
    return render(request, 'tenant_folder/dashboard/finance_dash.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('int', 'view')
def pedago_dashboard(request):
    # KPIs
    total_groups = Groupe.objects.count()
    active_groups = Groupe.objects.filter(etat__in=['enc', 'inscription']).count() # 'enc', 'inscription' derived from model choices
    total_students = GroupeLine.objects.values('student').distinct().count()
    active_timetables = Timetable.objects.filter(is_validated=True).count()

    # Today's Sessions
    days_map = {
        'Monday': 'Lundi',
        'Tuesday': 'Mardi',
        'Wednesday': 'Mercredi',
        'Thursday': 'Jeudi',
        'Friday': 'Vendredi',
        'Saturday': 'Samedi',
        'Sunday': 'Dimanche'
    }
    today_english = datetime.now().strftime("%A")
    today_french = days_map.get(today_english, today_english)
    
    # Filter for today's sessions (temporarily showing ALL for debug/visualization if day match fails)
    # todays_sessions = TimetableEntry.objects.filter(jour__iexact=today_french).select_related('timetable__groupe', 'cours', 'salle', 'formateur').order_by('heure_debut')
    todays_sessions = TimetableEntry.objects.filter(timetable__is_validated=True).select_related('timetable__groupe', 'cours', 'salle', 'formateur').order_by('heure_debut')

    # Students per Specialty (Chart)
    students_per_speciality = GroupeLine.objects.values('groupe__specialite__label').annotate(
        count=Count('student', distinct=True)
    ).order_by('-count')
    
    speciality_labels = [item['groupe__specialite__label'] for item in students_per_speciality]
    speciality_counts = [item['count'] for item in students_per_speciality]

    # Room Utilization (Gantt Data)
    # We need to construct data for ApexCharts rangeBar: [{'x': 'Room Name', 'y': [start_timestamp, end_timestamp], ...}]
    gantt_data = []
    
    # Base date for timestamps (today)
    today_date = datetime.now().date()
    
    for session in todays_sessions:
        # Combine today's date with time to get datetime
        start_datetime = datetime.combine(today_date, session.heure_debut)
        end_datetime = datetime.combine(today_date, session.heure_fin)
        
        # Convert to milliseconds timestamp
        start_ts = int(start_datetime.timestamp() * 1000)
        end_ts = int(end_datetime.timestamp() * 1000)
        
        gantt_data.append({
            'x': session.salle.nom,
            'y': [start_ts, end_ts],
            'course': session.cours.label if session.cours else 'N/A',
            'group': session.timetable.groupe.nom,
            'teacher': f"{session.formateur.nom} {session.formateur.prenom}" if session.formateur else "Non assigné"
        })
    
    # Sort by room name
    gantt_data.sort(key=lambda item: item['x'])

    # Recent Groups activity
    recent_groups = Groupe.objects.order_by('-updated_at')[:5]

    context = {
        'tenant': request.tenant,
        'total_groups': total_groups,
        'active_groups': active_groups,
        'total_students': total_students,
        'active_timetables': active_timetables,
        'todays_sessions': todays_sessions,
        'speciality_labels': speciality_labels,
        'speciality_counts': speciality_counts,
        'gantt_data': json.dumps(gantt_data, cls=DjangoJSONEncoder),
        'recent_groups': recent_groups,
        'today_label': today_french,
    }
    return render(request, 'tenant_folder/dashboard/pedago_dashboard.html', context)

@login_required(login_url="institut_app:login")
def ApiFinanceKPIs(request):
    # 1. Total Collected (Revenue)
    total_collected = Paiements.objects.aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
    
    # 2. Total Remaining Due (for collection rate calculation)
    total_remaining = DuePaiements.objects.filter(is_done=False).aggregate(Sum('montant_restant'))['montant_restant__sum'] or 0
    
    # 3. Collection Rate
    total_potential = total_collected + total_remaining
    collection_rate = (total_collected / total_potential * 100) if total_potential > 0 else 0
    
    # 4. Overdue Amount
    overdue_amount = DuePaiements.objects.filter(is_done=False, date_echeance__lt=datetime.now()).aggregate(Sum('montant_due'))['montant_due__sum'] or 0
    lists_overdue = DuePaiements.objects.filter(is_done=False, date_echeance__lt=datetime.now()).select_related('client').order_by('date_echeance').values('id', 'client__id', 'client__nom', 'client__prenom', 'client__email', 'montant_due', 'date_echeance', 'label')
    
    # 5. Upcoming Deadlines (Next 30 days)
    upcoming_start = datetime.now()
    upcoming_end = upcoming_start + timedelta(days=30)
    upcoming_deadlines_count = DuePaiements.objects.filter(
        is_done=False, 
        date_echeance__gte=upcoming_start,
        date_echeance__lte=upcoming_end
    ).count()
    
    # 6. Today's payments (Due today)
    echeance_du_jours = (DuePaiements.objects.filter(is_done=False, date_echeance = datetime.now())
                        .select_related('client')
                        .order_by('date_echeance')
                        .values('id', 'client__id', 'client__nom', 'client__prenom', 'client__email', 'montant_due', 'date_echeance', 'label'))

    # 7. Pending Amount (Total outstanding)
    pending_amount = total_remaining

    # 8. Upcoming Deadlines List (Next 30 days details)
    liste_echeance_avenir = (DuePaiements.objects.filter(
        is_done=False, 
        date_echeance__gt=datetime.now(),
        date_echeance__lte=upcoming_end
    ).select_related('client')
    .order_by('date_echeance')
    .values('id', 'client__id', 'client__nom', 'client__prenom', 'client__email', 'montant_due', 'date_echeance', 'label'))

    data = {
        'total_collected': total_collected,
        'collection_rate': round(collection_rate, 2),
        'upcoming_deadlines_count': upcoming_deadlines_count,
        'echeance_passer': overdue_amount, # keeping key for compatibility or updating front-end
        'overdue_amount': overdue_amount,
        'liste_echeance_echue': list(lists_overdue),
        'echeance_du_jours' : list(echeance_du_jours),
        'liste_echeance_avenir': list(liste_echeance_avenir),
        'pending_amount': pending_amount,
    }
    return JsonResponse(data)

@login_required(login_url="institut_app:login")
def Index(request):
    # Afficher le calendrier personnel de l'utilisateur (t_communication)
    return render(request, 'tenant_folder/communication/calendar.html')

def logout_view(request):
    if request.user.is_authenticated:
        try:
            request.user.session_info.last_session_key = None
            request.user.session_info.save(update_fields=["last_session_key"])
        except UserSession.DoesNotExist:
            pass
        logout(request)
    return redirect('institut_app:login')

@login_required(login_url='institut_app:login')
def ChangePasswordForce(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if not password or len(password) < 8:
            messages.error(request, "Le mot de passe doit faire au moins 8 caractères.")
        elif password != password_confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        else:
            user = request.user
            user.set_password(password)
            user.save()
            
            # Update last_password_change in profile
            profile, created = Profile.objects.get_or_create(user=user)
            profile.last_password_change = timezone.now()
            profile.force_password_change = False
            profile.save()
            
            # Update UserSession to prevent logout from other middlewares if any
            session_info, _ = UserSession.objects.get_or_create(user=user)
            session_info.last_session_key = request.session.session_key
            session_info.save()
            
            # We need to re-login the user because set_password logs them out
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            messages.success(request, "Votre mot de passe a été mis à jour avec succès.")
            return redirect('institut_app:index')
            
    return render(request, 'tenant_folder/users/force_password_change.html', {
        'tenant': request.tenant
    })

def ForgotPasswordRequestView(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')
        if not identifier:
            return JsonResponse({'status': 'error', 'message': 'Veuillez saisir votre email ou nom d\'utilisateur.'})
        
        from django.contrib.auth.models import User
        from django.db.models import Q
        user = User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()
        
        if user:
            from .models import PasswordResetRequest
            from institut_app.utils_notifications import send_notification_to_user
            
            if PasswordResetRequest.objects.filter(user=user, is_active=True).exists():
                return JsonResponse({'status': 'warning', 'message': 'Une demande est déjà en cours pour ce compte.'})
            
            PasswordResetRequest.objects.create(user=user)
            
            # Notifier les superutilisateurs en temps réel
            superusers = User.objects.filter(is_superuser=True)
            for su in superusers:
                send_notification_to_user(
                    user=su,
                    message=f"L'utilisateur {user.username} a demandé la réinitialisation de son mot de passe.",
                    link=""
                )
                
            return JsonResponse({'status': 'success', 'message': 'Votre demande a été envoyée à l\'administrateur. Veuillez patienter.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Utilisateur introuvable.'})
            
    return render(request, 'registration/forgot_password.html')

def ShowBlockedConnexion(request):
    if not request.session.get("allow_blocked_page"):
        return redirect("institut_app:index")  
    
    request.session.pop("allow_blocked_page")
    return render(request, "tenant_folder/blocked_connexion.html")


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Vérifier UserSession
                # Get global config
                from .models import GlobalConfiguration, UserSession
                global_config = GlobalConfiguration.get_solo()
                session_info, _ = UserSession.objects.get_or_create(user=user)

                # 1. Vérification du verrouillage par appareil (Device Lock)
                if global_config.device_lock_enabled and session_info.is_device_lock_enabled and session_info.device_uuid:
                    device_lock_cookie = request.COOKIES.get('device_lock')
                    if str(session_info.device_uuid) != device_lock_cookie:
                        request.session["allow_blocked_page"] = True
                        return redirect('institut_app:ShowBlockedConnexion')

                # 2. Vérification de la session active (Optionnel mais conservé pour sécurité)
                if global_config.device_lock_enabled and session_info.is_device_lock_enabled and session_info.last_session_key:
                    try:
                        session = Session.objects.get(session_key=session_info.last_session_key)
                        if session.expire_date > timezone.now():
                            # Si on veut être vraiment strict comme demandé : bloquer
                             request.session["allow_blocked_page"] = True
                             return redirect('institut_app:ShowBlockedConnexion')
                    except Session.DoesNotExist:
                        pass

                # Login réussi
                login(request, user)
                
                # Enregistrement de l'appareil si c'est la première fois ET que le verrouillage est actif
                import uuid
                if global_config.device_lock_enabled and session_info.is_device_lock_enabled and not session_info.device_uuid:
                    session_info.device_uuid = uuid.uuid4()
                
                # Si le verrouillage est désactivé, on peut quand même loguer avec un UUID généré à la volée 
                # (uniquement pour l'historique, pas pour le cookie permanent)
                log_device_uuid = session_info.device_uuid or uuid.uuid4()
                
                # NOUVEAU : Enregistrer l'historique de connexion
                from .models import UserDeviceLog
                
                # Helper pour récupérer l'IP
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                UserDeviceLog.objects.create(
                    user=user,
                    device_uuid=log_device_uuid,
                    user_agent=request.META.get('HTTP_USER_AGENT'),
                    ip_address=ip
                )
                
                session_info.last_session_key = request.session.session_key
                session_info.save()

                messages.success(request, f"Bienvenue, {user.username} ! Vous êtes connecté.")
                response = redirect('institut_app:index')
                
                # Déposer le cookie de verrouillage (UNIQUEMENT si activé globalement ET par utilisateur)
                if global_config.device_lock_enabled and session_info.is_device_lock_enabled:
                    response.set_cookie(
                        'device_lock', 
                        str(session_info.device_uuid), 
                        max_age=31536000, 
                        httponly=True, 
                        samesite='Lax'
                    )
                return response

            else:
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

        return render(request, 'registration/login.html')
    else:
        return redirect('institut_app:index')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        new_user = User(
            username=username,
            email=email,
            is_superuser = True,
        )
        new_user.set_password(password1)
        new_user.save()

        messages.success(request, 'Compte créé avec succès')
        return redirect('institut_app:login')
 
    return render(request, 'registration/register.html')

def ShowBlockedConnexion(request):
    if not request.session.get("allow_blocked_page"):
        return redirect("institut_app:index")  
    
    request.session.pop("allow_blocked_page")
    return render(request, "tenant_folder/blocked_connexion.html")

@login_required(login_url='institut_app:login')
@transaction.atomic
def NewEntreprise(request):
    form = EntrepriseForm()
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entreprise créée avec succès')
            return redirect('institut_app:liste_entreprise')
    
    context = {
        'form' : form,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/entreprise/new_entreprise.html',context)

@login_required(login_url='institut_app:login')
def ListeEntreprises(request):
    entreprises = Entreprise.objects.all()
    context = {
        'liste' : entreprises,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/entreprise/mes_entreprises.html', context)

@login_required(login_url='institut_app:login')
@transaction.atomic
def ModifierEntreprise(request, id):
    entreprise = Entreprise.objects.get(id=id)
    form = EntrepriseForm(instance=entreprise)
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entreprise modifiée avec succès')
            return redirect('institut_app:liste_entreprise')
    return render(request, 'tenant_folder/entreprise/modifier_entreprise.html', {'form': form})

def ApiUpdateEntreprise(request):
    designation = request.POST.get('designation')
    site_web = request.POST.get('site_web')
    rc = request.POST.get('rc')
    nif = request.POST.get('nif')
    nis = request.POST.get('nis')
    art = request.POST.get('art')
    adresse = request.POST.get('adresse')
    telephone = request.POST.get('telephone')
    
    print(designation)

@login_required(login_url='institut_app:login')
def ApiGetEntrepriseDetails(request):
    id = request.GET.get('id')
    entreprise = Entreprise.objects.filter(id=id).values('id','designation','rc','nif','art','nis','adresse','telephone','wilaya','pays','email','site_web')
    return JsonResponse(list(entreprise), safe=False)

@superuser_required
def UsersListePage(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/users/liste_users.html', context)

@login_required(login_url="institut_app:login")
@superuser_required
def ApiListeUsers(request):
    users = User.objects.all().values('id','is_staff','email','username','date_joined','is_active')
    return JsonResponse(list(users), safe=False)

@superuser_required
def ApiGetDetailsProfile(request):
    id = request.GET.get('id')
    obj = User.objects.get(id = id)
    profile = Profile.objects.filter(user = obj).values('id','adresse','role')

    if profile:
        return JsonResponse(list(profile),safe=False)
    else:
        return JsonResponse({'status' : 'error', 'message' : "Aucun profile trouvé pour l'utilisateur"})
    
@superuser_required
def ApiCreateProfile(request):
    id_user= request.POST.get('id_user')
    nom = request.POST.get('nom')
    prenom = request.POST.get('prenom')
    adresse = request.POST.get('adresse')

    user_obj = User.objects.get(id= id_user)

    profile = Profile(
        user = user_obj,
        adresse = adresse
    )
    profile.save()

    user_obj.first_name = nom
    user_obj.last_name = prenom
    user_obj.save()

    return JsonResponse({'status' : 'success', 'message' : "Le profile de l'utilisateur crée avec succès"})

@superuser_required
def ApiDeactivateUser(request):
    id = request.GET.get('id')
    if id:
        user = User.objects.get(id = id)
        user.is_active = False
        user.save()

        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-information-line me-2'></i>Désactiver avec succès"})
    else:
        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-shut-down-line'></i>Erreur"})
    
@superuser_required
def ApiActivateUser(request):
    id = request.GET.get('id')
    if id:
        user = User.objects.get(id = id)
        user.is_active = True
        user.save()

        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-information-line me-2'></i>Désactiver avec succès"})
    else:
        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-shut-down-line'></i>Le compte utilisateur a été desactiver avec succès"})
    
@superuser_required
def ListGroupePage(request):
    return render(request, "tenant_folder/users/groupe_list.html", {'tenant' : request.tenant})

@superuser_required
def ApilistGroupe(request):
    liste = CustomGroupe.objects.all().values('id', 'name', 'description', 'created_at')
    return JsonResponse(list(liste), safe=False)
    
@superuser_required
def NewCustomGroupe(request):
    form = CustomGroupForm()

    if request.method == "POST":
        form = CustomGroupForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,"Le groupe a été crée avec succès")
            return redirect('institut_app:ListGroupePage')
        else:
            messages.success(request,"Le groupe a été crée avec succès")
            return redirect('institut_app:ListGroupePage')
            
    context = {
        'form' : form,
    }
    return render(request,'tenant_folder/users/nouveau_groupe.html', context)

@superuser_required
def ApiGetGroupFrom(request):
    form = CustomGroupForm()
    form_html = form.as_p()
    return JsonResponse({'form' : form_html})

@superuser_required
def ApiGetNewUserForm(request):
    form = CreateNewUserForm()
    html = render_to_string('tenant_folder/users/html/form_create_user.html', {'form': form}, request=request)
    return JsonResponse({'form' : html})

@transaction.atomic
@superuser_required
def PageUpdateUserDetails(request, pk):
    obj = User.objects.get(id = pk)
    form = UserUpdateForm(instance=obj)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Les information de l'utilisateur ont été enregistrer avec succès")
            return redirect('institut_app:PageUpdateUserDetails', pk)
        else:
            messages.error(request, "Une erreur est survenue lors du traitement de la requete")
            return redirect('institut_app:PageUpdateUserDetails', pk)
    else:
        context = {
            'obj' : obj,
            'form' : form,
            'tenant' : request.tenant
        }
        return render(request, 'tenant_folder/users/update_user.html', context)

@superuser_required
def ApiSaveUser(request):
    if request.method == "POST":
        form = CreateNewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success' : True, 'message' : "L'utilisateur à été ajouter avec succès"})
        else:
            return JsonResponse({'success' : False, 'message' : "Erreur de traitement du formulaire"})
    else:
        return JsonResponse({"success" : False, 'message' : "Erreur"})

@superuser_required
def ApiCheckUsernameDisponibility(request):
    username = request.GET.get('username')
    try:
        obj = User.objects.get(username = username)
        if obj:
            return JsonResponse({'status' : 'success'})
        
    except:
         return JsonResponse({'status' : 'error'})

@superuser_required
def ApiGetUpdateGroupForm(request):
    id = request.GET.get('id')
    obj = CustomGroupe.objects.get(id = id)
    form = CustomUpdateGroupForm(instance=obj)
    form_html = form.as_p()
    return JsonResponse({'form' : form_html})

@superuser_required
def ApiSaveGroup(request):
    if request.method == 'POST':
        form = CustomGroupForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if obj:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success' : False, "message": "Le rôle  existe déja ! <br>Veuillez attribuer un nom diffents"})
        else:
            return JsonResponse({'success': False,"message": "Le rôle existe déja ! <br>Veuillez attribuer un nom diffents"})

@superuser_required
def ApiGetUserDetails(request):
    id = request.GET.get('id')
    try:
        user = User.objects.get(id = id)
        data = {
            'id':user.id,
            'username' : user.username,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'is_active' : user.is_active,
            'last_login' : user.last_login,
            'joined_date' : user.date_joined,
            'groups' : list(user.groups.values('id','name')),
            'permissions' : list(user.user_permissions.values('id','name'))
        }
        return JsonResponse(data, safe=False)
    
    except user.DoesNotExist:

        return JsonResponse({'error' : 'Utilisateur non trouvé'})

@superuser_required
def ApiGetGroupeDetails(request):
    id = request.GET.get('id')
    try:
        groupe = CustomGroupe.objects.get(id=id)
        data = {
            'id': groupe.id,
            'name': groupe.name,
            'description': groupe.description,
            'created_at': groupe.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'permissions': list(groupe.permissions.values('id', 'name', 'codename')),
        }
        return JsonResponse(data, safe=False)

    except CustomGroupe.DoesNotExist:
        return JsonResponse({'error': 'Groupe non trouvé'}, status=404)
    
@superuser_required
def ApiDeleteGroup(request):
    id = request.GET.get('id')
    obj = CustomGroupe.objects.get(id = id)
    obj.delete()
    return JsonResponse({'status' : 'success' , 'message' : "Le groupe à été supprimé avec succès" })

@login_required(login_url='institut_app:login')
def GetMyProfile(request):
    try:
        obj = Profile.objects.get(user = request.user)

        # Retrieve user roles with related module and role data
        user_roles = request.user.module_roles.select_related('module', 'role').all()
        
        detailed_roles = []
        for ur in user_roles:
            # Use the method from the model to get effective permissions
            permissions = ur.get_effective_permissions()
            
            detailed_roles.append({
                'user_role': ur,
                'permissions': permissions
            })

        from .models import Entreprise
        entreprise = Entreprise.objects.first()

        context = {
            'obj': obj,
            'detailed_roles': detailed_roles,
            'entreprise': entreprise,
        }
        return render(request, 'tenant_folder/users/mon-profile.html', context)
    
    except Exception as e: 
        print(f"Error in GetMyProfile: {e}") # Debugging aid
        return render(request, 'tenant_folder/users/mon-profile.html')

@login_required(login_url='institut_app:login')    
def UpdateMyProfile(request):
    form = UserProfileEditForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == "POST":
        form = UserProfileEditForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, "Votre profile a été mis à jour avec succès")
            return redirect('institut_app:profile')
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour de votre profile")

    context ={
        'form' : form,
        'profile_form': profile_form,
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/users/update_profile.html', context)

def Error404(request):
    return render(request,'tenant_folder/not_authorized.html')

@login_required(login_url='institut_app:login')
@superuser_required
def active_sessions_view(request):
    """
    List all active user sessions.
    Only shows sessions that have not expired.
    """
    user_sessions = UserSession.objects.exclude(last_session_key__isnull=True).exclude(last_session_key="")
    
    active_data = []
    now = timezone.now()
    
    for us in user_sessions:
        try:
            session = Session.objects.get(session_key=us.last_session_key)
            if session.expire_date > now:
                active_data.append({
                    'user': us.user,
                    'session_key': us.last_session_key,
                    'expire_date': session.expire_date,
                    'last_login': us.user.last_login
                })
        except Session.DoesNotExist:
            # Cleanup orphaned session keys
            us.last_session_key = None
            us.save(update_fields=["last_session_key"])
            
    context = {
        'active_sessions': active_data,
        'tenant': request.tenant
    }
    return render(request, 'tenant_folder/users/active_sessions.html', context)

@login_required(login_url='institut_app:login')
@superuser_required
def terminate_session_api(request):
    """
    API endpoint to manually terminate a user session.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_key = data.get('session_key')
            
            if session_key:
                # 1. Delete from Django's Session table
                Session.objects.filter(session_key=session_key).delete()
                
                # 2. Update UserSession model
                us = UserSession.objects.get(last_session_key=session_key)
                us.last_session_key = None
                us.save(update_fields=["last_session_key"])
                
                from t_crm.models import UserActionLog
                UserActionLog.objects.create(
                    user=request.user,
                    action_type='UPDATE',
                    target_model='UserSession',
                    target_id=str(us.user.id),
                    details=f"Terminaison de la session pour l'utilisateur {us.user.username}",
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                
                return JsonResponse({'status': 'success', 'message': 'Session terminée avec succès.'})
            return JsonResponse({'status': 'success', 'message': 'Session terminée avec succès.'})
        except UserSession.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Session non trouvée.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
                
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)



@login_required(login_url='institut_app:login')
@module_permission_required('ger','view')
@module_permission_required('ger','add')
@role_required('ger', ['Administrateur','Manager','Utilisateur','Superviseur'])
def directeur_dashboard(request):
    # --- 1. Commercial & Admission ---
    # Prospects du mois
    today = datetime.now()
    start_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    new_prospects_month = Prospets.objects.filter(created_at__gte=start_of_month).count()
    
    # Taux de conversion global
    total_prospects_all = Prospets.objects.count()
    converted_clients = Prospets.objects.filter(is_client=True).count()
    conversion_rate = (converted_clients / total_prospects_all * 100) if total_prospects_all > 0 else 0
    
    # Demandes en attente
    pending_inscriptions = ClientPaiementsRequest.objects.filter(client__statut='instance').count()
    
    # RDV aujourd'hui
    today_date = today.date()
    rdv_today = RendezVous.objects.filter(date_rendez_vous=today_date).count()
    
    # --- Statistiques d'Acquisition Avancées ---
    # 1. Canaux d'acquisition (Labels et Counts)
    canal_labels = dict(Prospets._meta.get_field('canal').choices)
    acquisition_channels_raw = Prospets.objects.values('canal').annotate(count=Count('canal')).order_by('-count')
    acquisition_channels = []
    total_canal_count = 0
    for item in acquisition_channels_raw:
        if item['canal']:
            count = item['count']
            total_canal_count += count
            acquisition_channels.append({
                'label': canal_labels.get(item['canal'], item['canal']),
                'count': count,
                'code': item['canal']
            })
    
    # 2. Situation du Contact (Source du Lead)
    situation_labels = dict(Prospets._meta.get_field('contact_situation').choices)
    contact_situations_raw = Prospets.objects.values('contact_situation').annotate(count=Count('contact_situation')).order_by('-count')
    contact_situations = []
    for item in contact_situations_raw:
        if item['contact_situation']:
            contact_situations.append({
                'label': situation_labels.get(item['contact_situation'], item['contact_situation']),
                'count': item['count'],
                'code': item['contact_situation']
            })

    # Top Channels (for the small list, top 5)
    top_channels = acquisition_channels[:5]

    # --- 2. Finance ---
    # CA du mois (Paiements)
    revenue_month = Paiements.objects.filter(date_paiement__gte=start_of_month).aggregate(Sum('montant_paye'))['montant_paye__sum'] or 0
    
    # Dépenses du mois
    expenses_month = Depenses.objects.filter(date_paiement__gte=start_of_month).aggregate(Sum('montant_ttc'))['montant_ttc__sum'] or 0
    
    balance = revenue_month - expenses_month
    
    # Reste à recouvrer (Global)
    total_due_remaining = DuePaiements.objects.filter(is_done=False).aggregate(Sum('montant_restant'))['montant_restant__sum'] or 0
    
    # Impayés critiques (< today)
    critical_dues_count = DuePaiements.objects.filter(is_done=False, date_echeance__lt=today_date).count()

    # --- 3. Pédago ---
    # Groupes actifs
    active_groups = Groupe.objects.filter(etat__in=['valider', 'enc']).count()
    
    # Salles occupées aujourd'hui
    days_map = {'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi', 'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'}
    today_fr = days_map.get(today.strftime("%A"), "")
    occupied_rooms_count = TimetableEntry.objects.filter(timetable__is_validated=True, jour__iexact=today_fr).values('salle').distinct().count()

    # --- 4. Examens ---
    # Taux réussite
    total_decisions = ExamDecisionEtudiant.objects.count()
    admis_count = ExamDecisionEtudiant.objects.filter(statut='valide').count()
    success_rate = (admis_count / total_decisions * 100) if total_decisions > 0 else 0
    
    # PVs en attente
    pending_pvs = PvExamen.objects.filter(est_valide=False).count()

    # --- 5. CRM Advanced Stats ---
    # Répartition des prospects par statut
    prospects_by_status = Prospets.objects.values('statut').annotate(count=Count('statut')).order_by('-count')
    status_labels = {'visiteur': 'Visiteur', 'prinscrit': 'Pré-inscrit', 'instance': 'Instance', 'convertit': 'Converti'}
    prospects_by_status_with_labels = []
    for status in prospects_by_status:
        prospects_by_status_with_labels.append({
            'status': status['statut'],
            'label': status_labels.get(status['statut'], status['statut']),
            'count': status['count']
        })

    # Statistiques Fiche de Voeux & Double Diplomation
    fiche_voeux_stats = FicheDeVoeux.objects.values('specialite__label', 'promo__label', 'is_confirmed').annotate(count=Count('id')).order_by('specialite__label', 'promo__label')
    fiche_voeux_double_stats = FicheVoeuxDouble.objects.values('specialite__label', 'promo__label', 'is_confirmed').annotate(count=Count('id')).order_by('specialite__label', 'promo__label')

    # Chart Evolution (7 derniers jours)
    from django.db.models.functions import TruncDate
    seven_days_ago = datetime.now() - timedelta(days=6)
    prospects_by_date = Prospets.objects.filter(created_at__gte=seven_days_ago).annotate(date=TruncDate('created_at')).values('date').annotate(count=Count('id')).order_by('date')
    
    chart_dates = []
    chart_counts = []
    for i in range(7):
        date = (datetime.now() - timedelta(days=6-i)).date()
        chart_dates.append(date.strftime('%b %d'))
        count = 0
        for item in prospects_by_date:
            if item['date'] == date:
                count = item['count']
                break
        chart_counts.append(count)

    # Derniers rappels
    recent_reminders = RendezVous.objects.filter(archived=False).select_related('prospect').order_by('-created_at')[:5]

    # --- 6. Executive Education ---
    from t_conseil.models import Devis, Facture, GroupeConseil
    exec_prospects = Prospets.objects.filter(context='con').count()
    exec_clients = Prospets.objects.filter(context='con', is_client=True).count()
    exec_devis_attente = Devis.objects.filter(etat='attente').count()
    exec_ca = Facture.objects.filter(type_facture='standard', etat='valide').aggregate(ca=Sum('lignes_facture__montant_ht'))['ca'] or 0
    exec_groupes_enc = GroupeConseil.objects.filter(etat='enc').count()

    context = {
        'tenant': request.tenant,
        'kpis': {
            'commercial': {
                'new_prospects': new_prospects_month,
                'conversion_rate': round(conversion_rate, 1),
                'pending_inscriptions': pending_inscriptions,
                'rdv_today': rdv_today,
                'top_channels': top_channels,
                'acquisition_channels': acquisition_channels,
                'contact_situations': contact_situations,
                'total_canal_count': total_canal_count
            },
            'finance': {
                'revenue_month': revenue_month,
                'expenses_month': expenses_month,
                'balance': balance,
                'total_due': total_due_remaining,
                'critical_dues': critical_dues_count
            },
            'pedago': {
                'active_groups': active_groups,
                'occupied_rooms': occupied_rooms_count,
            },
            'exam': {
                'success_rate': round(success_rate, 1),
                'pending_pvs': pending_pvs
            },
            'executive': {
                'prospects': exec_prospects,
                'clients': exec_clients,
                'devis_attente': exec_devis_attente,
                'ca': exec_ca,
                'groupes_enc': exec_groupes_enc,
            }
        },
        # CRM Data Injection
        'prospects_by_status': prospects_by_status_with_labels,
        'fiche_voeux_stats': fiche_voeux_stats,
        'fiche_voeux_double_stats': fiche_voeux_double_stats,
        'chart_dates': chart_dates,
        'chart_counts': chart_counts,
        'recent_reminders': recent_reminders
    }
    return render(request, 'tenant_folder/directeur/directeur.html', context)


@login_required(login_url="institut_app:login")
def ApiMarkNotificationRead(request):
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            notif = Notification.objects.get(id=id, user=request.user)
            notif.is_read = True
            notif.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

@login_required(login_url="institut_app:login")
def ApiMarkAllNotificationsRead(request):
    if request.method == "POST":
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

@login_required(login_url="institut_app:login")
def ApiDeleteNotification(request):
    if request.method == "POST":
        id = request.POST.get('id')
        try:
            notif = Notification.objects.get(id=id, user=request.user)
            notif.delete()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

@login_required(login_url="institut_app:login")
def AllNotificationsPage(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'tenant': request.tenant,
        'notifications': notifications
    }
    return render(request, 'tenant_folder/notifications/all_notifications.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('ger','view')
@module_permission_required('ger','add')
@module_permission_required('ger','change')
@role_required('ger', ['Administrateur','Manager','Utilisateur','Superviseur'])
def my_budget_campaigns(request):
    """
    Shows budget campaigns for the current tenant (Institute).
    Fetches data from the public schema (associe_app).
    """
    from associe_app.models import BudgetCampaign, BudgetLine, PostesBudgetaire
    
    with schema_context('public'):
        # Fetch active campaigns
        campaigns = BudgetCampaign.objects.filter(is_active=True).order_by('-date_debut')
        
        # Fetch all budget items for the modal and structure them (recursive arborescence)
        # Prefetch categories and payment types to avoid N+1
        all_postes = list(PostesBudgetaire.objects.all().prefetch_related(
            'payment_categories',
            'depense_categories'
        ).order_by('order', 'label'))
        
        def build_recursive_tree(nodes, parent_id=None):
            tree = []
            relevant_nodes = [n for n in nodes if n.parent_id == parent_id]
            for node in relevant_nodes:
                # Gather channels
                channels = set()
                try:
                    if node.type == 'recette':
                        for cat in node.payment_categories.all():
                            if cat.name:
                                channels.add(cat.name)
                    else:
                        for cat in node.depense_categories.all():
                            if cat.name:
                                channels.add(cat.name)
                except Exception:
                    pass
                
                tree.append({
                    'item': node,
                    'channels': sorted(list(channels)),
                    'children': build_recursive_tree(nodes, node.id)
                })
            return tree

        postes_tree = {
            'recette': build_recursive_tree([p for p in all_postes if p.type == 'recette']),
            'depense': build_recursive_tree([p for p in all_postes if p.type == 'depense'])
        }
        
        # Get budget lines for this specific institute
        institute = request.tenant
        budget_lines = BudgetLine.objects.filter(
            campaign__in=campaigns,
            institut=institute
        ).select_related('campaign')
        
        # Build a list of campaigns with their specific objective for this institute
        # Map campaign id to amount and statut for easy lookup
        objectives_map = {line.campaign_id: {'montant': line.montant, 'statut': line.statut} for line in budget_lines}
        
        campaign_data = []
        for campaign in campaigns:
            obj_data = objectives_map.get(campaign.id, {'montant': 0, 'statut': 'none'})
            campaign_data.append({
                'id': campaign.id,
                'slug': campaign.slug,
                'name': campaign.name,
                'date_debut': campaign.date_debut,
                'date_fin': campaign.date_fin,
                'objectif': obj_data['montant'],
                'statut': obj_data['statut'],
            })

    context = {
        'tenant': request.tenant,
        'campaign_data': campaign_data,
        'postes_tree': postes_tree,
    }
    return render(request, 'tenant_folder/budget/my_campaigns.html', context)
@login_required(login_url="institut_app:login")
@module_permission_required('ger','view')
@module_permission_required('ger','add')
@module_permission_required('ger','change')
@role_required('ger', ['Administrateur','Manager','Utilisateur','Superviseur'])
def budget_campaign_dispatch(request, campaign_slug):
    """
    Matrix view for tenants to dispatch their global budget objective 
    across their entities (Entreprises) and budget items (Postes).
    """
    from associe_app.models import BudgetCampaign, BudgetLine, PostesBudgetaire, BudgetLineDetail
    from django.db.models import Sum
    
    # 1. Basic Info (from public schema)
    with schema_context('public'):
        campaign = get_object_or_404(BudgetCampaign, slug=campaign_slug)
        # Global objective for this tenant set by Associe
        global_objective = BudgetLine.objects.filter(campaign=campaign, institut=request.tenant).first()
        
        if not global_objective:
            messages.error(request, "Aucun objectif global n'a été défini pour votre institut sur cette campagne.")
            return redirect('institut_app:my_budget_campaigns')

        # Get all budget items (Postes) with pre-fetched payment & depense categories
        all_postes = PostesBudgetaire.objects.prefetch_related('payment_categories', 'depense_categories').order_by('order', 'type', 'label')
        
        structured_postes = []
        for p in all_postes:
            if p.parent is None:
                children = [child for child in all_postes if child.parent_id == p.id]
                display_postes = []
                # If parent has direct categories or no children, add it to display
                if len(p.payment_categories.all()) > 0 or len(p.depense_categories.all()) > 0 or len(children) == 0:
                    display_postes.append(p)
                display_postes.extend(children)
                
                structured_postes.append({
                    'parent_poste': p,
                    'is_standalone': len(children) == 0,
                    'display_postes': display_postes
                })

    # 2. Entities (from tenant schema)
    entreprises = list(Entreprise.objects.all().order_by('designation'))

    # Status check
    can_edit = global_objective.statut in ['draft', 'rejected', 'none']

    if request.method == "POST":
        if not can_edit:
            messages.error(request, "Ce budget est déjà soumis ou validé et ne peut plus être modifié.")
            return redirect('institut_app:dispatch_budget', campaign_slug=campaign_slug)

        action = request.POST.get('action', 'save')
        
        saved_count = 0
        deleted_count = 0
        found_fields = 0
        
        try:
            from decimal import InvalidOperation
            with transaction.atomic():
                with schema_context('public'):
                    for key, value in request.POST.items():
                        if not key.startswith('amount_'):
                            continue
                        
                        found_fields += 1
                        try:
                            # Expected format: amount_{poste_id}_{cat_id}_{ent_id}
                            # cat_id might be 'None' for legacy or direct poste assignment (though we want to avoid that now)
                            parts = key.split('_')
                            if len(parts) == 5:
                                poste_id = int(parts[1])
                                cat_type = parts[2]
                                cat_id = int(parts[3])
                                ent_id = int(parts[4])
                            elif len(parts) == 4:
                                poste_id = int(parts[1])
                                cat_type = 'pay'
                                cat_id = int(parts[2])
                                ent_id = int(parts[3])
                            else:
                                continue
                            
                            # Robust cleaning: remove all non-numeric/non-separator chars
                            # but keep the last separator (dot or comma) as decimal if multiple
                            clean_val = value.strip()
                            if not clean_val:
                                amount_val = Decimal('0')
                            else:
                                # Robust cleaning: remove 'DA', all types of spaces, and handle separators
                                clean_val = clean_val.replace('DA', '').replace('\xa0', '').replace('\u202f', '').replace(' ', '').strip()
                                
                                if ',' in clean_val and '.' in clean_val:
                                    # Mixed format: handle based on last separator
                                    if clean_val.rfind('.') > clean_val.rfind(','):
                                        # 1,500.00 format
                                        clean_val = clean_val.replace(',', '')
                                    else:
                                        # 1.500,00 format
                                        clean_val = clean_val.replace('.', '').replace(',', '.')
                                elif ',' in clean_val:
                                    # 1500,00 format
                                    clean_val = clean_val.replace(',', '.')
                                # 1500.00 or 1500 format - no change needed
                                
                                try:
                                    amount_val = Decimal(clean_val)
                                except (InvalidOperation, ValueError):
                                    amount_val = Decimal('0')
                            
                                # Define lookup_kwargs BEFORE the if check to ensure it's always correct for the current item
                                lookup_kwargs = {
                                    'campaign': campaign,
                                    'institut_id': request.tenant.id,
                                    'poste_id': poste_id,
                                    'entreprise_id': ent_id,
                                }
                                if cat_type == 'pay':
                                    lookup_kwargs['payment_category_id'] = cat_id
                                    lookup_kwargs['depense_category_id'] = None
                                elif cat_type == 'dep':
                                    lookup_kwargs['payment_category_id'] = None
                                    lookup_kwargs['depense_category_id'] = cat_id
                                else:
                                    # This is 'none' or direct assignment
                                    lookup_kwargs['payment_category_id'] = None
                                    lookup_kwargs['depense_category_id'] = None

                                if amount_val > 0:
                                    # CONSOLIDATION: If saving at poste level (consolidated), clean up ANY existing
                                    # entries for this poste to avoid double counting from legacy granular data.
                                    if cat_type == 'none':
                                        BudgetLineDetail.objects.filter(
                                            campaign=campaign,
                                            institut_id=request.tenant.id,
                                            poste_id=poste_id
                                        ).delete()

                                    obj, created = BudgetLineDetail.objects.update_or_create(
                                        **lookup_kwargs,
                                        defaults={'montant': amount_val}
                                    )
                                    # Update T1-T4 for this detail
                                    t1_key = f"t1_{poste_id}_{cat_type}_{cat_id}"
                                    t2_key = f"t2_{poste_id}_{cat_type}_{cat_id}"
                                    t3_key = f"t3_{poste_id}_{cat_type}_{cat_id}"
                                    t4_key = f"t4_{poste_id}_{cat_type}_{cat_id}"
                                    
                                    if t1_key in request.POST: obj.t1_percent = min(max(float(request.POST.get(t1_key, 0) or 0), 0), 100)
                                    if t2_key in request.POST: obj.t2_percent = min(max(float(request.POST.get(t2_key, 0) or 0), 0), 100)
                                    if t3_key in request.POST: obj.t3_percent = min(max(float(request.POST.get(t3_key, 0) or 0), 0), 100)
                                    if t4_key in request.POST: obj.t4_percent = min(max(float(request.POST.get(t4_key, 0) or 0), 0), 100)
                                    obj.save()
                                    saved_count += 1
                                else:
                                    # Delete if 0 or empty
                                    deleted = BudgetLineDetail.objects.filter(**lookup_kwargs).delete()
                                    if deleted[0] > 0:
                                        deleted_count += 1
                        except (ValueError, TypeError):
                            continue
                    
                    # End of loop
            
            # --- POST-TRANSACTION PROCESSING ---
            if action == 'submit':
                from associe_app.models import BudgetLine
                with schema_context('public'):
                    # Force update in public schema
                    BudgetLine.objects.filter(
                        campaign_id=campaign.id, 
                        institut_id=request.tenant.id
                    ).update(statut='submitted')
                
                messages.success(request, "Votre proposition budgétaire a été soumise avec succès pour validation.")

                # Notification (isolated)
                try:
                    tenant_name = request.tenant.nom
                    campaign_name = campaign.name
                    notif_message = f"L'institut '{tenant_name}' a soumis son budget pour la campagne '{campaign_name}' pour validation."
                    notif_link = f"/budget-campaigns/{campaign.slug}/review/{request.tenant.id}/"
                    
                    with schema_context('public'):
                        public_users = get_user_model().objects.filter(is_active=True)
                        for p_user in public_users:
                            try:
                                send_notification_to_user(p_user, notif_message, notif_link)
                            except: pass
                except Exception as ne:
                    print(f"Notification error: {ne}")
            else:
                if found_fields == 0:
                    messages.warning(request, "Aucune donnée budgétaire n'a été détectée dans l'envoi.")
                else:
                    messages.success(request, f"Brouillon enregistré : {saved_count} montants sauvegardés.")
                            
        except Exception as e:
            messages.error(request, f"Erreur lors de l'enregistrement : {str(e)}")
                
        return redirect('institut_app:dispatch_budget', campaign_slug=campaign_slug)

    # 3. Fetch existing allocations (from public schema)
    with schema_context('public'):
        details = BudgetLineDetail.objects.filter(campaign=campaign, institut=request.tenant)
        # Map: (poste_id, cat_id, exp_id) -> BudgetLineDetail
        # For display, if we had multiple enterprises, we aggregate them here
        allocations = {}
        # Map: (poste_id, cat_id) -> {t1, t2, t3, t4}
        row_quarters = {}
        
        for d in details:
            # ONLY LOAD CONSOLIDATED RECORDS (ent_id = 0 and cat_type = 'none')
            # Legacy records (ent_id > 0 or specific categories) are ignored for display
            if d.entreprise_id != 0 or d.payment_category_id is not None or d.depense_category_id is not None:
                continue

            c_type = 'none'
            c_id = 0
            cat_type_key = 'none'

            # Key format: {poste_id}_none_0_0 (Consolidated Poste Level)
            key = f"{d.poste_id}_{cat_type_key}_{c_id}_0"
            
            if key not in allocations:
                allocations[key] = {
                    'montant': d.montant,
                    't1_percent': d.t1_percent,
                    't2_percent': d.t2_percent,
                    't3_percent': d.t3_percent,
                    't4_percent': d.t4_percent,
                }
            else:
                allocations[key]['montant'] += d.montant

            # The record is already consolidated (none, 0, 0), so we don't need a second aggregation step.
            
            row_key = f"{d.poste_id}_none_0"
            if row_key not in row_quarters:
                row_quarters[row_key] = {
                    't1': d.t1_percent,
                    't2': d.t2_percent,
                    't3': d.t3_percent,
                    't4': d.t4_percent
                }
            
        total_dispatched = details.aggregate(Sum('montant'))['montant__sum'] or 0
        total_dispatched_recette = details.filter(poste__type='recette').aggregate(Sum('montant'))['montant__sum'] or 0
        total_dispatched_depense = details.filter(poste__type='depense').aggregate(Sum('montant'))['montant__sum'] or 0

        from associe_app.models import BudgetExtensionRequest
        all_extensions = BudgetExtensionRequest.objects.filter(
            campaign=campaign, 
            institut=request.tenant
        ).prefetch_related('items', 'items__poste').order_by('-created_at')

    context = {
        'tenant': request.tenant,
        'approved_extensions': all_extensions,
        'campaign': campaign,
        'global_objective': global_objective,
        'structured_postes': structured_postes,
        'entreprises': entreprises,
        'allocations': allocations,
        'row_quarters': row_quarters,
        'total_dispatched': total_dispatched,
        'total_dispatched_recette': total_dispatched_recette,
        'total_dispatched_depense': total_dispatched_depense,
        'remaining': global_objective.montant - total_dispatched_recette,
        'percent_dispatched': (total_dispatched_recette / global_objective.montant * 100) if global_objective.montant > 0 else 0,
        'can_edit': can_edit,
        'statut': global_objective.statut,
        'commentaire': global_objective.commentaire,
    }
    return render(request, 'tenant_folder/budget/dispatch_budget.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('ger','view')
@module_permission_required('ger','add')
@module_permission_required('ger','change')
@role_required('ger', ['Administrateur','Manager','Utilisateur','Superviseur'])
def request_extension(request, campaign_slug):
    """
    View for institutes to request a budget extension (rallonge).
    Shows current validated budget and allows proposing new amounts.
    """
    from associe_app.models import BudgetCampaign, BudgetLine, PostesBudgetaire, BudgetLineDetail, BudgetExtensionRequest, BudgetExtensionItem
    from django_tenants.utils import schema_context
    
    # 1. Basic Info (from public schema)
    with schema_context('public'):
        campaign = get_object_or_404(BudgetCampaign, slug=campaign_slug)
        global_objective = BudgetLine.objects.filter(campaign=campaign, institut=request.tenant).first()
        
        if not global_objective or global_objective.statut != 'validated':
            messages.error(request, "Vous ne pouvez demander une rallonge que sur un budget validé.")
            return redirect('institut_app:dispatch_budget', campaign_slug=campaign_slug)

        # Check for pending requests
        pending_request = BudgetExtensionRequest.objects.filter(
            campaign=campaign, 
            institut=request.tenant, 
            status='pending'
        ).first()
        
        if pending_request:
            messages.warning(request, "Vous avez déjà une demande de rallonge en attente. Veuillez patienter.")
            return redirect('institut_app:dispatch_budget', campaign_slug=campaign_slug)

        all_postes = PostesBudgetaire.objects.filter(type='depense').prefetch_related('payment_categories', 'depense_categories').order_by('order', 'label')
        
        structured_postes = []
        for p in all_postes:
            if p.parent is None:
                children = [child for child in all_postes if child.parent_id == p.id]
                display_postes = []
                if len(p.payment_categories.all()) > 0 or len(p.depense_categories.all()) > 0 or len(children) == 0:
                    display_postes.append(p)
                display_postes.extend(children)
                
                structured_postes.append({
                    'parent_poste': p,
                    'is_standalone': len(children) == 0,
                    'display_postes': display_postes
                })

    # 2. Entities (from tenant schema)
    entreprises = list(Entreprise.objects.all().order_by('designation'))

    if request.method == "POST":
        motif = request.POST.get('motif')
        if not motif:
            messages.error(request, "Veuillez fournir un motif pour la demande.")
            return redirect(request.path)

        try:
            with transaction.atomic():
                with schema_context('public'):
                    # Create Request
                    ext_request = BudgetExtensionRequest.objects.create(
                        campaign=campaign,
                        institut=request.tenant,
                        motif=motif,
                        status='pending'
                    )

                    saved_count = 0
                    
                    # Iterate form data to find changes
                    # Expected format: extension_amount_{poste_id}_{cat_id}_{ent_id}
                    for key, value in request.POST.items():
                        if key.startswith('extension_amount_'):
                            try:
                                parts = key.split('_')
                                if len(parts) == 6:
                                    poste_id = int(parts[2])
                                    cat_type = parts[3]
                                    cat_id = int(parts[4])
                                    ent_id = int(parts[5])
                                elif len(parts) == 5:
                                    poste_id = int(parts[2])
                                    cat_type = 'pay'
                                    cat_id = int(parts[3])
                                    ent_id = int(parts[4])
                                else:
                                    continue
                                
                                increment_amount = float(value) if value else 0
                                
                                # Get current amount
                                lookup_kwargs = {
                                    'campaign': campaign,
                                    'institut': request.tenant,
                                    'poste_id': poste_id,
                                    'entreprise_id': ent_id
                                }
                                if cat_type == 'pay':
                                    lookup_kwargs['payment_category_id'] = cat_id
                                    lookup_kwargs['depense_category_id'] = None
                                elif cat_type == 'dep':
                                    lookup_kwargs['payment_category_id'] = None
                                    lookup_kwargs['depense_category_id'] = cat_id
                                else:
                                    lookup_kwargs['payment_category_id'] = None
                                    lookup_kwargs['depense_category_id'] = None
                                    
                                current_detail = BudgetLineDetail.objects.filter(**lookup_kwargs).first()
                                
                                current_amount = float(current_detail.montant) if current_detail else 0.0
                                
                                # Only save if there is a non-zero requested extension
                                if increment_amount > 0:
                                    item_kwargs = {
                                        'request': ext_request,
                                        'poste_id': poste_id,
                                        'entreprise_id': ent_id,
                                        'old_amount': current_amount,
                                        'requested_amount': increment_amount
                                    }
                                    if cat_type == 'pay':
                                        item_kwargs['payment_category_id'] = cat_id
                                    elif cat_type == 'dep':
                                        item_kwargs['depense_category_id'] = cat_id
                                    else:
                                        pass # It's a direct poste assignment

                                    BudgetExtensionItem.objects.create(**item_kwargs)
                                    saved_count += 1
                                    
                            except (ValueError, IndexError) as e:
                                continue

                    if saved_count == 0:
                        ext_request.delete()

                if saved_count > 0:
                    try:
                        from associe_app.utils import send_saas_notification
                        notif_msg = f"L'institut '{request.tenant.nom}' souhaite une rallonge budgétaire pour la campagne '{campaign.name}'."
                        notif_link = f"/configuration/budget-campaigns/extension-requests/{ext_request.id}/"
                        send_saas_notification(notif_msg, link=notif_link)
                    except Exception as notif_err:
                        print(f"Error sending SaaS notification: {notif_err}")

                    messages.success(request, f"Demande de rallonge envoyée avec succès ({saved_count} lignes modifiées).")
                    return redirect('institut_app:dispatch_budget', campaign_slug=campaign_slug)
                else:
                    messages.warning(request, "Aucune modification budgétaire détectée.")

        except Exception as e:
            messages.error(request, f"Erreur: {str(e)}")

    # 3. Fetch existing allocations for display
    with schema_context('public'):
        details = BudgetLineDetail.objects.filter(campaign=campaign, institut=request.tenant)
        # Map poste_cat_0 to aggregated amount
        allocations = {}
        for d in details:
            # ONLY LOAD CONSOLIDATED RECORDS (ent_id = 0 and cat_type = 'none')
            if d.entreprise_id != 0 or d.payment_category_id is not None or d.depense_category_id is not None:
                continue

            c_type = 'none'
            c_id = 0
                
            key = f"{d.poste_id}_{c_type}_{c_id}_0"
            allocations[key] = allocations.get(key, 0) + float(d.montant)

    context = {
        'tenant': request.tenant,
        'campaign': campaign,
        'structured_postes': structured_postes,
        'entreprises': entreprises,
        'allocations': allocations,
        'title': f"Demande de rallonge - {campaign.name}",
    }
    return render(request, 'tenant_folder/budget/request_extension.html', context)

@login_required(login_url="institut_app:login")
@module_permission_required('ger','view')
@module_permission_required('ger','add')
@module_permission_required('ger','change')
@role_required('ger', ['Administrateur','Manager','Utilisateur','Superviseur'])
def budget_campaign_realization(request, campaign_slug):
    """
    Matrix view for tracking budget realization: shows planned allocations vs realized expenses/payments.
    """
    from associe_app.models import BudgetCampaign, BudgetLine, PostesBudgetaire, BudgetLineDetail
    from associe_app.budget_utils import get_campaign_realization_data
    from django.db.models import Sum
    from datetime import datetime
    from django_tenants.utils import schema_context
    
    # 1. Basic Info (from public schema)
    with schema_context('public'):
        campaign = get_object_or_404(BudgetCampaign, slug=campaign_slug)
        # Global objective for this tenant set by Associe
        global_objective = BudgetLine.objects.filter(campaign=campaign, institut=request.tenant).first()
        
        if not global_objective or global_objective.statut != 'validated':
            messages.error(request, "Cette campagne n'est pas encore validée.")
            return redirect('institut_app:my_budget_campaigns')

    # 2. Fetch Realization Data using shared utility
    realization_data = get_campaign_realization_data(campaign, [request.tenant])
    combined_postes = realization_data['combined_postes']
    totals = realization_data['totals']

    # Identifiers for Global mapping
    total_dispatched_recette = totals['dispatched_recette']
    total_dispatched_depense = totals['dispatched_depense']
    total_realized_recette = totals['realized_recette']
    total_realized_depense = totals['realized_depense']
    total_dispatched = totals['global_dispatched']
    total_realized = totals['global_realized']

    today_date = timezone.now().date()

    from associe_app.models import BudgetExtensionRequest
    all_extensions = BudgetExtensionRequest.objects.filter(
        campaign=campaign, 
        institut=request.tenant
    ).prefetch_related('items', 'items__poste').order_by('-created_at')

    context = {
        'tenant': request.tenant,
        'approved_extensions': all_extensions,
        'campaign': campaign,
        'global_objective': global_objective,
        'combined_postes': combined_postes,
        'total_dispatched': total_dispatched,
        'total_realized': total_realized,
        
        'total_dispatched_recette': total_dispatched_recette,
        'total_realized_recette': total_realized_recette,
        'recette_ecart': total_realized_recette - total_dispatched_recette,
        'percent_realized_recette': (total_realized_recette / total_dispatched_recette * 100) if total_dispatched_recette > 0 else 0,
        
        'total_dispatched_depense': total_dispatched_depense,
        'total_realized_depense': total_realized_depense,
        'depense_ecart': total_realized_depense - total_dispatched_depense,
        'percent_realized_depense': (total_realized_depense / total_dispatched_depense * 100) if total_dispatched_depense > 0 else 0,
        
        'resultat_attendu': total_dispatched_recette - total_dispatched_depense,
        'rentabilite': ((total_dispatched_recette - total_dispatched_depense) / total_dispatched_recette * 100) if total_dispatched_recette > 0 else 0,
        
        'resultat_realise': total_realized_recette - total_realized_depense,
        'rentabilite_realise': ((total_realized_recette - total_realized_depense) / total_realized_recette * 100) if total_realized_recette > 0 else 0,

        'percent_dispatched': (total_dispatched_recette / global_objective.montant * 100) if global_objective.montant > 0 else 0,
        'percent_realized': (total_realized / total_dispatched * 100) if total_dispatched > 0 else 0,
        'global_ecart': total_realized - total_dispatched,
        'statut': global_objective.statut,
        'commentaire': global_objective.commentaire,
        'today': today_date,
        'active_quarter': (
            'T1 (Jui-Sep)' if today_date.month in [7, 8, 9] else
            'T2 (Oct-Déc)' if today_date.month in [10, 11, 12] else
            'T3 (Jan-Mar)' if today_date.month in [1, 2, 3] else
            'T4 (Avr-Juin)'
        )
    }
    return render(request, 'tenant_folder/budget/realization_budget.html', context)

@csrf_exempt
@login_required
def ApiVerifyPassword(request):
    """
    Vérifie le mot de passe de l'utilisateur pour le déverrouillage de session.
    """
    if request.method == 'POST':
        password = request.POST.get('password')
        if not password:
            return JsonResponse({'status': 'error', 'message': 'Mot de passe requis.'}, status=400)
        
        user = request.user
        if user.check_password(password):
            return JsonResponse({'status': 'success', 'message': 'Déverrouillé avec succès.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Mot de passe incorrect.'}, status=403)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@login_required(login_url='institut_app:login')
def knowledge_center_view(request):
    try:
        from saas_admin_app.models import KnowledgeCategory, KnowledgeResource
        
        categories = KnowledgeCategory.objects.all().order_by('order', 'name')
        resources = KnowledgeResource.objects.filter(is_published=True).order_by('category__order', 'order', '-created_at')
        
        categories_with_resources = []
        for cat in categories:
            cat_resources = resources.filter(category=cat)
            if cat_resources.exists():
                categories_with_resources.append({
                    'category': cat,
                    'resources': cat_resources
                })
    except ImportError:
        categories_with_resources = []
        
    context = {
        'tenant': request.tenant,
        'categories_with_resources': categories_with_resources,
    }
    return render(request, 'tenant_folder/knowledge/knowledge_center.html', context)
