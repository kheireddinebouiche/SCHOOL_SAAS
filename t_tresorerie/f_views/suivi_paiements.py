from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q, F
from django.utils.timezone import now
from t_crm.models import Prospets
from ..models import DuePaiements, Paiements
from t_groupe.models import Groupe, GroupeLine
from t_formations.models import Promos

@login_required(login_url="institut_app:login")
def PageSuiviPaiements(request):
    promos = Promos.objects.filter(etat="active")
    groupes = Groupe.objects.all()
    context = {
        'tenant': request.tenant,
        'promos': promos,
        'groupes': groupes,
    }
    return render(request, 'tenant_folder/comptabilite/tresorerie/suivi_paiements.html', context)

@login_required(login_url="institut_app:login")
def ApiSuiviPaiements(request):
    promo_id = request.GET.get('promo_id')
    groupe_id = request.GET.get('groupe_id')

    # Base queryset: Converted prospects
    prospects = Prospets.objects.filter(statut='convertit')

    if promo_id:
        prospects = prospects.filter(duepaiements__promo_id=promo_id)

    if groupe_id:
        prospects = prospects.filter(groupe_line_student__groupe_id=groupe_id)

    prospects = prospects.distinct()

    data = []
    today = now().date()

    for p in prospects:
        # Get all dues for this student
        dues_qs = DuePaiements.objects.filter(client=p, is_annulated=False)
        
        # Total due from the schedule
        total_due = dues_qs.aggregate(total=Sum('montant_due'))['total'] or 0
        
        # Total paid (exclude refunds)
        total_paid = Paiements.objects.filter(prospect=p, is_refund=False).aggregate(total=Sum('montant_paye'))['total'] or 0
        
        # Remaining balance
        total_restant = total_due - total_paid
        
        # Overdue amount: unpaid dues where date_echeance < today
        overdue_amount = dues_qs.filter(is_done=False, date_echeance__lt=today).aggregate(total=Sum('montant_restant'))['total'] or 0

        # Calculate if unpaid (reste à payer > 0 or overdue > 0)
        is_unpaid = (total_restant > 0 or overdue_amount > 0)

        # Skip if no promo is assigned to any dues
        if not dues_qs.filter(promo__isnull=False).exists():
            continue

        # Get promo
        promo_name = "N/A"
        first_due = dues_qs.order_by('-created_at').first()
        if first_due and first_due.promo:
            promo_name = first_due.promo.code
        
        # Get all groups
        group_lines = GroupeLine.objects.filter(student=p).select_related('groupe')
        group_names = [gl.groupe.nom for gl in group_lines if gl.groupe]
        group_name = " / ".join(group_names) if group_names else "Sans groupe"

        # Get dues details
        dues_list = []
        for d in dues_qs:
            dues_list.append({
                'label': d.label,
                'montant_due': float(d.montant_due),
                'montant_restant': float(d.montant_restant),
                'date_echeance': d.date_echeance.strftime("%d/%m/%Y") if d.date_echeance else "N/A",
                'is_done': d.is_done,
                'is_overdue': not d.is_done and d.date_echeance < today if d.date_echeance else False
            })

        data.append({
            'id': p.id,
            'nom': p.nom,
            'prenom': p.prenom,
            'full_name': f"{p.nom} {p.prenom}",
            'email': p.email,
            'telephone': p.telephone,
            'promo': promo_name,
            'groupe': group_name,
            'total_due': float(total_due),
            'total_paid': float(total_paid),
            'total_restant': float(total_restant),
            'total_overdue': float(overdue_amount),
            'is_unpaid': is_unpaid,
            'slug': p.slug,
            'dues': dues_list
        })

    return JsonResponse(data, safe=False)
