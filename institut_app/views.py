from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django_tenants.utils import schema_context
from .form import *
from .models import Profile
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.db import transaction
from django.template.loader import render_to_string
from t_crm.models import *
from t_exam.models import *
from t_tresorerie.models import DuePaiements
from t_formations.models import Promos
from t_groupe.models import Groupe, GroupeLine
from t_timetable.models import Timetable, TimetableEntry, Salle
from .models import UserSession, Profile
from django.contrib.sessions.models import Session
from django.utils import timezone
from django_otp.decorators import otp_required
from datetime import datetime, timedelta
from django.db.models import Count, Sum
from t_tresorerie.models import DuePaiements, Paiements, Depenses, ClientPaiementsRequest
import calendar
from django.db.models.functions import TruncMonth


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

def rh_dashboard(request):
    pass

def default_dashboard(request):
    pass

@login_required(login_url="institut_app:login")
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
    
    for i in range(6):
        month_date = today - timedelta(days=i*30) # approx
        month_start = datetime(month_date.year, month_date.month, 1)
        # End of month
        next_month = month_start + timedelta(days=32)
        month_end = datetime(next_month.year, next_month.month, 1) - timedelta(days=1)
        
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
            'period': month_start.strftime('%B %Y'),
            'revenue': revenue,
            'expenses': expenses,
            'profit': profit,
            'margin': margin,
            'is_positive': profit >= 0
        })

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
    lists_overdue = DuePaiements.objects.filter(is_done=False, date_echeance__lt=datetime.now()).select_related('client').order_by('date_echeance').values('id','client__nom','client__prenom','montant_due','date_echeance','label')
    
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
                        .values('id','client__nom','client__prenom','montant_due','date_echeance','label'))

    # 7. Pending Amount (Total outstanding)
    pending_amount = total_remaining

    # 8. Upcoming Deadlines List (Next 30 days details)
    liste_echeance_avenir = (DuePaiements.objects.filter(
        is_done=False, 
        date_echeance__gt=datetime.now(),
        date_echeance__lte=upcoming_end
    ).select_related('client')
    .order_by('date_echeance')
    .values('id','client__nom','client__prenom','montant_due','date_echeance','label'))

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


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Vérifier UserSession
                session_info, _ = UserSession.objects.get_or_create(user=user)

                if session_info.last_session_key:
                    try:
                        session = Session.objects.get(session_key=session_info.last_session_key)
                        if session.expire_date > timezone.now():
                            request.session["allow_blocked_page"] = True
                            return redirect('institut_app:ShowBlockedConnexion')
                    except Session.DoesNotExist:
                        pass

                # Nouvelle connexion
                login(request, user)
                session_info.last_session_key = request.session.session_key
                session_info.save(update_fields=["last_session_key"])

                messages.success(request, f"Bienvenue, {user.username} ! Vous êtes connecté.")
                return redirect('institut_app:index')

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

def UsersListePage(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/users/liste_users.html', context)

@login_required(login_url="institut_app:login")
def ApiListeUsers(request):
    users = User.objects.all().values('id','is_staff','email','username','date_joined','is_active')
    return JsonResponse(list(users), safe=False)

def ApiGetDetailsProfile(request):
    id = request.GET.get('id')
    obj = User.objects.get(id = id)
    profile = Profile.objects.filter(user = obj).values('id','adresse','role')

    if profile:
        return JsonResponse(list(profile),safe=False)
    else:
        return JsonResponse({'status' : 'error', 'message' : "Aucun profile trouvé pour l'utilisateur"})
    
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

def ApiDeactivateUser(request):
    id = request.GET.get('id')
    if id:
        user = User.objects.get(id = id)
        user.is_active = False
        user.save()

        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-information-line me-2'></i>Désactiver avec succès"})
    else:
        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-shut-down-line'></i>Erreur"})
    
def ApiActivateUser(request):
    id = request.GET.get('id')
    if id:
        user = User.objects.get(id = id)
        user.is_active = True
        user.save()

        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-information-line me-2'></i>Désactiver avec succès"})
    else:
        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-shut-down-line'></i>Le compte utilisateur a été desactiver avec succès"})
    
def ListGroupePage(request):
    return render(request, "tenant_folder/users/groupe_list.html", {'tenant' : request.tenant})

def ApilistGroupe(request):
    liste = CustomGroupe.objects.all().values('id', 'name', 'description', 'created_at')
    return JsonResponse(list(liste), safe=False)
    
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

def ApiGetGroupFrom(request):
    form = CustomGroupForm()
    form_html = form.as_p()
    return JsonResponse({'form' : form_html})

def ApiGetNewUserForm(request):
    form = CreateNewUserForm()
    html = render_to_string('tenant_folder/users/html/form_create_user.html', {'form': form}, request=request)
    return JsonResponse({'form' : html})

@transaction.atomic
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

def ApiCheckUsernameDisponibility(request):
    username = request.GET.get('username')
    try:
        obj = User.objects.get(username = username)
        if obj:
            return JsonResponse({'status' : 'success'})
        
    except:
         return JsonResponse({'status' : 'error'})

def ApiGetUpdateGroupForm(request):
    id = request.GET.get('id')
    obj = CustomGroupe.objects.get(id = id)
    form = CustomUpdateGroupForm(instance=obj)
    form_html = form.as_p()
    return JsonResponse({'form' : form_html})

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

        context = {
            'obj': obj,
            'detailed_roles': detailed_roles,
        }
        return render(request, 'tenant_folder/users/mon-profile.html', context)
    
    except Exception as e: 
        print(f"Error in GetMyProfile: {e}") # Debugging aid
        return render(request, 'tenant_folder/users/mon-profile.html')

@login_required(login_url='institut_app:login')    
def UpdateMyProfile(request):
    form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            
            messages.success(request, "Votre profile a été mis à jour avec succès")
            return redirect('institut_app:profile')
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour de votre profile")

    context ={
        'form' : form,
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/users/update_profile.html', context)

def Error404(request):
    return render(request,'tenant_folder/not_authorized.html')

@login_required(login_url='institut_app:login')
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
                
                return JsonResponse({'status': 'success', 'message': 'Session terminée avec succès.'})
            return JsonResponse({'status': 'success', 'message': 'Session terminée avec succès.'})
        except UserSession.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Session non trouvée.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
                
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@login_required(login_url='institut_app:login')
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
    # Demandes en attente
    pending_inscriptions = ClientPaiementsRequest.objects.filter(client__statut='instance').count()
    
    # RDV aujourd'hui
    today_date = today.date()
    rdv_today = RendezVous.objects.filter(date_rendez_vous=today_date).count()
    
    # Top Channels
    top_channels = Prospets.objects.values('canal').annotate(count=Count('canal')).order_by('-count')[:3]

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

    # --- 5. CRM Advanced Stats (Copied from CRM Dashboard) ---
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

    context = {
        'tenant': request.tenant,
        'kpis': {
            'commercial': {
                'new_prospects': new_prospects_month,
                'conversion_rate': round(conversion_rate, 1),
                'pending_inscriptions': pending_inscriptions,
                'rdv_today': rdv_today,
                'top_channels': top_channels
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
