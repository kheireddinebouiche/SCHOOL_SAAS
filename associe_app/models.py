from django.db import models
from app.models import Institut

# Create your models here.

class GlobalPaymentType(models.Model):
    name = models.CharField(max_length=100)
    payment_categories = models.ManyToManyField(
        'GlobalPaymentCategory',
        blank=True,
        related_name="payment_types",
        verbose_name="Catégories de paiement"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Global Payment Type"
        verbose_name_plural = "Global Payment Types"

    def __str__(self):
        return self.name

class GlobalPaymentCategory(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Global Payment category"
        verbose_name_plural = "Global Payment categories"

    def __str__(self):
        return self.name

class GlobalDepensesCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )
    payment_category = models.ForeignKey('GlobalPaymentCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='depense_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Global Depense category"
        verbose_name_plural = "Global Depenses categories"

    def __str__(self):
        return self.name

class PostesBudgetaire(models.Model):
    label = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sub_postes')
    
    TYPE_CHOICES = (
        ('depense', 'Dépense'),
        ('recette', 'Recette'),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='depense')

    depense_categories = models.ManyToManyField('GlobalDepensesCategory', blank=True, related_name='postes_budgetaires')
    payment_categories = models.ManyToManyField('GlobalPaymentCategory', blank=True, related_name='postes_budgetaires')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Poste Budgetaire"
        verbose_name_plural = "Postes Budgetaires"

    def __str__(self):
        return self.label

class BudgetCampaign(models.Model):
    name = models.CharField(max_length=255)
    date_debut = models.DateField()
    date_fin = models.DateField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Campagne Budgétaire"
        verbose_name_plural = "Campagnes Budgétaires"

    def __str__(self):
        return self.name

    @property
    def status_label(self):
        from datetime import date
        if self.is_active:
            return "Active"
        # If not active and end date is past, it's closed
        if self.date_fin < date.today():
            return "Clôturée"
        # If not active and end date is future/today, it's pending start
        return "En attente"

class BudgetLine(models.Model):
    campaign = models.ForeignKey(BudgetCampaign, on_delete=models.CASCADE, related_name='lines')
    institut = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='budget_lines')
    montant = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    STATUT_CHOICES = (
        ('draft', 'Brouillon'),
        ('submitted', 'Soumis'),
        ('validated', 'Validé'),
        ('rejected', 'Rejeté'),
    )
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='draft')
    commentaire = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ligne Budgétaire"
        verbose_name_plural = "Lignes Budgétaires"
        unique_together = ('campaign', 'institut')

    def __str__(self):
        return f"{self.campaign} - {self.institut}"

class BudgetLineDetail(models.Model):
    campaign = models.ForeignKey(BudgetCampaign, on_delete=models.CASCADE, related_name='details')
    institut = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='budget_details')
    poste = models.ForeignKey(PostesBudgetaire, on_delete=models.CASCADE, related_name='budget_details')
    payment_category = models.ForeignKey(GlobalPaymentCategory, on_delete=models.CASCADE, related_name='budget_details', null=True, blank=True)
    depense_category = models.ForeignKey(GlobalDepensesCategory, on_delete=models.CASCADE, related_name='budget_details', null=True, blank=True)
    entreprise_id = models.IntegerField()  # ID of the Entreprise in tenant schema
    montant = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Quarterly Dispatch Percentages (0-100)
    t1_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0) # Aug-Oct
    t2_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0) # Nov-Jan
    t3_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0) # Feb-Apr
    t4_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0) # May-Jul
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Détail Budget"
        verbose_name_plural = "Détails Budget"
        unique_together = ('campaign', 'institut', 'poste', 'payment_category', 'depense_category', 'entreprise_id')

    def __str__(self):
        return f"{self.campaign} - {self.poste} - E{self.entreprise_id}"

class BudgetExtensionRequest(models.Model):
    campaign = models.ForeignKey(BudgetCampaign, on_delete=models.CASCADE, related_name='extension_requests')
    institut = models.ForeignKey(Institut, on_delete=models.CASCADE, related_name='extension_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('approved', 'Approuvée'),
        ('rejected', 'Rejetée'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    motif = models.TextField(verbose_name="Motif de la demande")
    admin_comment = models.TextField(null=True, blank=True, verbose_name="Commentaire Admin")

    class Meta:
        verbose_name = "Demande de Rallonge"
        verbose_name_plural = "Demandes de Rallonge"
        ordering = ['-created_at']

    def __str__(self):
        return f"Rallonge - {self.institut} - {self.campaign}"

class BudgetExtensionItem(models.Model):
    request = models.ForeignKey(BudgetExtensionRequest, on_delete=models.CASCADE, related_name='items')
    poste = models.ForeignKey(PostesBudgetaire, on_delete=models.CASCADE)
    payment_category = models.ForeignKey(GlobalPaymentCategory, on_delete=models.CASCADE, null=True, blank=True)
    depense_category = models.ForeignKey(GlobalDepensesCategory, on_delete=models.CASCADE, null=True, blank=True)
    entreprise_id = models.IntegerField(help_text="ID of the Entreprise in tenant schema")
    
    old_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant Actuel")
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Nouveau Montant")

    class Meta:
        verbose_name = "Détail Rallonge"
        verbose_name_plural = "Détails Rallonge"
