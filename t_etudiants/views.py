from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from t_crm.models import NotesProcpects, RendezVous, UserActionLog
from django.db import transaction
from t_formations.models import Specialites, Promos
from t_groupe.models import Groupe
def ListeStudents(request):
    return render(request, 'tenant_folder/student/liste_des_etudiants.html')

@login_required(login_url="institut_app:login")
def ApiListeDesEtudiants(request):
    raw_liste = Prospets.objects.filter(statut="convertit").values(
        'id','nom','prenom','email','indic','telephone','date_naissance','nin',
        'groupe_line_student__groupe__nom','groupe_line_student__groupe__specialite__label',
        'groupe_line_student__groupe__id', 'photo', 'context', 'is_double'
    )
    
    students_dict = {}
    for item in raw_liste:
        s_id = item['id']
        if s_id not in students_dict:
            students_dict[s_id] = {
                'id': s_id,
                'nom': item['nom'],
                'prenom': item['prenom'],
                'email': item['email'],
                'indic': item['indic'],
                'telephone': item['telephone'],
                'date_naissance': item['date_naissance'],
                'nin': item['nin'],
                'photo': item['photo'],
                'context': item['context'],
                'is_double': item['is_double'],
                'groupe_line_student__groupe__nom': item['groupe_line_student__groupe__nom'],
                'groupe_line_student__groupe__specialite__label': item['groupe_line_student__groupe__specialite__label'],
                'groupe_line_student__groupe__id': item['groupe_line_student__groupe__id'],
            }
        else:
            existing = students_dict[s_id]
            if item['groupe_line_student__groupe__nom']:
                if existing['groupe_line_student__groupe__nom']:
                    if item['groupe_line_student__groupe__nom'] not in existing['groupe_line_student__groupe__nom']:
                        existing['groupe_line_student__groupe__nom'] += f" / {item['groupe_line_student__groupe__nom']}"
                else:
                    existing['groupe_line_student__groupe__nom'] = item['groupe_line_student__groupe__nom']
            
            if item['groupe_line_student__groupe__specialite__label']:
                if existing['groupe_line_student__groupe__specialite__label']:
                    if item['groupe_line_student__groupe__specialite__label'] not in existing['groupe_line_student__groupe__specialite__label']:
                        existing['groupe_line_student__groupe__specialite__label'] += f" / {item['groupe_line_student__groupe__specialite__label']}"
                else:
                    existing['groupe_line_student__groupe__specialite__label'] = item['groupe_line_student__groupe__specialite__label']
                    
    return JsonResponse(list(students_dict.values()), safe=False)

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
            note_obj = NotesProcpects.objects.create(
                prospect_id = etudiant,
                note = noteContent,
                tage = note_tags,
                context = "etudiant"
            )

            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='NotesProcpects',
                target_id=str(note_obj.id),
                details=f"Ajout d'une note pour l'étudiant ID {etudiant}",
                ip_address=request.META.get('REMOTE_ADDR')
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

        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='NotesProcpects',
            target_id=str(note.id),
            details=f"Modification de la note ID {note.id}",
            ip_address=request.META.get('REMOTE_ADDR')
        )

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

        UserActionLog.objects.create(
            user=request.user,
            action_type='UPDATE',
            target_model='NotesProcpects',
            target_id=str(note.id),
            details=f"Clôture de la note ID {note.id}",
            ip_address=request.META.get('REMOTE_ADDR')
        )

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

            rendezvous = RendezVous.objects.create(
                prospect = student,
                type = reminderType,
                object = reminderSubject,
                description = reminderDescription,
                date_rendez_vous = reminderDate,
                heure_rendez_vous = reminderTime,
                context = "etudiant"
            )

            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='RendezVous',
                target_id=str(rendezvous.id),
                details=f"Création d'un rappel pour l'étudiant ID {etudiant}: {reminderSubject}",
                ip_address=request.META.get('REMOTE_ADDR')
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
from t_crm.models import UserActionLog

