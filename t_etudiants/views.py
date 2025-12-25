from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from t_crm.models import NotesProcpects, RendezVous
from django.db import transaction



@login_required(login_url='institut_app:login')
def ListeStudents(request):
    return render(request, 'tenant_folder/student/liste_des_etudiants.html')

@login_required(login_url="institut_app:login")
def ApiListeDesEtudiants(request):
    liste = Prospets.objects.filter(statut="convertit" , is_affected=True).values('id','nom','prenom','email','indic','telephone','date_naissance','nin','groupe_line_student__groupe__nom','groupe_line_student__groupe__specialite__label','groupe_line_student__groupe__id')
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
        return JsonResponse({"status" : "error", 'message' : "Methode non autoriser"})


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

            return JsonResponse({"status" : "success",'message' : "La note est enregistrer avec succès"})
        except:
            return JsonResponse({"status" : "error", "message" : "Une erreur c'est produite lors du traitement de la requete"})
    else:
        return JsonResponse({"status" : "error", "message" : "Une erreur c'est produite lors du traitement de la requete"})

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
        return JsonResponse({'status': "error", "message" : "Methode non autoriser"})
    
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

        return JsonResponse({"status" : "success", "message" : "Le statut de la note a été changer"})
    else:
        return JsonResponse({"status" : "error", "message":"Methode non autoriser"})


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

            return JsonResponse({"status" : "success", "message" : "Les informations on été enregistrer avec suucès"})
        except:
            return JsonResponse({"status" : "error", "message" : "Une erreur c'est produite lors du traitement de la requete"})

    else:
        return JsonResponse({"status" : "error", "message" : "Methode non autoriser"})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateReminder(request):
    pass

@login_required(login_url='institut_app:login')
def StudentTransfert(request):
    pass

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

