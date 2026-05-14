from datetime import timedelta, datetime
from decimal import Decimal

def calculate_overtime(check_out_time, standard_end_time):
    """
    Calculates overtime hours if the employee stayed after the standard end time.
    Returns hours as a Decimal.
    """
    if not check_out_time or not standard_end_time:
        return Decimal('0.0')
        
    # Convert to datetime for comparison if they are time objects
    today = datetime.today()
    dt_check_out = datetime.combine(today, check_out_time)
    dt_standard_end = datetime.combine(today, standard_end_time)
    
    if dt_check_out > dt_standard_end:
        diff = dt_check_out - dt_standard_end
        hours = Decimal(diff.total_seconds()) / Decimal(3600)
        return hours.quantize(Decimal('0.01'))
    
    return Decimal('0.0')


def calculate_leave_duration(date_debut, date_fin, is_working_days=False):
    """
    Calculates the number of days between two dates.
    - If is_working_days is True: excludes Fridays and Saturdays (Algerian weekends).
    - Otherwise: counts all calendar days (Standard for Annual Leave in Algeria).
    """
    if not date_debut or not date_fin:
        return 0
    
    if not is_working_days:
        delta = date_fin - date_debut
        return delta.days + 1
    
    # Calculate working days (excluding Fri/Sat)
    count = 0
    curr_date = date_debut
    while curr_date <= date_fin:
        # In Algeria, Friday is 4 (if Monday is 0) or 5 (if Monday is 0 and Sunday is 6)
        # Using .weekday(): 0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun
        if curr_date.weekday() not in [4, 5]: # Exclude Friday and Saturday
            count += 1
        curr_date += timedelta(days=1)
    return count


def accrue_monthly_leave(employee):
    """
    Increments the leave balance by 2.5 days for a full month worked.
    Takes into account the recruitment date from the latest contract.
    """
    if not employee.date_recrutement:
        return
        
    accrual = Decimal('2.5')
    employee.solde_conge += accrual
    employee.save()

