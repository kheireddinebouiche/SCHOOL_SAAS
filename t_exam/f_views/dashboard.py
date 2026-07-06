from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from institut_app.decorators import submenu_access_required
from t_exam.models import SessionExam, ExamPlanification, Commissions, PvExamen

@login_required
def examens_dashboard(request):
    
    # KPIs
    total_sessions = SessionExam.objects.all().count()
    total_planifications = ExamPlanification.objects.all().count()
    total_commissions = Commissions.objects.all().count()
    total_pvs = PvExamen.objects.all().count()
    
    # Recent items
    dernieres_sessions = SessionExam.objects.all().order_by('-id')[:5]
    dernieres_commissions = Commissions.objects.all().order_by('-id')[:5]

    context = {
        "total_sessions": total_sessions,
        "total_planifications": total_planifications,
        "total_commissions": total_commissions,
        "total_pvs": total_pvs,
        "dernieres_sessions": dernieres_sessions,
        "dernieres_commissions": dernieres_commissions,
        "page_title": "Tableau de Bord - Examens"
    }
    
    return render(request, "tenant_folder/exams/dashboard.html", context)
