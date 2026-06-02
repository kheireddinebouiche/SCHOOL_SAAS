from django_tenants.test.cases import TenantTestCase
from decimal import Decimal
import datetime
from t_formations.models import Formateurs
from t_rh.models import Employees, Conges, Presence, HRConfig
from t_rh.payroll_utils import get_monthly_payroll_variables
from .models import Contrat, TypeContrat
from .logic import PaieEngine

class PaieEngineTest(TenantTestCase):
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

class PaieCongesTest(TenantTestCase):
    def setUp(self):
        self.employe = Employees.objects.create(nom="Test", prenom="Employe", etat="en cours")
        self.contrat = Contrat.objects.create(
            employee=self.employe,
            type_contrat=TypeContrat.CDI,
            date_debut=datetime.date(2024, 1, 1),
            salaire_base=Decimal('50000.00'),
            prime_transport=Decimal('0.00'),
            prime_panier=Decimal('0.00')
        )
        HRConfig.objects.create(heure_debut_standard=datetime.time(8, 0), heure_fin_standard=datetime.time(16, 30))

    def test_conge_paye_maintien_salaire(self):
        """
        Teste si un congé payé (Annuel) maintient le salaire de base
        """
        # Janvier 2024. Présence du 1er au 15
        last_presence_day = 1
        for i in range(1, 16):
            date_p = datetime.date(2024, 1, i)
            if date_p.weekday() not in [4, 5]: # Exclure vendredi/samedi
                Presence.objects.create(employee=self.employe, date=date_p, status='present')
                last_presence_day = i
        
        # Congé du 16 au 31
        Conges.objects.create(
            employee=self.employe,
            type_conge=Conges.TypeConge.ANNUEL,
            status=Conges.StatusConge.VALIDE,
            date_debut=datetime.date(2024, 1, last_presence_day + 1),
            date_fin=datetime.date(2024, 1, 31)
        )
        
        vars_paie = get_monthly_payroll_variables(self.employe, 1, 2024)
        result = PaieEngine.calculer_paie(self.contrat, jours_travailles=vars_paie['jours_travailles'])
        
        # 11 jours de présence + 12 jours de congés = 23 jours (>= 22 standard)
        self.assertGreaterEqual(vars_paie['jours_travailles'], 22)
        self.assertEqual(result['salaire_base_calcule'], Decimal('50000.00'))

    def test_conge_sans_solde_reduit_salaire(self):
        """
        Teste si un congé SANS SOLDE proratise (réduit) le salaire
        """
        last_presence_day = 1
        for i in range(1, 16):
            date_p = datetime.date(2024, 1, i)
            if date_p.weekday() not in [4, 5]: 
                Presence.objects.create(employee=self.employe, date=date_p, status='present')
                last_presence_day = i
        
        # Congé SANS SOLDE
        Conges.objects.create(
            employee=self.employe,
            type_conge=Conges.TypeConge.SANS_SOLDE,
            status=Conges.StatusConge.VALIDE,
            date_debut=datetime.date(2024, 1, last_presence_day + 1),
            date_fin=datetime.date(2024, 1, 31)
        )
        
        vars_paie = get_monthly_payroll_variables(self.employe, 1, 2024)
        result = PaieEngine.calculer_paie(self.contrat, jours_travailles=vars_paie['jours_travailles'])
        
        # Seulement 11 jours travaillés
        self.assertEqual(vars_paie['jours_travailles'], 11)
        
        # Salaire proratisé = 50000 * 11 / 22 = 25000
        self.assertEqual(result['salaire_base_calcule'], Decimal('25000.00'))

class PaieComplianceTest(TenantTestCase):
    def setUp(self):
        from t_rh.models import Contrats as HRContrats
        self.employe = Employees.objects.create(nom="Test", prenom="Compliance", etat="en cours")
        HRContrats.objects.create(employee=self.employe, date_embauche=datetime.date(datetime.date.today().year - 5, 1, 1))
        
        self.contrat = Contrat.objects.create(
            employee=self.employe,
            type_contrat=TypeContrat.CDI,
            date_debut=datetime.date(datetime.date.today().year - 5, 1, 1),
            salaire_base=Decimal('18000.00'), # Sous le SNMG
            prime_transport=Decimal('0.00'),
            prime_panier=Decimal('0.00')
        )
        HRConfig.objects.create(heure_debut_standard=datetime.time(8, 0), heure_fin_standard=datetime.time(16, 30))
        from t_ressource_humaine.models import ParametresPaie
        ParametresPaie.objects.create(taux_ss=Decimal('0.09'), taux_ss_patronal=Decimal('0.26'), snmg_valeur=Decimal('20000.00'), seuil_exoneration_irg=Decimal('30000.00'))

    def test_snmg_ajustement(self):
        result = PaieEngine.calculer_paie(self.contrat, jours_travailles=22)
        # Salaire devrait être ramené à 20000 (SNMG)
        self.assertEqual(result['salaire_base_calcule'], Decimal('20000.00'))
        
    def test_charges_patronales(self):
        result = PaieEngine.calculer_paie(self.contrat, jours_travailles=22)
        # Base SS sera 20000. Patronal = 20000 * 0.26 = 5200
        self.assertEqual(result['montant_ss_patronal'], Decimal('5200.00'))
        
    def test_calcul_iep_anciennete(self):
        from t_ressource_humaine.models import Rubrique
        rubrique_iep = Rubrique.objects.create(
            libelle="IEP", type_rubrique='GAIN', mode_calcul='ANCIENNETE', est_cotisable=True, est_imposable=True
        )
        # 2% par année d'expérience. 5 ans = 10%.
        lignes = [{'rubrique': rubrique_iep, 'valeur': Decimal('2.00')}]
        result = PaieEngine.calculer_paie(self.contrat, jours_travailles=22, lignes_rubriques=lignes)
        
        # Salaire Base = 20000 (SNMG). IEP = 10% de 20000 = 2000
        self.assertEqual(result['detail_lignes'][0]['montant'], Decimal('2000.00'))
        self.assertEqual(result['total_gains_cotisables'], Decimal('2000.00'))

    def test_carence_maladie(self):
        last_presence_day = 1
        for i in range(1, 16):
            date_p = datetime.date(2024, 1, i)
            if date_p.weekday() not in [4, 5]: 
                Presence.objects.create(employee=self.employe, date=date_p, status='present')
                last_presence_day = i
        
        Conges.objects.create(
            employee=self.employe, type_conge=Conges.TypeConge.MALADIE, status=Conges.StatusConge.VALIDE,
            date_debut=datetime.date(2024, 1, last_presence_day + 1), date_fin=datetime.date(2024, 1, 31)
        )
        vars_paie = get_monthly_payroll_variables(self.employe, 1, 2024)
        
        # Présence = 11 jours ouvrables. 
        # Congé du 16 au 31 (soit 12 jours ouvrables)
        # 3 jours de carence => 9 jours_conges_payes
        # jours_travailles = 11 + 9 = 20
        self.assertEqual(vars_paie['jours_travailles'], 20)
