from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *


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

        pass
    else:
        return JsonResponse({"status" : "error", 'message' : "Methode non autoriser"})

@login_required(login_url='institut_app:login')
def StudentTransfert(request):
    pass

@login_required(login_url='institut_app:login')
def StudentArchive(request):
    pass

@login_required(login_url='institut_app:login')
def StudentsDelete(request):
    pass