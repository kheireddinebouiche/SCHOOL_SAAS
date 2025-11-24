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


@login_required(login_url='institut_app:login')
def ApiLoadProspectPerosnalInfos(request):
    id_prospect = request.GET.get('id_prospect')
    prospect = Prospets.objects.filter(id=id_prospect).values('created_at','id','nin','nom','prenom','email','indic','telephone','type_prospect','canal','statut','etat','entreprise','poste_dans_entreprise','observation','has_second_wish').first()
    
    if prospect:
        obj = Prospets.objects.get(id= prospect['id'])
        prospect['created_at'] = prospect['created_at'].strftime("%Y-%m-%d %H:%M")
        prospect['statut_label'] = obj.get_statut_display()   

    return JsonResponse(prospect, safe=False)

@login_required(login_url='institut_app:login')
def ApiLoadProspectRendezVous(request):
   id_prospect = request.GET.get('id_prospect')
   rendez_vous = RendezVous.objects.filter(prospect__id=id_prospect, context = "prospect", archived=False).values('id','date_rendez_vous','heure_rendez_vous','type','object','created_at','statut')
   for l in rendez_vous:
       l_obj = RendezVous.objects.get(id = l['id'])
       l['status_label'] = l_obj.get_statut_display()
       l['type_label'] = l_obj.get_type_display()
       l['created_at'] = l_obj.created_at.strftime("%Y-%m-%d")
   return JsonResponse(list(rendez_vous), safe=False)

################################### Gestion des notes ##################################################
@login_required(login_url='institut_app:login')
def ApiLoadNote(request):
    prospect_id = request.GET.get('id_prospect')
    notes = NotesProcpects.objects.filter(prospect__id = prospect_id, context="prospect").values('id','prospect','created_by__username','created_at','note','tage')
    for l in notes:
        l_obj = NotesProcpects.objects.get(id = l['id'])
        l['tage'] = l_obj.get_tage_display()
    return JsonResponse(list(notes), safe=False)
    
@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiStoreNote(request):
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
        context = "prospect",
    )
    note.save()
    return JsonResponse({'status': 'success', 'message': 'Note enregistrée avec succès.'})

@login_required(login_url='institut_app:login')
def ApiDeleteNote(request):
    id_note = request.POST.get('id_note')
    try:
        note = NotesProcpects.objects.get(id=id_note)
        note.delete()
        return JsonResponse({'status': 'success', 'message': 'Note supprimée avec succès.'})
    except NotesProcpects.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Note non trouvée.'}, status=404)

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdateNote(request):
    pass


################################### !Gestion des notes##################################################



###################################Fiche de voeux prospect #############################################
@login_required(login_url='institut_app:login')
def ApiLoadFicheVoeuxProspect(request):
    id_prospect = request.GET.get('id_prospect')
    prospect = Prospets.objects.get(id = id_prospect)
    fiche_voeux = FicheDeVoeux.objects.filter(prospect = prospect)

    fiche_voeux_list = []
    for fiche in fiche_voeux:
        fiche_voeux_list.append({
            'id': fiche.id,
            'specialite_code': fiche.specialite.code,
            'specialite_label': fiche.specialite.label,
            'specialite_id' : fiche.specialite.id,
            'specialite_id_formation': fiche.specialite.formation.id,
            'promo' : fiche.promo.get_session_display()+'-'+fiche.promo.begin_year+'/'+fiche.promo.end_year,
            'created_at' : format(fiche.created_at,"Y-m-d H:i"),
            'updated_at' : format(fiche.updated_at,"Y-m-d H:i"),
            
        })
    return JsonResponse({'fiche_voeux': fiche_voeux_list})

@login_required(login_url="institut_app:login")
def ApiLoadFicheVoeuxDoubleProspect(request):
    if request.method == "GET":
        id_prospect = request.GET.get('id_prospect')
        prospect = Prospets.objects.get(id = id_prospect)
        fiche_voeux = FicheVoeuxDouble.objects.filter(prospect = prospect)

        fiche_voeux_list = []
        for fiche in fiche_voeux:
            fiche_voeux_list.append({
                'id': fiche.id,
                'specialite1_code': fiche.specialite.specialite1.code,
                'specialite1_label': fiche.specialite.specialite1.label,

                'specialite2_code': fiche.specialite.specialite2.code,
                'specialite2_label': fiche.specialite.specialite2.label,

                'promo' : fiche.promo.get_session_display()+'-'+fiche.promo.begin_year+'/'+fiche.promo.end_year,
                'created_at' : fiche.created_at,
                'updated_at' : fiche.updated_at
                
            })
        return JsonResponse({'fiche_voeux': fiche_voeux_list})
    else:
        return JsonResponse({"status":"error"})


