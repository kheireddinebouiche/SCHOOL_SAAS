from django.db import models
from django.contrib.auth.models import User
from t_formations.models import Formateurs
from institut_app.models import Entreprise

class TypeContrat(models.TextChoices):
    CDI = 'CDI', 'Contrat à Durée Indéterminée'
    CDD = 'CDD', 'Contrat à Durée Déterminée'
    VACATION = 'VACATION', 'Vacation (Paiement à l\'heure)'

class Contrat(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name='contrats_rh')
    formateur = models.ForeignKey(Formateurs, on_delete=models.CASCADE, related_name='contrats')
    type_contrat = models.CharField(max_length=20, choices=TypeContrat.choices, default=TypeContrat.CDD)
    
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    
    # Rémunération
    salaire_base = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Salaire de base mensuel ou Taux horaire si vacation")
    salaire_horaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Remplir si Vacation")
    
    # Primes fixes
    prime_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prime_panier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    actif = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return f"Contrat {self.get_type_contrat_display()} - {self.formateur}"

class FichePaie(models.Model):
    MOIS_CHOICES = [
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ]
    
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name='fiches_paie')
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name='fiches_paie_rh')
    mois = models.IntegerField(choices=MOIS_CHOICES)
    annee = models.IntegerField()
    
    # Variables du mois
    jours_travailles = models.IntegerField(default=22) # Standard 22 working days
    heures_travailles = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Pour les vacataires")
    heures_absence = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Nombre d'heures d'absence")
    
    # Primes variables / Retenues
    primes_exceptionnelles = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    retenues_absences = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avance_sur_salaire = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Calculs (Sauvegardés pour historique)
    salaire_base_calcule = models.DecimalField(max_digits=12, decimal_places=2, default=0) # Base * jours ou Taux * heures
    salaire_poste = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    base_ss = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    montant_ss = models.DecimalField(max_digits=12, decimal_places=2, default=0) # 9%
    
    salaire_imposable = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    irg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    net_a_payer = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    prime_panier = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    prime_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    generated_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['contrat', 'mois', 'annee']

class ParametresPaie(models.Model):
    entreprise = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True, related_name='parametres_paie')
    taux_ss = models.DecimalField(max_digits=5, decimal_places=4, default=0.09, help_text="Taux de sécurité sociale (ex: 0.09 pour 9%)")
    jours_travailles_standard = models.IntegerField(default=22, help_text="Nombre de jours travaillés standard par mois")
    heures_mensuelles_standard = models.DecimalField(max_digits=6, decimal_places=2, default=173.33, help_text="Nombre d'heures travaillés standard par mois (ex: 173.33)")
    seuil_exoneration_irg = models.DecimalField(max_digits=12, decimal_places=2, default=30000, help_text="Seuil d'exonération IRG")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paramètres de paie"
        verbose_name_plural = "Paramètres de paie"

    def __str__(self):
        return "Configuration de la paie"

    @classmethod
    def get_config(cls, entreprise=None):
        config, created = cls.objects.get_or_create(entreprise=entreprise)
        return config

class Rubrique(models.Model):
    TYPE_CHOICES = [
        ('GAIN', 'Gain (+)'),
        ('RETENUE', 'Retenue (-)'),
    ]
    
    MODE_CALCUL_CHOICES = [
        ('FIXE', 'Montant Fixe (DA)'),
        ('PERCENT', 'Pourcentage du Salaire de Base (%)'),
        ('HOURS', 'Nombre d\'heures (h)'),
    ]
    
    libelle = models.CharField(max_length=100)
    type_rubrique = models.CharField(max_length=10, choices=TYPE_CHOICES, default='GAIN')
    mode_calcul = models.CharField(max_length=10, choices=MODE_CALCUL_CHOICES, default='FIXE')
    est_cotisable = models.BooleanField(default=False, help_text="Soumis à la cotisation SS (9%) ?")
    est_imposable = models.BooleanField(default=False, help_text="Soumis à l'impôt IRG ?")
    actif = models.BooleanField(default=True)
    
    # Configuration des contrats éligibles (Stocké en JSON: ["CDI", "CDD"])
    types_contrat = models.JSONField(default=list, blank=True, help_text="Types de contrats éligibles (ex: ['CDI', 'CDD'])")
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.libelle} ({self.get_type_rubrique_display()})"
    
    class Meta:
        ordering = ['type_rubrique', 'libelle']

class RubriqueContrat(models.Model):
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name='rubriques_contrat')
    rubrique = models.ForeignKey(Rubrique, on_delete=models.CASCADE, related_name='contrats_lies')
    valeur = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Valeur par défaut (Montant, % ou Heures)")
    actif = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['contrat', 'rubrique']
        verbose_name = "Rubrique par Contrat"
        verbose_name_plural = "Rubriques par Contrat"
        
    def __str__(self):
        return f"{self.rubrique.libelle} pour {self.contrat} : {self.montant}"

class LignePaie(models.Model):
    fiche_paie = models.ForeignKey(FichePaie, on_delete=models.CASCADE, related_name='lignes_paie')
    rubrique = models.ForeignKey(Rubrique, on_delete=models.PROTECT)
    valeur_saisie = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="La valeur saisie (%, heures, ou montant)")
    montant = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Le montant calculé final")
    
    def __str__(self):
        return f"{self.rubrique.libelle}: {self.montant}"
