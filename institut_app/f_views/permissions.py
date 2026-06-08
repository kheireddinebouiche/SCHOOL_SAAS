from institut_app.decorators import superuser_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from ..models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required(login_url="institut_app:login")
@superuser_required
def ModulesPages(request):
    return render(request, 'tenant_folder/administration/permissions/modules.html')


@login_required(login_url="institut_app:login")
@superuser_required
def Role_Attribution(request):
    return render(request,"tenant_folder/administration/permissions/attribution_des_roles.html")

@login_required(login_url="institut_app:login")
@superuser_required
def ApiListeModules(request):
    if request.method == "GET":
        
        liste = Module.objects.all()
        data = []
        for i in liste:
            data.append({
                'id' : i.id,
                'name' : i.name,  # This is the code value (crm, ped, etc.)
                'name_display' : i.get_name_display(),  # This is the display value (CRM, Pédagogie, etc.)
                'description' : i.description,
                'is_active' : i.is_active,
                'created_at' : i.created_at,
                'updated_at' : i.updated_at,
            })

        return JsonResponse(list(data), safe=False)
    else:

        return JsonResponse({"status" : "error"})
    

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiAddModule(request):
    if request.method == "POST":
        addModuleName = request.POST.get('addModuleName')
        addModuleStatus = request.POST.get('addModuleStatus')
        addModuleDescription = request.POST.get('addModuleDescription')

        if not addModuleDescription or not addModuleStatus  or not addModuleName:
            return JsonResponse({"status":"error",'message':"Informations manquantes"})
        
        try:
            Module.objects.create(
                name=addModuleName,
                description = addModuleDescription,
                is_active = addModuleStatus,
            )

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='Module',
                details=f"Création du module {addModuleName}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({"status":"success",'message':"Le module a été crée avec succès"})

        except Exception as e:
            return JsonResponse({"status":"error","message":str(e)})

    else:
        return JsonResponse({"status":"error"})


