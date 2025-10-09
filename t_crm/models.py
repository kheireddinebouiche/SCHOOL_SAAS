from django.db import models
from django.contrib.auth.models import User
from t_formations.models import Formation,Specialites,Promos
from django_countries.fields import CountryField
from t_formations.models import DossierInscription
from .tenant_path import *
from t_remise.models import *
from phonenumber_field.modelfields import PhoneNumberField

INDICATIF = {
    '+1': '🇺🇸 +1 États-Unis / Canada',
    '+7': '🇷🇺 +7 Russie / Kazakhstan',
    '+20': '🇪🇬 +20 Égypte',
    '+27': '🇿🇦 +27 Afrique du Sud',
    '+30': '🇬🇷 +30 Grèce',
    '+31': '🇳🇱 +31 Pays-Bas',
    '+32': '🇧🇪 +32 Belgique',
    '+33': '🇫🇷 +33 France',
    '+34': '🇪🇸 +34 Espagne',
    '+36': '🇭🇺 +36 Hongrie',
    '+39': '🇮🇹 +39 Italie',
    '+40': '🇷🇴 +40 Roumanie',
    '+41': '🇨🇭 +41 Suisse',
    '+43': '🇦🇹 +43 Autriche',
    '+44': '🇬🇧 +44 Royaume-Uni',
    '+45': '🇩🇰 +45 Danemark',
    '+46': '🇸🇪 +46 Suède',
    '+47': '🇳🇴 +47 Norvège',
    '+48': '🇵🇱 +48 Pologne',
    '+49': '🇩🇪 +49 Allemagne',
    '+51': '🇵🇪 +51 Pérou',
    '+52': '🇲🇽 +52 Mexique',
    '+53': '🇨🇺 +53 Cuba',
    '+54': '🇦🇷 +54 Argentine',
    '+55': '🇧🇷 +55 Brésil',
    '+56': '🇨🇱 +56 Chili',
    '+57': '🇨🇴 +57 Colombie',
    '+58': '🇻🇪 +58 Venezuela',
    '+60': '🇲🇾 +60 Malaisie',
    '+61': '🇦🇺 +61 Australie',
    '+62': '🇮🇩 +62 Indonésie',
    '+63': '🇵🇭 +63 Philippines',
    '+64': '🇳🇿 +64 Nouvelle-Zélande',
    '+65': '🇸🇬 +65 Singapour',
    '+66': '🇹🇭 +66 Thaïlande',
    '+81': '🇯🇵 +81 Japon',
    '+82': '🇰🇷 +82 Corée du Sud',
    '+84': '🇻🇳 +84 Vietnam',
    '+86': '🇨🇳 +86 Chine',
    '+90': '🇹🇷 +90 Turquie',
    '+91': '🇮🇳 +91 Inde',
    '+92': '🇵🇰 +92 Pakistan',
    '+93': '🇦🇫 +93 Afghanistan',
    '+94': '🇱🇰 +94 Sri Lanka',
    '+95': '🇲🇲 +95 Myanmar',
    '+98': '🇮🇷 +98 Iran',
    '+211': '🇸🇸 +211 Soudan du Sud',
    '+212': '🇲🇦 +212 Maroc',
    '+213': '🇩🇿 +213 Algérie',
    '+216': '🇹🇳 +216 Tunisie',
    '+218': '🇱🇾 +218 Libye',
    '+220': '🇬🇲 +220 Gambie',
    '+221': '🇸🇳 +221 Sénégal',
    '+222': '🇲🇷 +222 Mauritanie',
    '+223': '🇲🇱 +223 Mali',
    '+224': '🇬🇳 +224 Guinée',
    '+225': '🇨🇮 +225 Côte d’Ivoire',
    '+226': '🇧🇫 +226 Burkina Faso',
    '+227': '🇳🇪 +227 Niger',
    '+228': '🇹🇬 +228 Togo',
    '+229': '🇧🇯 +229 Bénin',
    '+230': '🇲🇺 +230 Maurice',
    '+231': '🇱🇷 +231 Libéria',
    '+232': '🇸🇱 +232 Sierra Leone',
    '+233': '🇬🇭 +233 Ghana',
    '+234': '🇳🇬 +234 Nigeria',
    '+235': '🇹🇩 +235 Tchad',
    '+236': '🇨🇲 +236 Cameroun',
    '+237': '🇨🇫 +237 République centrafricaine',
    '+238': '🇨🇻 +238 Cap-Vert',
    '+239': '🇸🇹 +239 Sao Tomé et Principe',
    '+240': '🇬🇶 +240 Guinée équatoriale',
    '+241': '🇬🇦 +241 Gabon',
    '+242': '🇨🇬 +242 Congo-Brazzaville',
    '+243': '🇨🇩 +243 République démocratique du Congo',
    '+244': '🇦🇴 +244 Angola',
    '+245': '🇬🇼 +245 Guinée-Bissau',
    '+246': '🇮🇴 +246 Territoire britannique de l’océan Indien',
    '+248': '🇸🇨 +248 Seychelles',
    '+249': '🇸🇩 +249 Soudan',
    '+250': '🇷🇼 +250 Rwanda',
    '+251': '🇪🇹 +251 Éthiopie',
    '+252': '🇸🇴 +252 Somalie',
    '+253': '🇩🇯 +253 Djibouti',
    '+254': '🇰🇪 +254 Kenya',
    '+255': '🇹🇿 +255 Tanzanie',
    '+256': '🇺🇬 +256 Ouganda',
    '+257': '🇧🇮 +257 Burundi',
    '+258': '🇲🇿 +258 Mozambique',
    '+260': '🇿🇲 +260 Zambie',
    '+261': '🇲🇬 +261 Madagascar',
    '+262': '🇷🇪 +262 La Réunion',
    '+263': '🇿🇼 +263 Zimbabwe',
    '+264': '🇳🇦 +264 Namibie',
    '+265': '🇲🇼 +265 Malawi',
    '+266': '🇱🇸 +266 Lesotho',
    '+267': '🇧🇼 +267 Botswana',
    '+268': '🇸🇿 +268 Eswatini',
    '+269': '🇰🇲 +269 Comores',
    '+290': '🇸🇭 +290 Sainte-Hélène',
    '+291': '🇪🇷 +291 Érythrée',
    '+297': '🇦🇼 +297 Aruba',
    '+298': '🇫🇴 +298 Îles Féroé',
    '+299': '🇬🇱 +299 Groenland',
    '+350': '🇬🇮 +350 Gibraltar',
    '+351': '🇵🇹 +351 Portugal',
    '+352': '🇱🇺 +352 Luxembourg',
    '+353': '🇮🇪 +353 Irlande',
    '+354': '🇮🇸 +354 Islande',
    '+355': '🇦🇱 +355 Albanie',
    '+356': '🇲🇹 +356 Malte',
    '+357': '🇨🇾 +357 Chypre',
    '+358': '🇫🇮 +358 Finlande',
    '+359': '🇧🇬 +359 Bulgarie',
    '+370': '🇱🇹 +370 Lituanie',
    '+371': '🇱🇻 +371 Lettonie',
    '+372': '🇪🇪 +372 Estonie',
    '+373': '🇲🇩 +373 Moldavie',
    '+374': '🇦🇲 +374 Arménie',
    '+375': '🇧🇾 +375 Biélorussie',
    '+376': '🇦🇩 +376 Andorre',
    '+377': '🇲🇨 +377 Monaco',
    '+378': '🇸🇲 +378 Saint-Marin',
    '+380': '🇺🇦 +380 Ukraine',
    '+381': '🇷🇸 +381 Serbie',
    '+382': '🇲🇪 +382 Monténégro',
    '+385': '🇭🇷 +385 Croatie',
    '+386': '🇸🇮 +386 Slovénie',
    '+387': '🇧🇦 +387 Bosnie-Herzégovine',
    '+389': '🇲🇰 +389 Macédoine du Nord',
    '+420': '🇨🇿 +420 République tchèque',
    '+421': '🇸🇰 +421 Slovaquie',
    '+423': '🇱🇮 +423 Liechtenstein',
    '+500': '🇫🇰 +500 Îles Malouines',
    '+501': '🇧🇿 +501 Belize',
    '+502': '🇬🇹 +502 Guatemala',
    '+503': '🇸🇻 +503 Salvador',
    '+504': '🇭🇳 +504 Honduras',
    '+505': '🇳🇮 +505 Nicaragua',
    '+506': '🇨🇷 +506 Costa Rica',
    '+507': '🇵🇦 +507 Panama',
    '+508': '🇸🇧 +508 Saint-Pierre-et-Miquelon',
    '+509': '🇭🇹 +509 Haïti',
    '+590': '🇬🇵 +590 Guadeloupe',
    '+591': '🇧🇴 +591 Bolivie',
    '+592': '🇬🇾 +592 Guyana',
    '+593': '🇪🇨 +593 Équateur',
    '+594': '🇬🇫 +594 Guyane française',
    '+595': '🇵🇾 +595 Paraguay',
    '+596': '🇲🇶 +596 Martinique',
    '+597': '🇸🇷 +597 Suriname',
    '+598': '🇺🇾 +598 Uruguay',
    '+599': '🇨🇼 +599 Curaçao',
}


