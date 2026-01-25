from django.db import models
from t_etudiants.models import *
from institut_app.models import *
from t_formations.models import *
from t_crm.models import Prospets
from django.contrib.auth.models import User
import datetime
from django.db import models
from django.db.models import Max


class ClientPaiementsRequest(models.Model):
    
    client = models.ForeignKey(Prospets, on_delete=models.DO_NOTHING, null=True, blank=True)
    promo = models.ForeignKey(Promos, on_delete=models.CASCADE, null=True , blank=True)

    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, null=True, blank=True)
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True, blank=True)
    specialite_double = models.ForeignKey(DoubleDiplomation, on_delete=models.CASCADE, null=True, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid = models.BooleanField(default=False)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('tranche','Tranche'), ('mensuelle','Mensuelle'), ('totalite','Paiement unique')])

    motif = models.CharField(max_length=100, null=True, blank=True, choices=[('frais_f', 'Frais de formation'),('frais', 'Frais d\'admission'),('autre','Autres'),('dette','Module en dette'),('rach','Rachât de crédit')])

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    etat = models.CharField(max_length=100, null=True, blank=True, default='en_attente' ,choices=[('en_attente','En Attente'),('annulation','Demande d\'annulation'),('annulation_approuver','Demande d\'annulation approuvée'),('terminer','Cloturer')])
    approuved_annulation = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Demande de paiement"
        verbose_name_plural = "Demandes de paiement"

    def __str__(self):
        return f"{self.client.nom}"

class clientPaiementsRequestLine(models.Model):
    paiement_request = models.ForeignKey(ClientPaiementsRequest, on_delete=models.DO_NOTHING, null=True)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_paiement = models.DateField(null=True)
    observation = models.CharField(max_length=1000, null=True, blank=True)
    motif_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('fin','Frais d\'inscription'),('ass','Assurance'),('frf','Frais de formation')])
    etat = models.CharField(max_length=100, null=True, blank=True, choices=[('auc','Aucun paiement effectué'),('part','Paiement partiel'), ('tot','Paiement cash'),('ter','Paiement terminé')], default="auc")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.paiement_request

class DuePaiements(models.Model):

    client = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    ordre = models.IntegerField(null=True, blank=True)
    ref_echeancier = models.ForeignKey('EcheancierPaiement', null=True, blank=True, on_delete=models.SET_NULL)
    montant_due = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    montant_restant = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    date_echeance = models.DateField(null=True, blank=True)

    is_done = models.BooleanField(default=False)
    is_annulated= models.BooleanField(default=False)
    promo = models.ForeignKey(Promos, on_delete=models.CASCADE, null=True, blank=True, related_name="due_paiement_promo")
    type = models.CharField(max_length=100, null=True, blank=True, choices=[('frais_f',"Frais de formation"),('dette','Module en dette'),('autre','Autre'),('rach','Rachât de crédit')])
    observation = models.CharField(max_length=1000, null=True, blank=True)

    entite = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.label

class Paiements(models.Model):
    num = models.CharField(max_length=100, null=True, blank=True, unique=True, help_text="Numéro séquentiel de paiement")
    due_paiements = models.ForeignKey(DuePaiements, on_delete=models.CASCADE, null=True, blank=True)
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True, related_name="paiements")
    montant_paye = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    observation = models.CharField(max_length=100, null=True, blank=True)

    mode_paiement = models.CharField(max_length=100, null=True, blank=True,choices=[('che','Chèque'),('esp','Espèce'),('vir','Virement Bancaire')])

    paiement_label = models.CharField(max_length=100, null=True, blank=True)
    
    is_frais_inscription = models.BooleanField(default=False)
    reference_paiement = models.CharField(max_length=100, null=True, blank=True)
    context = models.CharField(max_length=100, null=True, blank=True,choices=[('frais_f','Frais de formation'),('autre','Autres'),('dette','Module en dette'),('facture','Paiement facture'),('rach','Rachât de crédit')])

    promo = models.ForeignKey(Promos, on_delete=models.CASCADE, null=True , blank=True, related_name="promo_paiements")
    
    is_done = models.BooleanField(default=False)
    is_refund = models.BooleanField(default=False)
    refund_id = models.ForeignKey('Rembourssements', null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.montant_paye)

    def save(self, *args, **kwargs):
        if not self.num:

            # 1. Vérifier chemin : Paiement → DuePaiement → Echeancier → Entreprise
            # if not self.due_paiements or not self.due_paiements.entite or not self.due_paiements.ref_echeancier:
            #     raise ValueError("Impossible de générer le numéro : ref_echeancier introuvable.")

            entite_obj = self.due_paiements.entite
            
            if not entite_obj:
                entite_obj = self.due_paiements.ref_echeancier.entite
            else:
                entite_obj = self.refund_id.entite

            # 2. Lecture des champs Entreprise
            entite = entite_obj.designation or "ENTITE"
            wilaya = str(entite_obj.code_wilaya).zfill(2) if entite_obj.code_wilaya else "00"
            annexe = str(entite_obj.numero).zfill(2) if entite_obj.numero else "00"

            # 3. Date du paiement
            date_p = self.date_paiement or datetime.date.today()

            # Conversion si la valeur est une chaîne
            if isinstance(date_p, str):
                date_p = datetime.datetime.strptime(date_p, "%Y-%m-%d").date()

            mois = date_p.strftime("%m")
            annee = date_p.strftime("%y")

            # 4. Génération séquence unique
            pattern = f"/ST/{entite}/{wilaya}/{annexe}/{mois}/{annee}"
            last = Paiements.objects.filter(num__endswith=pattern)\
                                    .aggregate(max_num=Max("num"))["max_num"]

            if last:
                last_seq = int(last.split("/")[0].replace("N°", ""))
                seq = str(last_seq + 1).zfill(6)
            else:
                seq = "000001"

            # 5. Construction du numéro final
            self.num = f"N°{seq}/ST/{entite}/{wilaya}/{annexe}/{mois}/{annee}"

        super().save(*args, **kwargs)
    
