from t_crm.models import Prospets, FicheDeVoeux, FicheVoeuxDouble
from t_formations.models import Promos
from t_tresorerie.models import PromoRembourssement

try:
    client = Prospets.objects.get(id=11)
    print(f"Client: {client.id} - {client.nom} {client.prenom}")
    print(f"Is Double: {client.is_double}")
    
    if client.is_double:
        fv = FicheVoeuxDouble.objects.filter(prospect=client, is_confirmed=True).last()
    else:
        fv = FicheDeVoeux.objects.filter(prospect=client, is_confirmed=True).last()
        
    if fv:
        print(f"Fiche ID: {fv.id}")
        print(f"Fiche.promo_id: {fv.promo_id}")
        if fv.promo:
            print(f"Promo Label: {fv.promo.label}")
            print(f"Promo ID from object: {fv.promo.id}")
            exists = Promos.objects.filter(id=fv.promo_id).exists()
            print(f"Promo ID {fv.promo_id} exists in Promos table: {exists}")
        else:
            print("Fiche has no promo linked.")
    else:
        print("No confirmed FicheDeVoeux/FicheVoeuxDouble found for this client.")
        # Check all fiches for this client
        all_fvs = FicheDeVoeux.objects.filter(prospect=client)
        print(f"Total FicheDeVoeux for client: {all_fvs.count()}")
        for f in all_fvs:
            print(f"  - ID: {f.id}, Confirmed: {f.is_confirmed}, Promo: {f.promo_id}")
            
    all_promos = list(Promos.objects.values_list('id', flat=True))
    print(f"All available Promo IDs in database: {all_promos}")

except Exception as e:
    print(f"Error: {e}")