class Prospets(models.Model):
    nin = models.CharField(max_length=255, null=True, blank=True)
    nom = models.CharField(max_length=255, null=True)
    photo = models.ImageField(upload_to=tenant_directory_path_for_image, null=True, blank=True)

    lead_source = models.CharField(max_length=100, null=True, blank=True, choices=[('viste','Visite'),('appel','Appel'),('prospectus','Prospectus')])
    
    prenom = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    indic = models.CharField(max_length=10, null=True, blank=True, choices=INDICATIF)
    telephone = models.CharField(max_length=14, null=True, blank=True)
    type_prospect = models.CharField(max_length=255, null=True, choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')])
    canal = models.CharField(max_length=255, null=True, choices=[('email', 'Email'), ('telephone', 'Téléphone'), ('autre', 'Autre'),('facebook', 'Facebook'),('linkedin', 'LinkedIn'),('instagram', 'Instagram' ),('tiktok', 'TikTok'),('bouche-a-oreille', 'Bouche à oreille'),('site','Site Web'),('prospectus','Prospectus'),('pub','Publicitée')])
    etat = models.CharField(max_length=255, null=True, blank=True, default='en_attente', choices=[('en_attente', 'En attente'), ('accepte', 'Accepté'), ('rejete', 'Rejeté')])
    nationnalite = models.CharField(max_length=100, null=True, blank=True)
    entreprise = models.CharField(max_length=255, null=True, blank=True)
    poste_dans_entreprise = models.CharField(max_length=100, null=True, blank=True, choices=[('salarie', 'Salarié'),('responsable','Résponsable'),('directeur','Directeur'),('gerant','Gérant')])
    observation = models.TextField(null=True, blank=True)

    motif_rejet = models.CharField(max_length=100, null=True, blank=True)

    groupe_sanguin = models.CharField(max_length=100, null=True, blank=True, choices=[('a-','A-'),('a+','A+'),('b+','B+'),('b-','B+'),('ab-','AB-'),('ab+','AB+'),('o-','o-'),('o+','o+')])
    nom_arabe = models.CharField(max_length=100, null=True, blank=True)
    prenom_arabe = models.CharField(max_length=100, null=True, blank=True)
    
    prenom_pere = models.CharField(max_length=100, null=True, blank=True)
    indic1 = models.CharField(max_length=10, null=True, blank=True, choices=INDICATIF)
    tel_pere = models.CharField(max_length=100, null=True, blank=True)

    nom_mere = models.CharField(max_length=100, null=True, blank=True)
    prenom_mere = models.CharField(max_length=100, null=True, blank=True)
    indic2 = models.CharField(max_length=10, null=True, blank=True, choices=INDICATIF)
    tel_mere = models.CharField(max_length=100, null=True, blank=True)

    has_endicap = models.BooleanField(default=False, null=True, blank=True)
    type_handicap = models.CharField(max_length=1000, null=True, blank=True)

    adresse = models.CharField(max_length=1000, null=True, blank=True)
    pays = models.CharField(max_length=100, null=True, blank=True)
    wilaya = models.CharField(max_length=100, null=True, blank=True)
    code_zip = models.CharField(max_length=100, null=True, blank=True)

    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(null=True, blank=True)
        
    niveau_scolaire = models.CharField(max_length=100, null=True, blank=True, choices=[('1_am','1 am'),('2_am','2 am'),('3_am', '3_am'),('4_am','4 am'),('1_as','1 AS'),('2_as','2 AS'),('terminal','Terminal'),('bac1','BAC +1'),('bac2','BAC +2'),('licence','Licence'),('m','Master')])
    diplome = models.CharField(max_length=100, null=True, blank=True)
    etablissement = models.CharField(max_length=100, null=True, blank=True)
    statut = models.CharField(max_length=100, null=True, blank=True, default='visiteur', choices=[('visiteur','Visiteur'),('prinscrit','Pré-inscript'),('instance','Instance de paiement'),('convertit','Convertit'),('annuler','Inscription Annulé')])

    profile_completed = models.BooleanField(default=False)
    has_completed_doc = models.BooleanField(default=False)
    has_derogation = models.BooleanField(default = False)
    has_second_wish = models.BooleanField(default=False)

    is_ets_prospect = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    has_special_echeancier = models.BooleanField(default=False)

    context = models.CharField(max_length=100, null=True, blank=True, choices=[('acc','Acceuil'),('con','Conseil')])

    contact_situation = models.CharField(max_length=100, null=True, blank=True, choices=[('fist_contact','Premiere visiste'),('a_appeler','Appelle téléphonique'),('est_passer','Visiste')])

    has_refund = models.BooleanField(default=False)

    prospect_date= models.DateField(null=True,blank=True)
    preinscri_date= models.DateField(null=True, blank=True)
    instance_date = models.DateField(null=True, blank=True)
    convertit_date = models.DateField(null=True, blank=True)

    is_affected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prospect"
        verbose_name_plural = "Prospects"

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class FicheDeVoeux(models.Model):
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True, related_name="prospect_fiche_voeux")
    specialite = models.ForeignKey(Specialites, on_delete=models.SET_NULL, null=True, blank=True, related_name="specialite_fiche_voeux")
    promo = models.ForeignKey(Promos, on_delete=models.SET_NULL, null=True, blank=True, related_name="promo_fiche_voeux", limit_choices_to={'etat':'active'})
    commentaire = models.CharField(max_length=1000, null=True, blank=True)

    is_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fiche de Voeux"
        verbose_name_plural = "Fiches de Voeux"
    
    def __str__(self):
        return f"Fiche de Voeux for {self.prospect.nom} {self.prospect.prenom}"
    
