from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .form import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django_tenants.utils import schema_context
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login



def Index(request):
    tenants = Institut.objects.exclude(schema_name='public')
    
    if request.method == 'POST':
        tenant_slug = request.POST.get('tenant_slug')
        return redirect_to_tenant(request, tenant_slug)
    
    context = {
        'tenants': tenants
    }
    return render(request, 'public_folder/organisation_select.html', context)

def redirect_to_tenant(request, tenant_slug):
    try:
        tenant = Institut.objects.get(nom=tenant_slug)
        domain = Domaine.objects.filter(tenant=tenant, is_primary=True).first()
        
        if domain:
            # Construire l'URL du tenant
            scheme = 'https' if request.is_secure() else 'http'
            tenant_url = f"{scheme}://{domain.domain}"
            
            # Pour le développement local avec port
            if 'localhost' in request.get_host():
                port = request.get_host().split(':')[1] if ':' in request.get_host() else '8000'
                tenant_url = f"{scheme}://{tenant.nom}.localhost:{port}"
            return redirect(tenant_url)
    except Institut.DoesNotExist:
        pass
    
    return redirect('tenant_selection')

def new_tenant(request):
    form = NewTenantForm()
    userForm = NewUser()

    if request.method == 'POST':
        form = NewTenantForm(request.POST)
        userForm = NewUser(request.POST)
        if form.is_valid() and userForm.is_valid():

            nom = form.cleaned_data.get('nom')
            adresse = form.cleaned_data.get('adresse')
            telephone = form.cleaned_data.get('telephone')

            username = userForm.cleaned_data.get('username')
            email = userForm.cleaned_data.get('email')
            password = userForm.cleaned_data.get('password')

            current_site = get_current_site(request)
            domain_name = current_site.domain.split(':')[0]

            tenant = Institut(
                schema_name = nom,
                nom = nom,
                telephone = telephone,
                adresse = adresse,
                tenant_type = 'second',

            )
            tenant.save()

            domain = Domaine(domain=f"{tenant.schema_name}.{domain_name}", tenant=tenant, is_primary=True)
            domain.save()
           
            with schema_context(tenant.schema_name):
                # Create default user
                default_user = User.objects.create_superuser(

                    username=username,
                    email=email,
                    password=password

                )
                default_user.save()

            messages.success(request,'Le compte à été crée avec succès')

            return redirect('index')
        

    context = {
        'form' : form,
        'userForm' : userForm,
    }
    return render(request, 'public_folder/new_tenant.html', context)

def tenant_list(request):
    list = Institut.objects.all()
    return render(request,'public_folder/list_tenant.html',{'list' : list})

def CreateSuperUser(request):
    form = NewUser()
    if request.method == 'POST':
        form = NewUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            
            tenant = getattr(request, 'tenant', None)
            with schema_context(tenant.schema_name):
                user = User.objects.create_superuser(
                    username = username,
                    email = email,
                    password = password
                )

                user.save()

                
            messages.success(request, "L'utilisateur à été crée avec succès")
            return redirect('index')
    else:

        context = {
            'form' : form,
        }
        return render(request,'public_folder/new_user.html', context)
    
def logout_view(request):
    logout(request)
    messages.success(request,'Vous étes maintenant déconnecter')
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username} ! Vous êtes connecté.")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            elif 'next' in request.GET:
                return redirect(request.GET.get('next'))
            
            if request.tenant.schema_name == 'public':
                return redirect('configuration_index')
            return redirect('index') 
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    
    return render(request, 'registration/login.html')

def profile(request):
    pass

def NombreLead(request):
    return render(request, 'public_folder/marketing/nombres_leads.html')

def socialEngagement(request):
    return render(request, 'public_folder/marketing/social_engagment.html')

from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string

@login_required
def tenant_comm_hub(request):
    # Existing code for tenant_comm_hub...
    # (Checking if I need to re-read it to not delete it. The user only asked for tenant_comm_detail changes mostly, but let's be safe.
    # Actually wait, replace_file_content replaces a block. I should only replace the imports and tenant_comm_detail logic.)
    # Since existing imports are at top, let me just add the new imports to the top first, then replace the view function.
    pass

# I will do this in two steps to be safe. 
# Step 1: Update imports
# Step 2: Update tenant_comm_detail
# Wait, I can do it in one go if I identify the block correctly. 
# The imports are at the top. tenant_comm_detail starts around line 190.
# Let's just create a new tool call to update imports first.

    current_tenant = request.tenant
    
    # If Master, show list of sub-tenants
    if current_tenant.tenant_type == 'master':
        tenants_list = Institut.objects.filter(tenant_type='second')
    # If Second, show list of Master tenants
    else:
        tenants_list = Institut.objects.filter(tenant_type='master')

    return render(request, 'tenant_folder/communication/inter_tenant_hub.html', {
        'tenants_list': tenants_list,
        'is_master': current_tenant.tenant_type == 'master'
    })

from django.http import JsonResponse

