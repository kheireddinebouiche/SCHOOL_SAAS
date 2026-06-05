from decimal import Decimal
from .models import ParametresPaie

class PaieEngine:
    """
    Moteur de calcul de paie - Règles Algériennes 2022
    """
    TAUX_SS = Decimal('0.09') # 9%

    @staticmethod
    def calculer_irg(imposable, config=None, is_particular=False):
        """
        Calcul de l'IRG selon le barème progressif, abattement 40% (min 1000, max 1500)
        et formules de lissage (LF 2022) pour cas général et cas particulier.
        """
        from .models import TrancheIRG
        imposable = Decimal(imposable)
        
        # Règle DGI: Arrondir le salaire imposable à la dizaine de DA inférieure avant le calcul
        imposable = (imposable // 10) * 10

        if config is None:
            config = ParametresPaie.get_config()
            
        if imposable <= config.seuil_exoneration_irg:
            return Decimal('0.00')

        # 1. Calcul de l'IRG Brut
        tranches = TrancheIRG.objects.all().order_by('min_montant')
        irg_brut = Decimal('0.00')
        
        if tranches.exists():
            for t in tranches:
                if imposable > t.min_montant:
                    borne_sup = t.max_montant if t.max_montant else imposable
                    base_calcul = min(imposable, borne_sup) - t.min_montant
                    irg_brut += base_calcul * t.taux
        else:
            # Fallback Barème Progressif 2022
            if imposable > 20000:
                base_23 = min(imposable, Decimal('40000')) - Decimal('20000')
                irg_brut += base_23 * Decimal('0.23')
            if imposable > 40000:
                base_27 = min(imposable, Decimal('80000')) - Decimal('40000')
                irg_brut += base_27 * Decimal('0.27')
            if imposable > 80000:
                base_30 = min(imposable, Decimal('160000')) - Decimal('80000')
                irg_brut += base_30 * Decimal('0.30')
            if imposable > 160000:
                base_33 = min(imposable, Decimal('320000')) - Decimal('160000')
                irg_brut += base_33 * Decimal('0.33')
            if imposable > 320000:
                base_35 = imposable - Decimal('320000')
                irg_brut += base_35 * Decimal('0.35')

        # 2. Premier abattement proportionnel de 40% (min 1000 DA, max 1500 DA)
        abattement = irg_brut * Decimal('0.40')
        if abattement < Decimal('1000.00'):
            abattement = Decimal('1000.00')
        elif abattement > Decimal('1500.00'):
            abattement = Decimal('1500.00')

        irg1 = max(Decimal('0.00'), irg_brut - abattement)

        # 3. Dispositifs de lissage (second abattement)
        if is_particular:
            # Cas particuliers (Retraités & Handicapés) entre 30 000 DA et 42 500 DA
            if 30000 < imposable <= 42500:
                irg_final = irg1 * Decimal('93') / Decimal('61') - Decimal('81213') / Decimal('41')
                return max(Decimal('0.00'), irg_final.quantize(Decimal('0.1')))
        else:
            # Cas général entre 30 000 DA et 35 000 DA
            if 30000 < imposable <= 35000:
                irg_final = irg1 * Decimal('137') / Decimal('51') - Decimal('27925') / Decimal('8')
                return max(Decimal('0.00'), irg_final.quantize(Decimal('0.1')))

        return irg1.quantize(Decimal('0.1'))


    @staticmethod
    def calculer_paie(contrat, jours_travailles=None, heures_travailles=0, primes_fixe=True, heures_absence=0, lignes_rubriques=None):
        """
        Calcule la fiche de paie complète.
        """
        config = ParametresPaie.get_config(entreprise=getattr(contrat, 'entreprise', None))
        taux_ss = Decimal(str(config.taux_ss))
        taux_ss_patronal = Decimal(str(getattr(config, 'taux_ss_patronal', '0.26')))
        snmg_valeur = Decimal(str(getattr(config, 'snmg_valeur', '20000.00')))
        jours_std = config.jours_travailles_standard
        heures_std = config.heures_mensuelles_standard
        
        # 1. Salaire de base
        # Fallback to hourly if mensalized base is 0 but hourly rate is present
        type_c = getattr(contrat, 'type_contrat', '')
        # Handle if type_contrat is an object (FK)
        if not isinstance(type_c, str):
            type_c = str(type_c)

        salaire_horaire = getattr(contrat, 'salaire_horaire', 0) or 0
        salaire_base_attr = getattr(contrat, 'salaire_base', 0) or 0

        if 'VACATION' in type_c or (not salaire_base_attr and salaire_horaire > 0):
            # Base = Taux * Heures
            salaire_base = Decimal(salaire_horaire) * Decimal(heures_travailles)
        else:
            # Base mensualisée
            salaire_base = Decimal(salaire_base_attr)
            
            # Vérification SNMG (si temps plein et jours standard)
            if salaire_base > 0 and salaire_base < snmg_valeur:
                salaire_base = snmg_valeur

            if jours_travailles < jours_std:
                 # Prorata temporis (Base * Jours / Standard)
                 salaire_base = (salaire_base * Decimal(jours_travailles)) / Decimal(jours_std)


        # 2. Primes
        p_panier = getattr(contrat, 'prime_panier', 0) or 0 if primes_fixe else 0
        p_transport = getattr(contrat, 'prime_transport', 0) or 0 if primes_fixe else 0

        # Calculate retenue amount for absences based on hourly rate
        if heures_absence > 0:
            if 'VACATION' in type_c or (not salaire_base_attr and salaire_horaire > 0):
                taux_horaire = Decimal(salaire_horaire)
            else:
                # For monthly base, calculate hourly rate: Base / Standard Hours
                taux_horaire = Decimal(salaire_base_attr) / Decimal(heures_std)

            
            retenue_absences_montant = Decimal(heures_absence) * taux_horaire
        else:
            retenue_absences_montant = Decimal('0.00')
        
        
        # Process Dynamic Rubrics
        # lignes_rubriques = [{'rubrique': RubriqueObj, 'valeur': Decimal}, ...]
        total_gains_cotisables = Decimal('0.00')
        total_gains_imposables_non_cotisables = Decimal('0.00')
        total_gains_non_imposables = Decimal('0.00')
        total_retenues = Decimal('0.00')
        
        detail_lignes = []
        
        if lignes_rubriques:
            for ligne in lignes_rubriques:
                rubrique = ligne['rubrique']
                valeur = Decimal(ligne['valeur'])
                
                # Calculate Montant based on Mode
                if rubrique.mode_calcul == 'PERCENT':
                    montant = (valeur * salaire_base) / Decimal('100')
                elif rubrique.mode_calcul == 'ANCIENNETE':
                    date_recrutement = getattr(contrat.employee, 'date_recrutement', None) if contrat.employee else None
                    if date_recrutement:
                        from datetime import date
                        today = date.today()
                        annees = today.year - date_recrutement.year - ((today.month, today.day) < (date_recrutement.month, date_recrutement.day))
                        pourcentage_total = valeur * Decimal(annees)
                        montant = (pourcentage_total * salaire_base) / Decimal('100')
                    else:
                        montant = Decimal('0.00')
                elif rubrique.mode_calcul == 'HOURS':
                    # Use hourly rate
                    if 'VACATION' in type_c or (not salaire_base_attr and salaire_horaire > 0):
                        th = Decimal(salaire_horaire)
                    else:
                        th = Decimal(salaire_base_attr) / Decimal(heures_std)
                    montant = valeur * th
                elif rubrique.mode_calcul == 'JOURS':
                    montant = valeur * Decimal(jours_travailles)

                else: # FIXE
                    montant = valeur
                
                montant = montant.quantize(Decimal('0.01'))
                detail_lignes.append({'rubrique': rubrique, 'valeur_saisie': valeur, 'montant': montant})
                
                if rubrique.type_rubrique == 'GAIN':
                    if rubrique.est_cotisable:
                        total_gains_cotisables += montant
                    elif rubrique.est_imposable: 
                        total_gains_imposables_non_cotisables += montant
                    else:
                        total_gains_non_imposables += montant
                elif rubrique.type_rubrique == 'RETENUE':
                    total_retenues += montant

        # 3. Base SS (Salaire de base - Absences + Gains Cotisables)
        base_ss = max(Decimal('0.00'), salaire_base - retenue_absences_montant + total_gains_cotisables)
        
        # 4. Montant SS
        montant_ss = base_ss * taux_ss
        montant_ss_patronal = base_ss * taux_ss_patronal
        
        # 5. Imposable (Base SS - SS + Primes Imposables Non Cotisables)
        salaire_imposable = (base_ss - montant_ss) + total_gains_imposables_non_cotisables
        
        # 6. IRG
        if 'VACATION' in type_c:
            # Réglementation Algérienne: L'IRG pour les formateurs vacataires 
            # (activités d'enseignement/formation) est une retenue à la source forfaitaire (généralement 15% ou 10%)
            # sans abattement.
            taux_irg_vacataire = Decimal(str(getattr(config, 'taux_irg_vacataire', '0.10'))) # Taux de base à 10% historique (ou 15% selon LF récente)
            irg = (salaire_imposable * taux_irg_vacataire).quantize(Decimal('0.01'))
        else:
            employee = getattr(contrat, 'employee', None)
            formateur = getattr(contrat, 'formateur', None)
            is_particular = False
            if employee:
                is_particular = getattr(employee, 'is_particular_irg', False)
            elif formateur:
                is_particular = getattr(formateur, 'is_particular_irg', False)
            irg = PaieEngine.calculer_irg(salaire_imposable, config=config, is_particular=is_particular)
        
        # 7. Net
        net_a_payer = (salaire_imposable - irg) + total_gains_non_imposables + p_panier + p_transport - total_retenues
        
        return {
            'salaire_base_calcule': salaire_base,
            'retenue_absences_montant': retenue_absences_montant,
            'base_ss': base_ss,
            'montant_ss': montant_ss,
            'montant_ss_patronal': montant_ss_patronal,
            'salaire_imposable': salaire_imposable,
            'irg': irg,
            'net_a_payer': net_a_payer,
            'prime_panier': p_panier,
            'prime_transport': p_transport,
            'total_gains_cotisables': total_gains_cotisables,
            'total_gains_imposables_non_cotisables': total_gains_imposables_non_cotisables,
            'total_gains_non_imposables': total_gains_non_imposables,
            'total_retenues': total_retenues,
            'detail_lignes': detail_lignes
        }
