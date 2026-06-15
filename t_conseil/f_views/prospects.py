from institut_app.decorators import module_permission_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from t_crm.models import Prospets


@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
def ApiListeProspect(request):
    liste = Prospets.objects.filter(type_prospect="entreprise", context="con", is_client=False).values('id','slug','nom','prenom','etat','entreprise','poste_dans_entreprise','observation','context','created_at','telephone','email', 'type_prospect')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'add')
@transaction.atomic
def ApiCreateProspect(request):
    if request.method == "POST":
        entreprise = request.POST.get('entreprise')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        email_entreprise = request.POST.get('email_entreprise')
        telephone_entreprise = request.POST.get('telephone_entreprise')
        indicatif = request.POST.get('indicatif')
        canal = request.POST.get('canal')
        observation = request.POST.get('observation')
        type_prospect = 'entreprise'
        
        if not entreprise:
            return JsonResponse({'status': 'error', 'message': "La désignation de l'entreprise est obligatoire."}, status=400)
        
        adresse = request.POST.get('adresse')
        wilaya = request.POST.get('wilaya')
        code_zip = request.POST.get('code_zip')

        try:
            from t_crm.models import ContactEntreprise
            prospect = Prospets.objects.create(
                entreprise=entreprise,
                nom=nom,
                prenom=prenom,
                email=email_entreprise or email,
                telephone=telephone_entreprise or telephone,
                indic=indicatif,
                canal=canal,
                observation=observation,
                type_prospect=type_prospect,
                adresse=adresse,
                wilaya=wilaya,
                code_zip=code_zip,
                context='con'
            )
            
            if nom or prenom or telephone or email:
                ContactEntreprise.objects.create(
                    prospect=prospect,
                    nom=nom,
                    prenom=prenom,
                    telephone=telephone,
                    email=email,
                    is_primary=True
                )
            
            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='Prospets',
                target_id=str(prospect.id),
                details=f"Création d'un prospect (Conseil): {entreprise}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return JsonResponse({'status': 'success', 'message': 'Prospect créé avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur lors de la création : {str(e)}'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'add')
def ApiAddContactEntreprise(request):
    if request.method == "POST":
        prospect_id = request.POST.get('prospect_id')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        poste = request.POST.get('poste')
        
        if not nom and not prenom:
            return JsonResponse({'status': 'error', 'message': "Le nom ou le prénom est obligatoire."}, status=400)
            
        try:
            prospect = Prospets.objects.get(id=prospect_id)
            from t_crm.models import ContactEntreprise
            contact = ContactEntreprise.objects.create(
                prospect=prospect,
                nom=nom,
                prenom=prenom,
                telephone=telephone,
                email=email,
                poste=poste
            )
            return JsonResponse({'status': 'success', 'message': 'Contact ajouté avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur lors de l\'ajout : {str(e)}'}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'view')
def ApiLoadContactsEntreprise(request):
    prospect_id = request.GET.get('prospect_id')
    if not prospect_id:
        return JsonResponse({'status': 'error', 'message': 'ID du prospect requis.'}, status=400)
    
    from t_crm.models import ContactEntreprise
    contacts = ContactEntreprise.objects.filter(prospect_id=prospect_id).values(
        'id', 'nom', 'prenom', 'telephone', 'email', 'poste', 'is_primary'
    )
    return JsonResponse({'status': 'success', 'contacts': list(contacts)})
@login_required(login_url="institut_app:login")
@module_permission_required('con', 'edit')
def ApiEditContactEntreprise(request):
    if request.method == "POST":
        contact_id = request.POST.get('contact_id')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        poste = request.POST.get('poste')
        
        if not nom and not prenom:
            return JsonResponse({'status': 'error', 'message': "Le nom ou le prénom est obligatoire."}, status=400)
            
        try:
            from t_crm.models import ContactEntreprise
            contact = ContactEntreprise.objects.get(id=contact_id)
            contact.nom = nom
            contact.prenom = prenom
            contact.telephone = telephone
            contact.email = email
            contact.poste = poste
            contact.save()
            return JsonResponse({'status': 'success', 'message': 'Contact modifié avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur lors de la modification : {str(e)}'}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

@login_required(login_url="institut_app:login")
@module_permission_required('con', 'delete')
def ApiDeleteContactEntreprise(request):
    if request.method == "POST":
        contact_id = request.POST.get('contact_id')
        try:
            from t_crm.models import ContactEntreprise
            contact = ContactEntreprise.objects.get(id=contact_id)
            if contact.is_primary:
                return JsonResponse({'status': 'error', 'message': "Le contact principal ne peut pas être supprimé directement."}, status=400)
            contact.delete()
            return JsonResponse({'status': 'success', 'message': 'Contact supprimé avec succès.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Erreur lors de la suppression : {str(e)}'}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)