@login_required(login_url='institut_app:login')
@superuser_required
def ApiListeRoles(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        data = []
        for role in roles:
            data.append({
                'id': role.id,
                'name': role.name,
                'level': role.level,
                'level_label' : role.get_level_display(),
                'description': role.description,
                'is_active': role.is_active,
                'created_at': role.created_at.strftime('%Y-%m-%d %H:%M:%S') if role.created_at else '',
                'updated_at': role.updated_at.strftime('%Y-%m-%d %H:%M:%S') if role.updated_at else '',
            })

        return JsonResponse(list(data), safe=False)
    else:
        return JsonResponse({'status': 'error'})


@login_required(login_url='institut_app:login')
@transaction.atomic
@superuser_required
def ApiAddRole(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        level = request.POST.get('level')
        is_active = request.POST.get('is_active')
        description = request.POST.get('description')

        if not name or level is None:
            return JsonResponse({'status':'error', 'message':'Le nom et le niveau sont requis'})

        try:
            # Vérifier si un rôle avec le même nom existe déjà
            if Role.objects.filter(name=name).exists():
                return JsonResponse({'status':'error', 'message': 'Un rôle avec ce nom existe déjà'})

            role = Role.objects.create(
                name=name,
                level=level,
                description=description or '',
                is_active=is_active in ['1', 'true', 'True', True, 'on']
            )

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='Role',
                target_id=str(role.id),
                details=f"Création du rôle {name}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({'status':'success', 'message':'Le rôle a été créé avec succès'})

        except ValueError:
            return JsonResponse({'status':'error', 'message': 'Le niveau doit être un nombre valide'})
        except Exception as e:
            return JsonResponse({'status':'error', 'message': str(e)})

    else:
        return JsonResponse({'status':'error'})


@login_required(login_url='institut_app:login')
@transaction.atomic
@superuser_required
def ApiUpdateRole(request):
    if request.method == 'POST':
        role_id = request.POST.get('id')
        name = request.POST.get('name')
        level = request.POST.get('level')
        is_active = request.POST.get('is_active')
        description = request.POST.get('description')

        if not role_id:
            return JsonResponse({'status':'error', 'message':'ID du rôle manquant'})

        try:
            role = Role.objects.get(id=role_id)

            if name:
                role.name = name
            if level:
                role.level = int(level)
            if is_active is not None:
                role.is_active = is_active in ['1', 'true', 'True', True, 'on']
            if description is not None:
                role.description = description

            role.save()

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='Role',
                target_id=str(role.id),
                details=f"Mise à jour du rôle {role.name}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({'status':'success', 'message':'Le rôle a été mis à jour avec succès'})

        except Role.DoesNotExist:
            return JsonResponse({'status':'error', 'message': 'Rôle non trouvé'})
        except ValueError:
            return JsonResponse({'status':'error', 'message': 'Le niveau doit être un nombre valide'})
        except Exception as e:
            return JsonResponse({'status':'error', 'message': str(e)})

    else:
        return JsonResponse({'status':'error'})


@login_required(login_url='institut_app:login')
@superuser_required
def ApiGetRoleDetails(request):
    role_id = request.GET.get('id')

    if not role_id:
        return JsonResponse({'status': 'error', 'message': 'ID du rôle manquant'})

    try:
        role = Role.objects.get(id=role_id)

        data = {
            'id': role.id,
            'name': role.name,
            'level': role.level,
            'description': role.description,
            'is_active': role.is_active,
            'created_at': role.created_at.strftime('%Y-%m-%d %H:%M:%S') if role.created_at else '',
            'updated_at': role.updated_at.strftime('%Y-%m-%d %H:%M:%S') if role.updated_at else '',
        }

        return JsonResponse(data, safe=False)

    except Role.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Rôle non trouvé'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required(login_url='institut_app:login')
@transaction.atomic
@superuser_required
def ApiDeleteRole(request):
    if request.method == 'POST':
        role_id = request.POST.get('id')

        if not role_id:
            return JsonResponse({'status':'error', 'message':'ID du rôle manquant'})

        try:
            role = Role.objects.get(id=role_id)

            # Vérifier si le rôle est actif
            if role.is_active:
                return JsonResponse({
                    'status':'error',
                    'message': 'Impossible de supprimer un rôle actif. Veuillez désactiver le rôle avant de le supprimer.'
                })

            role_name = role.name
            role.delete()

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='DELETE',
                target_model='Role',
                target_id=str(role_id),
                details=f"Suppression du rôle {role_name}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({'status':'success', 'message':'Le rôle a été supprimé avec succès'})

        except Role.DoesNotExist:
            return JsonResponse({'status':'error', 'message': 'Rôle non trouvé'})
        except Exception as e:
            return JsonResponse({'status':'error', 'message': str(e)})

    else:
        return JsonResponse({'status':'error'})


@login_required(login_url='institut_app:login')
@superuser_required
def ApiChangeRoleStatus(request):
    if request.method == 'POST':
        role_id = request.POST.get('id')
        is_active = request.POST.get('is_active')

        if not role_id:
            return JsonResponse({'status': 'error', 'message': 'ID du rôle manquant'})

        if is_active is None:
            return JsonResponse({'status': 'error', 'message': 'Statut du rôle manquant'})

        try:
            role = Role.objects.get(id=role_id)
            # Convertir correctement en booléen
            new_status = is_active in ['1', 'true', 'True', True, 'on']
            role.is_active = new_status
            role.save()

            # Déterminer le texte de statut pour la réponse
            status_text = 'activé' if new_status else 'désactivé'

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='Role',
                target_id=str(role.id),
                details=f"Statut {status_text} pour le rôle {role.name}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Le rôle a été {status_text} avec succès',
                'new_status': new_status
            })

        except Role.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Rôle non trouvé'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


# View functions for the roles page

@login_required(login_url='institut_app:login')
@superuser_required
def roles_page(request):
    """Page de gestion des rôles"""
    roles = Role.objects.all()
    context = {
        'titre': 'Gestion des Rôles',
        'roles': roles,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/administration/permissions/roles.html', context)


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiUpdateModule(request):
    if request.method == "POST":
        module_id = request.POST.get('id')
        name = request.POST.get('name')
        is_active = request.POST.get('is_active')
        description = request.POST.get('description')

        if not module_id:
            return JsonResponse({"status":"error", 'message':"ID du module manquant"})

        try:
            module = Module.objects.get(id=module_id)

            if name:
                module.name = name

            if is_active is not None:
                module.is_active = is_active in ['1', 'true', 'True', True, 'on']

            if description is not None:
                module.description = description

            module.save()

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='Module',
                target_id=str(module.id),
                details=f"Mise à jour du module {module.name}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({"status":"success", 'message':"Le module a été mis à jour avec succès"})

        except Module.DoesNotExist:
            return JsonResponse({"status":"error", "message": "Module non trouvé"})
        except Exception as e:
            return JsonResponse({"status":"error", "message": str(e)})

    else:
        return JsonResponse({"status":"error"})


@login_required(login_url="institut_app:login")
@superuser_required
def ApiGetModuleDetails(request):
    module_id = request.GET.get('id')

    if not module_id:
        return JsonResponse({"status": "error", "message": "ID du module manquant"})

    try:
        module = Module.objects.get(id=module_id)

        # Return the raw values instead of display values for editing
        data = {
            'id': module.id,
            'name': module.name,  # This returns the actual code value (crm, ped, etc.)
            'description': module.description,
            'is_active': module.is_active,
            'created_at': module.created_at,
            'updated_at': module.updated_at,
        }

        return JsonResponse(data, safe=False)

    except Module.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Module non trouvé"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@superuser_required
def ApiChangeModuleStatus(request):
    if request.method == "POST":
        module_id = request.POST.get('id')
        is_active = request.POST.get('is_active')

        if not module_id:
            return JsonResponse({"status": "error", "message": "ID du module manquant"})

        if is_active is None:
            return JsonResponse({"status": "error", "message": "Statut du module manquant"})

        try:
            module = Module.objects.get(id=module_id)
            # Convert to boolean properly
            new_status = is_active in ['1', 'true', 'True', True, 'on']
            module.is_active = new_status
            module.save()

            # Determine the status text for the response
            status_text = "activé" if new_status else "désactivé"

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='Module',
                target_id=str(module.id),
                details=f"Statut {status_text} pour le module {module.name}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({
                "status": "success",
                "message": f"Le module a été {status_text} avec succès",
                "new_status": new_status
            })

        except Module.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Module non trouvé"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    else:
        return JsonResponse({"status": "error", "message": "Méthode non autorisée"})


