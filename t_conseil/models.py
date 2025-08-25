from django.db import models
from institut_app.models import ConfigurationDesDocument

class Client(models.Model):
    nom = models.CharField(max_length=255, null=True, blank=True, help_text="Nom du client")
    email = models.EmailField(max_length=255, null=True, blank=True, help_text="Email du client")
    telephone = models.CharField(max_length=20, null=True, blank=True, help_text="Téléphone du client")
    adresse = models.TextField(null=True, blank=True, help_text="Adresse du client")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.nom if self.nom else "Client sans nom"

class FormateurConseil(models.Model):
    pass

class Thematiques(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True, help_text="Label de la thématique")
    description = models.TextField(null=True, blank=True, help_text="Description de la thématique")
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Prix de la thématique")
    duree = models.PositiveIntegerField(null=True, blank=True, help_text="Durée en minutes")
    etat = models.CharField(max_length=50, choices=[('archive', 'Archivé'), ('active', 'Active')], default='active')
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"

    def __str__(self):
        return self.label if self.label else "Thématique sans label"
    
class Devis(models.Model):
    client = models.CharField(max_length=255, null=True, blank=True, help_text="Nom du client")
    num_devis = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="Numéro du devis")
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Montant du devis")
    date_emission = models.DateField(null=True, blank=True, help_text="Date d'émission du devis")
    date_echeance = models.DateField(null=True, blank=True, help_text="Date d'échéance du devis")
    etat = models.CharField(max_length=50, choices=[
        ('brouillon', 'Brouillon'),
        ('envoye', 'Envoyé'),
        ('accepte', 'Accepté'),
        ('rejete', 'Rejeté'),
    ], default='brouillon')

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.num_devis:
           
            config = ConfigurationDesDocument.objects.first()
            prefix = config.prefix_devis if config else "DEV"

            last_devis = Devis.objects.filter(num_devis__startswith=prefix).order_by('-id').first()
            if last_devis and last_devis.num_devis:
                try:
                    last_num = int(last_devis.num_devis.split('-')[-1])
                except ValueError:
                    last_num = 0
                self.num_devis = f"{prefix}-{last_num + 1:04d}"
            else:
                self.num_devis = f"{prefix}-0001"

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Devis"
        verbose_name_plural = "Devis"

    def __str__(self):
        return f"{self.num_devis} pour {self.client}"

class LignesDevis(models.Model):
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name="lignes_devis")
    description = models.CharField(max_length=255, null=True, blank=True, help_text="Description de la ligne de devis")
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Montant de la ligne de devis")
    quantite = models.PositiveIntegerField(null=True, blank=True, help_text="Quantité de la ligne de devis")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Ligne de devis"
        verbose_name_plural = "Lignes de devis"

    def __str__(self):
        return f"Ligne de devis pour {self.devis.client} - {self.description}"
    
class Facture(models.Model):
    pass