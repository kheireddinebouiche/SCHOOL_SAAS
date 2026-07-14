from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from institut_app.decorators import submenu_access_required
from t_etudiants.models import Etudiant, StudentTransferRequest
from t_groupe.models import Groupe
from django.db.models import Count


@login_required
@submenu_access_required("scol", "etudiants")
def scolarite_dashboard(request):
    
    
    # KPIs
    total_etudiants = Etudiant.objects.all().count()
    total_groupes = Groupe.objects.all().count()
    transferts_en_attente = StudentTransferRequest.objects.filter(status='Pending').count()
    
    # Recent 5 Etudiants
    derniers_etudiants = Etudiant.objects.all().order_by('-id')[:5]
    
    # Recent 5 Transferts
    derniers_transferts = StudentTransferRequest.objects.all().order_by('-id')[:5]

    # All Groupes for table with pagination
    derniers_groupes = Groupe.objects.select_related('specialite', 'specialite__formation').annotate(num_etudiants=Count('groupe_line_groupe')).order_by('-date_creation')

    context = {
        "total_etudiants": total_etudiants,
        "total_groupes": total_groupes,
        "transferts_en_attente": transferts_en_attente,
        "derniers_etudiants": derniers_etudiants,
        "derniers_transferts": derniers_transferts,
        "derniers_groupes": derniers_groupes,
        "page_title": "Tableau de Bord - Scolarité"
    }
    
    return render(request, "tenant_folder/student/scolarite_dashboard.html", context)
