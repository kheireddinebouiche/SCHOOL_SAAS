from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from t_crm.models import NotesProcpects, RendezVous
from django.db import transaction
from t_formations.models import Specialites, Promos
from t_groupe.models import Groupe
def ListeStudents(request):
    return render(request, 'tenant_folder/student/liste_des_etudiants.html')

@login_required(login_url="institut_app:login")
def ApiListeDesEtudiants(request):
    liste = Prospets.objects.filter(statut="convertit").values('id','nom','prenom','email','indic','telephone','date_naissance','nin','groupe_line_student__groupe__nom','groupe_line_student__groupe__specialite__label','groupe_line_student__groupe__id', 'photo', 'context', 'is_double')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='institut_app:login')
def StudentDetails(request):
    pass


@login_required(login_url="institut_app:login")
def ApiSaveStudentDatas(request):
    if request.method == "POST":
        nom_pere = request.POST.get('nom_pere')
        indicatif_pere = request.POST.get('indicatif_pere')
        tel_pere = request.POST.get('tel_pere')
        nom_mere = request.POST.get('nom_mere')
        prenom_mere = request.POST.get('prenom_mere')
        etudiant = request.POST.get('etudiant')

       
        data={
            'nom_pere' : nom_pere,
            'indicatif_pere' : indicatif_pere,
            'tel_pere' : tel_pere,
            'nom_mere' : nom_mere,
            'prenom_mere' : prenom_mere,
            'etudiant' : etudiant,
        } 
        return JsonResponse({'status' : "success", "data" : data})
    else:
        return JsonResponse({"status" : "error", 'message' : "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiSaveStudentNote(request):
    if request.method == "POST":
        etudiant = request.POST.get('etudiant')
        noteContent = request.POST.get('noteContent')
        note_tags = request.POST.get('note_tags')
        try:
            NotesProcpects.objects.create(
                prospect_id = etudiant,
                note = noteContent,
                tage = note_tags,
                context = "etudiant"
            )

            return JsonResponse({"status" : "success",'message' : "La note est enregistrée avec succès"})
        except Exception as e:
            return JsonResponse({"status" : "error", "message" : "Une erreur s'est produite lors du traitement de la requête"})
    else:
        return JsonResponse({"status" : "error", "message" : "Une erreur s'est produite lors du traitement de la requête"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateStudentNote(request):
    if request.method == "POST":
        id = request.POST.get('id')
        noteContent = request.POST.get('noteContent')
        note_tags = request.POST.get('note_tags')

        note = NotesProcpects.objects.get(id= id)

        note.note = noteContent
        note.tage = note_tags
        note.save()

        return JsonResponse({'status': "success"})
    else:
        return JsonResponse({'status': "error", "message" : "Méthode non autorisée"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiAccomplirNote(request):
    if request.method == "POST":
        id = request.POST.get('id')
        observation = request.POST.get('observation')

        note = NotesProcpects.objects.get(id = id)
        note.observation = observation
        note.is_done = True
        note.save()

        return JsonResponse({"status" : "success", "message" : "Le statut de la note a été changé"})
    else:
        return JsonResponse({"status" : "error", "message":"Méthode non autorisée"})


@login_required(login_url="institut_app;login")
@transaction.atomic
def ApiSaveStudentRappel(request):
    if request.method == "POST":
        etudiant = request.POST.get('etudiant')
        reminderType = request.POST.get('reminderType')
        reminderSubject = request.POST.get('reminderSubject')
        reminderDate = request.POST.get('reminderDate')
        reminderTime = request.POST.get('reminderTime')
        reminderDescription = request.POST.get('reminderDescription')

        try:
            student = Prospets.objects.get(id = etudiant)

            RendezVous.objects.create(
                prospect = student,
                type = reminderType,
                object = reminderSubject,
                description = reminderDescription,
                date_rendez_vous = reminderDate,
                heure_rendez_vous = reminderTime,
                context = "etudiant"
            )

            return JsonResponse({"status" : "success", "message" : "Les informations ont été enregistrées avec succès"})
        except:
            return JsonResponse({"status" : "error", "message" : "Une erreur s'est produite lors du traitement de la requête"})

    else:
        return JsonResponse({"status" : "error", "message" : "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateReminder(request):
    pass

@login_required(login_url='institut_app:login')
def StudentTransfert(request):
    done_transfers = StudentTransferRequest.objects.filter(status='done').order_by('-updated_at')
    return render(request, 'tenant_folder/student/transfert.html', {'done_transfers': done_transfers})

@login_required(login_url='institut_app:login')
def StudentTransfertList(request):
    demandes = StudentTransferRequest.objects.all().order_by('-created_at')
    return render(request, 'tenant_folder/student/liste_demandes_transfert.html', {'demandes': demandes})

from t_formations.models import Specialites, Promos, Formation
from t_groupe.models import Groupe, GroupeLine, AffectationGroupe

@login_required(login_url='institut_app:login')
def ApiGetSpecialitesPromos(request):
    specialites = Specialites.objects.all().values('id', 'label', 'code', 'formation_id')
    promos = Promos.objects.filter(etat='active').values('id', 'code')
    formations = Formation.objects.all().values('code', 'nom')
    return JsonResponse({
        'specialites': list(specialites),
        'promos': list(promos),
        'formations': list(formations)
    })

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiRequestTransfer(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        origin_group_id = request.POST.get('origin_group_id')
        target_specialty_id = request.POST.get('target_specialty_id')
        target_promo_id = request.POST.get('target_promo_id')
        reason = request.POST.get('reason')

        try:
            StudentTransferRequest.objects.create(
                student_id=student_id,
                origin_group_id=origin_group_id,
                target_specialty_id=target_specialty_id,
                target_promo_id=target_promo_id,
                reason=reason,
                created_by=request.user
            )
            return JsonResponse({'status': 'success', 'message': 'Demande de transfert enregistrée.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdateTransferStatus(request):
    if request.method == "POST":
        request_id = request.POST.get('request_id')
        new_status = request.POST.get('status')
        
        try:
            transfer_request = StudentTransferRequest.objects.get(id=request_id)
            transfer_request.status = new_status
            transfer_request.save()
            return JsonResponse({'status': 'success', 'message': f'Statut mis à jour : {transfer_request.get_status_display()}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiExecuteTransfer(request):
    if request.method == "POST":
        request_id = request.POST.get('request_id')
        target_group_id = request.POST.get('target_group_id')

        try:
            transfer_request = StudentTransferRequest.objects.get(id=request_id)
            if transfer_request.status != 'approved':
                return JsonResponse({'status': 'error', 'message': 'La demande doit être approuvée avant d\'être exécutée.'})

            from t_groupe.models import GroupeLine, AffectationGroupe
            
            # 1. Remove old group line
            GroupeLine.objects.filter(student=transfer_request.student, groupe=transfer_request.origin_group).delete()

            # 2. Cleanup old affectation if different specialty
            if transfer_request.origin_group.specialite != transfer_request.target_specialty:
                AffectationGroupe.objects.filter(etudiant=transfer_request.student, specialite=transfer_request.origin_group.specialite).delete()

            # 3. Create new group line
            GroupeLine.objects.create(
                student=transfer_request.student,
                groupe_id=target_group_id
            )
            
            # 4. Update or Create AffectationGroupe for target specialty
            AffectationGroupe.objects.update_or_create(
                etudiant=transfer_request.student,
                specialite=transfer_request.target_specialty,
                defaults={'groupe_id': target_group_id}
            )

            transfer_request.status = 'done'
            transfer_request.target_group_id = target_group_id
            transfer_request.save()

            return JsonResponse({'status': 'success', 'message': 'Transfert exécuté avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url='institut_app:login')
def ApiGetGroupsForTransfer(request):
    specialty_id = request.GET.get('specialty_id')
    promo_id = request.GET.get('promo_id')
    groupes = Groupe.objects.filter(specialite_id=specialty_id, promotion_id=promo_id).values('id', 'nom')
    return JsonResponse(list(groupes), safe=False)

@login_required(login_url='institut_app:login')
def StudentArchive(request):
    pass

@login_required(login_url='institut_app:login')
def StudentsDelete(request):
    pass

@login_required(login_url="institut_app:login")
def ApiGetStudentFinancialsData(request):
    if request.method == "GET":
        from t_tresorerie.models import DuePaiements
        id_student = request.GET.get('id_student')

        echeancier_special = DuePaiements.objects.filter(client_id = id_student,type="frais_f").exclude(label="Frais d'inscription")
        data = []
        for i in echeancier_special:
            data.append({
                'montant_tranche' : i.montant_due,
                'date_echeancier' : i.date_echeance,
                'value' : i.label
            })
        
        return JsonResponse(list(data), safe=False)

    else:
        return JsonResponse({"status" : "error"})

