from django.db import models
from app.models import *
from django.contrib.auth.models import User
from institut_app.models import *


class Employees(models.Model):
    
    nom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    civilite = models.CharField(max_length=100, null=True, blank=True, choices=[('mr','Mr.'),('mme','Mme'),('mlle','Mlle')])
    email = models.EmailField(null=True, blank=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)

    adresse = models.TextField(null=True, blank=True)

    prenom_pere = models.CharField(max_length=100, null=True, blank=True)
    nom_mere = models.CharField(max_length=100, null=True, blank=True)
    prenom_mere = models.CharField(max_length=100, null=True, blank=True)

    cin = models.CharField(max_length=255, null=True, blank=True)
    nin = models.CharField(max_length=255, null=True, blank=True)
    secu = models.CharField(max_length=255, null=True, blank=True) 

    situation_familiale = models.CharField(max_length=255, null=True, blank=True, choices=[('C', 'Célibataire'), ('M', 'Marié(e)'), ('D', 'Divorcé(e)'), ('V', 'Veuf(ve)')])
    genre = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Masculin'), ('F', 'Feminin')])

    groupe_sanguin = models.CharField(max_length=5, null=True, blank=True, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, null=True, blank=True)

    bank = models.CharField(max_length=255, null=True, blank=True)
    rib = models.CharField(max_length=25, null=True, blank=True, help_text="RIB Bancaire (20 chiffres)")
    ccp = models.CharField(max_length=20, null=True, blank=True, help_text="Compte CCP")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_contract = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    
    etat = models.CharField(max_length=100, null=True, blank=True, choices=[('en cours', "En cours d'activité"),('demission',"Démissionnaire")])
    
    # Probation (Période d'essai)
    date_debut_probation = models.DateField(null=True, blank=True)
    date_fin_probation = models.DateField(null=True, blank=True)
    
    # Congés
    solde_conge = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Solde de congé actuel (jours)")
    solde_conge_annee_prec = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Reliquat année précédente")
    is_particular_irg = models.BooleanField(default=False, verbose_name="Cas particulier IRG (Retraité / Handicapé)", help_text="Cochez pour appliquer le barème particulier de l'IRG")


    class Meta:
        verbose_name="Employe"
        verbose_name_plural="Employes"

    @property
    def date_recrutement(self):
        # Récupère la date d'embauche du dernier contrat en date
        last_contract = self.contrats.order_by('-date_embauche').first()
        return last_contract.date_embauche if last_contract else None

    def __str__(self):
        nom = self.nom or ""
        prenom = self.prenom or ""
        res = f"{nom} {prenom}".strip()
        return res if res else f"Employé #{self.id}"

class HRConfig(models.Model):
    # Horaires de travail
    heure_debut_standard = models.TimeField(default="08:00")
    heure_fin_standard = models.TimeField(default="16:30")
    
    # Paramètres congés
    quota_annuel_conge = models.IntegerField(default=30)
    cloture_conge_mois = models.IntegerField(default=6) # Juin
    cloture_conge_jour = models.IntegerField(default=30)
    
    # Paramètres Heures Sup
    taux_heure_sup_standard = models.DecimalField(max_digits=5, decimal_places=2, default=1.5) # +50%
    taux_heure_sup_75 = models.DecimalField(max_digits=5, decimal_places=2, default=1.75) # +75%
    taux_heure_sup_nuit = models.DecimalField(max_digits=5, decimal_places=2, default=2.0) # +100%
    
    # Majorations
    jours_supplementaires_sud = models.IntegerField(default=10, help_text="Jours de congé supplémentaires pour le Sud")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration RH"
        verbose_name_plural = "Configurations RH"

    def __str__(self):
        return "Paramètres Généraux RH"


class Presence(models.Model):
    STATUS_CHOICES = [
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('late', 'En retard'),
        ('half_day', 'Demi-journée'),
    ]

    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='presences')
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    note = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['employee', 'date']
        verbose_name = "Présence"
        verbose_name_plural = "Présences"

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"

class Absences(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='absences_rh')
    date_debut = models.DateField()
    date_fin = models.DateField()
    motif = models.TextField(null=True, blank=True)
    justifie = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Absence"
        verbose_name_plural = "Absences"

    def __str__(self):
        return f"{self.employee} - {self.date_debut} au {self.date_fin}"


class Services(models.Model):
    label = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Service"
        verbose_name_plural="Services"

    def __str__(self):
        return self.label

