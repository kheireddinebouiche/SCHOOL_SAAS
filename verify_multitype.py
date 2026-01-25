
from decimal import Decimal
from t_ressource_humaine.logic import PaieEngine

# Mocking objects to avoid DB dependency in verification
class MockRubrique:
    def __init__(self, id, libelle, type_rubrique, mode_calcul, est_cotisable=True, est_imposable=True):
        self.id = id
        self.libelle = libelle
        self.type_rubrique = type_rubrique
        self.mode_calcul = mode_calcul
        self.est_cotisable = est_cotisable
        self.est_imposable = est_imposable

class MockContrat:
    def __init__(self, salaire_base, type_contrat='CDI'):
        self.salaire_base = Decimal(salaire_base)
        self.type_contrat = type_contrat
        self.salaire_horaire = None
        self.prime_panier = Decimal('0')
        self.prime_transport = Decimal('0')

class MockConfig:
    taux_ss = Decimal('0.09')
    jours_travailles_standard = Decimal('22')
    heures_mensuelles_standard = Decimal('173.33')
    seuil_exoneration_irg = Decimal('30000')

def run_test():
    print("--- Testing Multi-type Rubrics ---")
    
    # Patch ParametresPaie.get_config
    from t_ressource_humaine.models import ParametresPaie
    ParametresPaie.get_config = lambda entreprise=None: MockConfig()
    
    contrat = MockContrat(50000)
    config = MockConfig()
    
    # 1. Test Percentage Gain (e.g. IEP 10%)
    iep = MockRubrique(1, "IEP", "GAIN", "PERCENT", True, True)
    
    # 2. Test Hourly Deduction (e.g. Late 2 hours)
    retard = MockRubrique(2, "Retard", "RETENUE", "HOURS", False, False)
    
    lignes = [
        {'rubrique': iep, 'valeur': Decimal('10')},   # 10% of 50000 = 5000
        {'rubrique': retard, 'valeur': Decimal('2')} # 2h * (50000/173.33) ~= 2 * 288.47 = 576.94
    ]
    
    # Mocking PaieEngine.calculer_irg to simplify
    original_irg = PaieEngine.calculer_irg
    PaieEngine.calculer_irg = lambda x, config=None: Decimal('0') # Ignore IRG for simple math check
    
    result = PaieEngine.calculer_paie(contrat, 22, 0, lignes_rubriques=lignes)
    
    print(f"Base Salary: {contrat.salaire_base}")
    for ligne in result['detail_lignes']:
        print(f"Rubric: {ligne['rubrique'].libelle} | Value: {ligne['valeur_saisie']} | Calculated Montant: {ligne['montant']}")
    
    expected_iep = Decimal('5000.00')
    th = Decimal('50000') / Decimal('173.33')
    expected_retard = (Decimal('2') * th).quantize(Decimal('0.01'))
    
    print(f"Total Net: {result['net_a_payer']}")
    
    # Validation
    assert result['detail_lignes'][0]['montant'] == expected_iep
    assert result['detail_lignes'][1]['montant'] == expected_retard
    
    # (50000 + 5000) - (5000 + 500) * 0.09 = 55000 - 4950 = 50050.
    # Actually Net = (Imposable - IRG) + Non-Imposable - Retenues.
    # Base SS = 50000 + 5000 = 55000
    # SS = 4950
    # Imposable = 55000 - 4950 = 50050
    # Net = 50050 - 576.84 (rounded expected_retard) = 49473.06
    
    print("SUCCESS: Multi-type calculation PASSED")
    PaieEngine.calculer_irg = original_irg

if __name__ == "__main__":
    run_test()
