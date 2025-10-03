from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib import messages
from t_tresorerie.models import *
from t_formations.models import *
from django.db import transaction
from django.db.models import Count, Q
from django.core.exceptions import PermissionDenied
from functools import wraps
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta



def listeVisiteurs(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/crm/liste_visiteurs.html',context)

def ApiListeVisiteurs(request):
    liste = Visiteurs.objects.filter().values('id','cin','etat','type_visiteur','nom','prenom','email','telephone','created_at')

    for l in liste:
        l_obj = Visiteurs.objects.get(id=l['id'])
        l['type_visiteur_label'] = l_obj.get_type_visiteur_display()
        l['etat_label'] = l_obj.get_etat_display()

    return JsonResponse(list(liste), safe=False)

@transaction.atomic
def nouveauVisiteur(request):
    form = VisiteurForm()
    demande = DemandeInscriptionForm()
    if request.method == 'POST':
        form = VisiteurForm(request.POST)
        demande = DemandeInscriptionForm(request.POST)
        if form.is_valid() and demande.is_valid():
            visiteur = form.save()

            formation = demande.cleaned_data.get('formation')
            specialite = demande.cleaned_data.get('specialite')
            formule = demande.cleaned_data.get('formule')
            session = demande.cleaned_data.get('session')
            promo = demande.cleaned_data.get('promo')

            if formation and specialite and formule and session:
                demande = DemandeInscription(
                    visiteur = visiteur,
                    formation = formation, 
                    specialite = specialite,
                    session = session,
                    formule = formule,
                    promo = promo,
                )
                demande.save()

            messages.success(request, 'Visiteur ajouté avec succès')
            return redirect('t_crm:liste_visiteurs')
    else:
        context = {
            'form' : form,
            'demande' : demande,
        }
        return render(request, 'tenant_folder/crm/nouveau_visiteur.html', context)

def ApprouveVisiteurInscription(request,pk):
    visiteur = Visiteurs.objects.get(id= pk)
    
    new_paie_request = ClientPaiementsRequest(
        created_by = request.user,
        client = visiteur,
        amount = visiteur.formation__frais_inscription
    )

    new_paie_request.save()
    visiteur.has_paied = True
    visiteur.save()

def modifierVisiteur(request, id):
    pass

def supprimerVisiteur(request):
    if request.user.has_perm("t_crm.delete_visiteurs"):
        pk = request.POST.get('id')
        visiteur = Visiteurs.objects.get(id = pk)
        demande_inscription = DemandeInscription.objects.filter(visiteur = visiteur).count()
        if demande_inscription > 0:
            return JsonResponse({'success': False, 'message': 'Impossible de supprimer le visiteur car il a une demande d\'inscription en cours.'})
        else:
            visiteur.delete()
            return JsonResponse({'success': True, 'message': 'Visiteur supprimé avec succès'})
    else:
        return JsonResponse({'success': False, 'message': 'Vous n\'avez pas l\'autorisation de supprimer le visiteur'})


def detailsVisiteur(request, pk):
    if request.user.has_perm('t_crm.view_visiteurs'):
        permissions = request.user.get_all_permissions()
        print(permissions)
        obj = Visiteurs.objects.get(id = pk)
        context = {
            'obj' : obj,
            'tenant' : request.tenant
        }
        return render(request,'tenant_folder/crm/details_visiteur.html', context)
    else:
        messages.error(request,"Vous n'avez pas l'autorisation d'acceder a cette partie.")
        return redirect('t_crm:liste_visiteurs')
        
@transaction.atomic
def updateVisiteur(request,pk):
    obj = Visiteurs.objects.get(id = pk)
    form = VisiteurForm(instance=obj)
    if request.method == "POST":
        form = VisiteurForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"Les informations ont été sauvegarder ave succès")
            return redirect("t_crm:details_visiteur", pk)
        
        else:
            messages.error(request, "Une erreur c'est produite lors du traitement du formulaire")
            return redirect('t_crm:updateVisiteur', pk)
        
    else:

        context = {
            'form' : form,
            'tenant' : request.tenant
        }
        return render(request, "tenant_folder/crm/update_visiteur.html",context)

