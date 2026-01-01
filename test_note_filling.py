# Test script to verify the note filling functionality
# This script will test the models and view functions

from django.test import TestCase
from t_exam.models import *
from t_etudiants.models import Prospets
from t_groupe.models import Groupe
from t_formations.models import Formation, Specialite, Modules
from t_timetable.models import Salle
from django.contrib.auth.models import User
from datetime import datetime

class NoteFillingTest(TestCase):
    def setUp(self):
        # Create necessary objects for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create formation and specialite
        self.formation = Formation.objects.create(label="Test Formation")
        self.specialite = Specialite.objects.create(nom="Test Specialite", formation=self.formation)
        
        # Create groupe
        self.groupe = Groupe.objects.create(nom="Test Groupe", specialite=self.specialite)
        
        # Create module
        self.module = Modules.objects.create(
            label="Test Module",
            specialite=self.specialite,
            code_module="TM001",
            coef=2.0,
            duree=30
        )
        
        # Create salle
        self.salle = Salle.objects.create(nom="Salle A", code="SA001")
        
        # Create student
        self.etudiant = Prospets.objects.create(
            nom="Test",
            prenom="Student",
            groupe=self.groupe
        )
        
        # Create session exam
        self.session_exam = SessionExam.objects.create(
            label="Test Session",
            code="TS001",
            type_session="normal",
            date_debut=datetime.now(),
            date_fin=datetime.now()
        )
        
        # Create session exam line
        self.session_line = SessionExamLine.objects.create(
            session=self.session_exam,
            groupe=self.groupe,
            semestre="1",
            date_debut=datetime.now().date(),
            date_fin=datetime.now().date()
        )
        
        # Create exam planification
        self.exam_plan = ExamPlanification.objects.create(
            exam_line=self.session_line,
            salle=self.salle,
            date=datetime.now(),
            module=self.module,
            heure_debut=datetime.now().time(),
            heure_fin=datetime.now().time()
        )
        
        # Create model builtin
        self.model_builtin = ModelBuilltins.objects.create(
            label="Test Model",
            formation=self.formation,
            is_default=True
        )
        
        # Create builtin type notes
        self.builtin_type1 = BuiltinTypeNote.objects.create(
            builtin=self.model_builtin,
            code="INT1",
            libelle="Interrogation 1",
            max_note=20.0,
            has_sous_notes=True,
            nb_sous_notes=3,
            ordre=1
        )
        
        # Create builtin sous-notes
        self.builtin_sous1 = BuiltinSousNote.objects.create(
            type_note=self.builtin_type1,
            label="Assiduité",
            ordre=1
        )
        
        self.builtin_sous2 = BuiltinSousNote.objects.create(
            type_note=self.builtin_type1,
            label="Contrôle continue",
            ordre=2
        )
        
        self.builtin_sous3 = BuiltinSousNote.objects.create(
            type_note=self.builtin_type1,
            label="Teste",
            ordre=3
        )

    def test_pv_creation(self):
        """Test PV creation"""
        pv = PvExamen.objects.create(exam_planification=self.exam_plan)
        self.assertIsNotNone(pv)
        self.assertEqual(str(pv), f"PV - {self.module}")

    def test_exam_type_note_creation(self):
        """Test exam type note creation from builtin"""
        pv = PvExamen.objects.create(exam_planification=self.exam_plan)
        
        # Create exam type note from builtin
        exam_type = ExamTypeNote.objects.create(
            pv=pv,
            code=self.builtin_type1.code,
            libelle=self.builtin_type1.libelle,
            max_note=self.builtin_type1.max_note,
            has_sous_notes=self.builtin_type1.has_sous_notes,
            nb_sous_notes=self.builtin_type1.nb_sous_notes,
            ordre=self.builtin_type1.ordre
        )
        
        self.assertEqual(exam_type.libelle, "Interrogation 1")
        self.assertTrue(exam_type.has_sous_notes)

    def test_exam_note_creation(self):
        """Test exam note creation"""
        pv = PvExamen.objects.create(exam_planification=self.exam_plan)
        
        exam_type = ExamTypeNote.objects.create(
            pv=pv,
            code="INT1",
            libelle="Interrogation 1",
            max_note=20.0,
            has_sous_notes=True,
            nb_sous_notes=3,
            ordre=1
        )
        
        exam_note = ExamNote.objects.create(
            pv=pv,
            etudiant=self.etudiant,
            type_note=exam_type,
            valeur=15.5
        )
        
        self.assertEqual(exam_note.etudiant, self.etudiant)
        self.assertEqual(exam_note.valeur, 15.5)

    def test_exam_sous_note_creation(self):
        """Test exam sous-note creation"""
        pv = PvExamen.objects.create(exam_planification=self.exam_plan)
        
        exam_type = ExamTypeNote.objects.create(
            pv=pv,
            code="INT1",
            libelle="Interrogation 1",
            max_note=20.0,
            has_sous_notes=True,
            nb_sous_notes=3,
            ordre=1
        )
        
        exam_note = ExamNote.objects.create(
            pv=pv,
            etudiant=self.etudiant,
            type_note=exam_type
        )
        
        sous_note = ExamSousNote.objects.create(
            note=exam_note,
            valeur=18.0
        )
        
        self.assertEqual(sous_note.note, exam_note)
        self.assertEqual(sous_note.valeur, 18.0)
        
        # Test calculation
        exam_note.calculer_valeur()
        self.assertEqual(exam_note.valeur, 18.0)  # Since there's only one sous-note

if __name__ == '__main__':
    import os
    import django
    from django.conf import settings
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')  # Replace with your project name
    django.setup()
    
    # Run the tests
    import unittest
    unittest.main()