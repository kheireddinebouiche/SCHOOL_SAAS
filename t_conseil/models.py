from django.db import models
from institut_app.models import ConfigurationDesDocument, Entreprise
from t_crm.models import Prospets, Opportunite
from t_tresorerie.models import PaymentCategory



class Thematiques(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True, help_text="Label de la thématique")
    description = models.TextField(null=True, blank=True, help_text="Description de la thématique")
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Prix de la thématique")
    billing_type = models.CharField(max_length=50, choices=[('heure', 'Heure'), ('jour', 'Jour')], default='heure', help_text="Mode de facturation")
    default_tva = models.DecimalField(max_digits=5, decimal_places=2, default=19.00, help_text="TVA par défaut pour cette thématique")
    etat = models.CharField(max_length=50, choices=[('archive', 'Archivée'), ('active', 'Active')], default='active')
    
    categorie = models.CharField(max_length=20, choices=[('service', 'Service'), ('produit', 'Produit')], default='service', help_text="Catégorie de la thématique")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"

    def __str__(self):
        return self.label if self.label else "Thématique sans label"

class DASMapping(models.Model):
    designation = models.CharField(max_length=255, help_text="Désignation de l'association")
    thematique = models.ForeignKey(Thematiques, on_delete=models.CASCADE, related_name="das_mappings")
    payment_category = models.ForeignKey(PaymentCategory, on_delete=models.CASCADE, related_name="das_mappings")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mapping DAS"
        verbose_name_plural = "Mappings DAS"
        unique_together = ('thematique', 'payment_category')

    def __str__(self):
        return f"{self.designation} ({self.thematique.label} -> {self.payment_category.name})"
    
class Devis(models.Model):
    client = models.ForeignKey(Prospets,on_delete=models.CASCADE, help_text="Nom du client", related_name="client_devis")
    opportunite = models.ForeignKey(Opportunite, on_delete=models.SET_NULL, null=True, blank=True, related_name="opportunite_devis", help_text="Opportunité liée")
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
    
    show_tva = models.BooleanField(default=True, help_text="Afficher la TVA sur ce devis")
    show_remise = models.BooleanField(default=False, help_text="Afficher la remise sur ce devis")
    conditions_commerciales = models.TextField(null=True, blank=True, help_text="Conditions commerciales spécifiques à ce devis")

    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name="devis_entreprise")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.num_devis:
            # Find config for this enterprise or the first one if not set
            config = None
            if self.entreprise:
                config = ConseilConfiguration.objects.filter(entreprise=self.entreprise).first()
            
            if not config:
                config = ConseilConfiguration.objects.first()

            prefix = config.devis_prefix if config else "DEV"
            width = config.devis_counter_width if config else 4

            # Filter by enterprise to have separate counters
            qs = Devis.objects.all()
            if self.entreprise:
                qs = qs.filter(entreprise=self.entreprise)
            
            last_devis = qs.filter(num_devis__startswith=prefix).order_by('-id').first()
            if last_devis and last_devis.num_devis:
                try:
                    import re
                    match = re.search(r'(\d+)$', last_devis.num_devis)
                    last_num = int(match.group(1)) if match else 0
                except (ValueError, AttributeError):
                    last_num = 0
                self.num_devis = f"{prefix}-{last_num + 1:0{width}d}"
            else:
                self.num_devis = f"{prefix}-{1:0{width}d}"
            
            # Set default conditions if not provided
            if not self.conditions_commerciales:
                self.conditions_commerciales = config.default_conditions_commerciales if config else ""

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Devis"
        verbose_name_plural = "Devis"

    def __str__(self):
        return f"{self.num_devis} pour {self.client}"

class LignesDevis(models.Model):
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name="lignes_devis")
    thematique = models.ForeignKey(Thematiques, on_delete=models.SET_NULL, null=True, blank=True, related_name="lignes_devis")
    description = models.CharField(max_length=255, null=True, blank=True, help_text="Description courte de la ligne")
    long_description = models.TextField(null=True, blank=True, help_text="Description détaillée de la prestation")
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Montant de la ligne de devis")
    quantite = models.PositiveIntegerField(null=True, blank=True, help_text="Quantité de la ligne de devis")
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Prix unitaire HT")
    remise_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Pourcentage de remise")
    tva_percent = models.DecimalField(max_digits=5, decimal_places=2, default=19.00, help_text="Taux de TVA pour cette ligne")

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name = "Ligne de devis"
        verbose_name_plural = "Lignes de devis"

    def __str__(self):
        return f"Ligne de devis pour {self.devis.client} - {self.description}"
    