@login_required(login_url="institut_app:login")
@superuser_required
def ApiGetModulePermissions(request):
    module_id = request.GET.get('module_id')

    if not module_id:
        return JsonResponse({"status": "error", "message": "ID du module manquant"})

    try:
        module = Module.objects.get(id=module_id)

        # Récupérer toutes les permissions du module
        module_permissions = ModulePermission.objects.filter(module=module).select_related('module')

        permissions_data = []
        for mp in module_permissions:
            # Vérifier s'il y a des rôles qui ont cette permission (via RolePermission)
            is_granted = mp.roles.exists()  # Utilise la relation 'roles' définie dans le modèle ModulePermission

            permissions_data.append({
                'id': mp.id,
                'name': mp.get_permission_type_display(),  # Affiche le label de la permission
                'code': f"{mp.module.name}_{mp.permission_type}",  # Code de la permission
                'description': mp.description,
                'permission_type': mp.permission_type,
                'is_granted': is_granted
            })

        return JsonResponse({
            "status": "success",
            "permissions": permissions_data
        }, safe=False)

    except Module.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Module non trouvé"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@superuser_required
def ApiAddModulePermission(request):
    if request.method == "POST":
        module_id = request.POST.get('module_id')
        permission_type = request.POST.get('permission_type')
        description = request.POST.get('description', '')

        if not module_id:
            return JsonResponse({"status": "error", "message": "ID du module manquant"})

        if not permission_type:
            return JsonResponse({"status": "error", "message": "Type de permission manquant"})

        try:
            module = Module.objects.get(id=module_id)

            # Vérifier si cette combinaison module/permission_type existe déjà
            existing_permission = ModulePermission.objects.filter(
                module=module,
                permission_type=permission_type
            ).first()

            if existing_permission:
                return JsonResponse({
                    "status": "error",
                    "message": "Cette permission existe déjà pour ce module"
                })

            # Créer la nouvelle permission
            new_permission = ModulePermission.objects.create(
                module=module,
                permission_type=permission_type,
                description=description
            )

            return JsonResponse({
                "status": "success",
                "message": "Permission ajoutée avec succès",
                "permission_id": new_permission.id,
                "permission_name": new_permission.get_permission_type_display(),
                "permission_code": f"{module.name}_{permission_type}"
            })

        except Module.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Module non trouvé"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiUpdateModulePermission(request):
    if request.method == "POST":
        permission_id = request.POST.get('permission_id')
        permission_type = request.POST.get('permission_type')
        description = request.POST.get('description', '')
        is_granted = request.POST.get('is_granted', 'false') == 'true' or request.POST.get('is_granted') == '1' or request.POST.get('is_granted') == True

        if not permission_id:
            return JsonResponse({"status": "error", "message": "ID de la permission manquant"})

        if not permission_type:
            return JsonResponse({"status": "error", "message": "Type de permission manquant"})

        try:
            module_permission = ModulePermission.objects.get(id=permission_id)

            # Mettre à jour les champs de base
            module_permission.permission_type = permission_type
            module_permission.description = description
            module_permission.save()

            # Gérer l'état d'attribution de la permission (accordée ou révoquée)
            module = module_permission.module
            if is_granted:
                # Si la permission doit être accordée, créer les relations RolePermission pour les rôles du module
                user_module_roles = UserModuleRole.objects.filter(module=module).select_related('role')
                roles_for_module = set([umr.role for umr in user_module_roles])

                # Pour chaque rôle avec accès au module, s'assurer qu'il a la permission
                for role in roles_for_module:
                    RolePermission.objects.get_or_create(
                        role=role,
                        module_permission=module_permission
                    )
            else:
                # Si la permission doit être révoquée, supprimer les relations RolePermission pour cette permission
                RolePermission.objects.filter(module_permission=module_permission).delete()

            return JsonResponse({
                "status": "success",
                "message": "Permission mise à jour avec succès"
            })

        except ModulePermission.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Permission non trouvée"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiDeleteModulePermission(request):
    if request.method == "POST":
        permission_id = request.POST.get('permission_id')

        if not permission_id:
            return JsonResponse({"status": "error", "message": "ID de la permission manquant"})

        try:
            module_permission = ModulePermission.objects.get(id=permission_id)

            # Supprimer toutes les relations RolePermission pour cette permission
            RolePermission.objects.filter(module_permission=module_permission).delete()

            # Supprimer la permission
            module_permission.delete()

            return JsonResponse({
                "status": "success",
                "message": "Permission supprimée avec succès"
            })

        except ModulePermission.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Permission non trouvée"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@superuser_required
