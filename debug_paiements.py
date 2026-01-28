import os
import django
import sys

# Setup Django environment
sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from t_tresorerie.models import Paiements, PaymentCategory
from institut_app.models import Entreprise
from django.db.models import Sum, Q

from django_tenants.utils import schema_context
from app.models import Institut

def debug():
    print("Debugging Payments...")
    
    # Try to find a tenant
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        tenant = Institut.objects.first() # Fallback
    
    if not tenant:
        print("No tenant found.")
        return

    print(f"Using tenant: {tenant.nom} ({tenant.schema_name})")
    
    with schema_context(tenant.schema_name):
        entites = Entreprise.objects.all()
        print(f"Found {entites.count()} Entreprises.")
        
        paiements_count = Paiements.objects.count()
        print(f"Total Paiements in DB: {paiements_count}")
        
        for ent in entites:
            print(f"\n--- Entity: {ent.designation} ---")
            
            # Check via DuePaiements direct
            cnt_direct = Paiements.objects.filter(due_paiements__entite=ent).count()
            
            # Check via DuePaiements -> Echeancier
            cnt_echeancier = Paiements.objects.filter(
                due_paiements__entite__isnull=True, 
                due_paiements__ref_echeancier__entite=ent
            ).count()
            
            # Check via Prospect -> FicheDeVoeux -> Promo -> Entite
            # This is a heuristic backup path
            cnt_promo = Paiements.objects.filter(
                due_paiements__isnull=True,
                prospect__prospect_fiche_voeux__promo__entite=ent
            ).distinct().count()

            print(f"  Linked via DuePaiements.entite: {cnt_direct}")
            print(f"  Linked via DuePaiements.ref_echeancier.entite: {cnt_echeancier}")
            print(f"  Linked via Prospect.Promo.entite (heuristic for orphaned): {cnt_promo}")
            
        print("\n--- Category Check ---")
        cats = PaymentCategory.objects.all()
        print(f"Total Categories: {cats.count()}")
        roots = PaymentCategory.objects.filter(parent__isnull=True)
        print(f"Root Categories: {roots.count()}")
        for r in roots:
            print(f"  Root: {r.name}, Children: {r.children.count()}")

        from t_tresorerie.models import SpecialiteCompte
        print("\n--- Specialite Compte Check ---")
        mappings = SpecialiteCompte.objects.all()
        print(f"Total Mappings: {mappings.count()}")
        for m in mappings:
             print(f"  {m.specialite} -> {m.compte}")

        print("\n--- Payment Speciality Check ---")
        from django.apps import apps
        FicheDeVoeux = apps.get_model('t_crm', 'FicheDeVoeux')
        
        # Paiments linked to prospect
        linked_paiements = Paiements.objects.filter(prospect__isnull=False)
        print(f"Paiements with prospect: {linked_paiements.count()}")
        
        for p in linked_paiements[:10]:
             # Try to find speciality from fiche de voeux
             fiches = FicheDeVoeux.objects.filter(prospect=p.prospect)
             specs = [f.specialite.label for f in fiches if f.specialite]
             
             ent_due = p.due_paiements.entite if p.due_paiements else None
             ent_ech = p.due_paiements.ref_echeancier.entite if (p.due_paiements and p.due_paiements.ref_echeancier) else None
             
             # Check confirmation
             is_conf = any(f.is_confirmed for f in fiches)
             
             print(f"  Paiement {p.id}: Prospect {p.prospect}, Specs: {specs}, Confirmed: {is_conf}")
             print(f"     -> Due: {p.due_paiements}, EntiteDirect: {ent_due}, EntiteEch: {ent_ech}")

        print("\n--- Hierarchy Check ---")
        # Try to find the category linked in SpecialiteCompte for 'Bases de données'
        # From previous run we know it mapped to '704-101. BTS'
        # Let's find exactly that category
        
        target_cat = PaymentCategory.objects.filter(name__icontains="BTS").first()
        if target_cat:
             print(f"Target Category: {target_cat.name} (ID: {target_cat.id})")
             curr = target_cat
             chain = []
             while curr.parent:
                 chain.append(curr.parent.name)
                 curr = curr.parent
             print(f"  Ancestry (leaf -> root): {chain}")
             if not chain:
                 print("  It is a ROOT category.")
             else:
                 print(f"  Root Parent: {curr.name}")
                 print(f"  Is Root Parent in gathered roots? {roots.filter(id=curr.id).exists()}")
        else:
             print("Target Category BTS not found.")

if __name__ == '__main__':
    debug()
