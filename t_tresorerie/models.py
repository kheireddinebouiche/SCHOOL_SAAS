from django.db import models
from t_etudiants.models import *
from institut_app.models import *
from institut_app.models import Entreprise

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
    ref_echeancier = models.ForeignKey('EcheancierPaiement', on_delete=models.SET_NULL, null=True, blank=True)

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
    payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True)

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

    payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True)

    promo = models.ForeignKey(Promos, on_delete=models.CASCADE, null=True , blank=True, related_name="promo_paiements")
    entite = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)
    
    is_done = models.BooleanField(default=False)
    is_refund = models.BooleanField(default=False)
    refund_id = models.ForeignKey('Rembourssements', null=True, blank=True, on_delete=models.SET_NULL)

    # Tracking of receipt/quittance printing
    has_printed_quittance = models.BooleanField(default=False)
    quittance_printed_at = models.DateTimeField(null=True, blank=True)
    quittance_printed_by = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    facture = models.ForeignKey('t_conseil.Facture', on_delete=models.SET_NULL, null=True, blank=True, related_name='tresorerie_paiements')

    def __str__(self):
        return str(self.montant_paye)

    def save(self, *args, **kwargs):
        if self.refund_id:
            entite_obj = self.refund_id.entite
        elif self.due_paiements:
            entite_obj = self.due_paiements.entite
            if not entite_obj and self.due_paiements.ref_echeancier:
                entite_obj = self.due_paiements.ref_echeancier.entite
        else:
            entite_obj = None

        if entite_obj and not self.entite:
            self.entite = entite_obj

        if not self.num:

            if not entite_obj:
                 super().save(*args, **kwargs)
                 return

            entite_str = entite_obj.designation or "ENTITE"
            wilaya = str(entite_obj.code_wilaya).zfill(2) if entite_obj.code_wilaya else "00"
            annexe = str(entite_obj.numero).zfill(2) if entite_obj.numero else "00"

            date_p = self.date_paiement or datetime.date.today()

            if isinstance(date_p, str):
                date_p = datetime.datetime.strptime(date_p, "%Y-%m-%d").date()

            mois = date_p.strftime("%m")
            annee = date_p.strftime("%y")

            pattern = f"/ST/{entite_str}/{wilaya}/{annexe}/{mois}/{annee}"
            last = Paiements.objects.filter(num__endswith=pattern)\
                                    .aggregate(max_num=Max("num"))["max_num"]

            if last:
                last_seq = int(last.split("/")[0].replace("N°", ""))
                seq = str(last_seq + 1).zfill(6)
            else:
                seq = "000001"

            self.num = f"N°{seq}/ST/{entite_str}/{wilaya}/{annexe}/{mois}/{annee}"

        super().save(*args, **kwargs)
    
class Rembourssements(models.Model):
    
    client = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    facture = models.ForeignKey('t_conseil.Facture', on_delete=models.SET_NULL, null=True, blank=True, related_name='remboursements')
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
    specialite = models.ForeignKey(Specialites, null=True, blank=True, on_delete=models.CASCADE)
    
    frais_inscription = models.DecimalField(decimal_places=2, max_digits=200, null=True, blank=True)

    formation_double = models.ForeignKey(DoubleDiplomation, on_delete=models.CASCADE, null=True, blank=True)

    entite = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)
    remise = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True, blank=True)
    type_remise = models.CharField(max_length=20, default='fixe', choices=[('fixe', 'Montant Fixe'), ('pourcentage', 'Pourcentage')])
    
    majoration = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True, blank=True)
    type_majoration = models.CharField(max_length=20, default='fixe', choices=[('fixe', 'Montant Fixe'), ('pourcentage', 'Pourcentage')])
    
    has_remise = models.BooleanField(default=False)
    has_majoration = models.BooleanField(default=False)
    tarif_formation = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_approuved = models.BooleanField(default=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        if self.formation:
            return self.formation.nom
        elif self.formation_double:
            return self.formation_double.label
        return f"Échéancier {self.id}"

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
    
    frais_inscription = models.DecimalField(decimal_places=2, max_digits=200, null=True, blank=True)
    remise = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True, blank=True)
    type_remise = models.CharField(max_length=20, default='fixe', choices=[('fixe', 'Montant Fixe'), ('pourcentage', 'Pourcentage')])
    majoration = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True, blank=True)
    type_majoration = models.CharField(max_length=20, default='fixe', choices=[('fixe', 'Montant Fixe'), ('pourcentage', 'Pourcentage')])
    has_remise = models.BooleanField(default=False)
    has_majoration = models.BooleanField(default=False)
    tarif_formation = models.DecimalField(decimal_places=2, max_digits=20, default=0, null=True, blank=True)
    entite = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)

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
    date_depense = models.DateField(null=True, blank=True)
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
    promo = models.OneToOneField(Promos, on_delete=models.CASCADE, null=True)
    montant = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.montant

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

class DepensesCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    payment_category = models.ForeignKey('PaymentCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='depense_categories')
    description = models.TextField(null=True, blank=True)
    global_id = models.IntegerField(null=True, blank=True)
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
    category_type = models.CharField(
        max_length=50, 
        choices=[('standard', 'Standard'), ('rachat_credit', 'Rachat de Crédit')],
        default='standard',
        verbose_name="Type de Catégorie"
    )
    description = models.TextField(null=True, blank=True)
    global_id = models.IntegerField(null=True, blank=True)
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
    mode_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('che','Chèque'),('esp','Espèce'),('vir','Virement Bancaire')])
    date_operation = models.DateField(auto_now_add=True)
    reference = models.CharField(null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    entite = models.ForeignKey(Entreprise, on_delete=models.DO_NOTHING, null=True, blank=True)
    payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.num:
            if not self.entite:
                entite_nom = "ENTITE"
                wilaya = "00"
                annexe = "00"
            else:
                entite_nom = self.entite.designation or "ENTITE"
                wilaya = str(self.entite.code_wilaya).zfill(2) if self.entite.code_wilaya else "00"
                annexe = str(self.entite.numero).zfill(2) if self.entite.numero else "00"

            date_p = self.date_paiement or datetime.date.today()

            if isinstance(date_p, str):
                date_p = datetime.datetime.strptime(date_p, "%Y-%m-%d").date()

            mois = date_p.strftime("%m")
            annee = date_p.strftime("%y")

            pattern = f"/AP/{entite_nom}/{wilaya}/{annexe}/{mois}/{annee}"
            last = AutreProduit.objects.filter(num__endswith=pattern)\
                                    .aggregate(max_num=Max("num"))["max_num"]

            if last:
                last_seq = int(last.split("/")[0].replace("N°", ""))
                seq = str(last_seq + 1).zfill(6)
            else:
                seq = "000001"

            self.num = f"N°{seq}/AP/{entite_nom}/{wilaya}/{annexe}/{mois}/{annee}"

        super().save(*args, **kwargs)

class PlanComptable(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    intitule = models.CharField(max_length=255)
    classe = models.CharField(max_length=1)
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
    autre_produit = models.ForeignKey('AutreProduit', null=True, blank=True, on_delete=models.SET_NULL, related_name='lettrages')
    conseil_paiement = models.ForeignKey('t_conseil.Paiement', null=True, blank=True, on_delete=models.SET_NULL, related_name='lettrages')

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
    
class PaymentType(models.Model):
    name = models.CharField(max_length=100)
    payment_categories = models.ManyToManyField(PaymentCategory, related_name='payment_types')
    global_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Type de Paiement"
        verbose_name_plural = "Types de Paiement"

    def __str__(self):
        return self.name

class PenaltyGlobalConfiguration(models.Model):
    # Penalite de retard
    penalite_retard = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Pénalité de retard")
    penalite_retard_payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='penalite_retard_configs')

    # Rachat de credit
    prix_rachat_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Prix de rachat de crédit")
    prix_rachat_credit_payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='prix_rachat_credit_configs')

    # Frais de duplicata
    frais_duplicata = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Frais de duplicata")
    frais_duplicata_payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='frais_duplicata_configs')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration Globale des Pénalités"
        verbose_name_plural = "Configurations Globales des Pénalités"

    def __str__(self):
        return "Configuration Globale des Pénalités"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj

class SpecialiteCompte(models.Model):
    specialite = models.ForeignKey(Specialites, on_delete=models.CASCADE, null=True)
    compte = models.ForeignKey(PaymentCategory, on_delete=models.CASCADE, null=True)


    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.specialite.label} - {self.compte.label}"



