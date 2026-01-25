
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from t_ressource_humaine.models import Contrat, Rubrique, FichePaie, LignePaie
from t_ressource_humaine.logic import PaieEngine

def test_rubriques_dynamiques():
    print("--- Testing Dynamic Rubrics ---")
    
    # 1. Setup Data with Mock
    class MockEntreprise:
        id = 1
        
    class MockFormateur:
        def __str__(self): return "Formateur Test"

    class MockContrat:
        id = 1
        type_contrat = 'CDD'
        salaire_base = Decimal('50000.00')
        salaire_horaire = 0
        prime_transport = Decimal('1000.00')
        prime_panier = Decimal('1000.00')
        actif = True
        entreprise = MockEntreprise()
        formateur = MockFormateur()
    
    contrat = MockContrat()

    print(f"Using Mock Contract: Base {contrat.salaire_base}")

    # Create dummy Rubrics (DB required for these as they are FKs ideally, but Engine might not need FK if we pass objects)
    # However, LignePaie needs FK. But Engine just calculates.
    # We are testing PaieEngine.calculer_paie logic here.
    
    # We need real Rubrique objects if we want to query them or if engine uses attributes.
    # Engine uses .type_rubrique, .est_cotisable etc.
    # So we can use MockRubrique too!
    
    class MockRubrique:
        def __init__(self, libelle, type_r, cotisable, imposable):
            self.id = 1
            self.libelle = libelle
            self.type_rubrique = type_r
            self.est_cotisable = cotisable
            self.est_imposable = imposable
    
    prime_rendement = MockRubrique("Prime Rendement", 'GAIN', True, True)
    frais_mission = MockRubrique("Frais Mission", 'GAIN', False, False)
    retenue_pret = MockRubrique("Retenue Prêt", 'RETENUE', False, False)
    
    # 2. Simulate Calculation
    # Gains: +5000 (Cotisable), +2000 (Non Cotisable/Imposable)
    # Retenues: -1000
    
    lignes = [
        {'rubrique': prime_rendement, 'montant': Decimal('5000.00')},
        {'rubrique': frais_mission, 'montant': Decimal('2000.00')},
        {'rubrique': retenue_pret, 'montant': Decimal('1000.00')}
    ]
    
    from t_ressource_humaine.models import ParametresPaie
    # We need config for IRG. Engine calls PaieEngine.calculer_irg(val, config=config)
    # Logic: config = ParametresPaie.get_config(contrat.entreprise)
    # We need to mock get_config or the result.
    
    # Actually, logic.py logic:
    # config = ParametresPaie.get_config(contrat.entreprise)
    # irg = PaieEngine.calculer_irg(salaire_imposable, config=config)
    
    # So we need to ensure ParametresPaie.get_config works with MockEntreprise.
    # OR we can Mock PaieEngine.calculer_irg? No, we want to test it.
    
    # Let's hope ParametresPaie.get_config handles objects without DB access if we mock .objects?
    # No, it uses cls.objects.get_or_create.
    
    # Workaround:
    # We can create a real Config if DB works for it.
    # Or we can patch logic.py/ParametresPaie during test.
    # But simpler: The engine catches 'config' inside 'calculer_paie' ?
    # Let's check logic.py signature.
    # It accesses config inside.
    
    # If DB for ParametresPaie is fine, we are good.
    # verify_rubrics failed on Contrat only.
    
    # Let's try running this mock setup. 
    # If ParametresPaie fails, we will see.
    # NOTE: logic.py imports ParametresPaie.
    
    # We can also mock 'contrat.entreprise' to be None, then get_config(None) -> works.
    contrat.entreprise = None 

    
    # Base calculation
    # If CDD/CDI
    if contrat.type_contrat != 'VACATION':
        # Base: 50000 + 5000 = 55000 (Base SS)
        # SS: 55000 * 0.09 = 4950
        # Imposable: 55000 - 4950 = 50050
        # IRG: Scale(50050)
        # Net: (50050 - IRG) + 2000 - 1000
        pass
    
    res = PaieEngine.calculer_paie(contrat, jours_travailles=22, lignes_rubriques=lignes)
    
    print("\n--- Results ---")
    print(f"Salaire Base: {res['salaire_base_calcule']}")
    print(f"Gains Cotisables: {res['total_gains_cotisables']}")
    print(f"Base SS: {res['base_ss']}")
    print(f"Montant SS: {res['montant_ss']}")
    print(f"Gains Non Imposables: {res['total_gains_non_imposables']}")
    print(f"Total Retenues (Dynamic): {res['total_retenues']}")
    print(f"Net a Payer: {res['net_a_payer']}")
    
    # Verify logic
    expected_base_ss = max(Decimal(0), res['salaire_base_calcule'] - res['retenue_absences_montant'] + Decimal('5000.00'))
    
    if abs(res['base_ss'] - expected_base_ss) < 0.01:
        print("SUCCESS: Base SS includes cotisable gain.")
    else:
        print(f"FAILURE: Base SS mismatch. Got {res['base_ss']}, expected {expected_base_ss}")

    # Check Net flow
    # Net should include +2000 and -1000 directly
    # To verify exactly, we need IRG. But we can check if 2000 - 1000 net effect is there roughly
    # or just trust the components printed above if they match inputs.
    
    if res['total_gains_cotisables'] == Decimal('5000.00'):
        print("SUCCESS: Gains Cotisables correct.")
    
    if res['total_gains_non_imposables'] == Decimal('2000.00'):
        print("SUCCESS: Gains Non Imposables correct.")
        
    if res['total_retenues'] == Decimal('1000.00'):
        print("SUCCESS: Retenues correct.")

    # Cleanup
    # prime_rendement.delete()
    # frais_mission.delete() 
    # retenue_pret.delete()

if __name__ == "__main__":
    test_rubriques_dynamiques()
