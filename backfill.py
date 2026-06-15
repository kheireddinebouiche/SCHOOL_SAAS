import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from t_tresorerie.models import OperationsBancaire, SuiviChequeSortant

ops = OperationsBancaire.objects.filter(operation_type='sortie')
for op in ops:
    is_cheque = False
    if op.depense and op.depense.mode_paiement == 'che':
        is_cheque = True
    elif op.remboursement and op.remboursement.mode_rembourssement == 'che':
        is_cheque = True
    
    if is_cheque:
        statut = 'emis'
        has_date_paiement = False
        if op.depense and op.depense.date_paiement:
            has_date_paiement = True
        elif op.remboursement and op.remboursement.is_appliced:
            has_date_paiement = True
            
        if has_date_paiement or op.is_rapproche:
            statut = 'decaisse'
            
        obj, created = SuiviChequeSortant.objects.get_or_create(operation=op, defaults={'statut': statut})
        if created and statut == 'decaisse':
            obj.date_decaisse = op.date_operation
            obj.save()

print('Backfill complete.')
