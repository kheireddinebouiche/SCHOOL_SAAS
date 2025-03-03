from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *


@login_required(login_url='institut_app:login')
def ListeStudents(request):
    students = Etudiant.objects.all()
    context = {
        'liste' : students,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/student/liste_des_etudiants.html', context)

@login_required(login_url='institut_app:login')
def StudentDetails(request):
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