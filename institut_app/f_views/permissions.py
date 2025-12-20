from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from ..models import *
from django.contrib.auth.decorators import login_required
from django.db import transaction

@login_required(login_url="institut_app:login")
def ModulesPages(request):
    return render(request, 'tenant_folder/administration/permissions/modules.html')


@login_required(login_url="institut_app:login")
def Role_Attribution(request):
    return render(request,"tenant_folder/administration/permissions/attribution_des_roles.html")

@login_required(login_url="institut_app:login")
def ApiListeModules(request):
    if request.method == "GET":
        
        liste = Module.objects.all()
        data = []
        for i in liste:
            data.append({
                'id' : i.id,
                'name' : i.get_name_display(),
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

            return JsonResponse({"status":"success",'message':"Le module a été crée avec succès"})

        except Exception as e:
            return JsonResponse({"status":"error","message":str(e)})

    else:
        return JsonResponse({"status":"error"})


@login_required(login_url='institut_app:login')
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

            return JsonResponse({'status':'success', 'message':'Le rôle a été créé avec succès'})

        except ValueError:
            return JsonResponse({'status':'error', 'message': 'Le niveau doit être un nombre valide'})
        except Exception as e:
            return JsonResponse({'status':'error', 'message': str(e)})

    else:
        return JsonResponse({'status':'error'})


@login_required(login_url='institut_app:login')
@transaction.atomic
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

            role.delete()

            return JsonResponse({'status':'success', 'message':'Le rôle a été supprimé avec succès'})

        except Role.DoesNotExist:
            return JsonResponse({'status':'error', 'message': 'Rôle non trouvé'})
        except Exception as e:
            return JsonResponse({'status':'error', 'message': str(e)})

    else:
        return JsonResponse({'status':'error'})


@login_required(login_url='institut_app:login')
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

            return JsonResponse({"status":"success", 'message':"Le module a été mis à jour avec succès"})

        except Module.DoesNotExist:
            return JsonResponse({"status":"error", "message": "Module non trouvé"})
        except Exception as e:
            return JsonResponse({"status":"error", "message": str(e)})

    else:
        return JsonResponse({"status":"error"})


@login_required(login_url="institut_app:login")
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
def ApiGetRolePermissions(request):
    role_id = request.GET.get('role_id')

    if not role_id:
        return JsonResponse({"status": "error", "message": "ID du rôle manquant"})

    try:
        role = Role.objects.get(id=role_id)

        # Récupérer toutes les permissions du rôle
        role_permissions = RolePermission.objects.filter(role=role).select_related('module_permission', 'module_permission__module')

        permissions_data = []
        for rp in role_permissions:
            permissions_data.append({
                'id': rp.module_permission.id,
                'module_name': rp.module_permission.module.get_name_display(),
                'permission_name': rp.module_permission.get_permission_type_display(),
                'is_granted': True  # Toutes les permissions liées au rôle sont accordées
            })

        # Ajouter également les permissions qui ne sont pas encore attribuées au rôle
        all_module_permissions = ModulePermission.objects.all()
        for mp in all_module_permissions:
            # Vérifier si cette permission est déjà attribuée au rôle
            existing_rp = role_permissions.filter(module_permission=mp).first()
            if not existing_rp:
                permissions_data.append({
                    'id': mp.id,
                    'module_name': mp.module.get_name_display(),
                    'permission_name': mp.get_permission_type_display(),
                    'is_granted': False
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

            # Mettre à jour la relation
            old_role_permission.module_permission = new_module_permission
            old_role_permission.save()

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

            module.delete()

            return JsonResponse({"status":"success", 'message':"Le module a été supprimé avec succès"})

        except Module.DoesNotExist:
            return JsonResponse({"status":"error", "message": "Module non trouvé"})
        except Exception as e:
            return JsonResponse({"status":"error", "message": str(e)})

    else:
        return JsonResponse({"status":"error"})

 
