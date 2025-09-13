from django.db import models
from t_etudiants.models import *
from institut_app.models import *
from t_formations.models import *
from t_crm.models import *
from django.contrib.auth.models import User


class ClientPaiementsRequest(models.Model):
    
    client = models.ForeignKey(Visiteurs, on_delete=models.DO_NOTHING, null=True, blank=True)

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True)
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid = models.BooleanField(default=False)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('tranche','Tranche'), ('mensuelle','Mensuelle'), ('totalite','Paiement unique')])

    motif = models.CharField(max_length=100, null=True, blank=True, choices=[('frais', 'Frais d\'admission'),('autre','Autres'),('dette','Module en dette')])

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
    paiement_request = models.ForeignKey(ClientPaiementsRequest, on_delete=models.DO_NOTHING, null=True)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_paiement = models.DateField(null=True)
    observation = models.CharField(max_length=1000, null=True, blank=True)
    motif_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('fin','Frais d\'incription'),('ass','Assurance'),('frf','Frais de formation')])
    etat = models.CharField(max_length=100, null=True, blank=True, choices=[('auc','Aucun paiement effectuer'),('part','Paiement partiel'), ('tot','Paiement cash'),('ter','Paiement terminer')], default="auc")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.paiement_request

class Paiements(models.Model):
    paiement_line = models.ForeignKey(clientPaiementsRequestLine, on_delete=models.CASCADE, null=True, blank=True)
    montant_paye = models.FloatField(null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    observation = models.CharField(max_length=100, null=True, blank=True)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('che','Chèque'),('esp','Espece'),('vir','Virement Bancaire')])
    reference_paiement = models.CharField(max_length=100, null=True, blank=True)

    etat = models.CharField(max_length=100, null=True, blank=True, choices=[('val','Valider'),('dmr','Demande de remboursement'),('rem','Rembourssement approuvé')], default='val')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.montant_paye
    
class Rembourssements(models.Model):
    paiements = models.ForeignKey(Paiements, on_delete=models.CASCADE, null=True, blank=True)
    motif_rembourssement = models.CharField(max_length=100, null=True, blank=True)
    etat = models.CharField(max_length=100, null=True, blank=True, choices=[('enc','En cours de traitement'),('acp','Approuvé'),('ref','Refusé')], default="enc")

    is_approuved = models.BooleanField(default=False)
    observation = models.CharField(max_length=1000, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.paiements

class SeuilPaiements(models.Model):
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True)
    label = models.CharField(max_length=100, null=True)
    valeur = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('specialite', 'valeur')

    def __str__(self):
        return self.specialite
    

class Remises(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    taux = models.IntegerField(null=True, blank=True)
    is_enabled = models.BooleanField(default=False)

    is_archived = models.BooleanField(default=False)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.label
    

class EcheancierPaiement(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    promo = models.ForeignKey(Promos, null=True, blank=True, on_delete=models.CASCADE)
    formation = models.ForeignKey(Formation, null=True, blank=True, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_approuved = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.label

class EcheancierPaiementLine(models.Model):
    echeancier = models.ForeignKey(EcheancierPaiement, null=True, blank=True, on_delete=models.CASCADE)
    
    taux = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)

    date_echeancier = models.DateField(null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.echeancier.label

class EcheancierPaiementSepcial(models.Model):
    pass

class EcheancierPaiementSpecialLine(models.Model):
    pass
