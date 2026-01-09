import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings")
django.setup()

from django.contrib.auth import get_user_model
from institut_app.models import Module, Role, UserModuleRole, ModulePermission, RolePermission

User = get_user_model()
users = User.objects.all()
print(f"Users found: {users.count()}")

if users.count() > 0:
    user = users.first()
    print(f"Checking user: {user.username} (ID: {user.id})")
    
    roles = UserModuleRole.objects.filter(user=user)
    print(f"Assigned Roles: {roles.count()}")
    
    if roles.count() == 0:
        print("No roles found. Creating sample data...")
        # Create or Get Module
        mod, _ = Module.objects.get_or_create(name='crm', defaults={'description':'CRM Module'})
        
        # Create or Get Role
        role, _ = Role.objects.get_or_create(name='Manager CRM', defaults={'level': 3, 'description': 'Manager'})
        
        # Create Permissions
        perm_view, _ = ModulePermission.objects.get_or_create(module=mod, permission_type='view')
        perm_add, _ = ModulePermission.objects.get_or_create(module=mod, permission_type='add')
        
        # Assign Permissions to Role
        RolePermission.objects.get_or_create(role=role, module_permission=perm_view)
        RolePermission.objects.get_or_create(role=role, module_permission=perm_add)
        
        # Assign Role to User
        UserModuleRole.objects.create(user=user, module=mod, role=role)
        print(f"Assigned 'Manager CRM' to {user.username}")
    else:
        for r in roles:
            print(f"- {r.module.get_name_display()} : {r.role.name}")
            perms = r.get_effective_permissions()
            print(f"  Permissions: {[p.module_permission.get_permission_type_display() for p in perms]}")

else:
    print("No users found in DB.")