@login_required(login_url="institut_app:login")
def ApiLoadDoubleDiplomations(request):
    if request.method == "GET":
        liste = DoubleDiplomation.objects.all().values('id', 'label')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error"})
    
@login_required(login_url="institut_app:login")
def ApiLoadDoubleSpecialite(request):
    if request.method == "GET":
        id_formation = request.GET.get('id_formation')

        if not id_formation:
            return JsonResponse({"status":"error","message":"Informations manquantes"})

        obj = DoubleDiplomation.objects.get(id = id_formation)

        data = {
            'specialite1' : obj.specialite1.label,
            'specialite1_formation' : obj.specialite1.formation.nom,

            'specialite2' : obj.specialite2.label,
            'specialite2_formation' : obj.specialite2.formation.nom,

        }

        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def ApiLoadPromos(request):
    if request.method == "GET":
        liste = Promos.objects.all()
        data = []
        for i in liste:
            data.append({
                "id" : i.id,
                "code" : i.code,
                "start_year" : i.begin_year,
                "end_year" : i.end_year,
                "session" : i.get_session_display()
            })
        
        return JsonResponse({"data" : data},  safe=False)
        
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app")
def ApiCreateDoubleDiplomation(request):
    if request.method == "POST":
        id_prospect = request.POST.get('id_prospect')
        promo = request.POST.get('promo')
        formation = request.POST.get('formation')
        commentaires = request.POST.get('commentaires')

        if not id_prospect or not promo or not formation:
            return JsonResponse({"status":"error",'message':"Informations manquantes"})
        
        try:
            FicheVoeuxDouble.objects.create(
                prospect_id = id_prospect,
                specialite_id = formation,
                promo = Promos.objects.get(code = promo),
                commentaire = commentaires,
            )
            prospect = Prospets.objects.get(id = id_prospect)
            prospect.is_double =True
            prospect.save()

            ## Rajouter la suppression de la fiche de voeux standard dans le cas ou elle existe
            voeux_standard = FicheDeVoeux.objects.filter(prospect_id=id_prospect, promo = Promos.objects.get(code=promo), is_confirmed=False)

            if voeux_standard.exists():
                voeux_standard.delete()

            messages.success(request, "Inscription du prospect en double diplômation confirmé.")
            return JsonResponse({"status" : "success"})
        
        except Exception as e:
            return JsonResponse({"status" : "error", 'message' : str(e)})
        
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def ApiUpdateDoubleVoeux(request):
    if request.method == "POST":
        id_formation = request.POST.get('id_formation')
        id_prospect = request.POST.get('id_prospect')
        id_voeux = request.POST.get('id_voeux')
        promo = request.POST.get('promo')
        comment = request.POST.get('comment')

        if not id_formation or not promo or not id_voeux or not id_prospect:
            return JsonResponse({"status":"error","message":"Informations manquante"})
        
        obj = FicheVoeuxDouble.objects.get(id = id_voeux, prospect_id = id_prospect)

        obj.specialite = DoubleDiplomation.objects.get(id = id_formation)
        obj.promo = Promos.objects.get(code = promo)
        obj.commentaire = comment
        obj.save()

        return JsonResponse({"status" : "success", "message":"Les modifications ont été effectuer avec succès"})



    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="insitut_app:login")
@transaction.atomic
def ApiChangeToStandardCursus(request):
    if request.method == "POST":
        formation = request.POST.get('formation')
        promo = request.POST.get('promo')
        specialite = request.POST.get('specialite')
        commentaires = request.POST.get('commentaires')
        id_prospect = request.POST.get('id_prospect')

        if not formation or not promo or not specialite or not id_prospect:
            return JsonResponse({"status":"error",'message':"Informations manquante"})
        
        try:
            FicheDeVoeux.objects.create(
                prospect_id = id_prospect,
                specialite_id = specialite,
                promo = Promos.objects.get(code = promo),
                commentaire = commentaires
            )

            fiche_double = FicheVoeuxDouble.objects.get(prospect_id = id_prospect, is_confirmed=False, promo__code = promo)
            fiche_double.delete()

            prosepect = Prospets.objects.get(id = id_prospect)
            prosepect.is_double = False
            prosepect.save()

            messages.success(request, "L'inscription de l'étudiant à un cursus standard à été effectuer avec succès")
            return JsonResponse({"status":"success"})

        except Exception as e:
            return JsonResponse({"status" : "error", "message" : str(e)})

    else:
        return JsonResponse({"status":"error"})