class Rembourssements(models.Model):
    
    client = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    motif_rembourssement = models.CharField(max_length=100, null=True, blank=True)
    
    allowed_amount = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    etat = models.CharField(max_length=100, null=True, blank=True, choices=[('enc','En cours de traitement'),('acp','Approuvé'),('ref','Refusé')], default="enc")

    is_done = models.BooleanField(default=False)
    observation = models.CharField(max_length=1000, null=True, blank=True)

    mode_rembourssement = models.CharField(max_length=100, null=True, blank=True,choices=[('che','Chèque'),('esp','Espèce'),('vir','Virement Bancaire')])
    entite = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    
    is_appliced = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client
    
## ne pas utiliser cette classe
class PaiementRemboursement(models.Model):
    client = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    remboursement = models.ForeignKey(Rembourssements, on_delete=models.CASCADE, related_name="paiements_rembourses")
    paiement = models.ForeignKey(Paiements, on_delete=models.CASCADE, related_name="remboursements")
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True,choices=[('che','Chèque'),('esp','Espèce'),('vir','Virement Bancaire')])
    date_remboursement = models.DateField(null=True, blank=True)
    def __str__(self):
        return f"Remboursement {self.remboursement.id} - Paiement {self.paiement.id} : {self.montant}"

class SeuilPaiements(models.Model):
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True)
    label = models.CharField(max_length=100, null=True)
    valeur = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('specialite', 'valeur')

    def __str__(self):
        return self.specialite

class ModelEcheancier(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    promo = models.ForeignKey(Promos, null=True, blank=True, on_delete=models.CASCADE)
    nombre_tranche = models.IntegerField(null=True, blank=True)

    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_double_diplomation = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

class EcheancierPaiement(models.Model):
    model = models.ForeignKey(ModelEcheancier, on_delete=models.CASCADE, null=True, blank=True)
    formation = models.ForeignKey(Formation, null=True, blank=True, on_delete=models.CASCADE)
    
    ##Attribution des frais d'inscription
    frais_inscription = models.DecimalField(decimal_places=2, max_digits=200, null=True, blank=True)

    formation_double = models.ForeignKey(DoubleDiplomation, on_delete=models.CASCADE, null=True, blank=True)

    entite = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_approuved = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.formation.nom

class EcheancierPaiementLine(models.Model):
    echeancier = models.ForeignKey(EcheancierPaiement, null=True, blank=True, on_delete=models.CASCADE)
    taux = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    montant_tranche = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=100)
    date_echeancier = models.DateField(null=True, blank=True)
    
    entite = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.value

class EcheancierSpecial(models.Model):
    nombre_tranche = models.IntegerField(null=True, blank=True)
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)

    is_validate = models.BooleanField(default=False)
    is_approuved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.prospect.nom} - {self.prospect.prenom}'

class EcheancierPaiementSpecialLine(models.Model):
    echeancier = models.ForeignKey(EcheancierSpecial, null=True, blank=True, on_delete=models.CASCADE)
    taux = models.CharField(max_length=100, null=True, blank=True)
    value = models.CharField(max_length=100, null=True, blank=True)
    montant_tranche = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=100)
    date_echeancier = models.DateField(null=True, blank=True)

    entite = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)


    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def __str__(self):
        return self.echeancier.prospect.nom

class Caisse(models.Model):
    pass

