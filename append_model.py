import os

model_code = '''

class SuiviChequeSortant(models.Model):
    operation = models.OneToOneField(OperationsBancaire, on_delete=models.CASCADE, related_name='suivi_cheque')
    statut = models.CharField(max_length=50, choices=[
        ('emis', 'Emis'),
        ('attente_signature', 'En attente de signature'),
        ('remis', 'Remis au client/fournisseur'),
        ('decaisse', 'Décaissé')
    ], default='emis')
    date_emis = models.DateTimeField(auto_now_add=True)
    date_attente_signature = models.DateTimeField(null=True, blank=True)
    date_remis = models.DateTimeField(null=True, blank=True)
    date_decaisse = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cheque pour operation {self.operation.id} - {self.statut}"
'''

with open('t_tresorerie/models.py', 'a', encoding='utf-8') as f:
    f.write(model_code)