def ApiGetRolePermissions(request):
    role_id = request.GET.get('role_id')

    if not role_id:
        return JsonResponse({"status": "error", "message": "ID du rôle manquant"})

    try:
        role = Role.objects.get(id=role_id)

        # Récupérer TOUTES les permissions de module existantes
        all_module_permissions = ModulePermission.objects.select_related('module').all()
        
        # Récupérer les IDs des permissions déjà attribuées à ce rôle
        granted_permission_ids = set(RolePermission.objects.filter(role=role).values_list('module_permission_id', flat=True))

        permissions_data = []
        for mp in all_module_permissions:
            permissions_data.append({
                'id': mp.id,
                'module_permission_id': mp.id,
                'module_code': mp.module.name,  # Raw code (e.g. 'crm')
                'module_name': mp.module.get_name_display(), # Display name
                'permission_name': mp.get_permission_type_display(),
                'permission_type': mp.permission_type,
                'is_granted': mp.id in granted_permission_ids
            })

        return JsonResponse({
            "status": "success",
            "permissions": permissions_data
        }, safe=False)

    except Role.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Rôle non trouvé"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiSaveRolePermissions(request):
    if request.method == "POST":
        role_id = request.POST.get('role_id')
        permissions_data = request.POST.get('permissions_data')

        if not role_id:
            return JsonResponse({"status": "error", "message": "ID du rôle manquant"})

        if not permissions_data:
            return JsonResponse({"status": "error", "message": "Données de permissions manquantes"})

        try:
            import json
            permissions_data = json.loads(permissions_data)
            role = Role.objects.get(id=role_id)

            # Pour chaque permission dans les données reçues
            for perm_data in permissions_data:
                permission_id = perm_data.get('permission_id')
                is_granted = perm_data.get('is_granted', False)

                if permission_id:
                    try:
                        # Récupérer la permission spécifique
                        module_permission = ModulePermission.objects.get(id=permission_id)

                        if is_granted:
                            # Si la permission doit être accordée, créer la relation RolePermission
                            RolePermission.objects.get_or_create(
                                role=role,
                                module_permission=module_permission
                            )
                        else:
                            # Si la permission doit être révoquée, supprimer la relation RolePermission
                            RolePermission.objects.filter(
                                role=role,
                                module_permission=module_permission
                            ).delete()
                    except ModulePermission.DoesNotExist:
                        return JsonResponse({
                            "status": "error",
                            "message": f"Permission avec ID {permission_id} non trouvée"
                        })

            return JsonResponse({
                "status": "success",
                "message": "Permissions sauvegardées avec succès"
            })

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Données JSON invalides"})
        except Role.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Rôle non trouvé"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiAddRolePermission(request):
    if request.method == "POST":
        role_id = request.POST.get('role_id')
        module_name = request.POST.get('module')
        permission_type = request.POST.get('permission_type')

        if not role_id:
            return JsonResponse({"status": "error", "message": "ID du rôle manquant"})

        if not module_name or not permission_type:
            return JsonResponse({"status": "error", "message": "Module et type de permission sont requis"})

        try:
            role = Role.objects.get(id=role_id)
            module = Module.objects.get(name=module_name)

            # Vérifier si la permission spécifique existe déjà pour ce module
            module_permission, created = ModulePermission.objects.get_or_create(
                module=module,
                permission_type=permission_type
            )

            # Créer la relation RolePermission
            role_permission, created = RolePermission.objects.get_or_create(
                role=role,
                module_permission=module_permission
            )

            if created:
                return JsonResponse({
                    "status": "success",
                    "message": "Permission ajoutée avec succès au rôle"
                })
            else:
                return JsonResponse({
                    "status": "success",
                    "message": "La permission existait déjà pour ce rôle"
                })

        except Role.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Rôle non trouvé"})
        except Module.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Module non trouvé"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiUpdateRolePermission(request):
    if request.method == "POST":
        permission_id = request.POST.get('permission_id')
        role_id = request.POST.get('role_id')
        module_name = request.POST.get('module')
        permission_type = request.POST.get('permission_type')

        if not permission_id or not role_id:
            return JsonResponse({"status": "error", "message": "ID de la permission et du rôle sont requis"})

        if not module_name or not permission_type:
            return JsonResponse({"status": "error", "message": "Module et type de permission sont requis"})

        try:
            role = Role.objects.get(id=role_id)
            module = Module.objects.get(name=module_name)

            # Récupérer l'ancienne relation RolePermission
            old_role_permission = RolePermission.objects.get(id=permission_id, role=role)

            # Vérifier si la nouvelle permission de module existe, sinon la créer
            new_module_permission, created = ModulePermission.objects.get_or_create(
                module=module,
                permission_type=permission_type
            )

            # Vérifier si cette combinaison existe déjà pour ce rôle
            if RolePermission.objects.filter(role=role, module_permission=new_module_permission).exists():
                return JsonResponse({
                    "status": "error",
                    "message": "Cette permission existe déjà pour ce rôle"
                })

            # Supprimer l'ancienne relation
            old_role_permission.delete()

            # Créer la nouvelle relation
            RolePermission.objects.create(
                role=role,
                module_permission=new_module_permission
            )

            return JsonResponse({
                "status": "success",
                "message": "Permission mise à jour avec succès"
            })

        except RolePermission.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Permission de rôle non trouvée"})
        except Role.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Rôle non trouvé"})
        except Module.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Module non trouvé"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiDeleteRolePermission(request):
    if request.method == "POST":
        permission_id = request.POST.get('permission_id')
        role_id = request.POST.get('role_id')

        if not permission_id or not role_id:
            return JsonResponse({"status": "error", "message": "ID de la permission et du rôle sont requis"})

        try:
            role = Role.objects.get(id=role_id)

            # Récupérer la relation RolePermission
            role_permission = RolePermission.objects.get(id=permission_id, role=role)

            # Supprimer la relation
            role_permission.delete()

            return JsonResponse({
                "status": "success",
                "message": "Permission supprimée avec succès"
            })

        except RolePermission.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Permission de rôle non trouvée"})
        except Role.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Rôle non trouvé"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiDeleteModule(request):
    if request.method == "POST":
        module_id = request.POST.get('id')

        if not module_id:
            return JsonResponse({"status":"error", 'message':"ID du module manquant"})

        try:
            module = Module.objects.get(id=module_id)

            # Check if the module is active
            if module.is_active:
                return JsonResponse({
                    "status":"error",
                    "message": "Impossible de supprimer un module actif. Veuillez désactiver le module avant de le supprimer."
                })

            module_name = module.name
            module.delete()

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='DELETE',
                target_model='Module',
                target_id=str(module_id),
                details=f"Suppression du module {module_name}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({"status":"success", 'message':"Le module a été supprimé avec succès"})

        except Module.DoesNotExist:
            return JsonResponse({"status":"error", "message": "Module non trouvé"})
        except Exception as e:
            return JsonResponse({"status":"error", "message": str(e)})

    else:
        return JsonResponse({"status":"error"})

 
 
 
