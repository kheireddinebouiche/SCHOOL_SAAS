from django.db import models
from django.contrib.auth.models import User
from app.models import Institut

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)

class Entreprise(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)

    rc = models.CharField(max_length=255, null=True, blank=True)
    nif = models.CharField(max_length=255, null=True, blank=True)
    art = models.CharField(max_length=255, blank=True, null=True)
    nis = models.CharField(max_length=255, null=True, blank=True)

    adresse = models.CharField(max_length=255, null=True, blank=True)
    telephone = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    site_web = models.URLField(null=True, blank=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Entreprise"
        verbose_name_plural = "Entreprises"
    
    def __str__(self):
        return self.designation

class BankAccount(models.Model):
    tenant = models.ForeignKey(Institut, on_delete=models.CASCADE, null=True, blank=True)
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    num = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Label"
        verbose_name_plural="Labels"

    def __str__(self):
        return self.label
