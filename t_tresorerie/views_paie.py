from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime

from t_ressource_humaine.models import FichePaie
from t_tresorerie.models import Depenses, DepensesCategory
from institut_app.models import Entreprise

from django.contrib.auth.decorators import login_required
from institut_app.decorators import module_permission_required, submenu_access_required

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
@submenu_access_required('tre', 'paie_salaires')
def liste_paie_finance(request):
    """
    Affiche les fiches de paie groupées par mois/année pour le module finance.
    """
    entite = request.session.get('entite_id')
    
    month = request.GET.get('month')
    year = request.GET.get('year')
    entreprise_id = request.GET.get('entreprise')
    status = request.GET.get('status')

    fiches = FichePaie.objects.filter(is_validated=True)
    if entite:
        fiches = fiches.filter(entreprise_id=entite)
        
    if month and month.isdigit():
        fiches = fiches.filter(mois=int(month))
    if year and year.isdigit():
        fiches = fiches.filter(annee=int(year))
    if entreprise_id and entreprise_id.isdigit():
        fiches = fiches.filter(entreprise_id=int(entreprise_id))
    if status:
        if status == 'paid':
            fiches = fiches.filter(is_paid=True)
        elif status == 'unpaid':
            fiches = fiches.filter(is_paid=False)
            
    groupes = fiches.values('mois', 'annee', 'entreprise_id', 'entreprise__designation').annotate(
        total_employes=Count('id'),
        total_net=Sum('net_a_payer'),
        total_paye=Count('id', filter=Q(is_paid=True)),
        total_non_paye=Count('id', filter=Q(is_paid=False))
    ).order_by('-annee', '-mois', 'entreprise__designation')
    
    mois_dict = dict(FichePaie.MOIS_CHOICES)
    
    paies_groupees = []
    for g in groupes:
        g['mois_nom'] = mois_dict.get(g['mois'], str(g['mois']))
        g['est_paye'] = g['total_non_paye'] == 0
        paies_groupees.append(g)
        
    categories = DepensesCategory.objects.all()
    entreprises = Entreprise.objects.all().order_by('designation')
    years = FichePaie.objects.values_list('annee', flat=True).distinct().order_by('-annee')
    if not list(years):
        years = [timezone.now().year]

    context = {
        'paies_groupees': paies_groupees,
        'categories': categories,
        'entreprises': entreprises,
        'years': years,
        'selected_month': int(month) if month and month.isdigit() else None,
        'selected_year': int(year) if year and year.isdigit() else None,
        'selected_entreprise': int(entreprise_id) if entreprise_id and entreprise_id.isdigit() else None,
        'selected_status': status,
        'months_choices': [
            (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
            (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
            (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
        ]
    }
    return render(request, 'tenant_folder/tresorerie/paie/liste_paie_finance.html', context)


from django.views.decorators.http import require_POST
from django.db import transaction

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'add')
@submenu_access_required('tre', 'paie_salaires')
@require_POST
@transaction.atomic
def lancer_depense_paie(request):
    """
    Crée une dépense globale pour la paie d'un mois spécifique.
    """
    if request.method == 'POST':
        mois = request.POST.get('mois')
        annee = request.POST.get('annee')
        entreprise_id = request.POST.get('entreprise_id')
        category_id = request.POST.get('category_id')
        date_paiement_str = request.POST.get('date_paiement')
        entite_id = request.session.get('entite_id')
        
        if not mois or not annee or not category_id or not date_paiement_str:
            messages.error(request, "Veuillez fournir toutes les informations nécessaires, y compris la date de paiement.")
            return redirect('t_tresorerie:liste_paie_finance')
            
        try:
            date_paiement = datetime.strptime(date_paiement_str, '%Y-%m-%d').date()
        except ValueError:
            date_paiement = timezone.now().date()
            
        fiches = FichePaie.objects.filter(
            mois=mois, 
            annee=annee, 
            is_validated=True, 
            is_paid=False
        )
        
        if entreprise_id:
            fiches = fiches.filter(entreprise_id=entreprise_id)
        elif entite_id:
            fiches = fiches.filter(entreprise_id=entite_id)
            
        if not fiches.exists():
            messages.warning(request, "Aucune fiche de paie en attente de paiement pour ce mois et cette entité.")
            return redirect('t_tresorerie:liste_paie_finance')
            
        total_net = fiches.aggregate(total=Sum('net_a_payer'))['total'] or 0
        
        try:
            category = DepensesCategory.objects.get(id=category_id)
            try:
                entite = Entreprise.objects.get(id=entreprise_id) if entreprise_id else (Entreprise.objects.get(id=entite_id) if entite_id else None)
            except Entreprise.DoesNotExist:
                entite = None
            
            mois_dict = dict(FichePaie.MOIS_CHOICES)
            mois_nom = mois_dict.get(int(mois), str(mois))
            
            depense = Depenses.objects.create(
                label=f"Paie globale - {mois_nom} {annee} ({entite.designation if entite else 'Toutes entités'})",
                category=category,
                date_depense=timezone.now().date(),
                date_paiement=date_paiement,
                montant_ht=total_net,
                montant_ttc=total_net,
                etat=True,
                description=f"Règlement des fiches de paie pour le mois de {mois_nom} {annee} ({fiches.count()} employés).",
                entite=entite,
                mode_paiement='vir'
            )
            
            from t_tresorerie.models import OperationsBancaire
            OperationsBancaire.objects.create(
                operation_type="sortie",
                depense=depense,
                montant=depense.montant_ttc,
                reference_bancaire=depense.reference,
                date_operation=date_paiement
            )
            
            fiches.update(
                is_paid=True,
                date_paiement=date_paiement
            )
            
            messages.success(request, f"Dépense de {total_net} DA générée avec succès pour la paie de {mois_nom} {annee}.")
            
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {str(e)}")
            
    return redirect('t_tresorerie:liste_paie_finance')
