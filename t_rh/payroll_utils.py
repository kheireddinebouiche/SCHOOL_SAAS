from decimal import Decimal
from django.utils import timezone
from .models import Presence, Conges, HRConfig
from t_rh.utils import calculate_overtime
import calendar

def get_monthly_payroll_variables(employee, month, year):
    """
    Calculates worked days, overtime hours, and absence hours for an employee.
    """
    # 1. Period setup
    last_day = calendar.monthrange(year, month)[1]
    date_start = timezone.datetime(year, month, 1).date()
    date_end = timezone.datetime(year, month, last_day).date()
    
    # 2. Worked Days & Absences from Presence
    presences = Presence.objects.filter(employee=employee, date__range=[date_start, date_end])
    
    jours_travailles = 0
    heures_sup_totales = Decimal('0.0')
    
    config = HRConfig.objects.first()
    standard_end = config.heure_fin_standard if config else None
    
    for p in presences:
        if p.status == 'present':
            jours_travailles += 1
        elif p.status == 'half_day':
            jours_travailles += 0.5
            
        # Overtime calculation
        if p.check_out and standard_end:
            hs = calculate_overtime(p.check_out, standard_end)
            heures_sup_totales += hs
            
    # 3. Absences from Leaves (Conges)
    # Only count leaves that are "VALIDE" and "SANS_SOLDE" or "MALADIE" (if not fully paid)
    # For now, let's just count all validated days as "paid" or "unpaid"
    # Logic: worked_days = presences.count()
    # But what if they don't point every day?
    # Usually: days_to_pay = Standard_Days (22) - Unjustified_Absences
    
    # Let's count unjustified absences
    absences_injustifiees = presences.filter(status='absent', note__icontains='injustifié').count()
    
    # Also check if there are gaps (days without presence nor approved leave)
    # This is more complex. Let's stick to a simpler approach for now:
    # Worked Days = presences where status in ['present', 'half_day']
    
    return {
        'jours_travailles': jours_travailles,
        'heures_sup': heures_sup_totales,
        'absences_jours': absences_injustifiees,
    }