@login_required(login_url='institut_app:login')
def ApiGetSpecialitesPromos(request):
    specialites = Specialites.objects.all().values('id', 'label', 'code', 'formation_id')
    promos = Promos.objects.filter(etat='active').values('id', 'code')
    formations = Formation.objects.all().values('code', 'nom')
    double_diplomations = DoubleDiplomation.objects.all().values('id', 'label')
    return JsonResponse({
        'specialites': list(specialites),
        'promos': list(promos),
        'formations': list(formations),
        'double_diplomations': list(double_diplomations)
    })

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiRequestTransfer(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        origin_group_id = request.POST.get('origin_group_id')
        target_specialty_id = request.POST.get('target_specialty_id')
        target_promo_id = request.POST.get('target_promo_id')
        target_is_double = request.POST.get('target_is_double') == 'true'
        target_double_diploma_id = request.POST.get('target_double_diploma_id')
        reason = request.POST.get('reason')

        try:
            if StudentTransferRequest.objects.filter(student_id=student_id, status='pending').exists():
                return JsonResponse({'status': 'error', 'message': 'Une demande de transfert est déjà en attente pour cet étudiant.'})

            transfer_request = StudentTransferRequest.objects.create(
                student_id=student_id,
                origin_group_id=origin_group_id,
                target_specialty_id=target_specialty_id if not target_is_double else None,
                target_is_double=target_is_double,
                target_double_diploma_id=target_double_diploma_id if target_is_double else None,
                target_promo_id=target_promo_id,
                reason=reason,
                created_by=request.user
            )

            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='StudentTransferRequest',
                target_id=str(transfer_request.id),
                details=f"Nouvelle demande de transfert créée pour l'étudiant {transfer_request.student.nom} {transfer_request.student.prenom}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            # Notification
            from institut_app.utils_notifications import send_notification_to_module_level, send_notification_to_user
            from institut_app.models import GlobalConfiguration
            from django.urls import reverse
            from django.utils.translation import gettext as _

            message = _("Une nouvelle demande de transfert a été créée pour {} {}").format(transfer_request.student.nom, transfer_request.student.prenom)
            link = reverse('t_etudiants:StudentTransfertList')
            
            config = GlobalConfiguration.get_solo()
            if config.crm_notifications_enabled:
                if config.transfer_notification_mode == 'specific':
                    for receiver in config.transfer_notification_receivers.all():
                        send_notification_to_user(receiver, message, link)
                else:
                    send_notification_to_module_level('sco', [1, 2, 3], message, link=link)

            # Notification d'accusé de réception pour le demandeur
            msg_demandeur = _("Votre demande de transfert pour l'étudiant {} {} a bien été reçue et est en cours de traitement.").format(transfer_request.student.nom, transfer_request.student.prenom)
            send_notification_to_user(request.user, msg_demandeur, link)

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
        rejection_reason = request.POST.get('rejection_reason')
        
        try:
            transfer_request = StudentTransferRequest.objects.get(id=request_id)
            transfer_request.status = new_status
            if new_status == 'rejected' and rejection_reason:
                transfer_request.rejection_reason = rejection_reason
            transfer_request.save()
            
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='StudentTransferRequest',
                target_id=str(transfer_request.id),
                details=f"Mise à jour du statut de la demande de transfert de l'étudiant {transfer_request.student.nom} en {new_status}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return JsonResponse({'status': 'success', 'message': f'Statut mis à jour : {transfer_request.get_status_display()}'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiDeleteTransferRequest(request):
    if request.method == "POST":
        from institut_app.permissions.utils import user_can
        if not (user_can(request.user, 'scol', 'delete') or request.user.is_superuser):
            return JsonResponse({'status': 'error', 'message': 'Permission refusée. Vous n\'avez pas le droit de supprimer.'})

        request_id = request.POST.get('request_id')
        try:
            transfer_request = StudentTransferRequest.objects.get(id=request_id)
            student_nom = f"{transfer_request.student.nom} {transfer_request.student.prenom}"
            transfer_request.delete()
            
            UserActionLog.objects.create(
                user=request.user,
                action_type='DELETE',
                target_model='StudentTransferRequest',
                target_id=str(request_id),
                details=f"Suppression de la demande de transfert de l'étudiant {student_nom}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return JsonResponse({'status': 'success', 'message': 'Demande supprimée avec succès.'})
        except StudentTransferRequest.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Demande introuvable.'})
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

            # 2. Cleanup old affectations (for security, remove all if needed or just the current one)
            # Here we follow the logic of removing the primary one
            AffectationGroupe.objects.filter(etudiant=transfer_request.student, specialite=transfer_request.origin_group.specialite).delete()

            if transfer_request.target_is_double:
                # Handle Double Diploma: two groups
                target_group1_id = request.POST.get('target_group1_id')
                target_group2_id = request.POST.get('target_group2_id')
                
                spec1 = transfer_request.target_double_diploma.specialite1
                spec2 = transfer_request.target_double_diploma.specialite2

                # Specialty 1
                GroupeLine.objects.create(student=transfer_request.student, groupe_id=target_group1_id)
                AffectationGroupe.objects.update_or_create(
                    etudiant=transfer_request.student,
                    specialite=spec1,
                    defaults={'groupe_id': target_group1_id}
                )

                # Specialty 2
                GroupeLine.objects.create(student=transfer_request.student, groupe_id=target_group2_id)
                AffectationGroupe.objects.update_or_create(
                    etudiant=transfer_request.student,
                    specialite=spec2,
                    defaults={'groupe_id': target_group2_id}
                )
                
                transfer_request.student.is_double = True
                transfer_request.student.save()
            else:
                # Handle Standard Transfer: one group
                target_group_id = request.POST.get('target_group_id')
                
                GroupeLine.objects.create(student=transfer_request.student, groupe_id=target_group_id)
                AffectationGroupe.objects.update_or_create(
                    etudiant=transfer_request.student,
                    specialite=transfer_request.target_specialty,
                    defaults={'groupe_id': target_group_id}
                )
                
                transfer_request.student.is_double = False
                transfer_request.student.save()
                transfer_request.target_group_id = target_group_id

            transfer_request.status = 'done'
            transfer_request.save()

            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='StudentTransferRequest',
                target_id=str(transfer_request.id),
                details=f"Exécution du transfert pour l'étudiant {transfer_request.student.nom} {transfer_request.student.prenom}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

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