@login_required(login_url='institut_app:login')
def ApiUpdateFicheVoeuxProspect(request):
    pass

@login_required(login_url='institut_app:login')
def ApiDeleteFicheVoeuxProspect(request):
    pass


@login_required(login_url='institut_app:login')
def ApiStoreSecondVoeuxProspect(request):
    pass

@login_required(login_url='institut_app:login')
def ApiLoadSecondVoeuxProspect(request):
    pass


###################################Fiche de voeux prospect #############################################

###################################Gestion des rappels #############################################

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiStoreRappel(request):
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
        context = "prospect",
    )
    rappel.save()
    return JsonResponse({'status': 'success', 'message': 'Rappel enregistré avec succès.'})

@login_required(login_url='institut_app:login')
def ApiLoadRappel(request):
    id_prospect = request.GET.get('id_prospect')
    rappel = RendezVous.objects.filter(prospect__id=id_prospect, context="prospect", archived=False).values(
        'id', 'type','objet', 'date_rendez_vous', 'heure_rendez_vous', 'description', 'created_at','created_by'
    )
    for l in rappel:
        l_obj = RendezVous.objects.get(id = l['id'])
        l['type_label'] = l_obj.get_type_display()
        
    return JsonResponse(list(rappel), safe=False)

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiDeleteRappel(request):
    id_rappel = request.POST.get('id_rappel')
    try:
        rappel = RendezVous.objects.get(id=id_rappel)
        rappel.delete()
        return JsonResponse({'status': 'success', 'message': 'Rappel supprimé avec succès.'})
    except RendezVous.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Rappel non trouvé.'}, status=404)

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdateRappel(request):
    id_rappel = request.POST.get('id_rappel')
    type = request.POST.get('type')
    subject = request.POST.get('subject')
    date = request.POST.get('date')
    time = request.POST.get('time')
    description = request.POST.get('description')

    if not all([id_rappel, type, subject, date, time, description]):
        return JsonResponse({'status': 'error', 'message': 'Tous les champs sont requis.'}, status=400)

    try:
        rappel = RendezVous.objects.get(id=id_rappel)
        rappel.type = type
        rappel.object = subject
        rappel.date_rendez_vous = date
        rappel.heure_rendez_vous = time
        rappel.description = description
        rappel.save()
        return JsonResponse({'status': 'success', 'message': 'Rappel mis à jour avec succès.'})
    except RendezVous.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Rappel non trouvé.'}, status=404)
    
@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiChangeStateRappel(request):
    pass

@login_required(login_url='institut_app:login')
def ApiLoadRendezVousDetails(request):
    id_rendez_vous = request.GET.get('id_rendez_vous')
    object = RendezVous.objects.filter(id=id_rendez_vous).values('id','type','object','description','statut','date_rendez_vous','heure_rendez_vous')

    for i in object:
        i_obj = RendezVous.objects.get(id = i['id'])
        i['type_label'] = i_obj.get_type_display()
        i['statut_label'] = i_obj.get_statut_display()

    return JsonResponse(list(object), safe=False)

###################################Fiche de voeux prospect #############################################
from datetime import datetime

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiValidateProspect(request):
    if request.method == 'POST':
        id_prospect = request.POST.get('id_prospect')
        id_fiche_voeux = request.POST.get("id_fiche_voeux")
        try:
            prospect = Prospets.objects.get(id=id_prospect)
            prospect.etat = "accepte"
            prospect.statut = "prinscrit"
            prospect.preinscri_date = datetime.now()
            prospect.save()


            voeux = FicheDeVoeux.objects.get(id = id_fiche_voeux)
            voeux.is_confirmed = True
            voeux.save()

            return JsonResponse({'status': 'success', 'message': 'Prospect validé avec succès.'})
        except Prospets.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Prospect non trouvé.'})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'})

