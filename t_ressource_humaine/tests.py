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
        # Brut = 6085
        # Abattement 40% = 2434, plafonné à 1500 DA
        # Total IRG attendu = 6085 - 1500 = 4585
        irg_attendu = Decimal('4585.00')
        
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

    def test_calcul_irg_cas_general_30900(self):
        irg = PaieEngine.calculer_irg(Decimal('30900.00'), is_particular=False)
        self.assertEqual(irg, Decimal('550.10'))

    def test_calcul_irg_cas_general_30930(self):
        irg = PaieEngine.calculer_irg(Decimal('30930.00'), is_particular=False)
        self.assertEqual(irg, Decimal('561.20'))

    def test_calcul_irg_cas_particulier_30900(self):
        irg = PaieEngine.calculer_irg(Decimal('30900.00'), is_particular=True)
        self.assertEqual(irg, Decimal('312.50'))

    def test_calcul_irg_cas_particulier_30930(self):
        irg = PaieEngine.calculer_irg(Decimal('30930.00'), is_particular=True)
        self.assertEqual(irg, Decimal('318.80'))

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

    def test_employee_primes_in_bulk_generation(self):
        """
        Teste si les primes d'un employé sont bien calculées en masse et sauvegardées lors de la validation.
        """
        from t_ressource_humaine.models import Rubrique, RubriqueContrat, FichePaie, LignePaie
        
        self.contrat.salaire_base = Decimal('50000.00')
        self.contrat.save()
        
        # Créer une rubrique de prime cotisable
        prime_assiduite = Rubrique.objects.create(
            libelle="Prime de Panier",
            type_rubrique='GAIN',
            mode_calcul='FIXE',
            est_cotisable=True,
            est_imposable=True,
            valeur_defaut=Decimal('3000.00')
        )
        
        # Associer la rubrique au contrat de l'employé avec une valeur personnalisée (4000.00)
        RubriqueContrat.objects.create(
            contrat=self.contrat,
            rubrique=prime_assiduite,
            valeur=Decimal('4000.00'),
            actif=True
        )
        
        # 1. Résolution des rubriques pour l'employé
        contract_rubrics_config = {rc.rubrique_id: rc for rc in RubriqueContrat.objects.filter(contrat=self.contrat)}
        all_rubriques = Rubrique.objects.filter(actif=True).prefetch_related('eligible_types')
        
        lignes_rubriques = []
        for r in all_rubriques:
            if r.eligible_types.exists() and not r.eligible_types.filter(label__icontains=self.contrat.type_contrat).exists():
                continue
            rc = contract_rubrics_config.get(r.id)
            valeur = r.valeur_defaut
            if rc:
                if not rc.actif:
                    continue
                valeur = rc.valeur
            if valeur != 0:
                lignes_rubriques.append({'rubrique': r, 'valeur': valeur})
                
        # 2. Calculer
        res = PaieEngine.calculer_paie(
            self.contrat,
            jours_travailles=22,
            heures_absence=0,
            lignes_rubriques=lignes_rubriques
        )
        
        # Assertions sur les calculs
        # Base = 50000. Prime = 4000. Base SS = 50000 + 4000 = 54000.
        # SS = 54000 * 0.09 = 4860.
        # Imposable = (54000 - 4860) = 49140.
        self.assertEqual(res['salaire_base_calcule'], Decimal('50000.00'))
        self.assertEqual(res['total_gains_cotisables'], Decimal('4000.00'))
        self.assertEqual(res['base_ss'], Decimal('54000.00'))
        self.assertEqual(res['montant_ss'], Decimal('4860.00'))
        self.assertEqual(res['salaire_imposable'], Decimal('49140.00'))
        
        # 3. Simuler la création de la fiche et des lignes de paie lors de la validation
        fiche, created = FichePaie.objects.update_or_create(
            contrat=self.contrat,
            mois=1,
            annee=2024,
            defaults={
                'entreprise': None,
                'jours_travailles': 22,
                'heures_absence': 0,
                'salaire_base_calcule': res['salaire_base_calcule'],
                'montant_ss': res['montant_ss'],
                'base_ss': res['base_ss'],
                'salaire_imposable': res['salaire_imposable'],
                'irg': res['irg'],
                'net_a_payer': res['net_a_payer'],
                'prime_panier': res['prime_panier'],
                'prime_transport': res['prime_transport'],
                'is_validated': True,
            }
        )
        
        # Sauvegarde des lignes de paie
        LignePaie.objects.filter(fiche_paie=fiche).delete()
        for ligne in res['detail_lignes']:
            LignePaie.objects.create(
                fiche_paie=fiche,
                rubrique=ligne['rubrique'],
                valeur_saisie=ligne['valeur_saisie'],
                montant=ligne['montant']
            )
            
        # Assertions sur la base de données
        self.assertEqual(LignePaie.objects.filter(fiche_paie=fiche).count(), 1)
        ligne_enregistree = LignePaie.objects.get(fiche_paie=fiche, rubrique=prime_assiduite)
        self.assertEqual(ligne_enregistree.montant, Decimal('4000.00'))
