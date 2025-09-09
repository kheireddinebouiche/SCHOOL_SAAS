from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django_tenants.utils import schema_context
from .form import *
from .models import Profile
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.db import transaction
from django.template.loader import render_to_string
from t_crm.models import *
from .models import UserSession
from django.contrib.sessions.models import Session
from django.utils import timezone
from django_otp.decorators import otp_required
from datetime import datetime, timedelta
from django.db.models import Count


@login_required(login_url='institut_app:login')
def crm_dashboard(request):
    # KPIs
    total_prospects = Prospets.objects.count()
    
    # Nouveaux prospects cette semaine
    one_week_ago = datetime.now() - timedelta(days=7)
    new_prospects_this_week = Prospets.objects.filter(created_at__gte=one_week_ago).count()
    
    # Rappels en attente
    pending_reminders = RendezVous.objects.filter(statut='en_attente').count()
    
    # Taux de conversion (prospects convertis en visiteurs)
    converted_prospects = Prospets.objects.filter(statut='convertit').count()
    conversion_rate = (converted_prospects / total_prospects * 100) if total_prospects > 0 else 0
    
    # Derniers rappels
    recent_reminders = RendezVous.objects.filter(archived=False).select_related('prospect').order_by('-created_at')[:5]
    
    # Répartition des prospects par canal
    prospects_by_channel = Prospets.objects.values('canal').annotate(count=Count('canal')).order_by('-count')
    
    # Calcul du taux de conversion par canal
    channel_conversion_data = []
    for channel in prospects_by_channel:
        canal = channel['canal']
        total = channel['count']
        converted = Prospets.objects.filter(canal=canal, statut='convertit').count()
        conversion_rate = (converted / total * 100) if total > 0 else 0
        channel_conversion_data.append({
            'canal': canal,
            'count': total,
            'conversion_rate': round(conversion_rate, 2)
        })
    
    # Répartition des prospects par statut - version avec données factices pour test
    prospects_by_status = Prospets.objects.values('statut').annotate(count=Count('statut')).order_by('-count')
    
    # Ajout des labels pour l'affichage
    status_labels = {
        'visiteur': 'Visiteur',
        'prinscrit': 'Pré-inscrit',
        'instance': 'Instance',
        'convertit': 'Converti'
    }
    
    prospects_by_status_with_labels = []
    for status in prospects_by_status:
        status_code = status['statut']
        count = status['count']
        label = status_labels.get(status_code, status_code)
        prospects_by_status_with_labels.append({
            'status': status_code,
            'label': label,
            'count': count
        })
    
    # Si aucune donnée n'est disponible, utiliser des données factices pour test
    if not prospects_by_status_with_labels:
        prospects_by_status_with_labels = [
            {'status': 'visiteur', 'label': 'Visiteur', 'count': 150},
            {'status': 'prinscrit', 'label': 'Pré-inscrit', 'count': 80},
            {'status': 'instance', 'label': 'Instance', 'count': 45},
            {'status': 'convertit', 'label': 'Converti', 'count': 30}
        ]
        total_prospects = 305
    
    context = {
        'tenant': request.tenant,
        'total_prospects': total_prospects,
        'new_prospects_this_week': new_prospects_this_week,
        'pending_reminders': pending_reminders,
        'conversion_rate': round(conversion_rate, 2),
        'recent_reminders': recent_reminders,
        'channel_conversion_data': channel_conversion_data,
        'prospects_by_status': prospects_by_status_with_labels,
    }
    
    return render(request, 'tenant_folder/dashboard/crm_dashboard.html', context)

def rh_dashboard(request):
    pass

def default_dashboard(request):
    pass

@login_required(login_url="institut_app:login")
def Index(request):
    tenant = getattr(request, 'tenant', None)
    # Get the schema name or set it to "Unknown" if no tenant is found
    schema_name = tenant.schema_name if tenant else "Unknown"
    is_crm = request.user.groups.filter(name="CRM").exists()

    if is_crm:
        return crm_dashboard(request)
    else:
        return crm_dashboard(request)

