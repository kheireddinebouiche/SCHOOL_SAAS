from django.db import models
from django.contrib.auth.models import User
from t_formations.models import Formation,Specialites,Promos
from django_countries.fields import CountryField
from t_formations.models import DossierInscription
from .tenant_path import *

class Prospets(models.Model):
    nin = models.CharField(max_length=255, null=True, blank=True)
    nom = models.CharField(max_length=255, null=True)
    photo = models.ImageField(upload_to=tenant_directory_path_for_image, null=True, blank=True)
    
    prenom = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    telephone = models.CharField(max_length=15, null=True)
    type_prospect = models.CharField(max_length=255, null=True, choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')])
    canal = models.CharField(max_length=255, null=True, choices=[('email', 'Email'), ('telephone', 'Téléphone'), ('autre', 'Autre'),('facebook', 'Facebook'),('linkedin', 'LinkedIn'),('instagram', 'Instagram' ),('tiktok', 'TikTok')])
    etat = models.CharField(max_length=255, null=True, blank=True, default='en_attente', choices=[('en_attente', 'En attente'), ('accepte', 'Accepté'), ('rejete', 'Rejeté')])

    entreprise = models.CharField(max_length=255, null=True, blank=True)
    poste_dans_entreprise = models.CharField(max_length=100, null=True, blank=True, choices=[('salarie', 'Salarié'),('responsable','Résponsable'),('directeur','Directeur'),('gerant','Gérant')])
    observation = models.TextField(null=True, blank=True)

    motif_rejet = models.CharField(max_length=100, null=True, blank=True)

    groupe_sanguin = models.CharField(max_length=100, null=True, blank=True, choices=[('a-','A-'),('a+','A+'),('b+','B+'),('b-','B+'),('ab-','AB-'),('ab+','AB+'),('o-','o-'),('o+','o+')])
    nom_arabe = models.CharField(max_length=100, null=True, blank=True)
    prenom_arabe = models.CharField(max_length=100, null=True, blank=True)
    
    prenom_pere = models.CharField(max_length=100, null=True, blank=True)
    tel_pere = models.CharField(max_length=100, null=True, blank=True)

    nom_mere = models.CharField(max_length=100, null=True, blank=True)
    prenom_mere = models.CharField(max_length=100, null=True, blank=True)
    tel_mere = models.CharField(max_length=100, null=True, blank=True)

    has_endicap = models.BooleanField(default=False, null=True, blank=True)
    type_handicap = models.CharField(max_length=1000, null=True, blank=True)

    adresse = models.TextField(null=True, blank=True)

    date_naissance = models.DateField(null=True, blank=True)
        
    niveau_scolaire = models.CharField(max_length=100, null=True, blank=True, choices=[('1_am','1 am'),('2_am','2 am'),('3_am', '3_am'),('4_am','4 am'),('1_as','1 AS'),('2_as','2 AS'),('terminal','Terminal'),('bac1','BAC +1'),('bac2','BAC +2'),('licence','Licence'),('m','Master')])
    diplome = models.CharField(max_length=100, null=True, blank=True)
    etablissement = models.CharField(max_length=100, null=True, blank=True)
    statut = models.CharField(max_length=100, null=True, blank=True, default='visiteur', choices=[('visiteur','Visiteur'),('prinscrit','Pré-inscript'),('instance','Instance'),('convertit','Convertit')])

    profile_completed = models.BooleanField(default=False)
    has_completed_doc = models.BooleanField(default=False)
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

    commentaire = models.CharField(max_length=1000, null=True, blank=True)

    is_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fiche de Voeux"
        verbose_name_plural = "Fiches de Voeux"
    
    def __str__(self):
        return f"Fiche de Voeux for {self.prospect.nom} {self.prospect.prenom}"

class NotesProcpects(models.Model):
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    tage = models.CharField(max_length=255, null=True, blank=True,choices=[('important', 'Important'), ('a_revoir', 'A revoir'), ('a_contacte', 'A contacter'), ('a_relancer', 'A relancer')])
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    context= models.CharField(max_length=100, null=True, blank=True)
    is_done = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Note de Prospect"
        verbose_name_plural = "Notes de Prospects"

    def __str__(self):
        return f"Note for {self.prospect.nom} {self.prospect.prenom}"

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
    fiche_voeux = models.ForeignKey(FicheDeVoeux, blank=True, null=True, on_delete=models.CASCADE)
    prospect = models.ForeignKey(Prospets, null=True, blank=True, on_delete=models.CASCADE)
    id_document = models.ForeignKey(DossierInscription, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=tenant_directory_path, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        verbose_name="Documents de la demande d'inscription"
        verbose_name_plural = "Documents de la demande d'inscription"

    def __str__(self):
        return f"Documents for {self.demande_inscription.visiteur.nom} {self.demande_inscription.visiteur.prenom}"

class RelancesProspet(models.Model):
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    date_relance = models.DateField(null=True, blank=True)
    canal = models.CharField(max_length=255, null=True, choices=[('email', 'Email'), ('telephone', 'Téléphone'), ('autre', 'Autre')])
    objet = models.CharField(max_length=255, null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    etat = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Relance de Prospect"
        verbose_name_plural = "Relances de Prospects"

    def __str__(self):
        return f"Relance for {self.prospect.nom} {self.prospect.prenom}"

class RendezVous(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=255, null=True, choices=[('appel', 'Appel'), ('email', 'Email'),('rendez_vous','Rendez-vous'), ('autre', 'Autre')])
    object = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    statut = models.CharField(max_length=255, null=True, blank=True, default='en_attente', choices=[('en_attente', 'En attente'), ('confirme', 'Confirmé'), ('annule', 'Annulé'), ('termine', 'Terminé')])

    date_rendez_vous = models.DateField(null=True, blank=True)
    heure_rendez_vous = models.TimeField(null=True, blank=True)

    context= models.CharField(max_length=100, null=True, blank=True)

    observation = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rendez-vous {self.id} - {self.type} - {self.date_rendez_vous} {self.heure_rendez_vous}"

