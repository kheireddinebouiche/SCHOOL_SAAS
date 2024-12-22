from django_tenants.models import TenantMixin,DomainMixin
from django.db import models


class Institut(TenantMixin):
    nom = models.CharField(max_length=255, unique=True)
    adresse = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
    
class Domaine(DomainMixin):
    pass