def logout_view(request):
    if request.user.is_authenticated:
        try:
            request.user.session_info.last_session_key = None
            request.user.session_info.save(update_fields=["last_session_key"])
        except UserSession.DoesNotExist:
            pass
        logout(request)
    return redirect('institut_app:login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Vérifier UserSession
            session_info, _ = UserSession.objects.get_or_create(user=user)

            if session_info.last_session_key:
                try:
                    session = Session.objects.get(session_key=session_info.last_session_key)
                    if session.expire_date > timezone.now():
                        request.session["allow_blocked_page"] = True
                        return redirect('institut_app:ShowBlockedConnexion')
                except Session.DoesNotExist:
                    pass

            # Nouvelle connexion
            login(request, user)
            session_info.last_session_key = request.session.session_key
            session_info.save(update_fields=["last_session_key"])

            messages.success(request, f"Bienvenue, {user.username} ! Vous êtes connecté.")
            return redirect('institut_app:index')

        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        new_user = User(
            username=username,
            email=email,
            is_superuser = True,
        )
        new_user.set_password(password1)
        new_user.save()

        messages.success(request, 'Compte créé avec succès')
        return redirect('institut_app:login')
 
    return render(request, 'registration/register.html')


def ShowBlockedConnexion(request):
    if not request.session.get("allow_blocked_page"):
        return redirect("institut_app:index")  
    
    request.session.pop("allow_blocked_page")
    return render(request, "tenant_folder/blocked_connexion.html")

@login_required(login_url='institut_app:login')
@transaction.atomic
def NewEntreprise(request):
    form = EntrepriseForm()
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entreprise créée avec succès')
            return redirect('institut_app:liste_entreprise')
    
    context = {
        'form' : form,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/entreprise/new_entreprise.html',context)

@login_required(login_url='institut_app:login')
def ListeEntreprises(request):
    entreprises = Entreprise.objects.all()
    context = {
        'liste' : entreprises,
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/entreprise/mes_entreprises.html', context)

@login_required(login_url='institut_app:login')
@transaction.atomic
def ModifierEntreprise(request, id):
    entreprise = Entreprise.objects.get(id=id)
    form = EntrepriseForm(instance=entreprise)
    if request.method == 'POST':
        form = EntrepriseForm(request.POST, instance=entreprise)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entreprise modifiée avec succès')
            return redirect('institut_app:liste_entreprise')
    return render(request, 'tenant_folder/entreprise/modifier_entreprise.html', {'form': form})

def ApiUpdateEntreprise(request):
    designation = request.POST.get('designation')
    site_web = request.POST.get('site_web')
    rc = request.POST.get('rc')
    nif = request.POST.get('nif')
    nis = request.POST.get('nis')
    art = request.POST.get('art')
    adresse = request.POST.get('adresse')
    telephone = request.POST.get('telephone')
    
    print(designation)

@login_required(login_url='institut_app:login')
def ApiGetEntrepriseDetails(request):
    id = request.GET.get('id')
    entreprise = Entreprise.objects.filter(id=id).values('id','designation','rc','nif','art','nis','adresse','telephone','wilaya','pays','email','site_web')
    return JsonResponse(list(entreprise), safe=False)

def UsersListePage(request):
    context = {
        'tenant' : request.tenant,
    }
    return render(request, 'tenant_folder/users/liste_users.html', context)

def ApiListeUsers(request):
    users = User.objects.all().values('id','is_staff','email','username','date_joined','is_active')
    return JsonResponse(list(users), safe=False)

def ApiGetDetailsProfile(request):
    id = request.GET.get('id')
    obj = User.objects.get(id = id)
    profile = Profile.objects.filter(user = obj).values('id','adresse','role')

    if profile:
        return JsonResponse(list(profile),safe=False)
    else:
        return JsonResponse({'status' : 'error', 'message' : "Aucun profile trouvé pour l'utilisateur"})
    
def ApiCreateProfile(request):
    id_user= request.POST.get('id_user')
    nom = request.POST.get('nom')
    prenom = request.POST.get('prenom')
    adresse = request.POST.get('adresse')

    user_obj = User.objects.get(id= id_user)

    profile = Profile(
        user = user_obj,
        adresse = adresse
    )
    profile.save()

    user_obj.first_name = nom
    user_obj.last_name = prenom
    user_obj.save()

    return JsonResponse({'status' : 'success', 'message' : "Le profile de l'utilisateur crée avec succès"})

def ApiDeactivateUser(request):
    id = request.GET.get('id')
    if id:
        user = User.objects.get(id = id)
        user.is_active = False
        user.save()

        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-information-line me-2'></i>Désactiver avec succès"})
    else:
        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-shut-down-line'></i>Erreur"})
    
def ApiActivateUser(request):
    id = request.GET.get('id')
    if id:
        user = User.objects.get(id = id)
        user.is_active = True
        user.save()

        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-information-line me-2'></i>Désactiver avec succès"})
    else:
        return JsonResponse({'status' : 'success', 'message' : "<i class='ri-shut-down-line'></i>Le compte utilisateur a été desactiver avec succès"})
    
def ListGroupePage(request):
    return render(request, "tenant_folder/users/groupe_list.html", {'tenant' : request.tenant})

def ApilistGroupe(request):
    liste = CustomGroupe.objects.all().values('id', 'name', 'description', 'created_at')
    return JsonResponse(list(liste), safe=False)
    
def NewCustomGroupe(request):
    form = CustomGroupForm()

    if request.method == "POST":
        form = CustomGroupForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request,"Le groupe a été crée avec succès")
            return redirect('institut_app:ListGroupePage')
        else:
            messages.success(request,"Le groupe a été crée avec succès")
            return redirect('institut_app:ListGroupePage')
            
    context = {
        'form' : form,
    }
    return render(request,'tenant_folder/users/nouveau_groupe.html', context)

def ApiGetGroupFrom(request):
    form = CustomGroupForm()
    form_html = form.as_p()
    return JsonResponse({'form' : form_html})

def ApiGetNewUserForm(request):
    form = CreateNewUserForm()
    html = render_to_string('tenant_folder/users/html/form_create_user.html', {'form': form}, request=request)
    return JsonResponse({'form' : html})

@transaction.atomic
def PageUpdateUserDetails(request, pk):
    obj = User.objects.get(id = pk)
    form = UserUpdateForm(instance=obj)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance = obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Les information de l'utilisateur ont été enregistrer avec succès")
            return redirect('institut_app:PageUpdateUserDetails', pk)
        else:
            messages.error(request, "Une erreur est survenue lors du traitement de la requete")
            return redirect('institut_app:PageUpdateUserDetails', pk)
    else:
        context = {
            'obj' : obj,
            'form' : form,
            'tenant' : request.tenant
        }
        return render(request, 'tenant_folder/users/update_user.html', context)

def ApiSaveUser(request):
    if request.method == "POST":
        form = CreateNewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success' : True, 'message' : "L'utilisateur à été ajouter avec succès"})
        else:
            return JsonResponse({'success' : False, 'message' : "Erreur de traitement du formulaire"})
    else:
        return JsonResponse({"success" : False, 'message' : "Erreur"})

def ApiCheckUsernameDisponibility(request):
    username = request.GET.get('username')
    try:
        obj = User.objects.get(username = username)
        if obj:
            return JsonResponse({'status' : 'success'})
        
    except:
         return JsonResponse({'status' : 'error'})

def ApiGetUpdateGroupForm(request):
    id = request.GET.get('id')
    obj = CustomGroupe.objects.get(id = id)
    form = CustomUpdateGroupForm(instance=obj)
    form_html = form.as_p()
    return JsonResponse({'form' : form_html})

def ApiSaveGroup(request):
    if request.method == 'POST':
        form = CustomGroupForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if obj:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success' : False, "message": "Le rôle  existe déja ! <br>Veuillez attribuer un nom diffents"})
        else:
            return JsonResponse({'success': False,"message": "Le rôle existe déja ! <br>Veuillez attribuer un nom diffents"})

def ApiGetUserDetails(request):
    id = request.GET.get('id')
    try:
        user = User.objects.get(id = id)
        data = {
            'id':user.id,
            'username' : user.username,
            'first_name' : user.first_name,
            'last_name' : user.last_name,
            'email' : user.email,
            'is_active' : user.is_active,
            'last_login' : user.last_login,
            'joined_date' : user.date_joined,
            'groups' : list(user.groups.values('id','name')),
            'permissions' : list(user.user_permissions.values('id','name'))
        }
        return JsonResponse(data, safe=False)
    
    except user.DoesNotExist:

        return JsonResponse({'error' : 'Utilisateur non trouvé'})

def ApiGetGroupeDetails(request):
    id = request.GET.get('id')
    try:
        groupe = CustomGroupe.objects.get(id=id)
        data = {
            'id': groupe.id,
            'name': groupe.name,
            'description': groupe.description,
            'created_at': groupe.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'permissions': list(groupe.permissions.values('id', 'name', 'codename')),
        }
        return JsonResponse(data, safe=False)

    except CustomGroupe.DoesNotExist:
        return JsonResponse({'error': 'Groupe non trouvé'}, status=404)
    
def ApiDeleteGroup(request):
    id = request.GET.get('id')
    obj = CustomGroupe.objects.get(id = id)
    obj.delete()
    return JsonResponse({'status' : 'success' , 'message' : "Le groupe à été supprimé avec succès" })

def GetMyProfile(request):
    try:
        obj = Profile.objects.get(user = request.user)

        context = {
            'obj' : obj,
        }
        return render(request, 'tenant_folder/users/mon-profile.html', context)
    
    except:

        return render(request, 'tenant_folder/users/mon-profile.html')
    
def UpdateMyProfile(request):
    form = ProfileUpdateForm(instance=request.user.profile)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            
            messages.success(request, "Votre profile a été mis à jour avec succès")
            return redirect('institut_app:profile')
        else:
            messages.error(request, "Une erreur est survenue lors de la mise à jour de votre profile")

    context ={
        'form' : form,
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/users/update_profile.html', context)