from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime
from ..models import *
from django.db import transaction
from django.utils.dateformat import format
from django.utils.dateformat import format
from institut_app.decorators import *
from institut_app.utils_notifications import send_notification_to_module_level
from institut_app.models import GlobalConfiguration
from django.urls import reverse
from django.core.paginator import Paginator


@login_required(login_url='institut_app:login')
@module_permission_required('crm','view')
@module_permission_required('crm','add')
@module_permission_required('crm','approuv')
@role_required('crm', ['Administrateur','Superviseur'])
def liste_derogations(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', 'all')
    sort_order = request.GET.get('sort', 'recent')

    queryset = Derogations.objects.all().order_by('-created_at')

    # Apply filters
    if search_query:
        queryset = queryset.filter(
            Q(demandeur__nom__icontains=search_query) | 
            Q(demandeur__prenom__icontains=search_query)
        )
    
    if status_filter != 'all':
        queryset = queryset.filter(statut=status_filter)

    # Apply sorting
    if sort_order == 'old':
        queryset = queryset.order_by('date_de_demande')
    else:
        queryset = queryset.order_by('-date_de_demande')

    # Stats (full dataset for stats regardless of pagination)
    all_qs = Derogations.objects.all()
    stats = {
        'total': all_qs.count(),
        'en_attente': all_qs.filter(statut='en_attente').count(),
        'acceptee': all_qs.filter(statut='acceptee').count(),
        'rejetee': all_qs.filter(statut='rejetee').count(),
    }

    # Pagination
    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_title': 'Liste des dérogations',
        'page_obj': page_obj,
        'stats': stats,
        'filters': {
            'search': search_query,
            'status': status_filter,
            'sort': sort_order,
        },
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/crm/liste_derogations.html', context)


@login_required(login_url='institut_app:login')
def LoadDerogations(request):
    liste = Derogations.objects.all().order_by('-created_at').values('id','motif','date_de_demande','statut', 'type','demandeur','demandeur__nom','demandeur__prenom','updated_at')
    for i in liste:
        i_obj  = Derogations.objects.get(id = i['id'])
        i['updated_at'] = format(i_obj.updated_at, "Y-m-d H:i")
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def ApiCheckDerogationStatus(request):
    id_preinscrit = request.GET.get('id_preinscrit')
    try:
        obj = Derogations.objects.filter(demandeur__id = id_preinscrit, motif="Documents Incomplets").last()
        data = {
            'date_de_demande' : obj.date_de_demande,
            'date_de_traitement' : obj.date_de_traitement,
            'observation' : obj.observation,
            'motif' : "Documents Incomplets",
            'statut' : obj.get_statut_display(),
        }
        return JsonResponse({"status": obj.statut,'data':data}, safe=False)
    except:
        return JsonResponse({"status": "error"})
   
@login_required(login_url="institut_app:login")
def ApiStoreDerogation(request):
    id_preinscrit = request.POST.get('id_preinscrit')
    reason = request.POST.get('reason')

    preinscrit = Prospets.objects.get(id = id_preinscrit)
   
    Derogations.objects.create(
        demandeur = preinscrit,
        type = reason,
        motif = "Documents Incomplets",
    )

    # Send Notification to Supervisors (2) and Managers (3) of CRM module
    try:
        link = reverse('t_crm:liste_derogations')
        message = f"Nouvelle demande de dérogation de {preinscrit.nom} {preinscrit.prenom}"
        
        config = GlobalConfiguration.get_solo()
        if config.crm_notifications_enabled:
            send_notification_to_module_level('crm', [2, 3], message, link)
    except Exception as e:
        print(f"Error sending notification: {e}")

    return JsonResponse({"status" : 'success', 'message' : "La demande de dérogation est en attente de traitement."})

@login_required(login_url="institut_app:login")
def ApiGetDerogationDetails(request):
    id_derogation = request.GET.get('id_derogation')
    obj = Derogations.objects.get(id = id_derogation)

    data={
        'id' : obj.id,
        'demandeur' : obj.demandeur.id,
        'demandeur_nom' : obj.demandeur.nom,
        'demandeur_prenom' : obj.demandeur.prenom,
        'is_double' : obj.demandeur.is_double,
        'type' : obj.type,
        'motif' : obj.motif,
        'date_de_demande' : obj.date_de_demande,
        'statut' : obj.statut,
        'observation' : obj.observation,
    }

    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiTraiteDerogation(request):
    decision = request.POST.get('decision')
    commentaire = request.POST.get('commentaire')
    id_derogation = request.POST.get('id_derogation')

    obj = Derogations.objects.get(id = id_derogation)

    obj.etat = True
    obj.statut = decision
    obj.observation = commentaire

    obj.save()


    prospect = Prospets.objects.get(id = obj.demandeur.id)

    if decision == "acceptee":
        prospect.has_derogation = True
        prospect.save()
    else:
        prospect.has_derogation = False
        prospect.save()

    return JsonResponse({"status" : "success"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiDeleteDerogation(request):
    id_derogation = request.POST.get('id_derogation')
    try:
        obj = Derogations.objects.get(id=id_derogation)
        prospect = obj.demandeur
        
        # Delete the derogation
        obj.delete()
        
        # Check if there are any other accepted derogations for this prospect
        # to decide if we should keep the has_derogation flag
        other_accepted = Derogations.objects.filter(demandeur=prospect, statut='acceptee').exists()
        if not other_accepted:
            prospect.has_derogation = False
            prospect.save()
            
        return JsonResponse({"status": "success", "message": "Dérogation supprimée avec succès."})
    except Derogations.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Dérogation introuvable."})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})