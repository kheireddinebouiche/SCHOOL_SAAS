from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..forms import *
from ..models import *
from institut_app.models import *
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from t_groupe.models import *
from t_etudiants.models import *
from django.db.models import Count, Q


@login_required(login_url="institut_app:login")
def PageSuivieCours(request):
    seances = (LigneRegistrePresence.objects
               .filter()
               .annotate(
                    total=Count('seance_module'),
                    faites=Count('seance_module', filter=Q(seance_module__is_done=True))
                )
            )
    groupes = Groupe.objects.all()

    context = {
        'seances' : seances,
        'groupes' : groupes,
    }

    return render(request, 'tenant_folder/timetable/avancement/suivie_cours.html', context)