class Posts(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    service = models.ForeignKey(Services, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name="Poste"
        verbose_name_plural="Posts"

    def __str__(self):
        return self.label

class TachesPoste(models.Model):
    poste = models.ForeignKey(Posts, on_delete=models.CASCADE, null=True)
    label = models.CharField(max_length=100, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta: 
        verbose_name="Tache"
        verbose_name_plural = "Taches"
    
    def __str__(self):
        return self.label

class Conges(models.Model):
    class TypeConge(models.TextChoices):
        ANNUEL = 'ANNUEL', 'Congé Annuel'
        MALADIE = 'MALADIE', 'Congé Maladie'
        MATERNITE = 'MATERNITE', 'Congé Maternité'
        EXCEPTIONNEL = 'EXCEPTIONNEL', 'Congé Exceptionnel (Mariage, Décès, etc.)'
        SANS_SOLDE = 'SANS_SOLDE', 'Congé Sans Solde'
        RECUPERATION = 'RECUPERATION', 'Récupération'

    class StatusConge(models.TextChoices):
        BROUILLON = 'BROUILLON', 'Brouillon'
        EN_ATTENTE = 'EN_ATTENTE', 'En attente de validation'
        VALIDE = 'VALIDE', 'Validé'
        REFUSE = 'REFUSE', 'Refusé'
        ANNULE = 'ANNULE', 'Annulé'

    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='demandes_conge', null=True, blank=True)

    type_conge = models.CharField(max_length=20, choices=TypeConge.choices, default=TypeConge.ANNUEL)
    status = models.CharField(max_length=20, choices=StatusConge.choices, default=StatusConge.EN_ATTENTE)
    
    date_debut = models.DateField()
    date_fin = models.DateField()
    duree = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Nombre de jours ouvrables")
    
    motif = models.TextField(null=True, blank=True)
    justificatif = models.FileField(upload_to='conges/justificatifs/', null=True, blank=True)
    
    commentaire_rh = models.TextField(null=True, blank=True)
    valide_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='conges_valides')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Congé"
        verbose_name_plural="Congés"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.employee} - {self.type_conge} ({self.date_debut})"
    
class Paie(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True)

    salaire = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)
    date_paie = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Paie"
        verbose_name_plural="Paies"

    def __str__(self):
        return f"{self.employee.nom} {self.employee.prenom}"

class LigneFicheDePaie(models.Model):
    pass

class TemplateFichePaie(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    mode = models.CharField(max_length=100, null=True, blank=True, choices=[('vacataire','Enseignant vacataire'),('employe','Employe(e)')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Temple fiche de paie"
        verbose_name_plural = "Templates fiche de paie"

    def __str__(self):
        return self.label

class CategoriesContrat(models.Model):
    
    label = models.CharField(max_length=100, null=True)
    entite_legal = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    etat = models.CharField(max_length=100, null=True, choices=[('active', "Activé"),('disabled','Désactivé')], default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Catégorie de contrat"
        verbose_name_plural="Catégories de contrat"
    
    def __str__(self):
        return self.label

class TypesContrat(models.Model):
    label = models.CharField(max_length=255, null=True)
    categorie = models.ForeignKey(CategoriesContrat, null=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Type de contrat"
        verbose_name_plural="Types de contrat"

    def __str__(self):
        return self.label

class Contrats(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, null=True, blank=True, related_name="contrats")
    type_contrat = models.ForeignKey(TypesContrat, on_delete=models.CASCADE, null=True, blank=True, related_name="contrats")

    date_fin = models.DateField(null=True)

    poste = models.ForeignKey(Posts, null=True, on_delete=models.SET_NULL)
    service = models.ForeignKey('Services', on_delete=models.SET_NULL, null=True, blank=True)

    salaire_base = models.DecimalField(max_digits=200, decimal_places=2, null=True, blank=True)
    prime_panier = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prime_transport = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_embauche = models.DateField(null=True, blank=True)

    date_depart = models.DateField(null=True, blank=True)
    duree = models.CharField(max_length=100, null=True, blank=True)

    motif = models.TextField(null=True, blank=True)

    has_essai = models.BooleanField(null=True, blank=True)
    periode_essai = models.CharField(max_length=100, null=True, blank=True)
    mode_essei = models.CharField(max_length=100, null=True, blank=True, choices=[('m','Mois'),('a','Années')], default='m')
    observations = models.CharField(max_length=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name="Contrat"
        verbose_name_plural="Contrats"

    def __str__(self):
        return f"{self.employee.nom} {self.employee.prenom}"
    
class ArticlesContratStandard(models.Model):
    titre = models.CharField(max_length=255, blank=True, null=True)
    contenu = models.TextField(null=True)
    type_contrat = models.ForeignKey(TypesContrat, on_delete=models.CASCADE, null=True, blank=True, related_name="articles")

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.titre
    
class ArticleContratSpecial(models.Model):
    contrat = models.ForeignKey(Contrats, on_delete=models.CASCADE, null=True, blank=True, related_name="articles_special")

    label = models.CharField(max_length=255, blank=True)
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name="Article de contrat special"
        verbose_name_plural="Articles de contrat special"

    def __str__(self):
        return self.label