@login_required
@login_required
def tenant_comm_detail(request, tenant_id):
    current_tenant = request.tenant
    target_tenant = get_object_or_404(Institut, id=tenant_id)
    
    # Security check: Second tenant can only talk to Master
    if current_tenant.tenant_type == 'second' and target_tenant.tenant_type != 'master':
        messages.error(request, "Vous ne pouvez communiquer qu'avec le compte maître.")
        return redirect('institut_app:index')

    # Determine current folder ID from GET (nav) or POST (action parent)
    current_folder_id = request.GET.get('folder_id') or request.POST.get('parent_id')
    current_folder = None
    if current_folder_id and current_folder_id != 'null':
        current_folder = get_object_or_404(TenantFolder, id=current_folder_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        # 1. Send Message
        if action == 'send_message':
            message_content = request.POST.get('message')
            if message_content:
                msg = TenantMessage.objects.create(
                    sender=current_tenant,
                    receiver=target_tenant,
                    message=message_content
                )
                
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'status': 'success',
                        'message': msg.message,
                        'created_at': msg.created_at.strftime("%H:%M"),
                        'sender_id': msg.sender.id,
                        'is_me': True
                    })

        # 2. Create Folder
        elif action == 'create_folder':
            folder_name = request.POST.get('folder_name')
            if folder_name:
                TenantFolder.objects.create(
                    sender=current_tenant,
                    receiver=target_tenant,
                    name=folder_name,
                    parent=current_folder
                )
        
        # 3. Upload File
        elif action == 'upload_file':
            uploaded_file = request.FILES.get('file')
            if uploaded_file:
                TenantDocument.objects.create(
                    sender=current_tenant,
                    receiver=target_tenant,
                    file=uploaded_file,
                    description=uploaded_file.name,
                    folder=current_folder
                )

        # 4. Delete Folder
        elif action == 'delete_folder':
            folder_id = request.POST.get('item_id')
            if folder_id:
                folder = get_object_or_404(TenantFolder, id=folder_id)
                # Security: Only verify sender match
                if folder.sender == current_tenant:
                    folder.delete()

        # 5. Delete File
        elif action == 'delete_file':
            file_id = request.POST.get('item_id')
            if file_id:
                doc = get_object_or_404(TenantDocument, id=file_id)
                # Security: Only verify sender match
                if doc.sender == current_tenant:
                    doc.delete()

        # If it's not an AJAX request, redirect to avoid resubmission
        if request.headers.get('x-requested-with') != 'XMLHttpRequest':
            redirect_url = reverse('tenant_comm_detail', args=[tenant_id])
            if current_folder_id:
                redirect_url += f'?folder_id={current_folder_id}'
            return redirect(redirect_url)

    # --- Fetch Data for Context ---

    # Fetch shared folders (current level)
    folders = TenantFolder.objects.filter(
        (Q(sender=current_tenant) & Q(receiver=target_tenant)) |
        (Q(sender=target_tenant) & Q(receiver=current_tenant)),
        parent=current_folder
    ).order_by('-created_at')

    # Fetch shared documents (current level)
    documents = TenantDocument.objects.filter(
        (Q(sender=current_tenant) & Q(receiver=target_tenant)) |
        (Q(sender=target_tenant) & Q(receiver=current_tenant)),
        folder=current_folder
    ).order_by('-created_at')

    # Fetch messages
    messages_list = TenantMessage.objects.filter(
        (Q(sender=current_tenant) & Q(receiver=target_tenant)) |
        (Q(sender=target_tenant) & Q(receiver=current_tenant))
    ).order_by('created_at')
    
    # Mark incoming messages as read
    TenantMessage.objects.filter(sender=target_tenant, receiver=current_tenant, is_read=False).update(is_read=True)

    # If Master, we want the list of Seconds. If Second, we want list of Masters.
    if current_tenant.tenant_type == 'master':
        tenants_list = Institut.objects.filter(tenant_type='second')
    else:
        tenants_list = Institut.objects.filter(tenant_type='master')

    context = {
        'target_tenant': target_tenant,
        'messages_list': messages_list,
        'folders': folders,
        'documents': documents,
        'is_master': current_tenant.tenant_type == 'master',
        'tenants_list': tenants_list,
        'current_folder': current_folder,
    }

    # Handle AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Scenario A: Sidebar Update (Folder Nav / Create Folder / Upload File)
        # We detect this if we are in a sub-folder OR if it was a POST action (which implies staying in context)
        # Actually, let's simplify:
        # If GET and folder_id param exists (even empty string): Sidebar Update
        # If POST: Sidebar Update (because we return JSON for success toast + sidebar refresh)
        # If GET and NO folder_id param: Full Chat Update (Switching Tenant)
        
        is_sidebar_update = False
        if request.method == 'POST':
            is_sidebar_update = True
        elif 'folder_id' in request.GET:
            is_sidebar_update = True
            
        if is_sidebar_update:
            html = render_to_string('tenant_folder/communication/partials/sidebar_content.html', {
                'folders': folders,
                'documents': documents,
                'current_folder': current_folder
            }, request=request)
            return JsonResponse({
                'status': 'success', 
                'html': html,
                'current_folder_id': current_folder.id if current_folder else ''
            })
        else:
            # Full Chat Update (Switching Tenant)
            html = render_to_string('tenant_folder/communication/partials/main_chat.html', context, request=request)
            return JsonResponse({'status': 'success', 'html': html, 'type': 'full_chat'})

    # --- Full Page Render ---
    return render(request, 'tenant_folder/communication/inter_tenant_hub.html', context)
