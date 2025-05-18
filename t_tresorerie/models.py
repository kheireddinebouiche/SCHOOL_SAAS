from django.db import models
from t_etudiants.models import *
from institut_app.models import *
from t_formations.models import *
from t_crm.models import *
from django.contrib.auth.models import User


class ClientPaiementsRequest(models.Model):
    
    demandes = models.ForeignKey(DemandeInscription, on_delete=models.CASCADE, null=True, blank=True)

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True)
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    paid = models.BooleanField(default=False)

    mode_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('tranche','Tranche'), ('mensuelle','Mensuelle'), ('totalite','Paiement unique')])

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    etat = models.CharField(max_length=100, null=True, blank=True, default='en_attente' ,choices=[('en_attente','En Attente'),('annulation','Demande d\'annulation'),('annulation_approuver','Demande d\'annulation approuvée'),('terminer','Cloturer')])

    approuved_annulation = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Demande de paiement"
        verbose_name_plural = "Demandes de paiement"

    def __str__(self):
        return f"{self.student}"
    
class clientPaiementsRequestLine(models.Model):
    pass

class Paiements(models.Model):
    pass

class SeuilPaiements(models.Model):
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True)
    label = models.CharField(max_length=100, null=True)
    valeur = models.IntegerField(null=True)

    class Meta:
        unique_together = ('specialite', 'valeur')

    def __str__(self):
        return self.specialite