@login_required(login_url="institut_app:login")
@superuser_required
def ApiListeAttributions(request):
    if request.method == "GET":
        try:
            # Récupérer toutes les attributions avec les relations nécessaires
            attributions = UserModuleRole.objects.select_related('user', 'module', 'role', 'assigned_by').all()
            
            data = []
            for attribution in attributions:
                data.append({
                    'id': attribution.id,
                    'user': {
                        'id': attribution.user.id,
                        'username': attribution.user.username,
                        'first_name': attribution.user.first_name,
                        'last_name': attribution.user.last_name,
                    },
                    'module': {
                        'id': attribution.module.id,
                        'name': attribution.module.get_name_display(),
                        'name_code': attribution.module.name,
                    },
                    'role': {
                        'id': attribution.role.id,
                        'name': attribution.role.name,
                        'level': attribution.role.level,
                    },
                    'assigned_by': {
                        'id': attribution.assigned_by.id if attribution.assigned_by else None,
                        'username': attribution.assigned_by.username if attribution.assigned_by else 'Système',
                        'first_name': attribution.assigned_by.first_name if attribution.assigned_by else 'Système',
                        'last_name': attribution.assigned_by.last_name if attribution.assigned_by else '',
                    } if attribution.assigned_by else {
                        'id': None,
                        'username': 'Système',
                        'first_name': 'Système',
                        'last_name': '',
                    },
                    'assigned_at': attribution.assigned_at.strftime('%Y-%m-%d'),
                    'updated_at': attribution.updated_at.strftime('%Y-%m-%d'),
                })
            
            return JsonResponse({
                'status': 'success',
                'data': data
            }, safe=False)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiAddAttribution(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        module_id = request.POST.get('module_id')
        role_id = request.POST.get('role_id')
        
        if not user_id or not module_id or not role_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Tous les champs sont requis: utilisateur, module et rôle'
            })
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user = User.objects.get(id=user_id)
            module = Module.objects.get(id=module_id)
            role = Role.objects.get(id=role_id)
            
            # Vérifier si une attribution existe déjà pour cet utilisateur et ce module
            existing_attribution = UserModuleRole.objects.filter(user=user, module=module).first()
            if existing_attribution:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Cet utilisateur a déjà un rôle attribué pour ce module ({existing_attribution.role.name})'
                })
            
            # Créer l'attribution
            attribution = UserModuleRole.objects.create(
                user=user,
                module=module,
                role=role,
                assigned_by=request.user
            )
            
            # Activer automatiquement les sous-menus par défaut lors de l'attribution
            from institut_app.models import UserSubMenuAccess
            if module.name == 'tre':
                submenus = ['dashboard', 'tresorerie', 'exec_edu', 'remboursement', 'remises', 'caisse', 'banque', 'autres_paiements', 'depenses', 'fournisseurs', 'factures', 'parametres', 'echeanciers']
            elif module.name == 'scol':
                submenus = ['groupes', 'affectations', 'etudiants', 'transferts', 'presences', 'contrats']
            else:
                submenus = []
                
            for sc in submenus:
                UserSubMenuAccess.objects.get_or_create(
                    user=user,
                    module_code=module.name,
                    submenu_code=sc,
                    defaults={'is_active': True}
                )
            
            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='UserModuleRole',
                target_id=str(attribution.id),
                details=f"Attribution du rôle {role.name} au module {module.get_name_display()} pour l'utilisateur {user.username}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Attribution créée avec succès',
                'id': attribution.id
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Utilisateur non trouvé'
            })
        except Module.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Module non trouvé'
            })
        except Role.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Rôle non trouvé'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiBulkAddAttribution(request):
    """
    API pour créer plusieurs attributions à la fois (1 rôle pour plusieurs modules)
    """
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        role_id = request.POST.get('role_id')
        module_ids = request.POST.get('module_ids')  # Devrait être une liste JSON
        
        if not user_id or not role_id or not module_ids:
            return JsonResponse({
                'status': 'error',
                'message': 'Utilisateur, rôle et modules sont requis'
            })
        
        try:
            import json
            module_ids = json.loads(module_ids)
            
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            user = User.objects.get(id=user_id)
            role = Role.objects.get(id=role_id)
            
            created_count = 0
            errors = []
            
            for m_id in module_ids:
                try:
                    module = Module.objects.get(id=m_id)
                    
                    # Vérifier si une attribution existe déjà
                    if UserModuleRole.objects.filter(user=user, module=module).exists():
                        errors.append(f"Module {module.get_name_display()} : Déjà attribué")
                        continue
                    
                    UserModuleRole.objects.create(
                        user=user,
                        module=module,
                        role=role,
                        assigned_by=request.user
                    )
                    created_count += 1
                except Module.DoesNotExist:
                    errors.append(f"ID Module {m_id} non trouvé")
            
            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='CREATE',
                target_model='UserModuleRole',
                details=f"Attribution en masse du rôle {role.name} pour l'utilisateur {user.username} ({created_count} modules)",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({
                'status': 'success',
                'message': f'{created_count} attribution(s) créée(s) avec succès',
                'errors': errors
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiUpdateAttribution(request):
    if request.method == "POST":
        attribution_id = request.POST.get('id')
        user_id = request.POST.get('user_id')
        module_id = request.POST.get('module_id')
        role_id = request.POST.get('role_id')
        
        if not attribution_id:
            return JsonResponse({
                'status': 'error',
                'message': 'ID de l\'attribution manquant'
            })
        
        if not user_id or not module_id or not role_id:
            return JsonResponse({
                'status': 'error',
                'message': 'Tous les champs sont requis: utilisateur, module et rôle'
            })
        
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            attribution = UserModuleRole.objects.get(id=attribution_id)
            user = User.objects.get(id=user_id)
            module = Module.objects.get(id=module_id)
            role = Role.objects.get(id=role_id)
            
            # Vérifier si une autre attribution existe déjà pour cet utilisateur et ce module (sauf celle en cours de modification)
            existing_attribution = UserModuleRole.objects.filter(user=user, module=module).exclude(id=attribution_id).first()
            if existing_attribution:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Cet utilisateur a déjà un rôle attribué pour ce module ({existing_attribution.role.name})'
                })
            
            # Mettre à jour l'attribution
            attribution.user = user
            attribution.module = module
            attribution.role = role
            attribution.assigned_by = request.user
            attribution.save()
            
            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='UserModuleRole',
                target_id=str(attribution.id),
                details=f"Mise à jour de l'attribution pour l'utilisateur {user.username} (Module: {module.get_name_display()}, Rôle: {role.name})",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Attribution mise à jour avec succès'
            })
            
        except UserModuleRole.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Attribution non trouvée'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Utilisateur non trouvé'
            })
        except Module.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Module non trouvé'
            })
        except Role.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Rôle non trouvé'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiDeleteAttribution(request):
    if request.method == "POST":
        attribution_id = request.POST.get('id')

        if not attribution_id:
            return JsonResponse({
                'status': 'error',
                'message': 'ID de l\'attribution manquant'
            })

        try:
            attribution = UserModuleRole.objects.get(id=attribution_id)
            attribution.delete()

            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='DELETE',
                target_model='UserModuleRole',
                target_id=str(attribution_id),
                details=f"Suppression d'une attribution",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Attribution supprimée avec succès'
            })

        except UserModuleRole.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Attribution non trouvée'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