DEFAULT_RELANCE_CORPS = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rappel de Paiement</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #334155;">
    <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color: #f8fafc; padding: 40px 10px;">
        <tr>
            <td align="center">
                <table width="600" border="0" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03); overflow: hidden;">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%); padding: 35px 40px; text-align: left;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.5px;">Rappel d'échéance de paiement</h1>
                            <p style="color: #e2e8f0; margin: 5px 0 0 0; font-size: 14px;">{tenant_name} - Service Trésorerie</p>
                        </td>
                    </tr>
                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px;">
                            <h2 style="color: #0f172a; margin-top: 0; margin-bottom: 20px; font-size: 18px; font-weight: 600;">Bonjour {nom} {prenom},</h2>
                            <p style="line-height: 1.6; color: #475569; font-size: 15px; margin-bottom: 25px;">
                                Nous vous contactons pour vous rappeler que votre échéancier de paiement de formation présente une ou plusieurs échéances en attente de régularisation.
                            </p>
                            
                            <!-- Table structure -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; margin-bottom: 25px;">
                                <thead>
                                    <tr style="background-color: #f1f5f9;">
                                        <th style="padding: 12px; font-weight: 600; text-align: left; color: #475569; font-size: 13px; border-bottom: 2px solid #cbd5e1;">Échéance</th>
                                        <th style="padding: 12px; font-weight: 600; text-align: left; color: #475569; font-size: 13px; border-bottom: 2px solid #cbd5e1;">Date d'échéance</th>
                                        <th style="padding: 12px; font-weight: 600; text-align: right; color: #475569; font-size: 13px; border-bottom: 2px solid #cbd5e1;">Montant dû</th>
                                        <th style="padding: 12px; font-weight: 600; text-align: right; color: #475569; font-size: 13px; border-bottom: 2px solid #cbd5e1;">Reste à payer</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {table_rows}
                                </tbody>
                            </table>

                            <!-- Summary Banner -->
                            <div style="background-color: #fff1f2; border-left: 4px solid #f43f5e; padding: 15px 20px; border-radius: 6px; margin-bottom: 30px;">
                                <table width="100%" border="0" cellpadding="0" cellspacing="0">
                                    <tr>
                                        <td style="color: #9f1239; font-size: 15px; font-weight: 600;">Total restant à payer :</td>
                                        <td style="color: #be123c; font-size: 18px; font-weight: 700; text-align: right;">{total_remaining} DA</td>
                                    </tr>
                                </table>
                            </div>

                            <p style="line-height: 1.6; color: #475569; font-size: 15px; margin-bottom: 25px;">
                                Nous vous prions de bien vouloir procéder à la régularisation de ces montants dans les plus brefs délais auprès de notre service comptabilité.
                            </p>
                            
                            <p style="line-height: 1.6; color: #64748b; font-size: 13px; font-style: italic; border-top: 1px solid #e2e8f0; padding-top: 20px;">
                                Si vous avez déjà procédé à ce paiement récemment, merci de ne pas tenir compte de ce message ou de nous transmettre votre reçu de paiement pour mise à jour de votre dossier.
                            </p>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f1f5f9; padding: 25px 40px; text-align: center; font-size: 12px; color: #94a3b8;">
                            <p style="margin: 0 0 5px 0;">Ce courriel a été généré automatiquement par {tenant_name}.</p>
                            <p style="margin: 0;">© {annee_courante} Tous droits réservés.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""

