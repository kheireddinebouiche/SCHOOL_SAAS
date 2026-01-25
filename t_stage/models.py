from django.db import models
from t_crm.models import Prospets
from t_formations.models import Formateurs
from t_groupe.models import Groupe

class Stage(models.Model):
    CHOICES_STATUT = [
        ('en_cours', 'En cours'),
        ('soutenu', 'Soutenu'),
        ('ajourne', 'Ajourné'),
        ('annule', 'Annulé'),
    ]
    
    # Context
    groupe = models.ForeignKey(Groupe, on_delete=models.SET_NULL, null=True, blank=True, related_name='stages')
    
    # Un stage peut avoir plusieurs étudiants
    etudiants = models.ManyToManyField(Prospets, related_name='stages')
    
    encadrant = models.ForeignKey(Formateurs, on_delete=models.SET_NULL, null=True, blank=True, related_name='stages_encadres')
    
    sujet = models.CharField(max_length=500)
    problematique = models.TextField(null=True, blank=True)
    plan_previsionnel = models.TextField(null=True, blank=True)
    
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    
    taux_avancement = models.IntegerField(default=0, help_text="Taux d'avancement global (0-100%)")
    statut = models.CharField(max_length=20, choices=CHOICES_STATUT, default='en_cours')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Stage"
        verbose_name_plural = "Stages"

    def __str__(self):
        membres = f"{self.etudiant1}"
        if self.etudiant2:
            membres += f" & {self.etudiant2}"
        return f"{membres} - {self.sujet[:50]}..."

class FocusGroup(models.Model):
    nom = models.CharField(max_length=255)
    encadrant = models.ForeignKey(Formateurs, on_delete=models.CASCADE, related_name='focus_groups')
    thematique = models.CharField(max_length=255, null=True, blank=True)
    stages = models.ManyToManyField(Stage, related_name='focus_groups_membership', blank=True)
    
    date_creation = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Focus Group"
        verbose_name_plural = "Focus Groups"

    def __str__(self):
        return f"{self.nom} ({self.encadrant})"

class SeanceFocusGroup(models.Model):
    focus_group = models.ForeignKey(FocusGroup, on_delete=models.CASCADE, related_name='seances')
    date_seance = models.DateTimeField()
    duree_heures = models.DecimalField(max_digits=4, decimal_places=2, default=3.0, help_text="Durée en heures (ex: 3.5)")
    compte_rendu = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Séance Focus Group"
        verbose_name_plural = "Séances Focus Groups"

    def __str__(self):
        return f"Séance {self.focus_group.nom} du {self.date_seance.strftime('%d/%m/%Y')}"

class PresentationProgressive(models.Model):
    CHOICES_ETAPE = [
        (1, '1ère Présentation (25-35%)'),
        (2, '2ème Présentation (65-75%)'),
        (3, '3ème Présentation / Soutenance à blanc (~90%)'),
    ]
    
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='presentations')
    etape = models.IntegerField(choices=CHOICES_ETAPE)
    date_presentation = models.DateField()
    
    taux_avancement_declare = models.IntegerField(help_text="Taux d'avancement déclaré par le stagiaire")
    observations = models.TextField(null=True, blank=True)
    corrections_exigees = models.TextField(null=True, blank=True)
    delai_correction = models.DateField(null=True, blank=True, help_text="Délai maximum pour réaliser les corrections (ex: 15 jours)")
    
    validee = models.BooleanField(default=False, help_text="Cocher si la présentation est validée par l'encadrant")
    
    # Pour la soutenance à blanc (etape 3)
    examinateur = models.ForeignKey(Formateurs, on_delete=models.SET_NULL, null=True, blank=True, related_name='examinateur_presentations')

    class Meta:
        verbose_name = "Présentation Progressive"
        verbose_name_plural = "Présentations Progressives"
        unique_together = ['stage', 'etape']

    def __str__(self):
        return f"P{self.etape} - {self.stage}"

class ConseilValidation(models.Model):
    date_conseil = models.DateField()
    observations_generales = models.TextField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Conseil de Validation"
        verbose_name_plural = "Conseils de Validation"

    def __str__(self):
        return f"Conseil du {self.date_conseil.strftime('%d/%m/%Y')}"

class DecisionConseil(models.Model):
    CHOICES_DECISION = [
        ('soutenable', 'Soutenable (Lancement de la soutenance officielle)'),
        ('ajourne', 'Ajourné (Délai supplémentaire de 2 mois)'),
    ]
    
    conseil = models.ForeignKey(ConseilValidation, on_delete=models.CASCADE, related_name='decisions')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='decisions_conseil')
    decision = models.CharField(max_length=20, choices=CHOICES_DECISION)
    commentaire = models.TextField(null=True, blank=True)
    taux_final = models.IntegerField(help_text="Taux d'achèvement final constaté (95-100%)")

    class Meta:
        verbose_name = "Décision de Conseil"
        verbose_name_plural = "Décisions de Conseil"
        unique_together = ['conseil', 'stage']

    def __str__(self):
        return f"Décision {self.stage} : {self.get_decision_display()}"
