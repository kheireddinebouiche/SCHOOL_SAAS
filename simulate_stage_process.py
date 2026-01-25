import os
import django
from datetime import date, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from t_stage.models import Stage, FocusGroup, SeanceFocusGroup, PresentationProgressive, ConseilValidation, DecisionConseil
from t_crm.models import Prospets
from t_formations.models import Formateurs
from t_groupe.models import Groupe

def run_simulation():
    print("--- Démarrage de la simulation du processus de stage ---")
    
    # 1. Préparation des données (on récupère ou crée des objets existants)
    student = Prospets.objects.first()
    teacher = Formateurs.objects.first()
    groupe = Groupe.objects.first()
    
    if not student or not teacher:
        print("Erreur: Vous devez avoir au moins un étudiant (Prospets) et un formateur en base pour exécuter la simulation.")
        return

    # 2. Création d'un Stage
    stage = Stage.objects.create(
        etudiant1=student,
        encadrant=teacher,
        groupe=groupe,
        sujet="Simulation d'implémentation de processus de stage",
        problematique="Comment automatiser le suivi des stages ?",
        date_debut=date.today(),
        statut='en_cours'
    )
    print(f"1. Stage créé : {stage}")

    # 3. Création d'un Focus Group
    fg = FocusGroup.objects.create(
        nom="Groupe de recherche IA & Education",
        encadrant=teacher,
        thematique="Intelligence Artificielle"
    )
    fg.stages.add(stage)
    print(f"2. Focus Group créé et stage ajouté : {fg}")

    # 4. Simulation d'une séance de Focus Group
    seance = SeanceFocusGroup.objects.create(
        focus_group=fg,
        date_seance=django.utils.timezone.now(),
        duree_heures=4.0,
        compte_rendu="Première rencontre : discussion sur la méthodologie."
    )
    print(f"3. Séance de focus group enregistrée : {seance}")

    # 5. Les Présentations Progressives
    # P1 - 25% (Fin du 1er mois)
    p1 = PresentationProgressive.objects.create(
        stage=stage,
        etape=1,
        date_presentation=date.today() + timedelta(days=30),
        taux_avancement_declare=30,
        observations="Sujet validé, plan à affiner.",
        validee=True
    )
    print(f"4. Présentation P1 validée (30%)")

    # P2 - 70% (Fin du 3ème mois)
    p2 = PresentationProgressive.objects.create(
        stage=stage,
        etape=2,
        date_presentation=date.today() + timedelta(days=90),
        taux_avancement_declare=70,
        observations="Travail empirique bien avancé.",
        validee=True
    )
    print(f"5. Présentation P2 validée (70%)")

    # P3 - Soutenance à blanc (Fin du 5ème mois)
    p3 = PresentationProgressive.objects.create(
        stage=stage,
        etape=3,
        date_presentation=date.today() + timedelta(days=150),
        taux_avancement_declare=90,
        observations="Prêt pour le conseil de validation.",
        validee=True,
        examinateur=teacher # Utilise le même pour la simu
    )
    print(f"6. Soutenance à blanc effectuée (90%)")

    # 6. Conseil de Validation et décision finale
    conseil = ConseilValidation.objects.create(
        date_conseil=date.today() + timedelta(days=155),
        observations_generales="Promotion très active."
    )
    
    decision = DecisionConseil.objects.create(
        conseil=conseil,
        stage=stage,
        decision='soutenable',
        taux_final=98,
        commentaire="Excellent travail."
    )
    
    # Mise à jour du stage
    stage.taux_avancement = 98
    stage.statut = 'soutenu'
    stage.save()
    
    print(f"7. Conseil de validation terminé : Décision '{decision.get_decision_display()}'")
    print(f"--- Simulation terminée avec succès ---")

if __name__ == "__main__":
    run_simulation()
