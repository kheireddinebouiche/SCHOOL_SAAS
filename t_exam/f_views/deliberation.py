from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from t_exam.models import SessionExam, SessionExamLine, ExamPlanification, PvExamen, ExamTypeNote, ExamNote, ExamSousNote, ExamDecisionEtudiant, NoteBloc, BuiltinTypeNote, ModelBuilltins, DeliberationEtudiant
from t_groupe.models import Groupe, GroupeLine
from t_etudiants.models import Prospets
from t_formations.models import Modules
from django.db.models import Prefetch
from django.utils import timezone

# ReportLab imports for high-fidelity vector PDF generation
from reportlab.lib.pagesizes import A4, A3, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


@login_required(login_url="institut_app:login")
def groupe_deliberation_results_view(request, pk):

    session_line = get_object_or_404(SessionExamLine, id=pk)
    groupe = session_line.groupe

    # Get all session lines for this group and semester to compile complete results
    session_lines = SessionExamLine.objects.filter(
        groupe=groupe,
        semestre=session_line.semestre
    )

    # Get all exam planifications for these session lines
    exam_planifications = ExamPlanification.objects.filter(
        exam_line__in=session_lines
    ).select_related('module', 'pv')

    # Get all PVs for these exam planifications
    pvs = PvExamen.objects.filter(
        exam_planification__in=exam_planifications
    ).select_related('exam_planification__module').prefetch_related(
        'exam_types_notes__bloc',  # Get the bloc with in_pv_deliberation field
        'notes__etudiant',
        'notes__type_note',
        'notes__sous_notes',
        'decisions__etudiant'
    )

    # Cache NoteBloc IDs that appear in PV deliberation to avoid database queries in the loop
    delib_bloc_ids = set(NoteBloc.objects.filter(in_pv_deliberation=True).values_list('id', flat=True))

    # Get authorized note types for this group's formation model (with fallback to default model)
    model = ModelBuilltins.objects.filter(formation=groupe.specialite.formation).first()
    if not model:
        model = ModelBuilltins.objects.filter(is_default=True).first()

    if model:
        builtin_notes = {
            btn.code: btn
            for btn in BuiltinTypeNote.objects.filter(builtin=model)
        }
    else:
        builtin_notes = {}

    # Get all students in the group
    groupe_lines = GroupeLine.objects.filter(groupe=groupe).select_related('student')
    etudiants = [gl.student for gl in groupe_lines]

    # Group PVs by module
    modules_data = {}
    for pv in pvs:
        module = pv.exam_planification.module
        if module.id not in modules_data:
            modules_data[module.id] = {
                'module': module,
                'pvs': [],
                'all_exam_types_notes': [],
                'all_notes': [],
                'all_decisions': []
            }
        modules_data[module.id]['pvs'].append(pv)

    # Process each module to combine data from all its PVs
    pv_data = []
    for module_id, module_info in modules_data.items():
        module = module_info['module']
        pvs_list = module_info['pvs']

        # Collect all exam types notes from all PVs for this module
        exam_types_notes_dict = {}  # Use dict to avoid duplicates by code
        all_notes = []
        all_decisions = []

        for pv in pvs_list:
            # Get exam types notes that should appear in PV deliberation using prefetched cache
            # and filter/synchronize to keep only those authorized by the model configuration (BuiltinTypeNote)
            exam_types_notes = []
            for etn in pv.exam_types_notes.all():
                if etn.bloc_id in delib_bloc_ids and (not builtin_notes or etn.code in builtin_notes):
                    if builtin_notes and etn.code in builtin_notes:
                        # Dynamically synchronize sub-note configuration with the model in the database
                        btn = builtin_notes[etn.code]
                        etn.has_sous_notes = btn.has_sous_notes
                        etn.nb_sous_notes = btn.nb_sous_notes
                    exam_types_notes.append(etn)
            exam_types_notes.sort(key=lambda x: x.ordre)

            for etn in exam_types_notes:
                if etn.code not in exam_types_notes_dict:
                    exam_types_notes_dict[etn.code] = etn

            # Get all notes for these exam types from prefetched cache
            exam_types_notes_set = set(exam_types_notes)
            notes = [
                n for n in pv.notes.all()
                if n.type_note in exam_types_notes_set
            ]
            all_notes.extend(notes)

            # Get decisions for this PV from prefetched cache
            decisions = list(pv.decisions.all())
            all_decisions.extend(decisions)

        # Convert exam_types_notes_dict to ordered list
        exam_types_notes_list = sorted(exam_types_notes_dict.values(), key=lambda x: x.ordre)

        # Organize notes by student and type for easier access in template
        notes_by_student = {}
        for note in all_notes:
            student_id = note.etudiant.id
            type_note_code = note.type_note.code
            if student_id not in notes_by_student:
                notes_by_student[student_id] = {}
            
            # If there are multiple notes for same student and type (from different PVs),
            # we keep the latest or combine them based on your business logic
            if type_note_code not in notes_by_student[student_id]:
                notes_by_student[student_id][type_note_code] = []
            notes_by_student[student_id][type_note_code].append(note)

        # Organize decisions by student for easier access in template
        decisions_by_student = {}
        for decision in all_decisions:
            student_id = decision.etudiant.id
            # If student already has a decision, keep the one with non-zero moyenne
            # or the one with the highest moyenne (for rachat/rattrapage)
            if student_id in decisions_by_student:
                existing_decision = decisions_by_student[student_id]
                # Prioritize non-zero moyenne, or take the higher one
                if decision.moyenne and decision.moyenne > 0:
                    if not existing_decision.moyenne or existing_decision.moyenne == 0:
                        decisions_by_student[student_id] = decision
                    elif decision.moyenne > existing_decision.moyenne:
                        decisions_by_student[student_id] = decision
            else:
                decisions_by_student[decision.etudiant.id] = decision

        # Calculate total HTML columns for this module
        total_cols = 1  # 1 for Moyenne (UV)
        for etn in exam_types_notes_list:
            if etn.has_sous_notes:
                total_cols += etn.nb_sous_notes + 1
            else:
                total_cols += 1

        pv_data.append({
            'module': module,
            'pvs': pvs_list,
            'exam_types_notes': exam_types_notes_list,
            'notes': all_notes,
            'notes_by_student': notes_by_student,
            'decisions': all_decisions,
            'decisions_by_student': decisions_by_student,
            'total_columns': total_cols,
        })

    # Fetch deliberation records for this session line
    deliberations = DeliberationEtudiant.objects.filter(session_line=session_line)
    deliberations_by_student = {d.etudiant_id: d for d in deliberations}

    context = {
        'session_line': session_line,  # Pass the session line object
        'groupe': groupe,  # Pass the main group
        'etudiants': etudiants,
        'pv_data': pv_data,
        'deliberations_by_student': deliberations_by_student,
    }

    return render(request, 'tenant_folder/exams/groupe_deliberation_results.html', context)