@login_required(login_url="institut_app:login")
@superuser_required
def ApiGetAttributionDetails(request):
    """
    API pour récupérer les détails d'une attribution spécifique
    """
    attribution_id = request.GET.get('id')

    if not attribution_id:
        return JsonResponse({
            'status': 'error',
            'message': 'ID de l\'attribution manquant'
        })

    try:
        attribution = UserModuleRole.objects.select_related('user', 'module', 'role', 'assigned_by').get(id=attribution_id)

        data = {
            'id': attribution.id,
            'user_id': attribution.user.id,
            'user_username': attribution.user.username,
            'user_first_name': attribution.user.first_name,
            'user_last_name': attribution.user.last_name,
            'module_id': attribution.module.id,
            'module_name': attribution.module.name,
            'module_display_name': attribution.module.get_name_display(),
            'role_id': attribution.role.id,
            'role_name': attribution.role.name,
            'role_level': attribution.role.level,
            'assigned_by_id': attribution.assigned_by.id if attribution.assigned_by else None,
            'assigned_by_username': attribution.assigned_by.username if attribution.assigned_by else '',
            'assigned_by_first_name': attribution.assigned_by.first_name if attribution.assigned_by else '',
            'assigned_by_last_name': attribution.assigned_by.last_name if attribution.assigned_by else '',
            'assigned_at': attribution.assigned_at.strftime('%Y-%m-%d') if attribution.assigned_at else '',
            'updated_at': attribution.updated_at.strftime('%Y-%m-%d') if attribution.updated_at else '',
        }

        return JsonResponse({
            'status': 'success',
            'data': data
        })

    except UserModuleRole.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Attribution non trouvée'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })




@login_required(login_url="institut_app:login")
@superuser_required
def ApiListeUsersPermission(request):
    """
    API pour lister tous les utilisateurs
    """
    if request.method == "GET":
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()

            # Récupérer tous les utilisateurs
            users = User.objects.all().order_by('username')

            data = []
            for user in users:
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'is_active': user.is_active,
                    'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else ''
                }
                data.append(user_data)

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


@login_required(login_url="institut_app:login")
@superuser_required
def ApiGetRolePermissionsByRoleId(request):
    """
    API pour récupérer toutes les permissions du rôle pour un module spécifique
    Cette API renvoie toutes les permissions possibles pour le module, en indiquant celles accordées au rôle
    """
    role_id = request.GET.get('role_id')
    module_id = request.GET.get('module_id')  # Obligatoire : on veut voir les permissions du rôle pour un module spécifique

    if not role_id or not module_id:
        return JsonResponse({
            'status': 'error',
            'message': 'ID du rôle et ID du module sont requis'
        })

    try:
        role = Role.objects.get(id=role_id)
        module = Module.objects.get(id=module_id)

        # Récupérer toutes les permissions possibles pour ce module
        all_module_permissions = ModulePermission.objects.filter(module=module)

        # Récupérer les permissions qui sont accordées à ce rôle pour ce module
        role_granted_permissions = RolePermission.objects.filter(
            role=role,
            module_permission__module=module
        ).values_list('module_permission_id', flat=True)

        permissions_data = []
        for mp in all_module_permissions:
            is_granted = mp.id in role_granted_permissions
            permissions_data.append({
                'id': mp.id,
                'permission_type': mp.get_permission_type_display(),
                'description': mp.description,
                'module_name': mp.module.get_name_display(),
                'full_permission_name': f"{mp.module.get_name_display()} - {mp.get_permission_type_display()}",
                'module_permission_id': mp.id,
                'is_granted': is_granted  # Indique si cette permission est accordée à ce rôle
            })

        return JsonResponse({
            'status': 'success',
            'permissions': permissions_data
        }, safe=False)

    except Role.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Rôle non trouvé'
        })
    except Module.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Module non trouvé'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required(login_url="institut_app:login")
