
from decimal import Decimal
from t_ressource_humaine.logic import PaieEngine
from t_ressource_humaine.models import Rubrique, Contrat, Entreprise, Formateurs, ParametresPaie

# Setup Mocks / Temporary Data
print("--- Starting Payroll Verification ---")


# Monkey-patch ParametresPaie.get_config to avoid DB access
def mock_get_config(entreprise=None):
    return MockConfig()

ParametresPaie.get_config = mock_get_config
print("Monkey-patched ParametresPaie.get_config")

# Mock Rubriques (In memory)
class MockRubrique:
    def __init__(self, type_r, cotisable, imposable):
        self.type_rubrique = type_r
        self.est_cotisable = cotisable
        self.est_imposable = imposable

# Mock Contrat
class MockContrat:
    def __init__(self, base):
        self.salaire_base = Decimal(base)
        self.salaire_horaire = Decimal(0)
        self.type_contrat = 'CDD'
        self.prime_transport = Decimal(0)
        self.prime_panier = Decimal(0)
        self.entreprise = None 

# Mock Config
class MockConfig:
    taux_ss = Decimal('0.09')
    jours_travailles_standard = 22
    heures_mensuelles_standard = Decimal('173.33')
    seuil_exoneration_irg = Decimal('30000')

# Test Case
print("Running Calculation...")

contrat = MockContrat('50000')

rub_cotisable = MockRubrique('GAIN', True, True) 
rub_non_imp = MockRubrique('GAIN', False, False)
rub_retenue = MockRubrique('RETENUE', False, False)

lignes = [
    {'rubrique': rub_cotisable, 'montant': Decimal('5000')},
    {'rubrique': rub_non_imp, 'montant': Decimal('2000')},
    {'rubrique': rub_retenue, 'montant': Decimal('1000')}
]

res = PaieEngine.calculer_paie(contrat, jours_travailles=22, lignes_rubriques=lignes)

print(f"Salaire Base: {res['salaire_base_calcule']}")
print(f"Gains Cotisables: {res['total_gains_cotisables']}")
print(f"Base SS: {res['base_ss']} (Expected: 50000 + 5000 = 55000)")
print(f"Montant SS: {res['montant_ss']} (Expected: 55000 * 0.09 = 4950)")

salaire_imposable_expected = Decimal('55000') - Decimal('4950') # = 50050
print(f"Salaire Imposable: {res['salaire_imposable']} (Expected: {salaire_imposable_expected})")

print(f"IRG: {res['irg']}")

net_expected_pre_irg = salaire_imposable_expected + Decimal('2000') - Decimal('1000') # + NonImp - Retenue
net_expected = net_expected_pre_irg - res['irg']

print(f"Net A Payer: {res['net_a_payer']} (Expected: {net_expected})")

if abs(res['net_a_payer'] - net_expected) < 0.01:
    print("SUCCESS: Calculation Verification Passed.")
else:
    print("FAILURE: Calculation Mismatch.")