class Facture(models.Model):
    client = models.ForeignKey(Prospets, on_delete=models.CASCADE, help_text="Client facturé", null=True, blank=True)
    devis_source = models.ForeignKey(Devis, on_delete=models.SET_NULL, null=True, blank=True, related_name="facture")
    num_facture = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="Numéro de la facture")
    date_emission = models.DateField(null=True, blank=True)
    date_echeance = models.DateField(null=True, blank=True)
    
    tva = models.DecimalField(max_digits=5, decimal_places=2, default=19.00, help_text="Taux de TVA applicable")
    
    show_tva = models.BooleanField(default=True, help_text="Afficher la TVA sur cette facture")
    show_remise = models.BooleanField(default=False, help_text="Afficher la remise sur cette facture")
    
    MODE_PAIEMENT_CHOICES = [
        ('virement', 'Virement Bancaire'),
        ('cheque', 'Chèque'),
        ('espece', 'Espèces'),
        ('autre', 'Autre'),
    ]
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES, default='virement', help_text="Mode de paiement attendu")
    
    etat = models.CharField(max_length=50, choices=[
        ('brouillon', 'Brouillon'),
        ('envoye', 'Envoyée'),
        ('battente', 'En attente de paiement'),
        ('paye', 'Payée'),
        ('annule', 'Annulée'),
    ], default='brouillon')
    
    conditions_commerciales = models.TextField(null=True, blank=True, help_text="Conditions spécifiques à cette facture")
    
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name="factures_entreprise")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.num_facture:
            config = None
            if self.entreprise:
                config = ConseilConfiguration.objects.filter(entreprise=self.entreprise).first()
            
            if not config:
                config = ConseilConfiguration.objects.first()

            prefix = config.facture_prefix if config else "FAC"
            width = config.facture_counter_width if config else 4

            qs = Facture.objects.all()
            if self.entreprise:
                qs = qs.filter(entreprise=self.entreprise)

            last = qs.filter(num_facture__startswith=prefix).order_by('-id').first()
            if last and last.num_facture:
                try:
                    import re
                    match = re.search(r'(\d+)$', last.num_facture)
                    last_num = int(match.group(1)) if match else 0
                except (ValueError, AttributeError):
                    last_num = 0
                self.num_facture = f"{prefix}-{last_num + 1:0{width}d}"
            else:
                self.num_facture = f"{prefix}-{1:0{width}d}"

            # Set default conditions and payment methods if not provided
            if not self.conditions_commerciales:
                self.conditions_commerciales = config.default_conditions_commerciales if config else ""

        super().save(*args, **kwargs)

    def total_ttc(self):
        total_ttc = 0
        for ligne in self.lignes_facture.all():
            ligne_ht = ligne.montant_ht
            ligne_tva = ligne_ht * (ligne.tva_percent / 100)
            total_ttc += (ligne_ht + ligne_tva)
        return total_ttc
    total_ttc.short_description = "Total TTC"

class TvaConseil(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name="tvas_conseil")
    label = models.CharField(max_length=50, help_text="Ex: TVA 19%")
    valeur = models.DecimalField(max_digits=5, decimal_places=2, help_text="Valeur en %")
    is_default = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "TVA Conseil"
        verbose_name_plural = "TVAs Conseil"

    def __str__(self):
        return f"{self.label} ({self.valeur}%)"

class LignesFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="lignes_facture")
    thematique = models.ForeignKey(Thematiques, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    long_description = models.TextField(null=True, blank=True, help_text="Description détaillée de la prestation")
    quantite = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_ht = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remise_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tva_percent = models.DecimalField(max_digits=5, decimal_places=2, default=19.00)
    
class ConseilConfiguration(models.Model):
    """
    Configuration globale pour le module Conseil.
    Stocke les paramètres de TVA, Remises, et préférences d'affichage.
    """
    # Enterprise Association
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name="conseil_config", unique=True)

    # TVA Configuration
    default_tva_percent = models.DecimalField(max_digits=5, decimal_places=2, default=19.00, help_text="Taux de TVA par défaut (%)")
    show_tva_on_devis = models.BooleanField(default=True, help_text="Afficher la TVA sur les devis PDF/View")
    show_tva_on_facture = models.BooleanField(default=True, help_text="Afficher la TVA sur les factures PDF/View")
    
    # Remise (Discount) Configuration
    enable_remise_global = models.BooleanField(default=False, help_text="Activer la gestion des remises")
    default_remise_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Taux de remise par défaut (%)")
    show_remise_on_devis = models.BooleanField(default=False, help_text="Afficher la colonne remise sur les devis")
    show_remise_on_facture = models.BooleanField(default=False, help_text="Afficher la colonne remise sur les factures")

    default_conditions_commerciales = models.TextField(null=True, blank=True, help_text="Conditions commerciales par défaut")

    # General
    updated_at = models.DateTimeField(auto_now=True)

    # Document Numbering Configuration
    devis_prefix = models.CharField(max_length=20, default="DEV", help_text="Préfixe pour les devis")
    devis_counter_width = models.PositiveIntegerField(default=4, help_text="Longueur du compteur (ex: 4 pour 0001)")
    
    facture_prefix = models.CharField(max_length=20, default="FAC", help_text="Préfixe pour les factures")
    facture_counter_width = models.PositiveIntegerField(default=4, help_text="Longueur du compteur (ex: 4 pour 0001)")

    class Meta:
        verbose_name = "Configuration Conseil"
        verbose_name_plural = "Configuration Conseil"

    def __str__(self):
        return f"Configuration Conseil - {self.entreprise.designation if self.entreprise else 'Globale'}"

    def save(self, *args, **kwargs):
        # Ensure only one config per enterprise (or global)
        if not self.pk:
            if ConseilConfiguration.objects.filter(entreprise=self.entreprise).exists():
                # Update existing instead of creating? Or just prevent.
                # For safety, let's just allow it for now but the UI should handle it.
                pass
        super().save(*args, **kwargs)

class Paiement(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="paiements")
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateField()
    
    MODE_PAIEMENT_CHOICES = [
        ('virement', 'Virement Bancaire'),
        ('cheque', 'Chèque'),
        ('espece', 'Espèces'),
        ('autre', 'Autre'),
    ]
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES)
    reference = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"

    def __str__(self):
        return f"Paiement de {self.montant} pour {self.facture.num_facture}"