class ParametreFinancier(models.Model):
    """Singleton model for global financial parameters."""

    bloquer_date_paiement = models.BooleanField(
        default=True,
        verbose_name="Bloquer la date de paiement",
        help_text=(
            "Si activé, la date de paiement dans le modal d'enregistrement est "
            "pré-remplie avec la date du jour et verrouillée. "
            "Si désactivé, l'agent peut choisir librement la date."
        ),
    )

    # Droits de Timbre (Stamp Duty) - Algerian Legislation
    activer_timbre = models.BooleanField(
        default=False,
        verbose_name="Activer les droits de timbre",
        help_text="Activer le calcul automatique du droit de timbre (1% pour les paiements en espèces)."
    )
    taux_timbre = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=1.00, 
        verbose_name="Taux du timbre (%)"
    )
    timbre_min = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=5.00, 
        verbose_name="Montant minimum (DA)"
    )
    timbre_max = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=2500.00, 
        verbose_name="Montant maximum (DA)"
    )
    timbre_cash_only = models.BooleanField(
        default=True,
        verbose_name="Uniquement pour les espèces",
        help_text="Si activé, le timbre ne s'applique qu'aux paiements marqués comme 'Espèce'."
    )
    timbre_bareme = models.TextField(
        default='[{"min_ttc": 0, "max_ttc": 300, "rate": 0.0, "is_exempt": true}, {"min_ttc": 301, "max_ttc": 30000, "rate": 1.0, "is_exempt": false}, {"min_ttc": 30001, "max_ttc": 100000, "rate": 1.5, "is_exempt": false}, {"min_ttc": 100001, "max_ttc": null, "rate": 2.0, "is_exempt": false}]',
        verbose_name="Barème progressif des droits de timbre (JSON)",
        help_text="Liste ordonnée de tranches progressives avec min, max, taux et statut d'exonération au format JSON."
    )

    # Email Templates
    relance_echeancier_sujet = models.CharField(
        max_length=255,
        default="Rappel de paiement - Échéancier de formation - {nom} {prenom}",
        verbose_name="Sujet de l'email de relance"
    )
    relance_echeancier_corps = models.TextField(
        default=DEFAULT_RELANCE_CORPS,
        verbose_name="Corps de l'email de relance (HTML)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paramètre Financier"
        verbose_name_plural = "Paramètres Financiers"

    @classmethod
    def get_instance(cls):
        """Always returns the single settings record, creating it if needed."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

class SoldeInitial(models.Model):
    TYPES = [('caisse', 'Caisse'), ('banque', 'Banque')]
    type = models.CharField(max_length=10, choices=TYPES)
    montant = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    annee_scolaire = models.IntegerField(help_text="L'année de début de l'année scolaire (ex: 2023 pour 2023/2024)")
    date_solde = models.DateField(default=datetime.date.today)
    entite = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('type', 'annee_scolaire', 'entite')
        verbose_name = "Solde Initial"
        verbose_name_plural = "Soldes Initiaux"

    def __str__(self):
        entite_str = f" - {self.entite.designation}" if self.entite else ""
        return f"Solde {self.type} {self.annee_scolaire}/{self.annee_scolaire+1}{entite_str}: {self.montant}"

class DepotBanque(models.Model):
    num = models.CharField(max_length=100, null=True, blank=True, unique=True, help_text="Numéro séquentiel de remise de fonds")
    date_depot = models.DateField(default=datetime.date.today)
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    entite = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    agent_remettant = models.CharField(max_length=255, help_text="Nom de la personne qui dépose l'argent")
    banque_destinatrice = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True)
    reference_bordereau = models.CharField(max_length=100, null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dépôt en Banque"
        verbose_name_plural = "Dépôts en Banque"

    def __str__(self):
        return f"Dépôt {self.num} - {self.montant} DA"

    def save(self, *args, **kwargs):
        if not self.num:
            entite_obj = self.entite
            entite_str = entite_obj.designation or "ENTITE"
            wilaya = str(entite_obj.code_wilaya).zfill(2) if entite_obj.code_wilaya else "00"
            annexe = str(entite_obj.numero).zfill(2) if entite_obj.numero else "00"

            date_p = self.date_depot or datetime.date.today()
            mois = date_p.strftime("%m")
            annee = date_p.strftime("%y")

            pattern = f"/DEPOT/{entite_str}/{wilaya}/{annexe}/{mois}/{annee}"
            last = DepotBanque.objects.filter(num__endswith=pattern)\
                                     .aggregate(max_num=Max("num"))["max_num"]

            if last:
                try:
                    last_seq = int(last.split("/")[0].replace("N°", ""))
                    seq = str(last_seq + 1).zfill(6)
                except:
                    seq = "000001"
            else:
                seq = "000001"

            self.num = f"N°{seq}/DEPOT/{entite_str}/{wilaya}/{annexe}/{mois}/{annee}"

        super().save(*args, **kwargs)