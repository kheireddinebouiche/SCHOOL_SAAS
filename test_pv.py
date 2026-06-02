import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school.settings')
django.setup()

from django_tenants.utils import schema_context
from app.models import Institut
from t_exam.models import ExamPlanification, PvExamen, ExamTypeNote, ExamNote, ModelBuilltins
from t_groupe.models import GroupeLine

tenant = Institut.objects.get(code_tenant='INS16')
with schema_context(tenant.schema_name):
    exam_plan = ExamPlanification.objects.get(id=33)
    
    # Fetch or generate PV
    pv_examen, created = PvExamen.objects.get_or_create(exam_planification=exam_plan)
    
    groupe = exam_plan.exam_line
    print(f"Groupe line: {groupe}")
    print(f"Groupe: {groupe.groupe}")
    print(f"Specialite: {groupe.groupe.specialite}")
    print(f"Formation: {groupe.groupe.specialite.formation}")
    
    modele_builtins = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)
    print(f"Modele Builtins: {modele_builtins}")