@login_required(login_url="institut_app:login")
def groupe_deliberation_results_pdf_view(request, pk):
    session_line = get_object_or_404(SessionExamLine, id=pk)
    groupe = session_line.groupe

    # Get all session lines for this group and semester to compile complete results
    session_lines = SessionExamLine.objects.filter(
        groupe=groupe,
        semestre=session_line.semestre
    )

    # Get all exam planifications for these session lines
    exam_planifications = ExamPlanification.objects.filter(
        exam_line__in=session_lines
    ).select_related('module', 'pv')

    # Get all PVs for these exam planifications
    pvs = PvExamen.objects.filter(
        exam_planification__in=exam_planifications
    ).select_related('exam_planification__module').prefetch_related(
        'exam_types_notes__bloc',
        'notes__etudiant',
        'notes__type_note',
        'notes__sous_notes',
        'decisions__etudiant'
    )

    # Cache NoteBloc IDs that appear in PV deliberation to avoid database queries in the loop
    delib_bloc_ids = set(NoteBloc.objects.filter(in_pv_deliberation=True).values_list('id', flat=True))

    # Get authorized note types for this group's formation model (with fallback to default model)
    model = ModelBuilltins.objects.filter(formation=groupe.specialite.formation).first()
    if not model:
        model = ModelBuilltins.objects.filter(is_default=True).first()

    if model:
        builtin_notes = {
            btn.code: btn
            for btn in BuiltinTypeNote.objects.filter(builtin=model)
        }
    else:
        builtin_notes = {}

    # Get all students in the group
    groupe_lines = GroupeLine.objects.filter(groupe=groupe).select_related('student')
    etudiants = [gl.student for gl in groupe_lines]

    # Group PVs by module
    modules_data = {}
    for pv in pvs:
        module = pv.exam_planification.module
        if module.id not in modules_data:
            modules_data[module.id] = {
                'module': module,
                'pvs': [],
                'all_exam_types_notes': [],
                'all_notes': [],
                'all_decisions': []
            }
        modules_data[module.id]['pvs'].append(pv)

    # Process each module to combine data from all its PVs
    pv_data = []
    for module_id, module_info in modules_data.items():
        module = module_info['module']
        pvs_list = module_info['pvs']

        # Collect all exam types notes from all PVs for this module
        exam_types_notes_dict = {}  # Use dict to avoid duplicates by code
        all_notes = []
        all_decisions = []

        for pv in pvs_list:
            # Get exam types notes that should appear in PV deliberation using prefetched cache
            # and filter/synchronize to keep only those authorized by the model configuration (BuiltinTypeNote)
            exam_types_notes = []
            for etn in pv.exam_types_notes.all():
                if etn.bloc_id in delib_bloc_ids and (not builtin_notes or etn.code in builtin_notes):
                    if builtin_notes and etn.code in builtin_notes:
                        # Dynamically synchronize sub-note configuration with the model in the database
                        btn = builtin_notes[etn.code]
                        etn.has_sous_notes = btn.has_sous_notes
                        etn.nb_sous_notes = btn.nb_sous_notes
                    exam_types_notes.append(etn)
            exam_types_notes.sort(key=lambda x: x.ordre)

            for etn in exam_types_notes:
                if etn.code not in exam_types_notes_dict:
                    exam_types_notes_dict[etn.code] = etn

            # Get all notes for these exam types from prefetched cache
            exam_types_notes_set = set(exam_types_notes)
            notes = [
                n for n in pv.notes.all()
                if n.type_note in exam_types_notes_set
            ]
            all_notes.extend(notes)

            # Get decisions for this PV from prefetched cache
            decisions = list(pv.decisions.all())
            all_decisions.extend(decisions)

        # Convert exam_types_notes_dict to ordered list
        exam_types_notes_list = sorted(exam_types_notes_dict.values(), key=lambda x: x.ordre)

        # Organize notes by student and type for easier access
        notes_by_student = {}
        for note in all_notes:
            student_id = note.etudiant.id
            type_note_code = note.type_note.code
            if student_id not in notes_by_student:
                notes_by_student[student_id] = {}
            if type_note_code not in notes_by_student[student_id]:
                notes_by_student[student_id][type_note_code] = []
            notes_by_student[student_id][type_note_code].append(note)

        # Organize decisions by student for easier access
        decisions_by_student = {}
        for decision in all_decisions:
            student_id = decision.etudiant.id
            if student_id in decisions_by_student:
                existing_decision = decisions_by_student[student_id]
                if decision.moyenne and decision.moyenne > 0:
                    if not existing_decision.moyenne or existing_decision.moyenne == 0:
                        decisions_by_student[student_id] = decision
                    elif decision.moyenne > existing_decision.moyenne:
                        decisions_by_student[student_id] = decision
            else:
                decisions_by_student[decision.etudiant.id] = decision

        # Calculate total columns for this module
        total_cols = 1  # 1 for Moyenne (UV)
        for etn in exam_types_notes_list:
            if etn.has_sous_notes:
                total_cols += etn.nb_sous_notes + 1
            else:
                total_cols += 1

        pv_data.append({
            'module': module,
            'pvs': pvs_list,
            'exam_types_notes': exam_types_notes_list,
            'notes': all_notes,
            'notes_by_student': notes_by_student,
            'decisions': all_decisions,
            'decisions_by_student': decisions_by_student,
            'total_columns': total_cols,
        })

    # Setup the ReportLab document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="PV_Deliberation_{session_line.id}.pdf"'

    # Total grid columns
    total_grid_cols = 1 + sum(item['total_columns'] for item in pv_data) + 2

    # Dynamic page sizing and styling
    if total_grid_cols > 14:
        page_size = landscape(A3)
        margin = 15 * mm
        printable_width = 1105.5 - 2 * margin
        font_size_header = 7
        font_size_body = 7.5
    else:
        page_size = landscape(A4)
        margin = 10 * mm
        printable_width = 756.85 - 2 * margin
        font_size_header = 6.5
        font_size_body = 7

    doc = SimpleDocTemplate(
        response,
        pagesize=page_size,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=20 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    # Premium custom paragraph styles
    title_style = ParagraphStyle(
        'DelibTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=15,
        alignment=1,  # Centered
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DelibSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        alignment=1,  # Centered
        textColor=colors.HexColor("#475569"),
        spaceAfter=15
    )

    header_style = ParagraphStyle(
        'DelibHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=font_size_header,
        leading=font_size_header + 2,
        alignment=1,  # Centered
        textColor=colors.HexColor("#0f172a")
    )

    header_module_style = ParagraphStyle(
        'DelibHeaderModule',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=font_size_header + 1,
        leading=font_size_header + 3,
        alignment=1,  # Centered
        textColor=colors.HexColor("#0f172a")
    )

    header_sub_style = ParagraphStyle(
        'DelibHeaderSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=font_size_header - 0.5,
        leading=font_size_header + 1,
        alignment=1,  # Centered
        textColor=colors.HexColor("#475569")
    )

    student_style = ParagraphStyle(
        'DelibStudent',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=font_size_body,
        leading=font_size_body + 2,
        textColor=colors.HexColor("#0f172a")
    )

    cell_style = ParagraphStyle(
        'DelibCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=font_size_body,
        leading=font_size_body + 2,
        alignment=1,  # Centered
        textColor=colors.HexColor("#334155")
    )

    cell_moy_style = ParagraphStyle(
        'DelibCellMoy',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=font_size_body,
        leading=font_size_body + 2,
        alignment=1,  # Centered
        textColor=colors.HexColor("#0f172a")
    )

    # Initialize the header matrix (3 rows)
    header_matrix = [["" for _ in range(total_grid_cols)] for _ in range(3)]
    span_commands = []

    # Column 0: Student Name
    header_matrix[0][0] = Paragraph("<b>Étudiant</b>", header_style)
    span_commands.append(('SPAN', (0, 0), (0, 2)))

    col_idx = 1
    t_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#94a3b8")),
    ])

    for pv_item in pv_data:
        start_mod_col = col_idx
        end_mod_col = start_mod_col + pv_item['total_columns'] - 1

        # Fill module header
        header_matrix[0][start_mod_col] = Paragraph(f"<b>{pv_item['module'].label}</b>", header_module_style)
        span_commands.append(('SPAN', (start_mod_col, 0), (end_mod_col, 0)))

        etn_col_idx = start_mod_col
        for type_note in pv_item['exam_types_notes']:
            if type_note.has_sous_notes:
                span_width = type_note.nb_sous_notes + 1
                end_etn_col = etn_col_idx + span_width - 1

                # Note type header
                header_matrix[1][etn_col_idx] = Paragraph(f"<b>{type_note.libelle}</b>", header_style)
                span_commands.append(('SPAN', (etn_col_idx, 1), (end_etn_col, 1)))

                # Sub notes columns header (row 2)
                for sub_idx in range(type_note.nb_sous_notes):
                    header_matrix[2][etn_col_idx + sub_idx] = Paragraph(f"S{sub_idx + 1}", header_sub_style)
                
                # Final note of that type note header
                header_matrix[2][end_etn_col] = Paragraph(type_note.libelle, header_sub_style)

                etn_col_idx = end_etn_col + 1
            else:
                header_matrix[1][etn_col_idx] = Paragraph(f"<b>{type_note.libelle}</b>", header_style)
                span_commands.append(('SPAN', (etn_col_idx, 1), (etn_col_idx, 2)))
                etn_col_idx += 1

        # Moyenne UV header
        header_matrix[1][etn_col_idx] = Paragraph("<b>Moyenne (UV)</b>", header_style)
        span_commands.append(('SPAN', (etn_col_idx, 1), (etn_col_idx, 2)))

        col_idx = end_mod_col + 1

    # Last 2 columns: Décision Jury & Observation
    header_matrix[0][col_idx] = Paragraph("<b>Décision Jury</b>", header_style)
    span_commands.append(('SPAN', (col_idx, 0), (col_idx, 2)))

    header_matrix[0][col_idx + 1] = Paragraph("<b>Observation</b>", header_style)
    span_commands.append(('SPAN', (col_idx + 1, 0), (col_idx + 1, 2)))

    # Prepare table grid with headers
    table_data = list(header_matrix)

    # Populate rows for each student
    for etudiant in etudiants:
        row_data = [Paragraph(f"{etudiant.nom} {etudiant.prenom}", student_style)]
        
        for pv_item in pv_data:
            student_notes = pv_item['notes_by_student'].get(etudiant.id, {})
            
            for type_note in pv_item['exam_types_notes']:
                notes_list = student_notes.get(type_note.code, [])
                
                if type_note.has_sous_notes:
                    for sub_idx in range(type_note.nb_sous_notes):
                        val = "-"
                        if notes_list:
                            for note in notes_list:
                                sub_notes_list = list(note.sous_notes.all())
                                if sub_idx < len(sub_notes_list):
                                    val = str(sub_notes_list[sub_idx].valeur if sub_notes_list[sub_idx].valeur is not None else "-")
                        row_data.append(Paragraph(val, cell_style))
                    
                    main_val = "-"
                    if notes_list:
                        main_val = " / ".join(str(note.valeur if note.valeur is not None else "-") for note in notes_list)
                    row_data.append(Paragraph(main_val, cell_style))
                else:
                    main_val = "-"
                    if notes_list:
                        main_val = " / ".join(str(note.valeur if note.valeur is not None else "-") for note in notes_list)
                    row_data.append(Paragraph(main_val, cell_style))

            # Moyenne (UV) cell
            moy_val = "-"
            decision = pv_item['decisions_by_student'].get(etudiant.id, None)
            if decision and decision.moyenne is not None:
                moy_val = f"{decision.moyenne:.2f}"
            row_data.append(Paragraph(moy_val, cell_moy_style))

        # Blank spaces for manual entry of Jury Decision & Observation
        row_data.append(Paragraph("", cell_style))
        row_data.append(Paragraph("", cell_style))

        table_data.append(row_data)

    # Calculate column widths
    col_widths = []
    col_widths.append(85)
    
    mid_cols_count = total_grid_cols - 3
    remaining_w = printable_width - 85 - 80 - 80
    mid_w = remaining_w / mid_cols_count if mid_cols_count > 0 else 40
    
    if mid_w < 35 and page_size == landscape(A4):
        page_size = landscape(A3)
        printable_width = 1105.5 - 2 * margin
        remaining_w = printable_width - 85 - 80 - 80
        mid_w = remaining_w / mid_cols_count if mid_cols_count > 0 else 40
        doc.pagesize = page_size

    for _ in range(mid_cols_count):
        col_widths.append(mid_w)
        
    col_widths.append(80)
    col_widths.append(80)

    # Add SPAN commands to table style
    for cmd in span_commands:
        t_style.add(*cmd)

    # Add left alignment styling for student names
    t_style.add('ALIGN', (0, 3), (0, -1), 'LEFT')

    # Build the document story
    story = []
    
    # Header inside story
    story.append(Paragraph(f"PROCES-VERBAL DE DELIBERATION - GROUPE : {groupe.nom.upper()}", title_style))
    story.append(Paragraph(
        f"Session : {session_line.session.label} | Semestre : {session_line.semestre if session_line.semestre else 'N/A'} | Date d'Impression : {timezone.now().strftime('%d/%m/%Y')}",
        subtitle_style
    ))

    t = Table(table_data, colWidths=col_widths, repeatRows=3)
    t.setStyle(t_style)
    story.append(t)

    # Custom canvas drawer for header/footers
    class NumberedCanvas(canvas.Canvas):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._saved_page_states = []

        def showPage(self):
            self._saved_page_states.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            num_pages = len(self._saved_page_states)
            for state in self._saved_page_states:
                self.__dict__.update(state)
                self.draw_page_decorations(num_pages)
                super().showPage()
            super().save()

        def draw_page_decorations(self, page_count):
            self.saveState()
            width, height = self._pagesize
            
            # Header line and branding
            self.setFillColor(colors.HexColor("#1e293b"))
            self.setFont("Helvetica-Bold", 8)
            self.drawString(margin, height - 10 * mm, "SALDAE SYSTEMS - LOGICIEL DE GESTION SCOLAIRE")
            
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(margin, height - 12 * mm, width - margin, height - 12 * mm)
            
            # Footer line and details
            self.line(margin, 12 * mm, width - margin, 12 * mm)
            self.setFont("Helvetica", 7)
            self.setFillColor(colors.HexColor("#64748b"))
            self.drawString(margin, 8 * mm, f"Généré le: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
            self.drawRightString(width - margin, 8 * mm, f"Page {self._pageNumber} sur {page_count}")
            
            self.restoreState()

    doc.build(story, canvasmaker=NumberedCanvas)
    return response


@login_required(login_url="institut_app:login")
def api_save_deliberation_decision(request):
    if request.method == "POST":
        session_line_id = request.POST.get("session_line_id")
        student_id = request.POST.get("student_id")
        decision_jury = request.POST.get("decision_jury")
        observation = request.POST.get("observation")

        if not session_line_id or not student_id:
            return JsonResponse({"status": "error", "message": "Données manquantes."})

        session_line = get_object_or_404(SessionExamLine, id=session_line_id)
        student = get_object_or_404(Prospets, id=student_id)

        # Get all session lines for this group and semester to compile complete results
        session_lines = SessionExamLine.objects.filter(
            groupe=session_line.groupe,
            semestre=session_line.semestre
        )
        
        # Get all exam planifications for these session lines
        exam_planifications = ExamPlanification.objects.filter(
            exam_line__in=session_lines
        ).select_related('module', 'pv')
        
        # Get all PVs with related data
        pvs = PvExamen.objects.filter(
            exam_planification__in=exam_planifications
        ).prefetch_related(
            'notes__type_note',
            'decisions'
        )

        total_points = 0
        total_coef = 0

        # Group PVs by module to compute averages
        modules_dict = {}
        for pv in pvs:
            module = pv.exam_planification.module
            if module.id not in modules_dict:
                modules_dict[module.id] = []
            modules_dict[module.id].append(pv)

        for module_id, pvs_list in modules_dict.items():
            module = pvs_list[0].exam_planification.module
            all_decisions = []
            for pv in pvs_list:
                decision = next((d for d in pv.decisions.all() if d.etudiant_id == student.id), None)
                if decision:
                    all_decisions.append(decision)

            best_decision = None
            for decision in all_decisions:
                if not best_decision:
                    best_decision = decision
                elif decision.moyenne and decision.moyenne > 0:
                    if not best_decision.moyenne or best_decision.moyenne == 0:
                        best_decision = decision
                    elif decision.moyenne > best_decision.moyenne:
                        best_decision = decision

            coef = module.coef if module.coef else 1
            moy_coef = 0
            if best_decision and best_decision.moyenne:
                moy_coef = best_decision.moyenne * coef
                total_points += moy_coef
                total_coef += coef

        moyenne_semestre = round(total_points / total_coef, 2) if total_coef > 0 else 0

        # Get or create the DeliberationEtudiant record
        delib, created = DeliberationEtudiant.objects.get_or_create(
            session_line=session_line,
            etudiant=student
        )

        if decision_jury is not None:
            delib.decision_jury = decision_jury
        if observation is not None:
            delib.observation = observation
        delib.moyenne_semestre = moyenne_semestre
        delib.save()

        return JsonResponse({
            "status": "success", 
            "message": "Enregistrement réussi.",
            "moyenne_semestre": moyenne_semestre
        })

    return JsonResponse({"status": "error", "message": "Requête invalide."})

