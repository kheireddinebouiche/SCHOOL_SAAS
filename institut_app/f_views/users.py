from institut_app.decorators import superuser_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login
from django.contrib import messages
from django.db import transaction
from datetime import datetime
import json
from ..models import UserSession, UserDeviceLog

User = get_user_model()

@login_required(login_url="institut_app:login")
@superuser_required
def liste_users(request):
    return render(request, 'tenant_folder/users/liste_users.html')

@login_required(login_url="institut_app:login")
@superuser_required
def ApiListeUtilisateurs(request):
    if request.method == "GET":
        try:
            # Get all users with session info
            users = User.objects.all()
            
            user_data = []
            for user in users:
                session_info, _ = UserSession.objects.get_or_create(user=user)
                from ..models import PasswordResetRequest
                has_pending_reset = PasswordResetRequest.objects.filter(user=user, is_active=True).exists()
                
                user_data.append({
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else '',
                    'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '',
                    'is_superuser': user.is_superuser,
                    'is_device_lock_enabled': session_info.is_device_lock_enabled,
                    'has_pending_reset': has_pending_reset,
                })
            
            return JsonResponse(list(user_data), safe=False)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
@superuser_required
def ApiShowUserDetails(request):
    if request.method == "GET":
        user_id = request.GET.get('id')
        
        if not user_id:
            return JsonResponse({"status": "error", "message": "User ID is required"})
        
        try:
            user = User.objects.get(id=user_id)
            
            user_details = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
                'is_active': user.is_active,
                'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else '',
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '',
                'is_superuser': user.is_superuser,
            }
            
            return JsonResponse({"status": "success", "user": user_details})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiUpdateUser(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_staff = request.POST.get('is_staff')
        is_active = request.POST.get('is_active')
        is_superuser = request.POST.get('is_superuser')
        
        if not user_id:
            return JsonResponse({"status": "error", "message": "User ID is required"})
        
        try:
            user = User.objects.get(id=user_id)
            
            # Update user fields
            if username:
                user.username = username
            if email:
                user.email = email
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if is_staff is not None:
                user.is_staff = is_staff in ['1', 'true', 'True', True, 'on']
            if is_active is not None:
                user.is_active = is_active in ['1', 'true', 'True', True, 'on']
            if is_superuser is not None:
                user.is_superuser = is_superuser in ['1', 'true', 'True', True, 'on']
            
            user.save()
            
            return JsonResponse({"status": "success", "message": "User updated successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiDeleteUser(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        
        if not user_id:
            return JsonResponse({"status": "error", "message": "User ID is required"})
        
        try:
            user = User.objects.get(id=user_id)
            
            # Check if user is superuser to prevent accidental deletion
            if user.is_superuser:
                return JsonResponse({"status": "error", "message": "Cannot delete superuser account"})
            
            user.delete()
            
            return JsonResponse({"status": "success", "message": "User deleted successfully"})
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiChangeUserStatus(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        is_active = request.POST.get('is_active')

        if not user_id:
            return JsonResponse({"status": "error", "message": "User ID is required"})

        if is_active is None:
            return JsonResponse({"status": "error", "message": "Status is required"})

        try:
            user = User.objects.get(id=user_id)

            # Convert to boolean
            new_status = is_active in ['1', 'true', 'True', True, 'on']
            user.is_active = new_status
            user.save()

            status_text = "activé" if new_status else "désactivé"

            return JsonResponse({
                "status": "success",
                "message": f"Compte utilisateur {status_text} avec succès",
                "new_status": new_status
            })
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiCreateUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        is_staff = request.POST.get('is_staff')
        is_active = request.POST.get('is_active')

        # Validation
        if not username or not email or not password:
            return JsonResponse({"status": "error", "message": "Username, email, and password are required"})

        if len(password) < 8:
            return JsonResponse({"status": "error", "message": "Password must be at least 8 characters long"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"status": "error", "message": "Username already exists"})

        if User.objects.filter(email=email).exists():
            return JsonResponse({"status": "error", "message": "Email already exists"})

        try:
            # Create the new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name or '',
                last_name=last_name or '',
                is_staff=is_staff in ['1', 'true', 'True', True, 'on'],
                is_active=is_active in ['1', 'true', 'True', True, 'on']
            )

            # Initialize profile
            from ..models import Profile
            from django.utils import timezone
            Profile.objects.create(
                user=user,
                last_password_change=timezone.now()
            )

            return JsonResponse({
                "status": "success",
                "message": "Utilisateur créé avec succès",
                "user_id": user.id
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiChangeUserPassword(request):
    if request.method == "POST":
        user_id = request.POST.get('id')
        new_password = request.POST.get('password')

        if not user_id:
            return JsonResponse({"status": "error", "message": "User ID is required"})

        if not new_password:
            return JsonResponse({"status": "error", "message": "Password is required"})

        if len(new_password) < 8:
            return JsonResponse({"status": "error", "message": "Password must be at least 8 characters long"})

        try:
            user = User.objects.get(id=user_id)

            # Set the new password
            user.set_password(new_password)
            user.save()

            # Update last_password_change in profile
            from ..models import Profile
            from django.utils import timezone
            profile, created = Profile.objects.get_or_create(user=user)
            profile.last_password_change = timezone.now()
            profile.save()

            # Mark password reset requests as handled
            from ..models import PasswordResetRequest
            PasswordResetRequest.objects.filter(user=user, is_active=True).update(
                is_active=False, 
                handled_at=timezone.now(),
                handled_by=request.user
            )

            return JsonResponse({
                "status": "success",
                "message": "Mot de passe changé avec succès"
            })
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiResetDeviceLock(request):
    """
    Réinitialise le verrouillage de l'appareil pour un utilisateur.
    Permet à l'utilisateur de se connecter depuis un nouvel appareil.
    """
    if request.method == "POST":
        user_id = request.POST.get('id')
        if not user_id:
            return JsonResponse({"status": "error", "message": "ID utilisateur requis"})
        
        try:
            session_info, created = UserSession.objects.get_or_create(user_id=user_id)
            session_info.device_uuid = None
            session_info.last_session_key = None # On force aussi la déconnexion
            session_info.save()
            
            return JsonResponse({
                "status": "success", 
                "message": "Le verrouillage de l'appareil a été réinitialisé. L'utilisateur peut maintenant se connecter sur un nouveau poste."
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
@superuser_required
def DeviceManagementPage(request):
    """
    Page affichant l'historique des appareils et des connexions.
    """
    
    # On récupère tous les logs avec les infos utilisateur
    logs = UserDeviceLog.objects.select_related('user').all()
    
    # Statistiques rapides
    total_logs = logs.count()
    unique_devices = UserDeviceLog.objects.values('device_uuid').distinct().count()
    
    context = {
        'logs': logs,
        'total_logs': total_logs,
        'unique_devices': unique_devices,
        'page_title': "Historique des Appareils"
    }
    return render(request, 'tenant_folder/users/device_management.html', context)

@login_required(login_url="institut_app:login")
@superuser_required
def ApiToggleDeviceLock(request):
    """
    Active ou désactive le verrouillage par appareil pour un utilisateur.
    """
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            session_info, _ = UserSession.objects.get_or_create(user=user)
            
            # Basculer l'état
            session_info.is_device_lock_enabled = not session_info.is_device_lock_enabled
            session_info.save()
            
            status_text = "activé" if session_info.is_device_lock_enabled else "désactivé"
            return JsonResponse({
                "status": "success", 
                "message": f"Le verrouillage par appareil a été {status_text} pour {user.username}.",
                "is_enabled": session_info.is_device_lock_enabled
            })
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Utilisateur introuvable."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})

@login_required(login_url="institut_app:login")
@superuser_required
def LoginAsUser(request, user_id):
    if not request.user.is_superuser:
        messages.error(request, "Permission refusée.")
        return redirect('institut_app:UsersListePage')
    
    target_user = get_object_or_404(User, id=user_id)
    original_user_id = request.user.id
    
    # login flushes session, so set variable after login
    login(request, target_user, backend='django.contrib.auth.backends.ModelBackend')
    request.session['impersonator_id'] = original_user_id
    
    messages.success(request, f"Vous êtes maintenant connecté(e) en tant que {target_user.username}.")
    return redirect('institut_app:index')

@login_required(login_url="institut_app:login")
def RestoreOriginalUser(request):
    impersonator_id = request.session.get('impersonator_id')
    if impersonator_id:
        try:
            impersonator = User.objects.get(id=impersonator_id)
            login(request, impersonator, backend='django.contrib.auth.backends.ModelBackend')
            if 'impersonator_id' in request.session:
                del request.session['impersonator_id']
            messages.success(request, f"De retour sur votre compte administrateur ({impersonator.username}).")
        except User.DoesNotExist:
            messages.error(request, "Impossible de retrouver le compte d'origine.")
    else:
        messages.info(request, "Aucune session d'origine trouvée.")
    return redirect('institut_app:index')

@login_required(login_url="institut_app:login")
@superuser_required
def ApiGetSubMenuAccess(request):
    user_id = request.GET.get('id')
    module_code = request.GET.get('module_code', 'tre')
    
    if not user_id:
        return JsonResponse({"status": "error", "message": "ID utilisateur requis"})
        
    try:
        from institut_app.models import UserSubMenuAccess
        target_user = User.objects.get(id=user_id)
        accesses = UserSubMenuAccess.objects.filter(user=target_user, module_code=module_code)
        
        data = {acc.submenu_code: acc.is_active for acc in accesses}
        return JsonResponse({"status": "success", "data": data})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiToggleSubMenuAccess(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        user_id = data.get('id')
        module_code = data.get('module_code', 'tre')
        submenu_code = data.get('submenu_code')
        is_active = data.get('is_active')
        
        if not user_id or not submenu_code:
            return JsonResponse({"status": "error", "message": "Données incomplètes"})
            
        try:
            from institut_app.models import UserSubMenuAccess
            target_user = User.objects.get(id=user_id)
            access, created = UserSubMenuAccess.objects.get_or_create(
                user=target_user, 
                module_code=module_code, 
                submenu_code=submenu_code
            )
            access.is_active = is_active
            access.save()
            
            return JsonResponse({"status": "success", "message": "Paramètre mis à jour"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée"})