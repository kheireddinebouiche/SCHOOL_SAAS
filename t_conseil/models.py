from django.db import models
from django.contrib.auth.models import User
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

            # Filter by prefix to have a global counter for that prefix
            qs = Devis.objects.all()
            
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
    specialite = models.ForeignKey('t_formations.Specialites', on_delete=models.SET_NULL, null=True, blank=True, related_name="lignes_devis")

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
        ('vir', 'Virement Bancaire'),
        ('cheque', 'Chèque'),
        ('che', 'Chèque'),
        ('espece', 'Espèces'),
        ('esp', 'Espèces'),
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
    
    type_facture = models.CharField(max_length=20, choices=[('standard', 'Standard'), ('avoir', 'Avoir')], default='standard', help_text="Type de document")
    facture_source = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="avoirs_lies", help_text="Facture d'origine si c'est un avoir")
    
    conditions_commerciales = models.TextField(null=True, blank=True, help_text="Conditions spécifiques à cette facture")
    montant_timbre = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Droit de timbre (fixé à la création)")
    
    module_source = models.CharField(max_length=50, choices=[
        ('conseil', 'Executive Education'),
        ('tresorerie', 'Comptabilité')
    ], default='conseil', help_text="Module d'origine de la facture")

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

            if getattr(self, 'type_facture', 'standard') == 'avoir':
                prefix = config.avoir_prefix if config else "AV"
                width = config.avoir_counter_width if config else 4
            else:
                prefix = config.facture_prefix if config else "FAC"
                width = config.facture_counter_width if config else 4

            # Filter by prefix to have a global counter for that prefix
            qs = Facture.objects.all()

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

    def get_timbre(self):
        """Calculates Algerian Stamp Duty based on global ParametreFinancier (dynamic scale) or returns stored value."""
        from t_tresorerie.models import ParametreFinancier
        from decimal import Decimal
        import math
        import json
        
        # Priority 1: Stored value
        if self.montant_timbre > 0:
            return self.montant_timbre

        # Priority 1.5: Les factures d'avoir ne sont pas soumises au droit de timbre fiscal
        if getattr(self, 'type_facture', 'standard') == 'avoir':
            return Decimal('0')

        # Priority 2: Dynamic calculation based on settings
        config = ParametreFinancier.get_instance()
        if not config.activer_timbre:
            return Decimal('0')
            
        if config.timbre_cash_only and self.mode_paiement != 'espece':
            return Decimal('0')
            
        # Calculate TTC without timbre first
        total_ttc_raw = Decimal('0')
        for ligne in self.lignes_facture.all():
            total_ttc_raw += ligne.montant_ht * (Decimal('1') + (ligne.tva_percent / Decimal('100')))
            
        # Load bareme from config
        try:
            bareme = json.loads(config.timbre_bareme)
        except Exception:
            # Fallback bareme (LF 2025) in case of JSON parse error
            bareme = [
                {"min_ttc": 0, "max_ttc": 300, "rate": 0.0, "is_exempt": True},
                {"min_ttc": 301, "max_ttc": 30000, "rate": 1.0, "is_exempt": False},
                {"min_ttc": 30001, "max_ttc": 100000, "rate": 1.5, "is_exempt": False},
                {"min_ttc": 100001, "max_ttc": None, "rate": 2.0, "is_exempt": False}
            ]
            
        # Sort bareme by min_ttc
        bareme = sorted(bareme, key=lambda b: b.get('min_ttc', 0))
        
        # Find matching bracket
        matching_bracket = None
        for b in bareme:
            min_val = Decimal(str(b.get('min_ttc', 0)))
            max_val = b.get('max_ttc')
            if max_val is not None:
                max_val = Decimal(str(max_val))
                if min_val <= total_ttc_raw <= max_val:
                    matching_bracket = b
                    break
            else:
                if min_val <= total_ttc_raw:
                    matching_bracket = b
                    break
                    
        if not matching_bracket:
            # Fallback to last bracket
            matching_bracket = bareme[-1]
            
        rate = Decimal(str(matching_bracket.get('rate', 0.0)))
        is_exempt = matching_bracket.get('is_exempt', rate == 0)
        
        if is_exempt or rate == Decimal('0'):
            return Decimal('0')
            
        # Calculate per tranche or fraction of 100 DA based on total amount
        nb_tranches = Decimal(str(math.ceil(total_ttc_raw / 100)))
        timbre = nb_tranches * rate
        
        # Apply minimum legal (from config)
        min_stamp = max(config.timbre_min, Decimal('5'))
        if timbre < min_stamp:
            timbre = min_stamp
            
        # Round up to next integer to avoid fractional dinars on invoice
        return Decimal(str(math.ceil(timbre)))

    def total_ttc(self):
        from decimal import Decimal
        total_ttc = Decimal('0')
        for ligne in self.lignes_facture.all():
            ligne_ht = ligne.montant_ht
            ligne_tva = ligne_ht * (ligne.tva_percent / Decimal('100'))
            total_ttc += (ligne_ht + ligne_tva)
        
        # Add stamp duty
        total_ttc += self.get_timbre()
        
        return total_ttc
    total_ttc.short_description = "Total TTC (avec timbre)"

