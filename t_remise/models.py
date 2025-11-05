from django.db import models
from django.contrib.auth.models import User


class Remises(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)

    taux = models.IntegerField(null=True, blank=True)

    is_enabled = models.BooleanField(default=False)
    
    has_to_justify = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)

    description = models.TextField(max_length=3000, null=True, blank=True)

    is_value=models.BooleanField(default=False)
    montant = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.label
    

    