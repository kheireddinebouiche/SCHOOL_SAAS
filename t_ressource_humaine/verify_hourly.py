
import os
import django
from decimal import Decimal
from unittest.mock import patch, MagicMock

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from t_ressource_humaine.logic import PaieEngine
from t_ressource_humaine.models import Contrat

def test_absence_horaire_calcul():
    # Mock config
    mock_config = MagicMock()
    mock_config.taux_ss = Decimal('0.09')
    mock_config.jours_travailles_standard = 22
    mock_config.heures_mensuelles_standard = Decimal('173.33')
    mock_config.seuil_exoneration_irg = Decimal('30000')

    with patch('t_ressource_humaine.models.ParametresPaie.get_config', return_value=mock_config):
        # 1. Test CDI (Monthly)
        class CDIDeContrat:
            salaire_base = Decimal('50000.00')
            salaire_horaire = Decimal('0.00')
            type_contrat = 'CDD'
            prime_panier = Decimal('0.00')
            prime_transport = Decimal('0.00')
            entreprise = None

        contrat_cdi = CDIDeContrat()
        
        print("--- Test CDI (50000/month, 8h absence) ---")
        # Hourly rate should be 50000 / 173.33 = 288.467...
        # 8h absence = 2307.74
        res_cdi = PaieEngine.calculer_paie(contrat_cdi, jours_travailles=22, heures_absence=8)
        print(f"Retenue Montant: {res_cdi['retenue_absences_montant']}")
        print(f"Base SS: {res_cdi['base_ss']}")
        
        expected_retenue = (Decimal('50000.00') / Decimal('173.33')) * 8
        if abs(res_cdi['retenue_absences_montant'] - expected_retenue) < 0.01:
            print("SUCCESS: CDI Hourly deduction correct.")
        else:
            print(f"FAILURE: CDI Hourly deduction incorrect. Expected ~{expected_retenue}")

        # 2. Test Vacation
        class VacationContrat:
            salaire_base = Decimal('0.00')
            salaire_horaire = Decimal('1500.00')
            type_contrat = 'VACATION'
            prime_panier = Decimal('0.00')
            prime_transport = Decimal('0.00')
            entreprise = None

        contrat_vac = VacationContrat()
        
        print("\n--- Test Vacation (1500/h, 40h worked, 4h absence) ---")
        # Worked = 1500 * 40 = 60000
        # Absence = 1500 * 4 = 6000
        # Base SS = 54000
        res_vac = PaieEngine.calculer_paie(contrat_vac, heures_travailles=40, heures_absence=4)
        print(f"Salaire Base Calcule: {res_vac['salaire_base_calcule']}")
        print(f"Retenue Montant: {res_vac['retenue_absences_montant']}")
        print(f"Base SS: {res_vac['base_ss']}")
        
        if res_vac['retenue_absences_montant'] == Decimal('6000.00') and res_vac['base_ss'] == Decimal('54000.00'):
            print("SUCCESS: Vacation Hourly deduction correct.")
        else:
            print("FAILURE: Vacation Hourly deduction incorrect.")

if __name__ == "__main__":
    test_absence_horaire_calcul()
