from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from t_stage.models import Stage, FocusGroup, SeanceFocusGroup, PresentationProgressive, ConseilValidation, DecisionConseil
from t_crm.models import Prospets
from t_formations.models import Formateurs
from t_groupe.models import Groupe

class Command(BaseCommand):
    help = "Simule le processus complet d'un stage pour vérification."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("--- Démarrage de la simulation du processus de stage ---"))
        
        # 1. Préparation des données
        student = Prospets.objects.first()
        teacher = Formateurs.objects.first()
        groupe = Groupe.objects.first()
        
        if not student or not teacher:
            self.stdout.write(self.style.ERROR("Erreur: Vous devez avoir au moins un étudiant (Prospets) et un formateur en base pour exécuter la simulation."))
            return

        # 2. Création d'un Stage
        stage = Stage.objects.create(
            etudiant1=student,
            encadrant=teacher,
            groupe=groupe,
            sujet="Simulation Processus Stage",
            problematique="Automatisation du suivi",
            date_debut=date.today(),
            statut='en_cours'
        )
        self.stdout.write(f"1. Stage créé : {stage}")

        # 3. Création d'un Focus Group
        fg, _ = FocusGroup.objects.get_or_create(
            nom="Groupe SIMU",
            encadrant=teacher,
            defaults={'thematique': "Simulation"}
        )
        fg.stages.add(stage)
        self.stdout.write(f"2. Focus Group créé/récupéré : {fg}")

        # 4. Séance
        seance = SeanceFocusGroup.objects.create(
            focus_group=fg,
            date_seance=timezone.now(),
            duree_heures=4.0,
            compte_rendu="Simu séance"
        )
        self.stdout.write(f"3. Séance enregistrée : {seance}")

        # 5. Présentations
        for etape, taux in [(1, 30), (2, 70), (3, 90)]:
            p = PresentationProgressive.objects.create(
                stage=stage,
                etape=etape,
                date_presentation=date.today() + timedelta(days=etape*30),
                taux_avancement_declare=taux,
                validee=True
            )
            self.stdout.write(f" - P{etape} validée ({taux}%)")

        # 6. Conseil
        conseil = ConseilValidation.objects.create(
            date_conseil=date.today() + timedelta(days=160)
        )
        decision = DecisionConseil.objects.create(
            conseil=conseil,
            stage=stage,
            decision='soutenable',
            taux_final=98
        )
        
        stage.taux_avancement = 98
        stage.statut = 'soutenu'
        stage.save()
        
        self.stdout.write(self.style.SUCCESS(f"7. Conseil terminé : {decision.get_decision_display()}"))
        self.stdout.write(self.style.SUCCESS("--- Simulation terminée avec succès ---"))
