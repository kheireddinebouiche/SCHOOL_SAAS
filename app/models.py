from django_tenants.models import TenantMixin,DomainMixin
from django.db import models


class Institut(TenantMixin):
    nom = models.CharField(max_length=255, unique=True)
    adresse = models.TextField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    tenant_type = models.CharField(max_length=255, null=True, blank=True, choices=[('associe','Associe'),('master','Compte maitre'),('second','Compte standard')])

    def __str__(self):
        return self.nom
    
class Domaine(DomainMixin):
    pass

class TenantFolder(models.Model):
    sender = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='sent_folders')
    receiver = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='received_folders')
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TenantMessage(models.Model):
    sender = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender} to {self.receiver} - {self.created_at}"

class TenantDocument(models.Model):
    sender = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='sent_documents')
    receiver = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='received_documents')
    file = models.FileField(upload_to='tenant_docs/')
    folder = models.ForeignKey(TenantFolder, on_delete=models.CASCADE, null=True, blank=True, related_name='documents')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doc {self.id} from {self.sender}"