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

    motif = models.CharField(max_length=100, null=True, blank=True, choices=[('frais_f', 'Frais de formation'),('frais', 'Frais d\'admission'),('autre','Autres'),('dette','Module en dette'),('rach','RachÃ¢t de crÃ©dit')])

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    etat = models.CharField(max_length=100, null=True, blank=True, default='en_attente' ,choices=[('en_attente','En Attente'),('annulation','Demande d\'annulation'),('annulation_approuver','Demande d\'annulation approuvÃ©e'),('terminer','Cloturer')])
    approuved_annulation = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Demande de paiement"
        verbose_name_plural = "Demandes de paiement"

    def __str__(self):
        return f"{self.client.nom}" if self.client else f"Demande {self.id}"

class clientPaiementsRequestLine(models.Model):
    paiement_request = models.ForeignKey(ClientPaiementsRequest, on_delete=models.DO_NOTHING, null=True)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    data_paiement = models.DateField(null=True)
    observation = models.CharField(max_length=1000, null=True, blank=True)
    motif_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('fin','Frais d\'inscription'),('ass','Assurance'),('frf','Frais de formation')])
    etat = models.CharField(max_length=100, null=True, blank=True, choices=[('auc','Aucun paiement effectuÃ©'),('part','Paiement partiel'), ('tot','Paiement cash'),('ter','Paiement terminÃ©')], default="auc")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.paiement_request) if self.paiement_request else "Ligne Paiement"

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
    type = models.CharField(max_length=100, null=True, blank=True, choices=[('frais_f',"Frais de formation"),('dette','Module en dette'),('autre','Autre'),('rach','RachÃ¢t de crÃ©dit')])
    observation = models.CharField(max_length=1000, null=True, blank=True)

    entite = models.ForeignKey(Entreprise, on_delete=models.SET_NULL, null=True, blank=True)
    payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.label) if getattr(self, "label", None) else "Sans label"
class Paiements(models.Model):
    num = models.CharField(max_length=100, null=True, blank=True, unique=True, help_text="NumÃ©ro sÃ©quentiel de paiement")
    due_paiements = models.ForeignKey(DuePaiements, on_delete=models.CASCADE, null=True, blank=True)
    prospect = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True, related_name="paiements")
    montant_paye = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    observation = models.CharField(max_length=100, null=True, blank=True)

    mode_paiement = models.CharField(max_length=100, null=True, blank=True,choices=[('che','Chèque'),('esp','Espèce'),('vir','Virement Bancaire')])

    paiement_label = models.CharField(max_length=100, null=True, blank=True)
    
    is_frais_inscription = models.BooleanField(default=False)
    reference_paiement = models.CharField(max_length=100, null=True, blank=True)
    context = models.CharField(max_length=100, null=True, blank=True,choices=[('frais_f','Frais de formation'),('autre','Autres'),('dette','Module en dette'),('facture','Paiement facture'),('rach','Rachat de crédit')])

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

            format_str = getattr(entite_obj, 'quittance_format', None) or "NÂ°{seq}/ST/{entite}/{wilaya}/{annexe}/{mois}/{annee}"
            seq_length = getattr(entite_obj, 'quittance_sequence_length', 6) or 6

            format_str = format_str.replace('{entite}', entite_str).replace('{wilaya}', wilaya).replace('{annexe}', annexe).replace('{mois}', mois).replace('{annee}', annee)

            if "{seq}" in format_str:
                parts = format_str.split("{seq}")
                prefix_part = parts[0]
                suffix_part = parts[1] if len(parts) > 1 else ""
            else:
                prefix_part = format_str
                suffix_part = ""

            qs = Paiements.objects.filter(num__startswith=prefix_part)
            if suffix_part:
                qs = qs.filter(num__endswith=suffix_part)
            last = qs.aggregate(max_num=Max("num"))["max_num"]

            if last:
                # Remove prefix and suffix to get sequence
                seq_str = last[len(prefix_part):-len(suffix_part)] if len(suffix_part) > 0 else last[len(prefix_part):]
                try:
                    last_seq = int(seq_str)
                    seq = str(last_seq + 1).zfill(seq_length)
                except ValueError:
                    seq = str(1).zfill(seq_length)
            else:
                seq = str(1).zfill(seq_length)

            if "{seq}" in format_str:
                self.num = format_str.replace("{seq}", seq)
            else:
                self.num = f"{format_str}{seq}"

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
    category = models.ForeignKey('DepensesCategory', null=True, blank=True, on_delete=models.SET_NULL, related_name='remboursements')
    
    is_appliced = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client.nom} {self.client.prenom}" if self.client else f"Remboursement #{self.id}"
    
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
        return str(self.specialite) if self.specialite else "Seuil"

