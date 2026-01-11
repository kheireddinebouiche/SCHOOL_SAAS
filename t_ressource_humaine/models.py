from django.db import models
from django.contrib.auth.models import User
from t_formations.models import Formateurs

class TypeContrat(models.TextChoices):
    CDI = 'CDI', 'Contrat à Durée Indéterminée'
    CDD = 'CDD', 'Contrat à Durée Déterminée'
    VACATION = 'VACATION', 'Vacation (Paiement à l\'heure)'

class Contrat(models.Model):
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
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contrat {self.get_type_contrat_display()} - {self.formateur}"

class FichePaie(models.Model):
    MOIS_CHOICES = [
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ]
    
    contrat = models.ForeignKey(Contrat, on_delete=models.CASCADE, related_name='fiches_paie')
    mois = models.IntegerField(choices=MOIS_CHOICES)
    annee = models.IntegerField()
    
    # Variables du mois
    jours_travailles = models.IntegerField(default=22) # Standard 22 working days
    heures_travailles = models.DecimalField(max_digits=6, decimal_places=2, default=0, help_text="Pour les vacataires")
    
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
        ordering = ['-annee', '-mois']

    def __str__(self):
        return f"Fiche {self.mois}/{self.annee} - {self.contrat.formateur}"
