import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context, get_tenant_model
from django.db.models import Sum
from t_tresorerie.models import Rembourssements, Paiements, DuePaiements
from t_groupe.models import GroupeLine, AffectationGroupe

print("=== Running Refund Details Logic Validation ===")

Tenant = get_tenant_model()
tenants = Tenant.objects.exclude(schema_name='public')

for tenant in tenants:
    print(f"\n--- Checking Tenant: {tenant.schema_name} ---")
    with schema_context(tenant.schema_name):
        refunds = Rembourssements.objects.all()
        print(f"Total refund requests: {refunds.count()}")
        
        if refunds.exists():
            obj = refunds.first()
            print(f"Testing with Refund ID {obj.id} for Client: {obj.client.nom} {obj.client.prenom}")
            
            # 1. Groupe Info
            groupes = []
            for gl in GroupeLine.objects.filter(student=obj.client):
                if gl.groupe and gl.groupe.nom not in groupes:
                    groupes.append(gl.groupe.nom)
            for aff in AffectationGroupe.objects.filter(etudiant=obj.client):
                if aff.groupe and aff.groupe.nom not in groupes:
                    groupes.append(aff.groupe.nom)
            group_display = ", ".join(groupes) if groupes else "Non affecté"
            print(f"  - Groupes: {group_display}")
            
            # 2. Absence History
            from t_etudiants.models import HistoriqueAbsence
            abs_query = HistoriqueAbsence.objects.filter(etudiant=obj.client)
            absences_list = []
            for abs_obj in abs_query:
                if abs_obj.historique:
                    for entry in abs_obj.historique:
                        entry_date = entry.get('date', 'N/A')
                        for detail in entry.get('data', []):
                            absences_list.append({
                                'date': entry_date,
                                'module': detail.get('module', 'N/A'),
                                'code': detail.get('code', 'N/A'),
                                'etat': detail.get('etat', 'Absent')
                            })
            print(f"  - Absences count: {len(absences_list)}")
            
            # 3. Echeancier
            due_query = DuePaiements.objects.filter(client=obj.client).order_by('date_echeance', 'id')
            echeancier_list = []
            for due in due_query:
                paid_amount = Paiements.objects.filter(due_paiements=due).aggregate(total=Sum('montant_paye'))['total'] or 0
                echeancier_list.append({
                    'label': due.label or 'N/A',
                    'montant_due': float(due.montant_due) if due.montant_due else 0.0,
                    'montant_paye': float(paid_amount),
                    'montant_restant': float(due.montant_restant) if due.montant_restant is not None else float((due.montant_due or 0) - paid_amount),
                    'date_echeance': due.date_echeance.strftime("%d/%m/%Y") if due.date_echeance else "N/A",
                    'is_done': due.is_done
                })
            print(f"  - Echeancier tranches count: {len(echeancier_list)}")
            if echeancier_list:
                print(f"    First tranche: {echeancier_list[0]}")

print("\n=== Validation complete ===")