def ApiGetSpecialite(request):
    formation_id = request.GET.get('formation_id')
    formation_obj = Formation.objects.get(id = formation_id)
    specialites = Specialites.objects.filter(formation = formation_obj.code).values('id','label')
    return JsonResponse(list(specialites), safe=False)

def ApiGETDemandeInscription(request):
    id_visiteur = request.GET.get('id_visiteur')
    demandes = DemandeInscription.objects.filter(visiteur = id_visiteur).values('id','formation','specialite__label','created_at','etat')
    for demande in demandes:
        demande_obj = DemandeInscription.objects.get(id=demande['id'])
        demande['etat_label'] = demande_obj.get_etat_display()
    return JsonResponse(list(demandes), safe=False)

def ListeDemandeInscription(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/crm/liste_demande_inscription.html', context)

def ApiGetListeDemandeInscription(request):
    demandes = DemandeInscription.objects.all().values('id','visiteur__nom','visiteur__prenom','specialite__label','specialite__code','created_at','etat','visiteur__has_completed_documents')
    for demande in demandes:
        demande_obj = DemandeInscription.objects.get(id=demande['id'])
        demande['etat_label'] = demande_obj.get_etat_display()
        
    return JsonResponse(list(demandes), safe=False)

def ApiGetGrideDemandeInscription(request):
    specialites = Specialites.objects.all()

    specialites_demandes = []

    for specialite in specialites:
        # Récupérer les promotions associées à chaque spécialité
        demandes_par_promo = (
            specialite.demandeinscription_set
            .values('promo__label','promo__session')  # Agréger par le nom de la promotion
            .annotate(nb_demandes=Count('id'))  # Compter les demandes d'inscription
            .order_by('promo__label')  # Trier par nom de promotion
        )

        # Ajout de la spécialité et du nombre de demandes par promotion
        for promo in demandes_par_promo:
            specialite_data = {
                'code': specialite.code, 
                'label': specialite.label,
                'promotion': promo['promo__label'],
                'session' : promo['promo__session'],
                'nb_demande': promo['nb_demandes'],
                'id': specialite.id  
            }

            specialites_demandes.append(specialite_data)

    return JsonResponse({'specialites_demandes': specialites_demandes})

def ApiAddNewDemandeInscription(request):

    promo = request.POST.get('_promo')
    formation = request.POST.get('_formation')
    specialite = request.POST.get('_specialite')
    formule = request.POST.get('_formule')
    id_visiteur = request.POST.get('id_visiteur')

    if promo and formation and specialite and formule and id_visiteur:

        obj_specialite = Specialites.objects.get(id = specialite)
        obj = DemandeInscription.objects.filter(visiteur = id_visiteur, specialite = obj_specialite).count()
        if obj > 0:
            return JsonResponse({'status': "error", 'message': 'Demande d\'inscription déjà existante pour cette spécialité'})

        else:
            new_demande = DemandeInscription(
                visiteur = Visiteurs.objects.get(id = id_visiteur),
                formation = Formation.objects.get(id = formation),
                specialite = Specialites.objects.get(id = specialite),
                formule = formule,
                promo = Promos.objects.get(id = promo),
            )

            new_demande.save()
            return JsonResponse({'status': "success", 'message': 'Demande d\'inscription ajoutée avec succès'})
    else:
        return JsonResponse({'status': "error", 'message': 'Veuillez remplir tous les champs obligatoires'})

@transaction.atomic
def ApiConfirmDemandeInscription(request):

    id_demande = request.GET.get('id_demande')
    demande = DemandeInscription.objects.get(id = id_demande)
    demande.etat = 'accepte'
    
    user = demande.visiteur
    user.etat = "instance"
    user.save()

    demande_paiement = ClientPaiementsRequest(
        client = user,
        formation = demande.formation,
        specialite = demande.specialite,
        motif = "frais",
        amount = demande.formation.frais_inscription + demande.formation.frais_assurance + demande.specialite.prix,
    )

    demande_paiement.save()
    demande.save()

    seuil_frais_formation = SeuilPaiements.objects.get(specialite = demande.specialite)
    valeur = seuil_frais_formation.valeur

    demande_paiement_line = clientPaiementsRequestLine(
        paiement_request = demande_paiement,
        motif_paiement = "fin",
        etat = "auc",
        montant_paye = demande_paiement.formation.frais_inscription,
        montant_restant = demande_paiement.formation.frais_inscription,
    )
    demande_paiement_line.save()

    demande_paiement_line1 = clientPaiementsRequestLine(
        paiement_request = demande_paiement,
        motif_paiement = "ass",
        etat = "auc",
        montant_paye = demande_paiement.formation.frais_assurance,
        montant_restant = demande_paiement.formation.frais_assurance,
    )
    demande_paiement_line1.save()

    demande_paiement_line2 = clientPaiementsRequestLine(
        paiement_request = demande_paiement,
        motif_paiement = "frf",
        etat = "auc",
        montant_paye = demande.specialite.prix * (Decimal(valeur) / 100),
        montant_restant = demande.specialite.prix * (Decimal(valeur) / 100),
    )
    demande_paiement_line2.save()

    return JsonResponse({'status': 'success', 'message' : 'La demande d\'incription à été confirmer avec succès.'})

def ApiAnnulerDemandeInscription(request):
    id_demande = request.POST.get('id_demande')
    demande = DemandeInscription.objects.get(id = id_demande)
    paiement_request = ClientPaiementsRequest.objects.get(demandes = demande)
    paiement_request.etat = "annulation"
    paiement_request.save()
    demande.etat = 'annulation'
    demande.save()
    return JsonResponse({'status': "success", 'message': 'Demande d\'annulation effectuée avec succès'})    

def ApiRemoveDemandeInscription(request):
    if request.user.is_staff:
        id_demande = request.POST.get('id')
        demande = DemandeInscription.objects.get(id = id_demande)
        demande.delete()
        return JsonResponse({'status': "success", 'message': 'Demande d\'inscription annulée avec succès'})
    else:
        return JsonResponse({'status' : "error", "message" : "Action non autorisé pour votre niveau de compte"})

def filter_visiteur(request):
    search = request.GET.get('search')
    visiteur = Visiteurs.objects.all()

    if search:
        visiteurs = visiteur.filter(
            Q(cin__icontains=search) |
            Q(nom__icontains=search) |
            Q(prenom__icontains=search) |
            Q(telephone__icontains=search) |
            Q(email__icontains=search) |
            Q(type_visiteur__icontains=search)
        )

    data = []
    for v in visiteurs:
        data.append({
            'id' : v.id,
            'cin': v.cin,
            'nom_prenom': f"{v.nom} {v.prenom}",
            'email': v.email,
            'telephone' : v.telephone,
            'type_visiteur': v.get_type_visiteur_display(),
            'etat': v.etat,
            'etat_label' : v.get_etat_display()
        })
    return JsonResponse({'filtred': data})

@login_required(login_url='institut_app:login')
@transaction.atomic
def InscriptionParticulier(request):
    form = NewProspecFormParticulier()
    if request.method == "POST":
        form = NewProspecFormParticulier(request.POST)
        if form.is_valid():
            donnee = form.save()
            donnee.type_prospect = "particulier"
            donnee.etat
            donnee.save()

            voeux_specialite = request.POST.get('voeux_specialite')
            promo_selection = request.POST.get('promo_selection')


            if voeux_specialite is not None and voeux_specialite != "":
                specialite = Specialites.objects.get(id=voeux_specialite)
                FicheDeVoeux.objects.create(
                    prospect=donnee,
                    specialite=specialite,
                    promo = Promos.objects.get(code = promo_selection)
                )

            messages.success(request, "Prospect ajouté avec succès")
            return redirect('t_crm:ListeDesProspects')
        else:
            messages.error(request, "Une erreur s'est produite lors de l'enregistrement du prospect")

    context = {
        'tenant' : request.tenant,
        'form' : form,

    }
    return render(request, 'tenant_folder/crm/inscription_particulier.html', context)

@login_required(login_url='institut_app:login') 
def InscriptionEntreprise(request):
    form = NewProspecFormEntreprise()
    if request.method == "POST":
        form = NewProspecFormEntreprise(request.POST)
        if form.is_valid():
            donnee = form.save()
            donnee.type_prospect = "entreprise"
            donnee.etat
            donnee.save()
            messages.success(request, "Prospect ajouté avec succès")
            return redirect('t_crm:ListeDesProspects')
        else:
            messages.error(request, "Une erreur s'est produite lors de l'enregistrement du prospect")

    context = {
        'tenant' : request.tenant,
        'form' : form,

    }
    return render(request, 'tenant_folder/crm/inscription_entreprise.html', context)

@login_required(login_url='institut_app:login')
def ListeDesProspects(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/crm/liste-des-prospects.html', context)

from django.utils.dateformat import format

@login_required(login_url='institut_app:login')
def ApiLoadProspects(request):
    prospects = Prospets.objects.all().values('id', 'nin', 'nom', 'prenom', 'type_prospect','email','indic','telephone','canal','created_at','etat','entreprise')
    for l in prospects:
        l_obj = Prospets.objects.get(id=l['id'])
        l['type_prospect_label'] = l_obj.get_type_prospect_display()
        l['etat_label'] = l_obj.get_etat_display()
        l['created_at'] = format(l_obj.created_at, "Y-m-d H:i")
    return JsonResponse(list(prospects), safe=False)

@login_required(login_url='institut_app:login')
def ApiDeleteProspect(request):
    id_prospect = Prospets.objects.get(id = request.POST.get('id_prospect'))
    id_prospect.delete()

    return JsonResponse({'status': 'success', 'message': 'Prospect supprimé avec succès'})

@login_required(login_url='institut_app:login')
def ApiFilterProspect(request):
    filter_option = request.GET.get('filter_option')
    value = request.GET.get('value')

    if (filter_option == "filter-prospect"):
        prospects = Prospets.objects.filter(type_prospect=value, status="visiteur").values('id','entreprise', 'nom', 'prenom', 'type_prospect','email','telephone','canal','created_at','etat')
        for l in prospects:
            l_obj = Prospets.objects.get(id=l['id'])
            l['type_prospect_label'] = l_obj.get_type_prospect_display()
            l['etat_label'] = l_obj.get_etat_display()
    elif (filter_option == "date_filter-prospect"):
        prospects = Prospets.objects.filter(type_prospect=value, status="visiteur").order_by(value).values('id','entreprise', 'nom', 'prenom', 'type_prospect','email','telephone','canal','created_at','etat')
        for l in prospects:
            l_obj = Prospets.objects.get(id=l['id'])
            l['type_prospect_label'] = l_obj.get_type_prospect_display()
            l['etat_label'] = l_obj.get_etat_display()

    return JsonResponse(list(prospects), safe=False)

@login_required(login_url='institut_app:login')
def ApiFilterPrinscrit(request):
    filter_option = request.GET.get('filter_option')
    value = request.GET.get('value')

    if (filter_option == "filter-prospect"):
        prospects = Prospets.objects.filter(type_prospect=value, statut="prinscrit").values('id','entreprise', 'nom', 'prenom', 'type_prospect','email','telephone','canal','created_at','etat')
        for l in prospects:
            l_obj = Prospets.objects.get(id=l['id'])
            l['type_prospect_label'] = l_obj.get_type_prospect_display()
            l['etat_label'] = l_obj.get_etat_display()
    elif (filter_option == "date_filter-prospect"):
        prospects = Prospets.objects.filter(type_prospect=value, statut="prinscrit").order_by(value).values('id','entreprise', 'nom', 'prenom', 'type_prospect','email','telephone','canal','created_at','etat')
        for l in prospects:
            l_obj = Prospets.objects.get(id=l['id'])
            l['type_prospect_label'] = l_obj.get_type_prospect_display()
            l['etat_label'] = l_obj.get_etat_display()

    return JsonResponse(list(prospects), safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadFormation(request):
    liste = Formation.objects.all().values('id','nom','code')
    return JsonResponse(list(liste), safe=False) 

@login_required(login_url='institut_app:login')
def ApiLoadSpecialite(request):
    id_formation = request.GET.get('id_formation')
    specialites = Specialites.objects.filter(formation = Formation.objects.get(id=id_formation)).values('id','code','label')
    return JsonResponse(list(specialites), safe=False)

@login_required(login_url='institut_app:login')
def DetailsProspect(request, pk):
    prospect = Prospets.objects.get(id=pk)
    if prospect.type_prospect == "particulier":
        context = {
            'tenant' : request.tenant,
            'pk' : pk,
        }
        return render(request, 'tenant_folder/crm/details_prospect.html', context)
    else:
        context = {
            'tenant' : request.tenant,
            'pk' : pk,
        }
        return render(request, 'tenant_folder/crm/details_prospect_ets.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadProspectDetails(request):
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
            'specialite_id_formation': fiche.specialite.formation.id
        })
   

    data_formation=[]
    formation = Formation.objects.all()
    for f in formation:
        data_formation.append({
            'id': f.id,
            'nom': f.nom,
            'code': f.code,
        })

    data_specialite=[]
    specialites = Specialites.objects.all()
    for s in specialites:
        data_specialite.append({
            'id': s.id,
            'code': s.code,
            'label': s.label,
        })
    data = {
        'id': prospect.id,
        'nin': prospect.nin,
        'nom': prospect.nom,
        'prenom': prospect.prenom,
        'email': prospect.email,
        'telephone': prospect.telephone,
        'canal': prospect.canal,
        'observation' : prospect.observation,
        'entreprise' : prospect.entreprise,
    }
    return JsonResponse({'prospect': data, 'fiche_voeux': fiche_voeux_list,'formations': data_formation,'specialites': data_specialite})

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdatePropectDetails(request):
    id_prospect = request.POST.get('id_prospect')
    last_name = request.POST.get('nom')
    first_name = request.POST.get('prenom')
    email = request.POST.get('email')
    telephone = request.POST.get('telephone')
    canal = request.POST.get('canal')
    observation = request.POST.get('observation')
    voeux_specialite = request.POST.get('voeux_specialite')

    prospect_obj = Prospets.objects.get(id=id_prospect)
    fiche_voeux = FicheDeVoeux.objects.filter(prospect=prospect_obj)
    fiche_voeux.delete()
    fiche_voeux = FicheDeVoeux.objects.create(
        prospect=prospect_obj,
        specialite=Specialites.objects.get(id=voeux_specialite),
    )

    prospect = Prospets.objects.get(id = id_prospect)
    prospect.nom = last_name
    prospect.prenom = first_name
    prospect.email = email
    prospect.telephone = telephone
    prospect.canal = canal
    prospect.observation = observation
    prospect.save()

    return JsonResponse({'status': 'success', 'message': 'Les informations du prospect ont été mises à jour avec succès.'})

@login_required(login_url='institut_app:login')
@transaction.atomic
def ApiUpdateProspectEtsDetails(request):
    id_prospect = request.POST.get('id_prospect')
    
    entreprise = request.POST.get('entreprise_informations')
    last_name = request.POST.get('last_name_ets')
    first_name = request.POST.get('first_name_ets')
    email = request.POST.get('email_ets')
    telephone = request.POST.get('telephone_ets')
    canal = request.POST.get('canal_ets')
    observation = request.POST.get('observation_ets')

    prospect = Prospets.objects.get(id = id_prospect)
    prospect.entreprise = entreprise
    prospect.nom = last_name
    prospect.prenom = first_name
    prospect.email = email
    prospect.telephone = telephone
    prospect.canal = canal
    prospect.observation = observation
    prospect.save()

    return JsonResponse({'status': 'success', 'message': 'Les informations du prospect ont été mises à jour avec succès.'})

@login_required(login_url="institut_app:login")
def ApiCheckIfVoeuxExiste(request):
    id_prospoect = request.GET.get('id_prospect')
    fiche_voeux  = FicheDeVoeux.objects.filter(prospect = Prospets.objects.get(id=id_prospoect), is_confirmed = False)

    if fiche_voeux:
        return JsonResponse({'status' : 'success'})
    else:
        return JsonResponse({'status' : 'error'})


