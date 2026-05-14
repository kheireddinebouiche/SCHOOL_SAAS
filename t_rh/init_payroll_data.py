from decimal import Decimal
from t_ressource_humaine.models import TrancheIRG, ParametresPaie
from institut_app.models import Entreprise

def initialize_payroll_data():
    # 1. Ensure Global Config exists
    ent = Entreprise.objects.first()
    config = ParametresPaie.get_config(entreprise=ent)
    
    # Update global defaults if they are set to 0 or defaults
    config.taux_ss = Decimal('0.09')
    config.seuil_exoneration_irg = Decimal('30000')
    config.save()

    
    # 2. Populate IRG 2022 Brackets if empty
    if not TrancheIRG.objects.exists():
        tranches = [
            (0, 20000, 0),
            (20000, 40000, 0.23),
            (40000, 80000, 0.27),
            (80000, 160000, 0.30),
            (160000, 320000, 0.33),
            (320000, None, 0.35),
        ]
        
        for mini, maxi, taux in tranches:
            TrancheIRG.objects.create(
                min_montant=Decimal(mini),
                max_montant=Decimal(maxi) if maxi else None,
                taux=Decimal(taux)
            )
        print("IRG Brackets initialized successfully.")

if __name__ == "__main__":
    initialize_payroll_data()
