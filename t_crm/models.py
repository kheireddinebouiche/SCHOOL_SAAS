from django.db import models
from django.contrib.auth.models import User
from t_formations.models import Formation,Specialites,Promos
from django_countries.fields import CountryField


class Prospets(models.Model):
    nin = models.CharField(max_length=255, null=True, blank=True)
    nom = models.CharField(max_length=255, null=True)
    prenom = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    telephone = models.CharField(max_length=15, null=True)
    type_prospect = models.CharField(max_length=255, null=True, choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')])
    canal = models.CharField(max_length=255, null=True, choices=[('email', 'Email'), ('telephone', 'Téléphone'), ('autre', 'Autre')])
    etat = models.CharField(max_length=255, null=True, blank=True, default='en_attente', choices=[('en_attente', 'En attente'), ('accepte', 'Accepté'), ('rejete', 'Rejeté')])

    observation = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prospect"
        verbose_name_plural = "Prospects"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class FicheDeVoeux(models.Model):
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    specialite = models.ForeignKey(Specialites, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fiche de Voeux"
        verbose_name_plural = "Fiches de Voeux"
    
    def __str__(self):
        return f"Fiche de Voeux for {self.prospect.nom} {self.prospect.prenom}"

class Visiteurs(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    civilite = models.CharField(max_length=255, null=True, choices=[('monsieur', 'Mr.'), ('madame', 'Mme')])
    nom = models.CharField(max_length=255, null=True)
    prenom = models.CharField(max_length=255, null=True)
    date_naissance = models.DateField(null=True)
    lieu_naissance = models.CharField(max_length=255, null=True)

    email = models.EmailField(null=True)
    telephone = models.CharField(max_length=15, null=True)

    adresse = models.TextField(null=True)
    pays = CountryField(null=True)

    type_visiteur = models.CharField(max_length=255, null=True, choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    has_paied_enrollment = models.BooleanField(default=False)
    has_completed_documents = models.BooleanField(default=False)
    has_paid_fees = models.BooleanField(default=False)

    cin = models.CharField(max_length=255, null=True, blank=True)

    niveau_etude = models.CharField(max_length=255, null=True, blank=True, choices=[('9af','9 AF/ 4 AM'),('1as','1 AS/2 AS'),('ter','Terminal'),('bac', 'Bac'), ('bac+2', 'Bac+2'), ('bac+3', 'Bac+3'), ('bac+4', 'Bac+4'), ('bac+5', 'Bac+5')])

    situation_family = models.CharField(max_length=255, null=True, blank=True, choices=[('celibataire', 'Célibataire'), ('marie', 'Marié(e)')])
    situation_professionnelle = models.CharField(max_length=255, null=True, blank=True, choices=[('etudiant', 'Etudiant(e)'), ('salarié', 'Salarié(e)'), ('employeur', 'Employeur'),('sans_emploi', 'Sans emploi')])
    post_occupe = models.CharField(max_length=255, null=True, blank=True)
    experience = models.CharField(max_length=255, null=True, blank=True)
    entreprise = models.CharField(max_length=255, null=True, blank=True)

    is_student = models.BooleanField(default=False)
    is_entreprise = models.BooleanField(default=False)

    etat = models.CharField(max_length=255, null=True, blank=True, default='visiteur' , choices=[('visiteur','Visiteur'),('instance', 'En Instance'),('en_attente', 'En attente'), ('inscrit', 'Inscrit'), ('rejete', 'Rejeté')])
    
    observation = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name="Visiteur"
        verbose_name_plural = "Visiteurs"

    def __str__(self):
        return f"{self.nom} {self.prenom}"
    
class DemandeInscription(models.Model):
    visiteur = models.ForeignKey(Visiteurs, on_delete=models.CASCADE, null=True, blank=True)
    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True, blank=True)
    specialite = models.ForeignKey(Specialites, on_delete=models.SET_NULL, null=True, blank=True)
    promo = models.ForeignKey(Promos, on_delete=models.SET_NULL, null=True, blank=True, related_name="promo_demande_inscription", limit_choices_to={'etat':'active'})
    formule = models.CharField(max_length=255, null=True, blank=True, choices=[('week', 'Week-End'), ('jour', 'Cours du jour'), ('soir', 'Cours du soir')])
    session = models.CharField(max_length=255, null=True, blank=True, choices=[('octobre', 'Octobre'), ('mars', 'mars')])
    etat = models.CharField(max_length=255, null=True, blank=True, default='en_attente', choices=[('annulation_approuver' , 'Demande d\'annulation approuvée'),('annulation', 'Demande d\'annulation'),('en_attente', 'En attente'), ('accepte', 'Accepté'), ('rejete', 'Rejeté'),('paiment','Procédure de paiement')])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name="created_by_demande_inscription")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_by_demande_inscription")

    class Meta:
        verbose_name="Demande d'inscription"
        verbose_name_plural = "Demandes d'inscription"

    def __str__(self):
        return f"{self.visiteur.nom} + {self.visiteur.prenom} - {self.specialite.label}"

class DocumentsDemandeInscription(models.Model):
    demande_inscription = models.ForeignKey(DemandeInscription, on_delete=models.CASCADE, null=True, blank=True)
    cin = models.FileField(upload_to='documents/cin/', null=True, blank=True)
    bac = models.FileField(upload_to='documents/bac/', null=True, blank=True)
    diplome = models.FileField(upload_to='documents/diplome/', null=True, blank=True)
    photo = models.FileField(upload_to='documents/photo/', null=True, blank=True)
    cv = models.FileField(upload_to='documents/cv/', null=True, blank=True)

    class Meta:
        verbose_name="Documents de la demande d'inscription"
        verbose_name_plural = "Documents de la demande d'inscription"

    def __str__(self):
        return f"Documents for {self.demande_inscription.visiteur.nom} {self.demande_inscription.visiteur.prenom}"

class RelancesProspet(models.Model):
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    date_relance = models.DateField(null=True, blank=True)
    canal = models.CharField(max_length=255, null=True, choices=[('email', 'Email'), ('telephone', 'Téléphone'), ('autre', 'Autre')])
    observation = models.TextField(null=True, blank=True)
    etat = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Relance de Prospect"
        verbose_name_plural = "Relances de Prospects"

    def __str__(self):
        return f"Relance for {self.prospect.nom} {self.prospect.prenom}"
