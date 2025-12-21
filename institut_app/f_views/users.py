from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
import json

User = get_user_model()

@login_required(login_url="institut_app:login")
def liste_users(request):
    return render(request, 'tenant_folder/users/liste_users.html')

@login_required(login_url="institut_app:login")
def ApiListeUtilisateurs(request):
    if request.method == "GET":
        try:
            # Get all users
            users = User.objects.all()
            
            user_data = []
            for user in users:
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
                })
            
            return JsonResponse(list(user_data), safe=False)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
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