class ModelEcheancier(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    promo = models.ForeignKey(Promos, null=True, blank=True, on_delete=models.CASCADE)
    nombre_tranche = models.IntegerField(null=True, blank=True)

    description = models.CharField(max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_double_diplomation = models.BooleanField(default=False)
    has_frais_inscription = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.label) if getattr(self, "label", None) else "Sans label"
class EcheancierPaiement(models.Model):
    model = models.ForeignKey(ModelEcheancier, on_delete=models.CASCADE, null=True, blank=True)
    formation = models.ForeignKey(Formation, null=True, blank=True, on_delete=models.CASCADE)
    specialite = models.ForeignKey(Specialites, null=True, blank=True, on_delete=models.CASCADE)
    
    frais_inscription = models.DecimalField(decimal_places=2, max_digits=200, null=True, blank=True)
    date_frais_inscription = models.DateField(null=True, blank=True)

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
            return self.formation.nom or f"ÃchÃ©ancier {self.id}"
        elif self.formation_double:
            return self.formation_double.label or f"ÃchÃ©ancier {self.id}"
        return f"ÃchÃ©ancier {self.id}"

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
        return str(self.value) if self.value else "Ligne Echeancier"

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
        return f'{self.prospect.nom} - {self.prospect.prenom}' if self.prospect else f"Echeancier {self.id}"

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
        if self.echeancier and self.echeancier.prospect:
            return str(self.echeancier.prospect.nom)
        return f"Ligne Spe {self.id}"

class Caisse(models.Model):
    pass

class Depenses(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    fournisseur = models.ForeignKey(Fournisseur, null=True, blank=True, on_delete=models.CASCADE)
    client = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    date_depense = models.DateField(null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    montant_ht = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    tva = models.CharField(max_length=10, null=True, blank=True)
    montant_ttc= models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    timbre = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    piece = models.FileField(upload_to=tenant_directory_path_for_piece_depanse, null=True, blank=True)
    etat = models.BooleanField(default=False)
    reference_document = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    entite = models.ForeignKey(Entreprise, on_delete=models.CASCADE, null=True, blank=True)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True,choices=[('che','ChÃ¨que'),('esp','EspÃ¨ce'),('vir','Virement Bancaire')])

    reference = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.label) if getattr(self, "label", None) else "Sans label"
class DepenseLigne(models.Model):
    depense = models.ForeignKey(Depenses, on_delete=models.CASCADE, related_name='lignes')
    designation = models.CharField(max_length=255)
    category = models.ForeignKey("DepensesCategory", null=True, blank=True, on_delete=models.SET_NULL)
    quantite = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    prix_unitaire_ht = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    tva = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Taux de TVA en %")
    montant_ht = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    montant_tva = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    montant_ttc = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.designation} ({self.depense.label})"


class PromoRembourssement(models.Model):
    promo = models.OneToOneField(Promos, on_delete=models.CASCADE, null=True)
    montant = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.montant) if self.montant else "0.00"