@superuser_required
def ApiGetAttributionPermissions(request):
    """
    Récupère toutes les permissions possibles pour le module d'une attribution,
    en indiquant si elles sont accordées par le rôle ET si elles sont explicitement désactivées.
    """
    attribution_id = request.GET.get('attribution_id')
    if not attribution_id:
        return JsonResponse({'status': 'error', 'message': 'ID de l\'attribution requis'})
    
    try:
        attribution = UserModuleRole.objects.select_related('role', 'module').get(id=attribution_id)
        module = attribution.module
        role = attribution.role
        
        # Toutes les permissions possibles pour ce module
        all_module_permissions = ModulePermission.objects.filter(module=module)
        
        # Permissions accordées par le rôle
        role_granted_ids = set(RolePermission.objects.filter(
            role=role,
            module_permission__module=module
        ).values_list('module_permission_id', flat=True))
        
        # Permissions explicitement désactivées pour cet utilisateur
        denied_ids = set(attribution.denied_permissions.values_list('id', flat=True))
        
        permissions_data = []
        for mp in all_module_permissions:
            permissions_data.append({
                'id': mp.id,
                'permission_type': mp.get_permission_type_display(),
                'description': mp.description,
                'is_granted_by_role': mp.id in role_granted_ids,
                'is_denied': mp.id in denied_ids
            })
            
        return JsonResponse({
            'status': 'success',
            'permissions': permissions_data
        })
    except UserModuleRole.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Attribution non trouvée'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiTogglePermissionDenial(request):
    """
    Bascule l'état de désactivation d'une permission pour une attribution.
    """
    if request.method == "POST":
        attribution_id = request.POST.get('attribution_id')
        permission_id = request.POST.get('permission_id')
        
        if not attribution_id or not permission_id:
            return JsonResponse({'status': 'error', 'message': 'IDs requis'})
            
        try:
            attribution = UserModuleRole.objects.get(id=attribution_id)
            permission = ModulePermission.objects.get(id=permission_id)
            
            if attribution.denied_permissions.filter(id=permission.id).exists():
                attribution.denied_permissions.remove(permission)
                message = "Permission réactivée"
                is_denied = False
            else:
                attribution.denied_permissions.add(permission)
                message = "Permission désactivée"
                is_denied = True
                
            from t_crm.models import UserActionLog
            UserActionLog.objects.create(
                user=request.user,
                action_type='UPDATE',
                target_model='UserModuleRole',
                target_id=str(attribution_id),
                details=f"Bascule de désactivation de permission : {message} pour l'attribution ID {attribution_id}",
                ip_address=request.META.get('REMOTE_ADDR')
            )

            return JsonResponse({
                'status': 'success', 
                'message': message,
                'is_denied': is_denied
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


import json

@login_required(login_url="institut_app:login")
@superuser_required
def ApiExportModules(request):
    try:
        modules = Module.objects.all().prefetch_related('permissions')
        data = []
        for module in modules:
            permissions = []
            for perm in module.permissions.all():
                permissions.append({
                    'permission_type': perm.permission_type,
                    'description': perm.description
                })
            
            data.append({
                'name': module.name,  # Code (crm, ped, etc.)
                'description': module.description,
                'is_active': module.is_active,
                'permissions': permissions
            })
            
        json_data = json.dumps(data, indent=4)
        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="modules_export.json"'
        return response
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

@login_required(login_url="institut_app:login")
@transaction.atomic
@superuser_required
def ApiImportModules(request):
    if request.method == 'POST' and request.FILES.get('file'):
        try:
            json_file = request.FILES['file']
            data = json.load(json_file)
            
            created_count = 0
            updated_count = 0
            
            for item in data:
                # Update or create Module
                # Note: name is unique, so we can use it for lookup
                module, created = Module.objects.update_or_create(
                    name=item['name'],
                    defaults={
                        'description': item.get('description', ''),
                        'is_active': item.get('is_active', True)
                    }
                )
                
                if created:
                    created_count += 1
                else:
                    updated_count += 1
                
                # Update or create permissions for the module
                if 'permissions' in item:
                    for perm_data in item['permissions']:
                        ModulePermission.objects.update_or_create(
                            module=module,
                            permission_type=perm_data['permission_type'],
                            defaults={
                                'description': perm_data.get('description', '')
                            }
                        )
            
            return JsonResponse({
                "status": "success", 
                "message": f"Import réussi: {created_count} modules créés, {updated_count} mis à jour."
            })
            
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Fichier JSON invalide"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
            
    return JsonResponse({"status": "error", "message": "Aucun fichier fourni"})
