from t_formations.models import Promos
from t_crm.models import FicheDeVoeux, Prospets

print("--- Checking Promos ---")
promo_6 = Promos.objects.filter(id=6).first()
if promo_6:
    print(f"Promo 6 found: {promo_6.label} (code: {promo_6.code})")
else:
    print("Promo 6 NOT found in database.")
    
print("\n--- Checking All Promos ---")
all_promos = Promos.objects.all()
for p in all_promos:
    print(f"ID: {p.id}, Label: {p.label}")

print("\n--- Checking FicheDeVoeux for ID 11 ---")
try:
    client = Prospets.objects.get(id=11)
    print(f"Client 11: {client.nom} {client.prenom}")
    fvs = FicheDeVoeux.objects.filter(prospect_id=11)
    for f in fvs:
        print(f"Fiche ID: {f.id}, Promo ID: {f.promo_id}, Confirmed: {f.is_confirmed}")
except Exception as e:
    print(f"Error checking client: {e}")