class Depenses(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, null=True, blank=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey("DepensesCategory", null=True, blank=True, on_delete=models.SET_NULL)
    date_paiement = models.DateField(null=True, blank=True)
    montant_ht = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    tva = models.CharField(max_length=10, null=True, blank=True)
    montant_ttc= models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    piece = models.FileField(upload_to=tenant_directory_path_for_piece_depanse, null=True, blank=True)
    etat = models.BooleanField(default=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    entite = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True,choices=[('che','Chèque'),('esp','Espèce'),('vir','Virement Bancaire')])

    reference = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.label


class PromoRembourssement(models.Model):
    promo = models.ForeignKey(Promos, on_delete=models.CASCADE, null=True, unique=True)
    montant = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.montant

####################### GESTION DES CATEGORIES DE DEPENSES #############################################
 
class TypeDepense(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.label
    
class SousTypeDepense(models.Model):
    type = models.ForeignKey(TypeDepense, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.label

####################### FIN GESTION DES CATEGORIES DE PRODUIT ##########################################


####################### GESTION DES CATEGORIES DE PRODUIT ET DE DEPENSES ##############################################

class DepensesCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Depense category"
        verbose_name_plural = "Depenses categories"

    def __str__(self):
        return self.name
   
class PaymentCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Payment category"
        verbose_name_plural = "Payment categories"

    def __str__(self):
        return self.name
   
class AutreProduit(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    num = models.CharField(max_length=100, null=True, blank=True, unique=True, help_text="Numéro séquentiel de paiement")
    client = models.ForeignKey(Prospets, on_delete=models.DO_NOTHING, null=True, blank=True)
    montant_paiement = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('chq','Chéque'),('vir','Virement'),('cach','Cash')])
    date_operation = models.DateField(auto_now_add=True)
    reference = models.CharField(null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    entite = models.ForeignKey(Entreprise, on_delete=models.DO_NOTHING, null=True, blank=True)
    compte = models.ForeignKey(PaymentCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.num:
            if not self.entite:
                # Fallback or error if entite is required for numbering.
                # Assuming default behavior or skipping numbering if no entite, 
                # BUT the pattern uses entite. Let's use "ENTITE" if None to avoid crash,
                # or better, raise validation error if strict.
                # Given user request to be "like Paiements", we try to mimic.
                # Paiements uses self.due_paiements.entite.
                entite_nom = "ENTITE"
                wilaya = "00"
                annexe = "00"
            else:
                entite_nom = self.entite.designation or "ENTITE"
                wilaya = str(self.entite.code_wilaya).zfill(2) if self.entite.code_wilaya else "00"
                annexe = str(self.entite.numero).zfill(2) if self.entite.numero else "00"

            # 3. Date du paiement
            date_p = self.date_paiement or datetime.date.today()

            # Conversion si la valeur est une chaîne
            if isinstance(date_p, str):
                date_p = datetime.datetime.strptime(date_p, "%Y-%m-%d").date()

            mois = date_p.strftime("%m")
            annee = date_p.strftime("%y")

            # 4. Génération séquence unique
            pattern = f"/AP/{entite_nom}/{wilaya}/{annexe}/{mois}/{annee}"
            last = AutreProduit.objects.filter(num__endswith=pattern)\
                                    .aggregate(max_num=Max("num"))["max_num"]

            if last:
                last_seq = int(last.split("/")[0].replace("N°", ""))
                seq = str(last_seq + 1).zfill(6)
            else:
                seq = "000001"

            # 5. Construction du numéro final
            # Using AP to distinguish from standard Paiements (ST)
            self.num = f"N°{seq}/AP/{entite_nom}/{wilaya}/{annexe}/{mois}/{annee}"

        super().save(*args, **kwargs)

####################### GESTION DES CATEGORIES DE PRODUIT ET DE DEPENSES ##############################################

class PlanComptable(models.Model):
    numero = models.CharField(max_length=20, unique=True)   # ex: "531", "7061"
    intitule = models.CharField(max_length=255)             # ex: "Caisse", "Prestations de service"
    classe = models.CharField(max_length=1)                 # ex: "5"
    type_compte = models.CharField(
        max_length=20,
        choices=[
            ("actif", "Actif"),
            ("passif", "Passif"),
            ("charge", "Charge"),
            ("produit", "Produit"),
            ("hors_bilan", "Hors bilan"),
        ],
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.numero} - {self.intitule}"
    
class OperationsBancaire(models.Model):
    compte_bancaire = models.ForeignKey(BankAccount, on_delete=models.CASCADE, null=True, blank=True)

    operation_type = models.CharField(max_length=10,choices=[('entree', 'Encaissement'), ('sortie', 'Décaissement')])

    paiement = models.ForeignKey(Paiements,null=True, blank=True,on_delete=models.SET_NULL,related_name='lettrages')

    depense = models.ForeignKey(Depenses,null=True, blank=True,on_delete=models.SET_NULL,related_name='lettrages')

    montant = models.DecimalField(max_digits=20, decimal_places=2)

    date_operation = models.DateField(auto_now_add=True)

    reference_bancaire = models.CharField(max_length=255, null=True, blank=True)
    justification = models.TextField(null=True, blank=True)

    is_rapproche = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    date_paiement = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lettrage {self.id} - {self.compte_bancaire}"
    
class SpecialiteCompte(models.Model):
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True)
    compte = models.ForeignKey(PaymentCategory, on_delete=models.CASCADE, null=True)


    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.specialite.label} - {self.compte.label}"