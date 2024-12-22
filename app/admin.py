from django.contrib import admin
from .models import *

class TenantAdminSite(admin.AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.register(Institut)
        self.register(Domaine)

tenant_admin_site = TenantAdminSite(name="tenant_admin_site")