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
