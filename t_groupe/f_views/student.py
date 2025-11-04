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

    remises = RemiseAppliquerLine.objects.filter(prospect = student, remise_appliquer__is_approuved = True,remise_appliquer__is_applicated = True)
    
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
        'remises' : remises,
    }
    return render(request, 'tenant_folder/student/profile_etudiant.html',context)


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdate_etudiant(request):
    
    id = request.POST.get('id_etudiant')
    etu = Prospets.objects.get(id=id)
    etu.nom = request.POST.get('nom')
    etu.prenom = request.POST.get('prenom')
    etu.date_naissance = request.POST.get('date_naissance') or None
    etu.lieu_naissance = request.POST.get('lieu_naissance')
    etu.nationnalite = request.POST.get('nationalite')
    etu.email = request.POST.get('email')
    etu.telephone = request.POST.get('telephone')
    etu.adresse = request.POST.get('adresse')
    etu.niveau_scolaire = request.POST.get('niveau_etude')
    etu.diplome = request.POST.get('dernier_diplome')
    etu.etablissement = request.POST.get('etablissement_origine')
    etu.prenom_pere = request.POST.get('nom_pere')
    etu.tel_pere = request.POST.get('tel_pere')
    etu.nom_mere = request.POST.get('nom_mere')
    etu.prenom_mere = request.POST.get('prenom_mere')
    etu.tel_mere = request.POST.get('tel_mere')
    # Tu peux aussi stocker les indicatifs :
    etu.indic1 = request.POST.get('indicatif_pere')
    etu.indic2 = request.POST.get('indicatif_mere')
    etu.save()
    print(id,request.POST.get('nationalite'))

    messages.success(request,'Information mises à jours')
    return JsonResponse({'status': 'success'})

  