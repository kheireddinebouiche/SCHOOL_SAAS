from django.db import models
from django.contrib.auth.models import User
from .models import Prospets

class Opportunite(models.Model):
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, related_name='opportunites')
    nom = models.CharField(max_length=255, help_text="Nom de l'opportunité")
    
    stage = models.CharField(
        max_length=50, 
        default='entrant', 
        choices=[
            ('entrant', 'Entrant'),
            ('contacte', 'Contacté'),
            ('negociation', 'Négociation'),
            ('devis_envoye', 'Devis envoyé'),
            ('en_negociation', 'En Négociation'),
            ('facture', 'Facturé'),
            ('recouvrement', 'RECOUVREMENT'),
        ]
    )
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Budget")
    probability = models.IntegerField(default=0, verbose_name="Probabilité (%)")
    commercial = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="opportunites_conseil")
    closing_date = models.DateField(null=True, blank=True, verbose_name="Date de closing prévue")
    is_active = models.BooleanField(default=True, verbose_name="Pipeline Actif")
    is_favorite = models.BooleanField(default=False, verbose_name="Favori")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Opportunité"
        verbose_name_plural = "Opportunités"

    def __str__(self):
        return f"{self.nom} - {self.prospect}"
