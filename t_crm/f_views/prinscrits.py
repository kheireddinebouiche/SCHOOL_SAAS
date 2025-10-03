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
from django.utils.dateformat import format
from .generate_paiements import ApiGeneratePaiementRequest
from django.db.models import Q, Sum


@login_required(login_url='intitut_app:login')
def ListeDesPrinscrits(request):
    context = {
        'tenant' : request.tenant
    }

    return render(request,'tenant_folder/crm/preinscrits/liste-des-preinscrits.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadPrinscrits(request):
    #liste = Prospets.objects.filter(statut = "prinscrit").values('id', 'nin', 'nom', 'prenom', 'type_prospect','email','telephone','canal','created_at','etat','entreprise')
    liste = Prospets.objects.filter(Q(statut = "prinscrit") | Q(statut= "instance") | Q(statut= "convertit")).values('statut','id', 'nin', 'nom', 'prenom', 'type_prospect','email','telephone','canal','created_at','etat','entreprise')
    for i in liste:
        i_obj = Prospets.objects.get(id=i['id'])
        i['etat_label'] = i_obj.get_etat_display()
        i['type_prospect_label'] = i_obj.get_type_prospect_display()
        i['statut_label'] = i_obj.get_statut_display()
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

    try:
        prospect = Prospets.objects.get(id=id_prospect)

    except Prospets.DoesNotExist:
        return JsonResponse({'error': 'Prospect non trouvé'}, status=404)

    data = {
        'id': prospect.id,
        'statut_key' : prospect.statut,
        'statut': prospect.get_statut_display(), 
        'nom': prospect.nom,
        'prenom': prospect.prenom,
        'email': prospect.email,
        'telephone': prospect.telephone,
        'canal': prospect.get_canal_display() if hasattr(prospect, "get_canal_display") else prospect.canal,
        'adresse': prospect.adresse,
        'date_naissance': prospect.date_naissance.strftime("%Y-%m-%d") if prospect.date_naissance else None,
        'created_at': prospect.created_at.strftime("%Y-%m-%d %H:%M") if prospect.created_at else None,

        'preinscri_date' : prospect.preinscri_date.strftime("%Y-%m-%d") if prospect.preinscri_date else None,
        'instance_date' : prospect.instance_date.strftime("%Y-%m-%d") if prospect.instance_date else None,
        'convertit_date' : prospect.convertit_date.strftime("%Y-%m-%d") if prospect.convertit_date else None,

        'nin' : prospect.nin,
        'groupe_sanguin' : prospect.groupe_sanguin,
        'nom_arabe' : prospect.nom_arabe,
        'prenom_arabe' : prospect.prenom_arabe,
        'prenom_pere' : prospect.prenom_pere,
        'tel_pere' : prospect.tel_pere,
        'nom_mere' : prospect.nom_mere,
        'prenom_mere' : prospect.prenom_mere,
        'tel_mere' : prospect.tel_mere,
        'has_endicap' : prospect.has_endicap,
        'type_handicap' : prospect.type_handicap,
        'adresse' : prospect.adresse,
        'date_naissance' : prospect.date_naissance,
        'niveau_scolaire' : prospect.get_niveau_scolaire_display(),
        'niveau_scolaire_pure' : prospect.niveau_scolaire,
        'diplome' : prospect.diplome,
        'etablissement' : prospect.etablissement,

        'pays' : prospect.pays,
        'wilaya' : prospect.wilaya,
        'code_zip' : prospect.code_zip,
        'lieu_naissance' : prospect.lieu_naissance,
    }

    return JsonResponse(data, safe=False)


@login_required(login_url='institut_app:login')
def ApiLoadPreinscritRendezVous(request):
   id_prospect = request.GET.get('id_prospect')
   rendez_vous = RendezVous.objects.filter(prospect__id=id_prospect, context="prinscrit", archived = False).values('id','date_rendez_vous','heure_rendez_vous','type','object','created_at','statut')
   for l in rendez_vous:
       l_obj = RendezVous.objects.get(id = l['id'])
       l['status_label'] = l_obj.get_statut_display()
       l['type_label'] = l_obj.get_type_display()
       l['created_at'] = format(l_obj.created_at, "Y-m-d H:i"),
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
    pays = request.POST.get('pays')
    wilaya = request.POST.get('wilaya')
    code_zip = request.POST.get('code_zip')
    lieu_naissance = request.POST.get('lieu_naissance')

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
    preinscrit.pays = pays
    preinscrit.wilaya = wilaya
    preinscrit.code_zip = code_zip
    preinscrit.lieu_naissance = lieu_naissance


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
@transaction.atomic
def add_document(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            doc_type = request.POST.get("type")
            file = request.FILES.get("file")
            id_prospect = request.POST.get('id_prospect')
            try :
                DocumentsDemandeInscription.objects.get(
                    prospect__id = id_prospect, 
                    fiche_voeux = FicheDeVoeux.objects.get(prospect__id = id_prospect),
                    id_document__id=doc_type
                )
                return JsonResponse({'success' : False, "error" : "Document déja présent !"})
            except:
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

@login_required(login_url="institut_app:login")
def check_all_required_docs(request):
    prospect_id = request.GET.get("id_prospect")
    try:
        fiche_voeux = FicheDeVoeux.objects.get(prospect__id=prospect_id)
        formation = fiche_voeux.specialite.formation
    except FicheDeVoeux.DoesNotExist:
        return JsonResponse({
            "success": False,
            "missing_docs": [],
            "error": "Aucune fiche de vœux trouvée pour ce prospect"
        })

    required_docs = DossierInscription.objects.filter(
        formation=formation,
        is_required=True
    )

    provided_docs = DocumentsDemandeInscription.objects.filter(
        prospect_id=prospect_id,
        id_document__in=required_docs
    ).exclude(file="")

    missing_docs = required_docs.exclude(
        id__in=provided_docs.values_list("id_document_id", flat=True)
    )

    if missing_docs.exists():
        return JsonResponse({
            "success": False,
            #"missing_docs": list(missing_docs.values_list("label", flat=True))
            "missing_docs": list(missing_docs.values("id", "label"))
        })

    return JsonResponse({
        "success": True,
        "missing_docs": []
    })

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiStoreNotePreinscrit(request):
    id_prospect = request.POST.get('id_prospect')
    content = request.POST.get('content')
    tags = request.POST.get('tags')

    if not content:
        return JsonResponse({'status': 'error', 'message': 'Le contenu de la note est requis.'}, status=400)

    note = NotesProcpects.objects.create(
        prospect=Prospets.objects.get(id=id_prospect),
        created_by=request.user,
        note=content,
        tage = tags,
        context = "prinscrit",
    )
    note.save()
    return JsonResponse({'status': 'success', 'message': 'Note enregistrée avec succès.'})

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiStoreRappelPreinscrit(request):
    type = request.POST.get('type')
    subject = request.POST.get('subject')
    date = request.POST.get('date')
    time = request.POST.get('time')
    description = request.POST.get('description')
    id_prospect = request.POST.get('id_prospect')

    if not all([type, subject, date, time, description, id_prospect]):
        return JsonResponse({'status': 'error', 'message': 'Tous les champs sont requis.'})

    rappel = RendezVous.objects.create(
        type=type,
        object=subject,
        date_rendez_vous=date,
        heure_rendez_vous=time,
        description=description,
        prospect=Prospets.objects.get(id=id_prospect),
        created_by=request.user,
        context = "prinscrit",
    )
    rappel.save()
    return JsonResponse({'status': 'success', 'message': 'Rappel enregistré avec succès.'})

def get_prospects_incomplets():
    # Tous les prospects préinscrits
    prospects = Prospets.objects.filter(type_prospect="particulier").filter(Q(statut = "prinscrit") | Q(statut= "instance") | Q(statut="convertit"))
    results = []

    for prospect in prospects:
        # Récupérer la fiche de voeux confirmée ou non
        try:
            fiche_voeux = FicheDeVoeux.objects.get(prospect=prospect)
        except FicheDeVoeux.DoesNotExist:
            continue  # si pas de fiche, on ignore

        formation = fiche_voeux.specialite.formation
        if not formation:
            continue  # si pas de formation, on ignore

        # Documents requis pour cette formation
        docs_requis = DossierInscription.objects.filter(formation=formation)
        total_docs = docs_requis.count()

        # Documents déjà uploadés par le prospect
        docs_fournis = DocumentsDemandeInscription.objects.filter(
            prospect=prospect,
            fiche_voeux=fiche_voeux,
            file__isnull=False
        ).values_list("id_document_id", flat=True)

        provided_docs = len(docs_fournis)

        # Documents manquants
        docs_manquants = docs_requis.exclude(id__in=docs_fournis)

        # Calculate progression (percentage of completed documents)
        progression = int((provided_docs / total_docs) * 100) if total_docs > 0 else 0

        if not docs_fournis:
            results.append({
                "prospect": prospect,
                "cas": "aucun document fourni",
                "documents_manquants": list(docs_requis.values("id", "label")),
                "progression": progression,
                "total_docs": total_docs,
                "provided_docs": provided_docs
            })
        elif docs_manquants.exists():
            results.append({
                "prospect": prospect,
                "cas": "documents manquants",
                "documents_manquants": list(docs_manquants.values("id", "label")),
                "progression": progression,
                "total_docs": total_docs,
                "provided_docs": provided_docs
            })

    return results

@login_required(login_url="institut_app:login")
def ApiGetDossierDetails(request):
    id_prospect = request.GET.get('id_prospect')
    
    try:
        prospect = Prospets.objects.get(id=id_prospect)
        
        # Get the fiche de voeux
        try:
            fiche_voeux = FicheDeVoeux.objects.get(prospect=prospect)
        except FicheDeVoeux.DoesNotExist:
            fiche_voeux = None
            
        # Get formation and required documents
        formation = None
        docs_manquants = []
        docs_fournis = []
        total_docs = 0
        provided_docs = 0
        progression = 0
        
        if fiche_voeux:
            formation = fiche_voeux.specialite.formation
            
            if formation:
                # Documents requis pour cette formation
                docs_requis = DossierInscription.objects.filter(formation=formation)
                total_docs = docs_requis.count()
                
                # Documents déjà uploadés par le prospect
                docs_fournis_qs = DocumentsDemandeInscription.objects.filter(
                    prospect=prospect,
                    fiche_voeux=fiche_voeux,
                    file__isnull=False
                ).values_list("id_document_id", flat=True)
                
                docs_fournis = list(docs_fournis_qs)
                provided_docs = len(docs_fournis)
                
                # Documents manquants
                docs_manquants_qs = docs_requis.exclude(id__in=docs_fournis)
                docs_manquants = list(docs_manquants_qs.values("id", "label"))
                
                # Calculate progression (percentage of completed documents)
                if total_docs > 0:
                    progression = int((provided_docs / total_docs) * 100)
        
        response_data = {
            'id': prospect.id,
            'nom': prospect.nom,
            'prenom': prospect.prenom,
            'email': prospect.email,
            'telephone': prospect.telephone,
            'type_prospect': prospect.type_prospect,
            'entreprise': prospect.entreprise,
            'created_at': prospect.created_at.strftime('%Y-%m-%d') if prospect.created_at else None,
            'documents_manquants': docs_manquants,
            'documents_fournis': docs_fournis,
            'progression': progression,
            'total_documents': total_docs,
            'documents_fournis_count': provided_docs
        }
        
        return JsonResponse({'success': True, 'data': response_data})
        
    except Prospets.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Prospect non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@login_required(login_url="institut_app:login")
def prospects_incomplets_view(request):
    data = get_prospects_incomplets()
    context = {
        'data': data,
        'tenant': request.tenant
    }
    return render(request, "tenant_folder/crm/preinscrits/prospects_incomplets.html", context)

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiValidatePreinscrit(request):
    id_preinscrit=  request.GET.get('id_preinscrit')

    try:
        preinscrit = Prospets.objects.get(id = id_preinscrit)
        fiche_voeux = FicheDeVoeux.objects.filter(prospect = preinscrit, is_confirmed = True).first()

        specialite = fiche_voeux.specialite
        promo = fiche_voeux.promo

      
        ClientPaiementsRequest.objects.create(
            client = preinscrit,
            promo = promo,
            specialite = specialite,
            motif = "frais_f"
        )
        
        
        preinscrit.statut = "instance"

        preinscrit.save()

        

        return JsonResponse({"status": "success"})
    except:
        return JsonResponse({"status":"error",'message' : "Une erreur systeme c'est produite, veuillez contacter l'administrateur"})

@login_required(login_url="institut_app:login")
def ApiLoadFinancialData(request):
    if request.method == "GET":
        id_prospect = request.GET.get('id_preinscrit')

        paiements = Paiements.objects.filter(prospect__id = id_prospect, context="frais_f").aggregate(total_paye=Sum('montant_paye'))['total_paye'] or 0
        paiementDue = DuePaiements.objects.filter(client__id = id_prospect).aggregate(total_due=Sum('montant_due'))['total_due'] or 0

        data = {
            'montant_paye' : paiements,
            'montant_total' : paiementDue,
        }

        return JsonResponse(data, safe=False)