class TypeDepense(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.label) if getattr(self, "label", None) else "Sans label"
class SousTypeDepense(models.Model):
    type = models.ForeignKey(TypeDepense, on_delete=models.CASCADE, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.label) if getattr(self, "label", None) else "Sans label"
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
        choices=[('standard', 'Standard'), ('rachat_credit', 'Rachat de CrÃ©dit')],
        default='standard',
        verbose_name="Type de CatÃ©gorie"
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
    num = models.CharField(max_length=100, null=True, blank=True, unique=True, help_text="NumÃ©ro sÃ©quentiel de paiement")
    client = models.ForeignKey(Prospets, on_delete=models.DO_NOTHING, null=True, blank=True)
    montant_paiement = models.DecimalField(decimal_places=2, max_digits=100, null=True, blank=True)
    mode_paiement = models.CharField(max_length=100, null=True, blank=True, choices=[('che','ChÃ¨que'),('esp','EspÃ¨ce'),('vir','Virement Bancaire')])
    date_operation = models.DateField(auto_now_add=True)
    reference = models.CharField(null=True, blank=True)
    date_paiement = models.DateField(null=True, blank=True)
    entite = models.ForeignKey(Entreprise, on_delete=models.DO_NOTHING, null=True, blank=True)
    payment_category = models.ForeignKey('PaymentCategory', on_delete=models.SET_NULL, null=True, blank=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return str(self.label) if getattr(self, "label", None) else "Sans label"
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

            format_str = getattr(self.entite, 'quittance_format', None) or "N°{seq}/ST/{entite}/{wilaya}/{annexe}/{mois}/{annee}"
            seq_length = getattr(self.entite, 'quittance_sequence_length', 6) or 6

            format_str = format_str.replace('{entite}', entite_str).replace('{wilaya}', wilaya).replace('{annexe}', annexe).replace('{mois}', mois).replace('{annee}', annee)

            if "{seq}" in format_str:
                parts = format_str.split("{seq}")
                prefix_part = parts[0]
                suffix_part = parts[1] if len(parts) > 1 else ""
            else:
                prefix_part = format_str
                suffix_part = ""

            qs = AutreProduit.objects.filter(num__startswith=prefix_part)
            if suffix_part:
                qs = qs.filter(num__endswith=suffix_part)
            last = qs.aggregate(max_num=Max("num"))["max_num"]

            if last:
                # Remove prefix and suffix to get sequence
                seq_str = last[len(prefix_part):-len(suffix_part)] if len(suffix_part) > 0 else last[len(prefix_part):]
                try:
                    last_seq = int(seq_str)
                    seq = str(last_seq + 1).zfill(seq_length)
                except ValueError:
                    seq = str(1).zfill(seq_length)
            else:
                seq = str(1).zfill(seq_length)

            if "{seq}" in format_str:
                self.num = format_str.replace("{seq}", seq)
            else:
                self.num = f"{format_str}{seq}"

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

    operation_type = models.CharField(max_length=10,choices=[('entree', 'Encaissement'), ('sortie', 'DÃ©caissement')])

    paiement = models.ForeignKey(Paiements,null=True, blank=True,on_delete=models.SET_NULL,related_name='lettrages')
    depense = models.ForeignKey(Depenses,null=True, blank=True,on_delete=models.SET_NULL,related_name='lettrages')
    autre_produit = models.ForeignKey('AutreProduit', null=True, blank=True, on_delete=models.SET_NULL, related_name='lettrages')
    conseil_paiement = models.ForeignKey('t_conseil.Paiement', null=True, blank=True, on_delete=models.SET_NULL, related_name='lettrages')
    remboursement = models.ForeignKey(Rembourssements, null=True, blank=True, on_delete=models.SET_NULL, related_name='lettrages')

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
    penalite_retard = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="PÃ©nalitÃ© de retard")
    penalite_retard_payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='penalite_retard_configs')

    # Rachat de credit
    prix_rachat_credit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Prix de rachat de crÃ©dit")
    prix_rachat_credit_payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='prix_rachat_credit_configs')

    # Frais de duplicata
    frais_duplicata = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Frais de duplicata")
    frais_duplicata_payment_type = models.ForeignKey('PaymentType', on_delete=models.SET_NULL, null=True, blank=True, related_name='frais_duplicata_configs')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration Globale des PÃ©nalitÃ©s"
        verbose_name_plural = "Configurations Globales des PÃ©nalitÃ©s"

    def __str__(self):
        return "Configuration Globale des PÃ©nalitÃ©s"

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
                            <h1 style="color: #ffffff; margin: 0; font-size: 24px; font-weight: 700; letter-spacing: -0.5px;">Rappel d'Ã©chÃ©ance de paiement</h1>
                            <p style="color: #e2e8f0; margin: 5px 0 0 0; font-size: 14px;">{tenant_name} - Service TrÃ©sorerie</p>
                        </td>
                    </tr>
                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px;">
                            <h2 style="color: #0f172a; margin-top: 0; margin-bottom: 20px; font-size: 18px; font-weight: 600;">Bonjour {nom} {prenom},</h2>
                            <p style="line-height: 1.6; color: #475569; font-size: 15px; margin-bottom: 25px;">
                                Nous vous contactons pour vous rappeler que votre Ã©chÃ©ancier de paiement de formation prÃ©sente une ou plusieurs Ã©chÃ©ances en attente de rÃ©gularisation.
                            </p>
                            
                            <!-- Table structure -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: collapse; margin-bottom: 25px;">
                                <thead>
                                    <tr style="background-color: #f1f5f9;">
                                        <th style="padding: 12px; font-weight: 600; text-align: left; color: #475569; font-size: 13px; border-bottom: 2px solid #cbd5e1;">ÃchÃ©ance</th>
                                        <th style="padding: 12px; font-weight: 600; text-align: left; color: #475569; font-size: 13px; border-bottom: 2px solid #cbd5e1;">Date d'Ã©chÃ©ance</th>
                                        <th style="padding: 12px; font-weight: 600; text-align: right; color: #475569; font-size: 13px; border-bottom: 2px solid #cbd5e1;">Montant dÃ»</th>
                                        <th style="padding: 12px; font-weight: 600; text-align: right; color: #475569; font-size: 13px; border-bottom: 2px solid #cbd5e1;">Reste Ã  payer</th>
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
                                        <td style="color: #9f1239; font-size: 15px; font-weight: 600;">Total restant Ã  payer :</td>
                                        <td style="color: #be123c; font-size: 18px; font-weight: 700; text-align: right;">{total_remaining} DA</td>
                                    </tr>
                                </table>
                            </div>

                            <p style="line-height: 1.6; color: #475569; font-size: 15px; margin-bottom: 25px;">
                                Nous vous prions de bien vouloir procÃ©der Ã  la rÃ©gularisation de ces montants dans les plus brefs dÃ©lais auprÃ¨s de notre service comptabilitÃ©.
                            </p>
                            
                            <p style="line-height: 1.6; color: #64748b; font-size: 13px; font-style: italic; border-top: 1px solid #e2e8f0; padding-top: 20px;">
                                Si vous avez dÃ©jÃ  procÃ©dÃ© Ã  ce paiement rÃ©cemment, merci de ne pas tenir compte de ce message ou de nous transmettre votre reÃ§u de paiement pour mise Ã  jour de votre dossier.
                            </p>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f1f5f9; padding: 25px 40px; text-align: center; font-size: 12px; color: #94a3b8;">
                            <p style="margin: 0 0 5px 0;">Ce courriel a Ã©tÃ© gÃ©nÃ©rÃ© automatiquement par {tenant_name}.</p>
                            <p style="margin: 0;">Â© {annee_courante} Tous droits rÃ©servÃ©s.</p>
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
    
    compte_tva_collectee = models.ForeignKey(
        'PaymentCategory', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='param_tva_collectee', 
        verbose_name="CatÃ©gorie Recette TVA CollectÃ©e",
        help_text="CatÃ©gorie de recette utilisÃ©e pour la TVA sur les factures clients"
    )
    
    compte_tva_deductible = models.ForeignKey(
        'DepensesCategory', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='param_tva_deductible', 
        verbose_name="Type DÃ©pense TVA DÃ©ductible",
        help_text="Type de dÃ©pense utilisÃ© pour la TVA sur les achats fournisseurs"
    )
    
    compte_timbre_collecte = models.ForeignKey(
        'PaymentCategory', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='param_timbre_collecte', 
        verbose_name="CatÃ©gorie Recette Droit de Timbre",
        help_text="CatÃ©gorie de recette utilisÃ©e pour les droits de timbre collectÃ©s"
    )
    
    compte_timbre_charge = models.ForeignKey(
        'DepensesCategory', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='param_timbre_charge', 
        verbose_name="Type DÃ©pense Droit de Timbre",
        help_text="Type de dÃ©pense utilisÃ© pour les droits de timbre payÃ©s"
    )

    bloquer_date_paiement = models.BooleanField(
        default=True,
        verbose_name="Bloquer la date de paiement",
        help_text=(
            "Si activÃ©, la date de paiement dans le modal d'enregistrement est "
            "prÃ©-remplie avec la date du jour et verrouillÃ©e. "
            "Si dÃ©sactivÃ©, l'agent peut choisir librement la date."
        ),
    )

    # Droits de Timbre (Stamp Duty) - Algerian Legislation
    activer_timbre = models.BooleanField(
        default=False,
        verbose_name="Activer les droits de timbre",
        help_text="Activer le calcul automatique du droit de timbre (1% pour les paiements en espÃ¨ces)."
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
        verbose_name="Uniquement pour les espÃ¨ces",
        help_text="Si activÃ©, le timbre ne s'applique qu'aux paiements marquÃ©s comme 'EspÃ¨ce'."
    )
    timbre_bareme = models.TextField(
        default='[{"min_ttc": 0, "max_ttc": 300, "rate": 0.0, "is_exempt": true}, {"min_ttc": 301, "max_ttc": 30000, "rate": 1.0, "is_exempt": false}, {"min_ttc": 30001, "max_ttc": 100000, "rate": 1.5, "is_exempt": false}, {"min_ttc": 100001, "max_ttc": null, "rate": 2.0, "is_exempt": false}]',
        verbose_name="BarÃ¨me progressif des droits de timbre (JSON)",
        help_text="Liste ordonnÃ©e de tranches progressives avec min, max, taux et statut d'exonÃ©ration au format JSON."
    )

    # Email Templates
    relance_echeancier_sujet = models.CharField(
        max_length=255,
        default="Rappel de paiement - ÃchÃ©ancier de formation - {nom} {prenom}",
        verbose_name="Sujet de l'email de relance"
    )
    relance_echeancier_corps = models.TextField(
        default=DEFAULT_RELANCE_CORPS,
        verbose_name="Corps de l'email de relance (HTML)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ParamÃ¨tre Financier"
        verbose_name_plural = "ParamÃ¨tres Financiers"

    @classmethod
    def get_instance(cls):
        """Always returns the single settings record, creating it if needed."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

class SoldeInitial(models.Model):
    TYPES = [('caisse', 'Caisse'), ('banque', 'Banque')]
    type = models.CharField(max_length=10, choices=TYPES)
    montant = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    annee_scolaire = models.IntegerField(help_text="L'annÃ©e de dÃ©but de l'annÃ©e scolaire (ex: 2023 pour 2023/2024)")
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
    num = models.CharField(max_length=100, null=True, blank=True, unique=True, help_text="NumÃ©ro sÃ©quentiel de remise de fonds")
    date_depot = models.DateField(default=datetime.date.today)
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    entite = models.ForeignKey(Entreprise, on_delete=models.CASCADE)
    agent_remettant = models.CharField(max_length=255, help_text="Nom de la personne qui dÃ©pose l'argent")
    banque_destinatrice = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, null=True, blank=True)
    reference_bordereau = models.CharField(max_length=100, null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    
    cree_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "DÃ©pÃ´t en Banque"
        verbose_name_plural = "DÃ©pÃ´ts en Banque"

    def __str__(self):
        return f"DÃ©pÃ´t {self.num} - {self.montant} DA"

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
                    last_seq = int(last.split("/")[0].replace("NÂ°", ""))
                    seq = str(last_seq + 1).zfill(6)
                except:
                    seq = "000001"
            else:
                seq = "000001"

            self.num = f"NÂ°{seq}/DEPOT/{entite_str}/{wilaya}/{annexe}/{mois}/{annee}"

        super().save(*args, **kwargs)

class ReglementFournisseur(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='reglements')
    date_reglement = models.DateField()
    reference = models.CharField(max_length=255, null=True, blank=True)
    observation = models.TextField(null=True, blank=True)
    total_paye = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReglementDepense(models.Model):
    reglement = models.ForeignKey(ReglementFournisseur, on_delete=models.CASCADE, related_name='depenses_payees')
    depense = models.ForeignKey(Depenses, on_delete=models.CASCADE, related_name='reglements')
    montant_affecte = models.DecimalField(max_digits=20, decimal_places=2)

class PaiementFournisseurMode(models.Model):
    reglement = models.ForeignKey(ReglementFournisseur, on_delete=models.CASCADE, related_name='modes_paiement')
    mode_paiement = models.CharField(max_length=100, choices=[('che','Chèque'),('esp','Espèce'),('vir','Virement Bancaire')])
    montant = models.DecimalField(max_digits=20, decimal_places=2)
    banque = models.CharField(max_length=255, null=True, blank=True)
    reference_paiement = models.CharField(max_length=255, null=True, blank=True)
    
    etat_cheque = models.CharField(max_length=50, null=True, blank=True, choices=[('emis','Émis'),('signature','En attente de signature'),('remis','Remis au fournisseur'),('decaisse','Décaissé')])
    date_emission = models.DateField(null=True, blank=True)
    date_signature = models.DateField(null=True, blank=True)
    date_remise = models.DateField(null=True, blank=True)
    date_encaissement = models.DateField(null=True, blank=True)


class SuiviChequeSortant(models.Model):
    depense = models.OneToOneField(Depenses, on_delete=models.CASCADE, related_name='suivi_cheque', null=True, blank=True)
    remboursement = models.OneToOneField('Rembourssements', on_delete=models.CASCADE, related_name='suivi_cheque', null=True, blank=True)
    
    statut = models.CharField(max_length=50, choices=[
        ('emis', 'Emis'),
        ('attente_signature', 'En attente de signature'),
        ('remis', 'Remis au client/fournisseur'),
        ('decaisse', 'Décaissé'),
        ('en_attente', 'En attente'),
        ('effectue', 'Virement effectué')
    ], default='emis')
    date_emis = models.DateTimeField(auto_now_add=True)
    date_attente_signature = models.DateTimeField(null=True, blank=True)
    date_remis = models.DateTimeField(null=True, blank=True)
    date_decaisse = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.depense:
            return f"Cheque pour depense {self.depense.id} - {self.statut}"
        elif self.remboursement:
            return f"Cheque pour remboursement {self.remboursement.id} - {self.statut}"
        return f"Cheque inconnu - {self.statut}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Depenses)
def create_suivi_cheque_depense(sender, instance, created, **kwargs):
    if instance.mode_paiement in ['che', 'vir']:
        statut = 'emis' if instance.mode_paiement == 'che' else 'en_attente'
        has_date_paiement = bool(instance.date_paiement)
        
        # Check if reconciled
        is_rapproche = instance.lettrages.filter(is_rapproche=True).exists()
            
        if has_date_paiement or is_rapproche:
            statut = 'decaisse' if instance.mode_paiement == 'che' else 'effectue'
            
        obj, c = SuiviChequeSortant.objects.get_or_create(depense=instance, defaults={'statut': statut})
        if c and statut in ['decaisse', 'effectue']:
            obj.date_decaisse = instance.date_paiement or instance.created_at
            obj.save()

@receiver(post_save, sender='t_tresorerie.Rembourssements')
def create_suivi_cheque_remboursement(sender, instance, created, **kwargs):
    if instance.mode_rembourssement in ['che', 'vir']:
        statut = 'emis' if instance.mode_rembourssement == 'che' else 'en_attente'
        
        # Check if reconciled
        is_rapproche = instance.lettrages.filter(is_rapproche=True).exists()
            
        if is_rapproche:
            statut = 'decaisse' if instance.mode_rembourssement == 'che' else 'effectue'
            
        obj, c = SuiviChequeSortant.objects.get_or_create(remboursement=instance, defaults={'statut': statut})
        if c and statut in ['decaisse', 'effectue']:
            obj.date_decaisse = instance.created_at
            obj.save()
