from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ..models import ModelBuilltins, BuiltinTypeNote, BuiltinSousNote
from t_formations.models import Formation, Modules
from t_timetable.models import Salle
from t_exam.models import *
from t_groupe.models import Groupe,GroupeLine
from django.db import transaction, IntegrityError
import json
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# ReportLab imports for high-fidelity vector PDF generation
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm


@login_required(login_url="institut_app:login")
def GeneratePvModal(request, pk):
    obj = ExamPlanification.objects.get(id=pk)
    groupe = SessionExamLine.objects.get(id=obj.exam_line.id)

    modeleBuiltin = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)

    # Get students from the group
    all_students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id)

    # Get the commission results for the session if it exists
    commission_results = {}
    if groupe.session.commission:
        commission_results = {
            result.etudiants.id: result.result
            for result in CommisionResult.objects.filter(
                commission=groupe.session.commission,
                modules__id=obj.module.id  # Filter by the current module
            ).distinct()
        }

    # Filter students based on commission results and exam type
    exam_type = obj.type_examen
    filtered_students = []

    for student_line in all_students:
        student_id = student_line.student.id
        commission_result = commission_results.get(student_id, None)

        # Apply filtering based on exam type and commission result
        if exam_type == 'normal':
            # For normal exam, show ALL students regardless of commission result
            # But handle their status differently in the template
            filtered_students.append(student_line)
        elif exam_type == 'rachat':
            # For rachat exam, show students with 'rach' result
            if commission_result == 'rach':
                filtered_students.append(student_line)
        elif exam_type == 'rattrage':
            # For rattrapage exam, we need to find the original exam's PV to check ExamDecisionEtudiant
            # Look for the original normal exam for this module and group
            original_planification = ExamPlanification.objects.filter(
                exam_line=groupe,
                module=obj.module,
                type_examen='normal'  # Original normal exam
            ).first()

            if original_planification:
                original_pv = PvExamen.objects.filter(exam_planification=original_planification).first()
                if original_pv:
                    # Show students who have 'rattrapage' status in the original exam's decisions
                    if ExamDecisionEtudiant.objects.filter(pv=original_pv, etudiant=student_line.student, statut='rattrapage').exists():
                        filtered_students.append(student_line)
            else:
                # If no original exam found, check the current PV as fallback
                pv_examen, created = PvExamen.objects.get_or_create(exam_planification=obj)
                if ExamDecisionEtudiant.objects.filter(pv=pv_examen, etudiant=student_line.student, statut='rattrapage').exists():
                    filtered_students.append(student_line)
        else:
            # Default: show all students
            filtered_students.append(student_line)

    students = filtered_students

    session = groupe.session.get_type_session_display()
    date_debut = groupe.session.date_debut.date()
    date_fin = groupe.session.date_fin.date()
    module = obj.module.label
    note_eliminatoire = obj.module.n_elimate

    # Get or create the PvExamen record
    pv_examen, created = PvExamen.objects.get_or_create(exam_planification=obj)

    # If this is the first time creating the PV, create the ExamTypeNote records based on BuiltinTypeNote
    if created:
        for builtin_type_note in modeleBuiltin.types_notes.all().order_by('bloc__ordre', 'ordre'):  # Order by bloc first, then by ordre
            exam_type_note = ExamTypeNote.objects.create(
                pv=pv_examen,
                bloc=builtin_type_note.bloc,  # Copy the bloc from the builtin type note
                code=builtin_type_note.code,
                libelle=builtin_type_note.libelle,
                max_note=builtin_type_note.max_note,
                has_sous_notes=builtin_type_note.has_sous_notes,
                nb_sous_notes=builtin_type_note.nb_sous_notes,
                is_calculee=builtin_type_note.is_calculee,
                in_moyenne=builtin_type_note.in_moyenne,
                type_calcul=builtin_type_note.type_calcul,
                ordre=builtin_type_note.ordre,
                coefficient=builtin_type_note.coefficient
            )

            # Create ExamNote records for each student for this type of note
            for student_line in students:
                exam_note = ExamNote.objects.create(
                    pv=pv_examen,
                    etudiant=student_line.student,
                    type_note=exam_type_note,
                    valeur=None
                )

                # If this type note has sous-notes, create them
                if builtin_type_note.has_sous_notes and builtin_type_note.nb_sous_notes > 0:
                    for builtin_sous_note in builtin_type_note.sous_notes.all().order_by('ordre'):
                        ExamSousNote.objects.create(
                            note=exam_note,
                            valeur=0.0  # Use 0.0 instead of None to avoid NOT NULL constraint
                        )

        # Create dependencies for the exam type notes based on builtin dependencies
        for builtin_type_note in modeleBuiltin.types_notes.all():
            exam_type_note = ExamTypeNote.objects.filter(pv=pv_examen, code=builtin_type_note.code).first()
            if exam_type_note:
                for dependency in builtin_type_note.dependencies.all():
                    # Find the corresponding exam type note for the dependency
                    dependent_exam_note = ExamTypeNote.objects.filter(
                        pv=pv_examen,
                        code=dependency.child.code
                    ).first()
                    if dependent_exam_note:
                        ExamTypeNoteDependency.objects.get_or_create(
                            parent=exam_type_note,
                            child=dependent_exam_note
                        )

    # Get the builtin model to match the IDs used in the template
    modele_builtins = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)

    # Get the exam type notes for this PV
    exam_types_notes = pv_examen.exam_types_notes.all()

    # Create a mapping from builtin codes to exam type notes for filtering
    exam_type_notes_by_code = {etn.code: etn for etn in exam_types_notes}

    # Get builtin type notes based on exam type for filtering
    exam_type = obj.type_examen  # Get the actual type, not the display value
    if exam_type == 'normal':
        # For normal exam, get builtin types where both is_rattrapage and is_rachat are False
        builtin_types_to_include = modele_builtins.types_notes.filter(is_rattrapage=False, is_rachat=False).order_by('bloc__ordre', 'ordre')
    elif exam_type == 'rattrage':
        # For rattrapage exam, get builtin types where is_rattrapage is True
        builtin_types_to_include = modele_builtins.types_notes.filter(is_rattrapage=True).order_by('bloc__ordre', 'ordre')
    elif exam_type == 'rachat':
        # For rachat exam, get builtin types where is_rachat is True
        builtin_types_to_include = modele_builtins.types_notes.filter(is_rachat=True).order_by('bloc__ordre', 'ordre')
    else:
        # Default case: get all builtin type notes
        builtin_types_to_include = modele_builtins.types_notes.all().order_by('bloc__ordre', 'ordre')

    # Get corresponding exam type notes based on the builtin types
    all_types_notes = []
    for builtin_type in builtin_types_to_include:
        if builtin_type.code in exam_type_notes_by_code:
            all_types_notes.append(exam_type_notes_by_code[builtin_type.code])

    # Separate type notes with sub-notes from those without sub-notes
    # Show types with sub-notes first, then types without sub-notes
    types_with_sous_notes = [tn for tn in all_types_notes if tn.has_sous_notes and tn.nb_sous_notes > 0]
    types_without_sous_notes = [tn for tn in all_types_notes if not tn.has_sous_notes]

    # Combine the two lists: first with sub-notes, then without sub-notes
    filtered_types_notes = types_with_sous_notes + types_without_sous_notes

    # Get all available blocs for this model
    all_available_blocs = NoteBloc.objects.filter(types_notes__builtin=modele_builtins).distinct().order_by('ordre')

    # Group type notes by blocs for the template
    # Initialize all available blocs with empty types list
    blocs_with_types = {}
    bloc_order = {}  # To maintain bloc order

    # Initialize all available blocs
    for bloc in all_available_blocs:
        blocs_with_types[bloc.id] = {
            'bloc': bloc,
            'types': []
        }
        bloc_order[bloc.id] = bloc.ordre

    # Add 'no_bloc' entry for type notes without blocs
    blocs_with_types['no_bloc'] = {
        'bloc': None,
        'types': []
    }

    # Add filtered type notes to their respective blocs
    for type_note in filtered_types_notes:
        bloc = type_note.bloc
        bloc_key = bloc.id if bloc else 'no_bloc'

        if bloc_key in blocs_with_types:
            blocs_with_types[bloc_key]['types'].append(type_note)

    # Sort blocs by order
    sorted_bloc_keys = sorted([bloc.id for bloc in all_available_blocs],
                             key=lambda x: bloc_order[x])

    # Create ordered list of blocs with their types
    ordered_blocs_with_types = []
    for bloc_key in sorted_bloc_keys:
        ordered_blocs_with_types.append(blocs_with_types[bloc_key])

    # Add no_bloc if it has types
    if blocs_with_types['no_bloc']['types']:
        ordered_blocs_with_types.append(blocs_with_types['no_bloc'])

    # Create mappings between builtin type note IDs and exam type note objects
    builtin_to_exam_mapping = {}
    exam_to_builtin_mapping = {}  # This will map exam_type_note.id to builtin_type_note.id

    for exam_type_note in pv_examen.exam_types_notes.all():
        # Find the corresponding builtin type note by code
        builtin_type_note = modele_builtins.types_notes.filter(code=exam_type_note.code).first()
        if builtin_type_note:
            # Use the builtin type note ID as key to match template expectations
            builtin_to_exam_mapping[builtin_type_note.id] = exam_type_note
            # Also create reverse mapping for template access
            exam_to_builtin_mapping[exam_type_note.id] = builtin_type_note.id

    # Prepare data for the template - use builtin IDs as keys to match template
    student_notes_data = {}
    for student_line in students:
        student_notes_data[student_line.student.id] = {}
        for builtin_type_note in filtered_types_notes:  # Use filtered types instead of all
            # Get the corresponding builtin type note by code to get the ID
            corresponding_builtin = modele_builtins.types_notes.filter(code=builtin_type_note.code).first()
            if corresponding_builtin:
                # Get the corresponding exam type note
                exam_type_note = builtin_to_exam_mapping.get(corresponding_builtin.id)
                if exam_type_note:
                    exam_note = ExamNote.objects.filter(
                        pv=pv_examen,
                        etudiant=student_line.student,
                        type_note=exam_type_note
                    ).first()

                    if exam_note:
                        sous_notes_list = list(exam_note.sous_notes.all())

                        student_notes_data[student_line.student.id][corresponding_builtin.id] = {
                            'value': float(exam_note.valeur) if exam_note.valeur is not None else None,
                            'sous_notes': [{'valeur': float(sn.valeur) if sn.valeur is not None else None} for sn in sous_notes_list] if exam_type_note.has_sous_notes else []
                        }
                    else:
                        # If no exam note exists yet, create empty data structure
                        student_notes_data[student_line.student.id][corresponding_builtin.id] = {
                            'value': None,
                            'sous_notes': []
                        }

    # Get existing decisions for this PV
    decisions_existantes = {}

    # Get decisions for this specific PV
    for decision in ExamDecisionEtudiant.objects.filter(pv=pv_examen):
        decisions_existantes[decision.etudiant.id] = {
            'statut': decision.statut,
            'moyenne': decision.moyenne
        }

    # For makeup exams, we should look for the original exam's decisions for this module and group
    if exam_type == 'rattrage':
        # Find the original normal exams for this module and group
        original_planifications = ExamPlanification.objects.filter(
            exam_line=groupe,
            module=obj.module,
            type_examen='normal'  # Original normal exam
        )

        for original_plan in original_planifications:
            original_pv = PvExamen.objects.filter(exam_planification=original_plan).first()
            if original_pv:
                for decision in ExamDecisionEtudiant.objects.filter(pv=original_pv, statut='rattrapage'):
                    # Add the makeup decisions from the original exam
                    decisions_existantes[decision.etudiant.id] = {
                        'statut': decision.statut,
                        'moyenne': decision.moyenne
                    }

    # Pass the existing decisions to the template context
    existing_decisions = {}
    for decision in ExamDecisionEtudiant.objects.filter(pv=pv_examen):
        existing_decisions[decision.etudiant.id] = {
            'moyenne': decision.moyenne,
            'statut': decision.statut
        }

    # Get dependencies for calculated notes to pass to frontend
    # Create dependency mapping for frontend calculations
    dependencies_data = {}
    for builtin_type in builtin_types_to_include:
        exam_type_note = builtin_to_exam_mapping.get(builtin_type.id)
        if exam_type_note:
            # Get dependencies for this type note from the exam type note dependencies
            dependencies = []
            for dependency in exam_type_note.dependencies.all():  # Use exam type note dependencies
                # Find the corresponding builtin type note for the dependency to get the ID
                dependent_builtin = modele_builtins.types_notes.filter(code=dependency.child.code).first()
                if dependent_builtin:
                    dependencies.append({
                        'builtin_id': dependent_builtin.id,  # Use the builtin ID for frontend mapping
                        'code': dependency.child.code,
                        'libelle': dependency.child.libelle
                    })

            dependencies_data[builtin_type.id] = {
                'type_calcul': exam_type_note.type_calcul,
                'is_calculee': exam_type_note.is_calculee,
                'in_moyenne': exam_type_note.in_moyenne,
                'dependencies': dependencies,
                'max_note': exam_type_note.max_note,
                'has_sous_notes': exam_type_note.has_sous_notes,
                'nb_sous_notes': exam_type_note.nb_sous_notes,
                'coefficient': exam_type_note.coefficient
            }

    import json

    # Convert dependencies_data to JSON string for template
    dependencies_data_json = json.dumps(dependencies_data)

    # Determine which students should have their lines grayed out for normal exam type
    rach_ajou_students = set()
    rachat_only_students = set()  # Students specifically in rachat situation
    rachat_students_details = []  # Detailed information about rachat students
    commission_stats = {'total': 0, 'rach': 0, 'ajou': 0}

    if exam_type == 'normal':
        # For normal exam, identify students who have 'rach' or 'ajou' status in commission results
        for student_id, result in commission_results.items():
            if result in ['rach', 'ajou']:
                rach_ajou_students.add(student_id)

            # Specifically identify students in rachat situation for yellow highlighting
            if result == 'rach':
                rachat_only_students.add(student_id)

                # Get student details for rachat students
                from t_etudiants.models import Prospets
                try:
                    student = Prospets.objects.get(id=student_id)
                    rachat_students_details.append({
                        'id': student.id,
                        'nom': student.nom,
                        'prenom': student.prenom,
                        'matricule': student.matricule,
                        'matricule_interne': student.matricule_interne,
                    })
                except Prospets.DoesNotExist:
                    # Handle case where student doesn't exist
                    pass

            # Count statistics
            if result == 'rach':
                commission_stats['rach'] += 1
            elif result == 'ajou':
                commission_stats['ajou'] += 1

        # Total students with commission results
        commission_stats['total'] = len(commission_results)

    # Pass commission results to template for special handling
    context = {
        'pk': pk,
        'groupe': groupe,
        'modele': modeleBuiltin,
        'filtered_types_notes': filtered_types_notes,  # Pass the filtered types
        'ordered_blocs_with_types': ordered_blocs_with_types,  # Pass the grouped blocs with types
        'all_available_blocs': all_available_blocs,  # Pass all available blocs for reference
        'students': students,
        'pv_examen': pv_examen,
        'student_notes_data': student_notes_data,
        'session' : f"{session} - {date_debut}/{date_fin}",
        "module" : module,
        'note_eliminatoire' : note_eliminatoire,
        'decisions_existantes': decisions_existantes,
        'existing_decisions': existing_decisions,  # Pass existing decisions to template
        'commission_results': commission_results,  # Pass commission results to template
        'exam_planification': obj,  # Pass the exam planification object to template
        'dependencies_data': dependencies_data_json,  # Pass dependency data as JSON string for frontend calculations
        'builtin_types_to_include': builtin_types_to_include,  # Pass builtin types for template
        'exam_to_builtin_mapping': exam_to_builtin_mapping,  # Pass mapping for template access
        'rach_ajou_students': rach_ajou_students,  # Pass students with rachat/ajourné status
        'rachat_only_students': rachat_only_students,  # Pass students specifically in rachat situation
        'rachat_students_details': rachat_students_details,  # Pass detailed information about rachat students
        'commission_stats': commission_stats,  # Pass commission statistics
    }
    return render(request, 'tenant_folder/exams/remplissage_notes.html', context)


