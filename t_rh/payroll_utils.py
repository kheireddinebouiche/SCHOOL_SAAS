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
    from t_rh.utils import calculate_leave_duration
    
    conges_valides = Conges.objects.filter(
        employee=employee,
        status=Conges.StatusConge.VALIDE,
        date_debut__lte=date_end,
        date_fin__gte=date_start
    )
    
    jours_conges_payes = 0
    for conge in conges_valides:
        # Ne compter que les congés payés pour le maintien de salaire
        # La maternité est payée à 100% par la CNAS, l'entreprise ne paie pas ce salaire
        if conge.type_conge not in [Conges.TypeConge.SANS_SOLDE, Conges.TypeConge.MATERNITE]:
            overlap_start = max(date_start, conge.date_debut)
            overlap_end = min(date_end, conge.date_fin)
            
            # On calcule toujours en jours ouvrables pour l'intégration paie 
            # (afin de matcher avec le standard de 22 jours)
            jours = calculate_leave_duration(overlap_start, overlap_end, is_working_days=True)
            
            if conge.type_conge == Conges.TypeConge.MALADIE:
                # Les 3 premiers jours de l'arrêt maladie sont des jours de carence (non rémunérés)
                if overlap_start == conge.date_debut:
                    jours = max(0, jours - 3)
                    
            jours_conges_payes += jours
            
    # Ajout des congés payés aux jours travaillés pour ne pas pénaliser le salaire
    jours_travailles += jours_conges_payes
    
    # Absences injustifiées (basé sur le pointage)
    absences_injustifiees = presences.filter(status='absent', note__icontains='injustifié').count()
    
    return {
        'jours_travailles': jours_travailles,
        'heures_sup': heures_sup_totales,
        'absences_jours': absences_injustifiees,
        'jours_conges_payes': jours_conges_payes,
    }
