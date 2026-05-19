import os
import django
import sys

sys.path.append(r'c:\Users\kheir\Documents\saldae\SCHOOL_SAAS')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "school.settings") 
django.setup()

from django.db import connection
from django_tenants.utils import get_tenant_model
from t_exam.models import SessionExamLine, ModelBuilltins, BuiltinTypeNote, NoteBloc

Tenant = get_tenant_model()
t = Tenant.objects.get(schema_name='alger')
connection.set_tenant(t)

try:
    sel = SessionExamLine.objects.get(id=16)
    groupe = sel.groupe
    specialite = groupe.specialite
    formation = specialite.formation
    print(f"SessionExamLine 16: ID={sel.id}, Semestre={sel.semestre}")
    print(f"Groupe: ID={groupe.id}, Name={groupe}")
    print(f"Specialite: ID={specialite.id}, Label={specialite.label}")
    print(f"Formation: ID={formation.id if formation else None}, Nom={formation.nom if formation else 'None'}")
    
    # Active model
    model = ModelBuilltins.objects.filter(formation=formation).first()
    print(f"Specific Model: {model}")
    default_model = ModelBuilltins.objects.filter(is_default=True).first()
    print(f"Default Model: {default_model}")
    
    active_model = model if model else default_model
    print(f"Active Model: {active_model}")
    
    if active_model:
        print("\nBuiltinTypeNotes in Active Model:")
        for btn in BuiltinTypeNote.objects.filter(builtin=active_model):
            print(f" - Code: {btn.code}, Libelle: {btn.libelle}, Bloc: {btn.bloc.label if btn.bloc else 'None'}, is_calculee: {btn.is_calculee}, has_sous_notes: {btn.has_sous_notes}, nb_sous_notes: {btn.nb_sous_notes}")
            
    # Let's also look at all NoteBlocs
    print("\nNote Blocs:")
    for nb in NoteBloc.objects.all():
        print(f" - Code: {nb.code}, Label: {nb.label}, in_pv_deliberation: {nb.in_pv_deliberation}, in_builltin_note: {nb.in_builltin_note}")

    # Let's see if there are other BuiltinTypeNotes in this tenant
    print("\nAll BuiltinTypeNotes in this tenant:")
    for btn in BuiltinTypeNote.objects.all():
        print(f" - Model: {btn.builtin.label} (ID={btn.builtin.id}, Formation={btn.builtin.formation}), Code: {btn.code}, Libelle: {btn.libelle}, has_sous_notes: {btn.has_sous_notes}, nb_sous_notes: {btn.nb_sous_notes}")

except Exception as e:
    import traceback
    traceback.print_exc()