class TvaConseil(models.Model):
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
    specialite = models.ForeignKey('t_formations.Specialites', on_delete=models.SET_NULL, null=True, blank=True)
    
class ConseilConfiguration(models.Model):
    """
    Configuration globale pour le module Conseil.
    Stocke les paramètres de TVA, Remises, et préférences d'affichage.
    """
    # Enterprise Association
    entreprise = models.OneToOneField(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name="conseil_config")

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

    avoir_prefix = models.CharField(max_length=20, default="AV", help_text="Préfixe pour les avoirs")
    avoir_counter_width = models.PositiveIntegerField(default=4, help_text="Longueur du compteur pour avoir (ex: 4 pour 0001)")

    # Droits de Timbre (Stamp Duty) - Algerian Legislation
    enable_stamp_duty = models.BooleanField(default=False, help_text="Activer les droits de timbre (Algérie)")
    stamp_duty_rate = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, help_text="Taux du timbre en % (Standard: 1%)")
    stamp_duty_min = models.DecimalField(max_digits=10, decimal_places=2, default=5.00, help_text="Montant minimum du timbre (DZD)")
    stamp_duty_max = models.DecimalField(max_digits=10, decimal_places=2, default=10000.00, help_text="Plafond du timbre (DZD)")
    apply_stamp_duty_on_cash_only = models.BooleanField(default=True, help_text="Appliquer uniquement sur les paiements en espèces")

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
        ('vir', 'Virement Bancaire'),
        ('che', 'Chèque'),
        ('esp', 'Espèce'),
        ('autre', 'Autre'),
    ]
    mode_paiement = models.CharField(max_length=20, choices=MODE_PAIEMENT_CHOICES)
    reference = models.CharField(max_length=100, null=True, blank=True)
    is_done = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"

class Participant(models.Model):
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, related_name="participants_pool", null=True, blank=True)
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name="participants", null=True, blank=True)
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name="participants", null=True, blank=True)
    
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)
    
    poste = models.CharField(max_length=255, null=True, blank=True)
    nin = models.CharField(max_length=255, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confirmed_for_scolarite = models.BooleanField(default=False)
    scolarite_note = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class GroupeConseil(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE, related_name='groupes_conseil')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    lieu_formation = models.CharField(max_length=255, null=True, blank=True, help_text="Lieu de l'action de formation")
    jours_travail = models.CharField(max_length=255, null=True, blank=True, help_text="Jours de travail prévus (ex: Lun, Mar, Jeu)")
    
    etat = models.CharField(max_length=200, choices=[('brouillon','Brouillon'),('enc', 'En cours'), ('cloture', 'Clôturé')], default='brouillon')

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='groupes_conseil_crees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Groupe Conseil"
        verbose_name_plural = "Groupes Conseil"

    def __str__(self):
        return f"{self.nom} - {self.devis.num_devis}"

class GroupeConseilParticipant(models.Model):
    groupe = models.ForeignKey(GroupeConseil, on_delete=models.CASCADE, related_name='participants_groupe')
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='groupes_impliques')

    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Participant du Groupe Conseil"
        verbose_name_plural = "Participants des Groupes Conseil"

    def __str__(self):
        return f"{self.groupe.nom} - {self.participant.nom} {self.participant.prenom}"

class GroupeConseilThematique(models.Model):
    groupe = models.ForeignKey(GroupeConseil, on_delete=models.CASCADE, related_name='affectations_thematiques')
    thematique = models.ForeignKey(Thematiques, on_delete=models.CASCADE)
    formateur = models.ForeignKey('t_formations.Formateurs', on_delete=models.SET_NULL, null=True, blank=True)
    
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Affectation Thématique Groupe Conseil"
        verbose_name_plural = "Affectations Thématiques Groupes Conseil"

    def __str__(self):
        formateur_str = self.formateur if self.formateur else "Sans formateur"
        return f"{self.groupe.nom} - {self.thematique.label} ({formateur_str})"

class GroupeConseilPlanning(models.Model):
    groupe = models.ForeignKey(GroupeConseil, on_delete=models.CASCADE, related_name='planning')
    thematique = models.ForeignKey(Thematiques, on_delete=models.CASCADE)
    formateur = models.ForeignKey('t_formations.Formateurs', on_delete=models.SET_NULL, null=True, blank=True)
    
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    
    note = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Planning Groupe Conseil"
        verbose_name_plural = "Plannings Groupes Conseil"
        ordering = ['date', 'heure_debut']

    def __str__(self):
        return f"{self.groupe.nom} - {self.thematique.label} le {self.date}"
