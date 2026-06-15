import re

with open('t_tresorerie/f_views/caisse.py', 'r', encoding='utf-8') as f:
    content = f.read()

depense_find = "depenses = Depenses.objects.filter(reglements__isnull=True, mode_paiement__in=['vir', 'che'], date_paiement__gte=start_date, date_paiement__lte=end_date, etat=True).order_by('date_paiement').exclude(date_paiement__isnull=True).values("
depense_replace = "depenses = Depenses.objects.filter(reglements__isnull=True, mode_paiement__in=['vir', 'che'], date_paiement__gte=start_date, date_paiement__lte=end_date, etat=True).order_by('date_paiement').exclude(date_paiement__isnull=True).exclude(Q(mode_paiement='che') & ~Q(lettrages__suivi_cheque__statut='decaisse') & Q(lettrages__suivi_cheque__isnull=False)).values("
content = content.replace(depense_find, depense_replace)

remb_find = "remboursements = Rembourssements.objects.filter(\n        mode_rembourssement__in=['vir', 'che'], is_appliced=True, updated_at__date__gte=start_date, updated_at__date__lte=end_date\n    ).values("
remb_replace = "remboursements = Rembourssements.objects.filter(\n        mode_rembourssement__in=['vir', 'che'], is_appliced=True, updated_at__date__gte=start_date, updated_at__date__lte=end_date\n    ).exclude(Q(mode_rembourssement='che') & ~Q(lettrages__suivi_cheque__statut='decaisse') & Q(lettrages__suivi_cheque__isnull=False)).values("
content = content.replace(remb_find, remb_replace)

with open('t_tresorerie/f_views/caisse.py', 'w', encoding='utf-8') as f:
    f.write(content)
