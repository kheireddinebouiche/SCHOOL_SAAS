import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from app.models import Institut
from t_crm.models import FicheDeVoeux, FicheVoeuxDouble, Prospets
from t_formations.models import Promos

def check_fiches():
    tenant = Institut.objects.exclude(schema_name='public').first()
    if not tenant:
        return

    with schema_context(tenant.schema_name):
        p1 = Promos.objects.get(id=1)
        print(f"Promo: {p1.session} (ID: {p1.id})")
        
        fvs = FicheDeVoeux.objects.filter(promo_id=p1.id)
        print(f"Total FicheDeVoeux linked to promo: {fvs.count()}")
        for f in fvs:
            print(f"  Fiche ID: {f.id}, Prospect: {f.prospect} (statut: {f.prospect.statut}), Confirmed: {f.is_confirmed}")
            
        fvd = FicheVoeuxDouble.objects.filter(promo_id=p1.id)
        print(f"Total FicheVoeuxDouble linked to promo: {fvd.count()}")
        for f in fvd:
            print(f"  Fiche ID: {f.id}, Prospect: {f.prospect} (statut: {f.prospect.statut}), Confirmed: {f.is_confirmed}")

if __name__ == '__main__':
    check_fiches()
