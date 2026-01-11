from django.test import TestCase
from decimal import Decimal
import datetime
from t_formations.models import Formateurs
from .models import Contrat, TypeContrat
from .logic import PaieEngine

class PaieEngineTest(TestCase):
    def setUp(self):
        self.formateur = Formateurs.objects.create(nom="Test", prenom="User")

    def test_calcul_paie_standard_cdd(self):
        """
        Test d'un salaire standard de 50,000 DA + Primes
        """
        contrat = Contrat.objects.create(
            formateur=self.formateur,
            type_contrat=TypeContrat.CDD,
            date_debut=datetime.date.today(),
            salaire_base=Decimal('50000.00'),
            prime_transport=Decimal('2000.00'),
            prime_panier=Decimal('4000.00')
        )
        
        # Act
        result = PaieEngine.calculer_paie(contrat, jours_travailles=22)
        
        # Assertions
        salaire_base = Decimal('50000.00')
        ss_attendue = salaire_base * Decimal('0.09') # 4500
        imposable_attendu = salaire_base - ss_attendue # 45500
        
        # IRG Calcul Manuelle sur 45500
        # 0-20000: 0
        # 20001-40000: 20000 * 0.23 = 4600
        # 40001-45500: 5500 * 0.27 = 1485
        # Total IRG = 6085
        irg_attendu = Decimal('6085.00')
        
        net_attendu = (imposable_attendu - irg_attendu) + Decimal('2000.00') + Decimal('4000.00')
        
        print(f"\n--- Resultats Test ---")
        print(f"Base: {result['salaire_base_calcule']}")
        print(f"SS: {result['montant_ss']} (Attendu: {ss_attendue})")
        print(f"Imposable: {result['salaire_imposable']} (Attendu: {imposable_attendu})")
        print(f"IRG: {result['irg']} (Attendu: {irg_attendu})")
        print(f"Net: {result['net_a_payer']} (Attendu: {net_attendu})")
        
        self.assertEqual(result['montant_ss'], ss_attendue)
        self.assertEqual(result['salaire_imposable'], imposable_attendu)
        self.assertEqual(result['irg'], irg_attendu)
        self.assertEqual(result['net_a_payer'], net_attendu)

    def test_exoneration_irg(self):
        """
        Test d'un salaire bas exonéré d'IRG (< 30,000 DA imposable)
        Base 32,000 -> SS 2,880 -> Imposable 29,120 (<30k) -> IRG 0
        """
        contrat = Contrat.objects.create(
            formateur=self.formateur,
            type_contrat=TypeContrat.CDD,
            date_debut=datetime.date.today(),
            salaire_base=Decimal('32000.00'),
            prime_transport=0,
            prime_panier=0
        )
        
        result = PaieEngine.calculer_paie(contrat, jours_travailles=22)
        
        self.assertEqual(result['irg'], Decimal('0.00'))
        self.assertEqual(result['net_a_payer'], result['salaire_imposable']) # Net = Imposable car IRG 0