@login_required(login_url="institut_app:login")
def DownloadBlankPvsPdf(request):
    """
    Generates a single, high-fidelity landscape A4 PDF compiled server-side via ReportLab,
    containing blank PVs (Procès-Verbaux) for a list of comma-separated ExamPlanification IDs.
    """
    plan_ids_str = request.GET.get('plan_ids', '')
    if not plan_ids_str:
        return HttpResponse("Aucun examen spécifié.", status=400)
    
    try:
        plan_ids = [int(x) for x in plan_ids_str.split(',') if x.strip()]
    except ValueError:
        return HttpResponse("Liste d'examens invalide.", status=400)
        
    if not plan_ids:
        return HttpResponse("Aucun examen spécifié.", status=400)

    # Setup the ReportLab document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="PV_Vierges.pdf"'
    
    # Page setup: landscape A4
    doc = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        leftMargin=15*mm,
        rightMargin=15*mm,
        topMargin=15*mm,
        bottomMargin=15*mm
    )
    
    styles = getSampleStyleSheet()
    
    # Premium customized paragraph styles
    title_style = ParagraphStyle(
        'PVTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1,  # Centered
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'PVSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=12,
        alignment=1,  # Centered
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )
    
    meta_label_style = ParagraphStyle(
        'PVMetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#475569")
    )
    
    meta_val_style = ParagraphStyle(
        'PVMetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )
    
    cell_hdr_style = ParagraphStyle(
        'PVCellHdr',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        alignment=1,  # Centered
        textColor=colors.HexColor("#1e293b")
    )
    
    cell_data_style = ParagraphStyle(
        'PVCellData',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        alignment=1,  # Centered
        textColor=colors.HexColor("#0f172a")
    )
    
    cell_data_left_style = ParagraphStyle(
        'PVCellDataLeft',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        alignment=0,  # Left-aligned
        textColor=colors.HexColor("#0f172a")
    )

    story = []
    
    for plan_idx, pk in enumerate(plan_ids):
        try:
            obj = ExamPlanification.objects.get(id=pk)
        except ExamPlanification.DoesNotExist:
            continue
            
        # Check if the PV is already validated; if so, skip it for blank PV printing
        is_validated = obj.pv.est_valide if hasattr(obj, 'pv') else False
        if is_validated:
            continue
            
        groupe = SessionExamLine.objects.get(id=obj.exam_line.id)
        modeleBuiltin = ModelBuilltins.objects.get(formation=groupe.groupe.specialite.formation)
        all_students = GroupeLine.objects.filter(groupe_id=groupe.groupe.id)
        
        # Get commission results for session filtering if normal
        commission_results = {}
        if groupe.session.commission:
            commission_results = {
                result.etudiants.id: result.result
                for result in CommisionResult.objects.filter(
                    commission=groupe.session.commission,
                    modules__id=obj.module.id
                ).distinct()
            }
            
        # Filter students based on exam type and commission status
        exam_type = obj.type_examen
        filtered_students = []
        for student_line in all_students:
            student_id = student_line.student.id
            commission_result = commission_results.get(student_id, None)
            
            if exam_type == 'normal':
                filtered_students.append(student_line)
            elif exam_type == 'rachat':
                if commission_result == 'rach':
                    filtered_students.append(student_line)
            elif exam_type == 'rattrage':
                original_planification = ExamPlanification.objects.filter(
                    exam_line=groupe,
                    module=obj.module,
                    type_examen='normal'
                ).first()
                if original_planification:
                    original_pv = PvExamen.objects.filter(exam_planification=original_planification).first()
                    if original_pv:
                        if ExamDecisionEtudiant.objects.filter(pv=original_pv, etudiant=student_line.student, statut='rattrapage').exists():
                            filtered_students.append(student_line)
                else:
                    pv_examen = PvExamen.objects.filter(exam_planification=obj).first()
                    if pv_examen and ExamDecisionEtudiant.objects.filter(pv=pv_examen, etudiant=student_line.student, statut='rattrapage').exists():
                        filtered_students.append(student_line)
            else:
                filtered_students.append(student_line)

        # Get the PvExamen record if it exists
        pv_examen = PvExamen.objects.filter(exam_planification=obj).first()
        
        # Determine builtin note types to include
        if exam_type == 'normal':
            builtin_types_to_include = modeleBuiltin.types_notes.filter(is_rattrapage=False, is_rachat=False).order_by('bloc__ordre', 'ordre')
        elif exam_type == 'rattrage':
            builtin_types_to_include = modeleBuiltin.types_notes.filter(is_rattrapage=True).order_by('bloc__ordre', 'ordre')
        elif exam_type == 'rachat':
            builtin_types_to_include = modeleBuiltin.types_notes.filter(is_rachat=True).order_by('bloc__ordre', 'ordre')
        else:
            builtin_types_to_include = modeleBuiltin.types_notes.all().order_by('bloc__ordre', 'ordre')

        all_types_notes = list(builtin_types_to_include)
        types_with_sous_notes = [tn for tn in all_types_notes if tn.has_sous_notes and tn.nb_sous_notes > 0]
        types_without_sous_notes = [tn for tn in all_types_notes if not tn.has_sous_notes]
        filtered_types_notes = types_with_sous_notes + types_without_sous_notes

        # Construct PV layout structure
        if plan_idx > 0:
            story.append(PageBreak())
            
        # 1. Page Title
        session_name = groupe.session.get_type_session_display()
        date_debut_str = groupe.session.date_debut.date().strftime("%d/%m/%Y")
        date_fin_str = groupe.session.date_fin.date().strftime("%d/%m/%Y")
        session_label = f"Session d'examens : {session_name} ({date_debut_str} au {date_fin_str})"
        
        story.append(Paragraph("PROCES-VERBAL DE NOTES", title_style))
        story.append(Paragraph(session_label, subtitle_style))
        
        # 2. Meta Information Section
        meta_data = [
            [
                Paragraph("<b>Module / Matière :</b>", meta_label_style),
                Paragraph(obj.module.label, meta_val_style),
                Paragraph("<b>Type d'examen :</b>", meta_label_style),
                Paragraph(obj.get_type_examen_display(), meta_val_style)
            ],
            [
                Paragraph("<b>Groupe :</b>", meta_label_style),
                Paragraph(groupe.groupe.nom, meta_val_style),
                Paragraph("<b>Note Éliminatoire :</b>", meta_label_style),
                Paragraph(f"{obj.module.n_elimate or 0.0} / 20", meta_val_style)
            ],
            [
                Paragraph("<b>Date d'édition :</b>", meta_label_style),
                Paragraph(timezone.now().strftime("%d/%m/%Y"), meta_val_style),
                Paragraph("", meta_label_style),
                Paragraph("", meta_val_style)
            ]
        ]
        
        meta_table = Table(meta_data, colWidths=[100, 278, 100, 278])
        meta_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 15))
        
        # 3. Marks Grid Table Headers
        row0 = [
            Paragraph("N°", cell_hdr_style),
            Paragraph("Nom et Prénom", cell_hdr_style),
            Paragraph("Matricule", cell_hdr_style)
        ]
        row1 = [
            Paragraph("", cell_hdr_style),
            Paragraph("", cell_hdr_style),
            Paragraph("", cell_hdr_style)
        ]
        
        spans = [
            ('SPAN', (0, 0), (0, 1)),
            ('SPAN', (1, 0), (1, 1)),
            ('SPAN', (2, 0), (2, 1)),
        ]
        
        col_idx = 3
        for type_note in filtered_types_notes:
            if type_note.has_sous_notes and type_note.nb_sous_notes > 0:
                nb_sn = type_note.nb_sous_notes
                spans.append(('SPAN', (col_idx, 0), (col_idx + nb_sn, 0)))
                row0.append(Paragraph(f"{type_note.libelle}<br/>(Max: {type_note.max_note})", cell_hdr_style))
                for _ in range(nb_sn):
                    row0.append("")
                
                builtin_type = modeleBuiltin.types_notes.filter(code=type_note.code).first()
                if builtin_type:
                    for sn in builtin_type.sous_notes.all().order_by('ordre'):
                        row1.append(Paragraph(f"{sn.label}<br/>(Max: {sn.max_note})", cell_hdr_style))
                else:
                    for i in range(nb_sn):
                        row1.append(Paragraph(f"SN {i+1}", cell_hdr_style))
                
                total_lbl = type_note.libelle
                if type_note.is_calculee and type_note.type_calcul:
                    total_lbl += f" ({type_note.type_calcul})"
                else:
                    total_lbl += " (Total)"
                row1.append(Paragraph(total_lbl, cell_hdr_style))
                
                col_idx += nb_sn + 1
            else:
                spans.append(('SPAN', (col_idx, 0), (col_idx, 1)))
                row0.append(Paragraph(f"{type_note.libelle}<br/>(Max: {type_note.max_note})", cell_hdr_style))
                row1.append("")
                col_idx += 1
                
        # Average Column (Moyenne UV)
        spans.append(('SPAN', (col_idx, 0), (col_idx, 1)))
        row0.append(Paragraph("Moyenne UV", cell_hdr_style))
        row1.append("")
        total_cols = col_idx + 1
        
        table_data = [row0, row1]
        
        # Student marks grid population
        for idx, student_line in enumerate(filtered_students, 1):
            student_row = [
                Paragraph(str(idx), cell_data_style),
                Paragraph(f"{student_line.student.nom} {student_line.student.prenom}", cell_data_left_style),
                Paragraph(student_line.student.matricule_interne or student_line.student.matricule or "", cell_data_style)
            ]
            for _ in range(total_cols - 3):
                student_row.append("")
            table_data.append(student_row)
            
        # Column widths distribution for perfect A4 landscape alignment
        col_widths = [25, 130, 75]
        remaining_width = 756.85 - 25 - 130 - 75
        col_w = remaining_width / (total_cols - 3)
        for _ in range(total_cols - 3):
            col_widths.append(col_w)
            
        t_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), colors.HexColor("#f8fafc")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#475569")),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ] + spans)
        
        t = Table(table_data, colWidths=col_widths, repeatRows=2)
        t.setStyle(t_style)
        
        story.append(t)
        
    # Compile the final document
    doc.build(story)
    return response