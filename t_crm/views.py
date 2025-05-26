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

