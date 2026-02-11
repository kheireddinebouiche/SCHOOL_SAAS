from django.db import models

# Create your models here.

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
