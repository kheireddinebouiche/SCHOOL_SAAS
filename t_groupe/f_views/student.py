from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from t_crm.models import *
from t_tresorerie.models import *
from django.db.models import Count, Sum



@login_required(login_url="institut_app:login")
def StudentDetails(request, pk):
    
    student = Prospets.objects.get(id = pk)
    groupe = GroupeLine.objects.get(student = student)
    paiements = Paiements.objects.filter(prospect = student)
    documents = DocumentsDemandeInscription.objects.filter(prospect = student)
    notes = NotesProcpects.objects.filter(prospect = student, context="etudiant")
    rappels = RendezVous.objects.filter(prospect = student, context="etudiant" )
    echeanciers = DuePaiements.objects.filter(client = student, type='frais_f').order_by('ordre')
    
    montant_due = DuePaiements.objects.filter(client = student, is_done=False, type='frais_f').aggregate(total=Sum('montant_restant'))['total'] or 0
    montant_paye = Paiements.objects.filter(prospect= student, context="frais_f").aggregate(total=Sum('montant_paye'))['total'] or 0
    total_a_paye = FicheDeVoeux.objects.filter(prospect = student, is_confirmed=True).first()

     

    context = {
        'pk' : pk,
        'etudiant' : student,
        'groupe' : groupe,
        'paiements' : paiements,
        'documents' : documents,
        'notes' : notes,
        'rappels' : rappels,
        'echeanciers' : echeanciers,
        'montant_due' : montant_due,
        'montant_paye' : montant_paye,
        'total_a_paye' : total_a_paye.specialite.formation.prix_formation + total_a_paye.specialite.formation.frais_inscription,
    }
    return render(request, 'tenant_folder/student/profile_etudiant.html',context)