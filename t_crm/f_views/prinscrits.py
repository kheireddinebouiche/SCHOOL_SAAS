from django.shortcuts import render,redirect
from django.http import JsonResponse
from ..models import *
from ..forms import *
from django.contrib import messages
from t_tresorerie.models import *
from t_formations.models import *
from django.db import transaction
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from functools import wraps
from decimal import Decimal
from django.contrib.auth.decorators import login_required


@login_required(login_url='intitut_app:login')
def ListeDesPrinscrits(request):
    context = {
        'tenant' : request.tenant
    }

    return render(request,'tenant_folder/crm/preinscrits/liste-des-preinscrits.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadPrinscrits(request):
    liste = Prospets.objects.filter(statut = "prinscrit").values('id', 'nin', 'nom', 'prenom', 'type_prospect','email','telephone','canal','created_at','etat','entreprise')
    for i in liste:
        i_obj = Prospets.objects.get(id=i['id'])
        i['etat_label'] = i_obj.get_etat_display()
        i['type_prospect_label'] = i_obj.get_type_prospect_display()
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='intitut_app:login')
def DetailsPrinscrit(request, pk):
    
    context = {
        'pk' : pk,
        'tenant' : request.tenant
    }
    return render(request, 'tenant_folder/crm/preinscrits/details-preinscrit.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadPreinscrisPerosnalInfos(request):
    id_prospect = request.GET.get('id_prospect')
    prospect = Prospets.objects.filter(id=id_prospect).values('etablissement','diplome','niveau_scolaire','date_naissance','adresse','type_handicap','has_endicap','tel_mere','prenom_mere','nom_mere','tel_pere','groupe_sanguin','nom_arabe','prenom_arabe','prenom_pere','created_at','id','nin','nom','prenom','email','telephone','type_prospect','canal','statut','etat','entreprise','poste_dans_entreprise','observation').first()
    
    return JsonResponse(prospect, safe=False)

@login_required(login_url='institut_app:login')
def ApiLoadPreinscritRendezVous(request):
   id_prospect = request.GET.get('id_prospect')
   rendez_vous = RendezVous.objects.filter(prospect__id=id_prospect, context="prinscrit").values('id','date_rendez_vous','heure_rendez_vous','type','object','created_at','statut')
   for l in rendez_vous:
       l_obj = RendezVous.objects.get(id = l['id'])
       l['status_label'] = l_obj.get_statut_display()
       l['type_label'] = l_obj.get_type_display()
       l['created_at'] = l_obj.created_at
   return JsonResponse(list(rendez_vous), safe=False)


@login_required(login_url='institut_app:login')
def ApiLoadNotePr(request):
    prospect_id = request.GET.get('id_prospect')
    notes = NotesProcpects.objects.filter(prospect__id = prospect_id, context="prinscrit").values('id','prospect','created_by__username','created_at','note','tage')
    for l in notes:
        l_obj = NotesProcpects.objects.get(id = l['id'])
        l['tage'] = l_obj.get_tage_display()
    return JsonResponse(list(notes), safe=False)

@login_required(login_url='intitut_app:login')
def ApiCheckHasCompletedProfile(request):
    id_preinscrit = request.GET.get('id_preinscrit')
    obj = Prospets.objects.get(id = id_preinscrit)

    data = {
        'profile_completed' : str(obj.profile_completed).lower(),
    }
    return JsonResponse({'profile_completed' : data})

@login_required(login_url='institut_app:login')
def ApiCheckCompletedDoc(request):
    id_preinscrit = request.GET.get('id_preinscrit')
    statut = Prospets.objects.get(id = id_preinscrit)

    data = {
        'has_completed_doc': str(statut.has_completed_doc).lower(),
    }
    return JsonResponse(data)

@login_required(login_url='intitut_app:login')
def ApiUpdatePreinscritInfos(request):
    nom_arabe = request.POST.get('nom_arabe')
    prenom_arabe = request.POST.get('prenom_arabe')
    date_naissance = request.POST.get('date_naissance')
    prenom_pere = request.POST.get('prenom_pere')
    tel_pere = request.POST.get('tel_pere')
    nom_mere = request.POST.get('nom_mere')
    prenom_mere = request.POST.get('prenom_mere')
    tel_mere = request.POST.get('tel_mere')
    has_handicap = request.POST.get('has_handicap')
    type_handicap = request.POST.get('type_handicap')
    groupe_sanguin = request.POST.get('groupe_sanguin')
    adresse = request.POST.get('adresse')
    niveau_scolaire = request.POST.get('niveau_scolaire')
    diplome = request.POST.get('diplome')
    etablissement_diplome = request.POST.get('etablissement_diplome')
    id_preinscrit = request.POST.get('id_preinscrit')
    nin = request.POST.get('nin')

    preinscrit = Prospets.objects.get(id = id_preinscrit)

    preinscrit.nom_arabe = nom_arabe
    preinscrit.prenom_arabe = prenom_arabe
    preinscrit.date_naissance = date_naissance
    preinscrit.prenom_pere = prenom_pere
    preinscrit.tel_pere = tel_pere
    preinscrit.nom_mere = nom_mere
    preinscrit.prenom_mere = prenom_mere
    preinscrit.tel_mere = tel_mere
    preinscrit.has_endicap = has_handicap
    preinscrit.type_handicap = type_handicap
    preinscrit.groupe_sanguin = groupe_sanguin
    preinscrit.adresse = adresse
    preinscrit.niveau_scolaire = niveau_scolaire
    preinscrit.diplome = diplome
    preinscrit.etablissement = etablissement_diplome
    preinscrit.nin = nin
    preinscrit.profile_completed= True

    preinscrit.save()

    return JsonResponse({'status' : "success", "message" : "Les informations du preinscrit ont été mis à jours avec succès"})

@login_required(login_url='institut_app:login')
def ApiLoadRequiredDocs(request):
    id_preinscrit = request.GET.get('id_preinscrit')

    specialites = FicheDeVoeux.objects.get(prospect__id = id_preinscrit) 
    formation_id = specialites.specialite.formation.id

    files = DossierInscription.objects.filter(formation = formation_id).values('id','label','is_required')
    return JsonResponse(list(files), safe=False)

@login_required(login_url='institut_app:login')
def add_document(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            doc_type = request.POST.get("type")
            file = request.FILES.get("file")
            id_prospect = request.POST.get('id_prospect')

            if not name or not doc_type or not file:
                return JsonResponse({"success": False, "error": "Champs manquants"})

            document = DocumentsDemandeInscription.objects.create(
                id_document=DossierInscription.objects.get(id=doc_type),
                file=file,
                prospect = Prospets.objects.get(id = id_prospect),
                fiche_voeux = FicheDeVoeux.objects.get(prospect__id = id_prospect),
                label = name,
            )

            return JsonResponse({"success": True, "id": document.id})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Méthode non autorisée"})

@login_required(login_url='institut_app:login')
def LoadPresinscritDocs(request):
    id_preinscrit = request.GET.get('id_preinscrit')
    
    docs = DocumentsDemandeInscription.objects.filter(prospect__id = id_preinscrit,fiche_voeux = FicheDeVoeux.objects.get(prospect__id = id_preinscrit))
    data = [{
        "id": doc.id,
        "label": doc.label,
        "id_document__label": doc.id_document.label if doc.id_document else "",
        "created_at": doc.created_at.strftime("%d/%m/%Y %H:%M"),
        "file": doc.file.url if doc.file else "",
    } for doc in docs]

    return JsonResponse(data, safe=False)

@login_required(login_url='intitut_app:login')
def DeleteDocumentPreinscrit(request):
    id_document = request.POST.get('id_document')
    obj = DocumentsDemandeInscription.objects.get(id = id_document)

    obj.delete()

    return JsonResponse({'status' : "success",'message' : "La suppression a été effectuer avec succès"})

def check_all_required_docs(request):
    prospect_id = request.GET.get("id_prospect")
    try:
        fiche_voeux = FicheDeVoeux.objects.get(prospect_id=prospect_id)
        formation = fiche_voeux.specialite.formation
    except FicheDeVoeux.DoesNotExist:
        return False, []

    # Tous les documents obligatoires de la formation
    required_docs = DossierInscription.objects.filter(
        formation=formation,
        is_required=True
    )

    # Documents déjà fournis par le prospect
    provided_docs = DocumentsDemandeInscription.objects.filter(
        prospect_id=prospect_id,
        id_document__in=required_docs
    ).exclude(file="")

    # Vérification
    missing_docs = required_docs.exclude(
        id__in=provided_docs.values_list("id_document_id", flat=True)
    )

    if missing_docs.exists():
        return False, list(missing_docs.values_list("label", flat=True))
    return True, []