@login_required(login_url="institut_app:login")
def ApiValidateProspectDouble(request):
    if request.method == "POST":
        id_prospect = request.POST.get('id_prospect')
        id_fiche_voeux = request.POST.get("id_fiche_voeux")
        try:
            prospect = Prospets.objects.get(id=id_prospect)
            prospect.etat = "accepte"
            prospect.statut = "prinscrit"
            prospect.preinscri_date = datetime.now()
            prospect.save()


            voeux = FicheVoeuxDouble.objects.get(id = id_fiche_voeux)
            voeux.is_confirmed = True
            voeux.save()

            return JsonResponse({'status': 'success', 'message': 'Prospect validé avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({"status" : "error"})

@login_required(login_url='institut_app:login')
def ApiCheckStatutProspect(request):
    
    prospect = Prospets.objects.get(id=request.GET.get('id_prospect'))

    data = {
        'id': prospect.id,
        'etat': prospect.etat
    }
    return JsonResponse({'data': data})

@login_required(login_url="institut_app:login")
def ApiLoadFormationAndSpecialite(request):
    formation = Formation.objects.all()
    specialite = Specialites.objects.all()

    formation_liste = []
    for i in formation:
        formation_liste.append({
            'id' : i.id,
            'code' : i.code,
            'nom' : i.nom,
        })
    
    specialite_liste = []
    for i in specialite:
        specialite_liste.append({
            'id' : i.id,
            'code' : i.code,
            'label' : i.label,
        })

    return JsonResponse({'formation' : formation_liste, 'specialite' : specialite_liste})

@login_required(login_url="institut_app:login")
def ApiLoadFormation(request):
    formation = Formation.objects.all()
    promos = Promos.objects.all()
    
    formation_liste = []
    for i in formation:
        formation_liste.append({
            'id' : i.id,
            'code' : i.code,
            'nom' : i.nom,
        })

    promo_liste = []
    for i in promos:
        promo_liste.append({
            "id" : i.id,
            "code" : i.code,
            'begin_year' : i.begin_year,
            'end_year' : i.end_year,
            'session' : i.get_session_display(),
        })

    return JsonResponse({'formation':formation_liste,"promo" : promo_liste})

@login_required(login_url="institut_app:login")
def ApiLoadSpecialiteProspect(request):
    id_formation = request.GET.get('id_formation')
    formation = Formation.objects.get(id = id_formation)
    obj = Specialites.objects.filter(formation__code = formation.code)

    data = []
    for i in obj:
        data.append({
            "id" : i.id,
            "label" : i.label,
            "code" : i.code,
        })

    return JsonResponse({'specialite' : data}, safe=False)

@login_required(login_url="intitut_app:login")
@transaction.atomic
def ApiUpdateVoeux(request):
    id_prospect = request.POST.get('id_prospect')
    id_specialite = request.POST.get('specialite')
    id_fiche = request.POST.get('id_voeux')
    promo = request.POST.get('promo')
    
    if not id_prospect or not id_specialite or not id_fiche:
        return JsonResponse({"status" : "error", 'message': "Veuillez remplir tous les champs"})
    
    fiche = FicheDeVoeux.objects.get(id = id_fiche, prospect = Prospets.objects.get(id=id_prospect))    
    fiche.specialite = Specialites.objects.get(id = id_specialite)
    fiche.promo = Promos.objects.get(code = promo)
    fiche.save()
    return JsonResponse({'status' : "success", 'message' : "Fiche de voeux mis a jours avec succès"})


@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdateProspectData(request):
    nom = request.POST.get('nom')
    prenom = request.POST.get('prenom')
    email = request.POST.get('email')
    telephone = request.POST.get('telephone')
    observation = request.POST.get('observation')
    id_prospect = request.POST.get('id_prospect')
    indic = request.POST.get('indic')

    prospect = Prospets.objects.get(id = id_prospect)

    prospect.nom = nom
    prospect.prenom = prenom
    prospect.email = email
    prospect.observation = observation
    prospect.telephone = telephone
    prospect.indic = indic

    prospect.save()

    return JsonResponse({'status' : 'success', 'message' : "Les informations du prospect ont été mise à jour"})

@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiCreateVoeux(request):
    specialite = request.POST.get('specialite')
    id_prospect = request.POST.get('id_prospect')
    promo = request.POST.get('promo')
    comment = request.POST.get('comment')

    FicheDeVoeux.objects.create(
        prospect = Prospets.objects.get(id = id_prospect),
        specialite = Specialites.objects.get(id = specialite),
        promo = Promos.objects.get(code = promo),
        commentaire = comment
    )

    return JsonResponse({"status" : "success", "message" : "La fiche de voeux a été enregistrer avec succès"})

@login_required(login_url="institut_app:login")
def ApiConfirmeDoubleDiplome(request):
    if request.method == "POST":
        pass
    else:
        return JsonResponse({"status":"error"})