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


@login_required(login_url='institut_app:login')
def Index(request):
    tenant = getattr(request, 'tenant', None)
    # Get the schema name or set it to "Unknown" if no tenant is found
    schema_name = tenant.schema_name if tenant else "Unknown"
    context = {
        'schema_name' : schema_name,
        'tenant' : tenant,
    }
    return render(request, 'tenant_folder/index.html', context)

def logout_view(request):
    logout(request)
    messages.success(request,'Vous étes maintenant déconnecter')
    return redirect('institut_app:login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} ! Vous êtes connecté.")
            return redirect('institut_app:index')  # Redirigez vers une page de votre choix
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
            
        )
        new_user.set_password(password1)
        new_user.save()

        messages.success(request, 'Compte créé avec succès')
        return redirect('institut_app:login')
 
    return render(request, 'registration/register.html')

@login_required(login_url='institut_app:login')
@transaction.atomic
def NewEntreprise(request):
    form = EntrepriseForm()
    if request.method == 'POST':
        form = EntrepriseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entreprise créée avec succès')
            return redirect('institut_app:index')
    
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

@login_required(login_url='institut_app:login')
def detailsEntreprise(request, pk):
    entreprise = Entreprise.objects.get(id=pk)
    updateForm = EntrepriseForm(instance=entreprise)
    if request.method == "POST":
        updateForm = EntrepriseForm(request.POST, instance=entreprise)
        if updateForm.is_valid():
            updateForm.save()
            messages.success(request, "Les informations ont été modifier avec succès")
            return redirect("institut_app:details_entreprise", pk)
    context = {
        'entreprise' : entreprise,
        'tenant' : request.tenant,
        'updateForm' : updateForm,
    }
    return render(request, 'tenant_folder/entreprise/details_entreprise.html', context)

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