class FicheDeVoeuxAddiotionnel(models.Model):
    order = models.CharField(max_length=10, null=True, blank=True)
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    specialite = models.ForeignKey(Specialites, on_delete=models.SET_NULL, null=True, blank=True)
    promo = models.ForeignKey(Promos, on_delete=models.SET_NULL, null=True, blank=True, related_name="promo_fiche_voeux_secondaire", limit_choices_to={'etat':'active'})
    commentaire = models.CharField(max_length=1000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fiche de Voeux secondaire"
        verbose_name_plural = "Fiches de Voeux secondaire"
    
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
    statut = models.CharField(max_length=255, null=True, blank=True, default='en_attente', choices=[('en_attente', 'En attente'), ('confirme', 'Confirmé'), ('annule', 'Annulé'), ('termine', 'Terminé'),('abouti','Abouti'),('nabouti','Non abouti')])

    date_rendez_vous = models.DateField(null=True, blank=True)
    heure_rendez_vous = models.TimeField(null=True, blank=True)

    context= models.CharField(max_length=100, null=True, blank=True)

    observation = models.CharField(max_length=100, null=True, blank=True)

    archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rendez-vous {self.id} - {self.type} - {self.date_rendez_vous} {self.heure_rendez_vous}"

class Derogations(models.Model):
    demandeur = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    motif = models.CharField(max_length=100, null=True, blank=True)
    date_de_demande = models.DateField(auto_now_add=True)
    statut = models.CharField(max_length=100, null=True, blank=True, choices=[('en_attente','En attente'),('acceptee','Acceptée'),('rejetee','Rejetée')], default="en_attente")
    date_de_traitement = models.DateField(null=True, blank=True, auto_now_add=True)
    observation = models.CharField(max_length=1000, null=True, blank=True)
    etat = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __stre__(self):
        return f"{self.demandeur.nom} {self.demandeur.prenom}"
  
class CrmCounter(models.Model):
    date_counter = models.DateField(null=True, blank=True)
    visite_counter = models.IntegerField(default=0)
    phone_counter = models.IntegerField(default=0)

    def __str__(self):
        return self.date_counter
    
class RemiseAppliquer(models.Model):
    remise  = models.ForeignKey(Remises, on_delete=models.CASCADE, null=True, blank=True)
    is_approuved = models.BooleanField(default=False)
    is_applicated = models.BooleanField(default=False)
    fichie_justificatif = models.FileField(upload_to=tenant_directory_path, null=True, blank=True)
    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.remise.label
    
class RemiseAppliquerLine(models.Model):
    remise_appliquer = models.ForeignKey(RemiseAppliquer, null=True, blank=True, on_delete=models.CASCADE)
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.prospect.nom} - {self.prenom}'
    




