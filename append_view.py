# This will append the PrintBulletinPDF view to t_exam/f_views/builltins.py

import os

view_code = """

@login_required(login_url="institut_app:login")
@module_permission_required('exa', 'view')
def PrintBulletinPDF(request, session_line_id, student_id):
    from pdf_editor.models import DocumentTemplate
    from pdf_editor.utils import render_template_with_context
    from django.utils import timezone
    from django.http import HttpResponse

    try:
        session_line = SessionExamLine.objects.get(id=session_line_id)
        student = Prospets.objects.get(id=student_id)
        
        session_lines = SessionExamLine.objects.filter(groupe=session_line.groupe, semestre=session_line.semestre)
        exam_planifications = ExamPlanification.objects.filter(exam_line__in=session_lines).select_related('module', 'pv')
        
        pvs = PvExamen.objects.filter(exam_planification__in=exam_planifications).select_related('exam_planification__module', 'exam_planification').prefetch_related(
            'exam_types_notes__bloc',
            'notes__type_note',
            'notes__sous_notes',
            'decisions'
        )
        
        bulletin_bloc_ids = set(NoteBloc.objects.filter(Q(in_pv_deliberation=True) | Q(in_builltin_note=True)).values_list('id', flat=True))
        
        modules_dict = {}
        for pv in pvs:
            module = pv.exam_planification.module
            if module.id not in modules_dict:
                modules_dict[module.id] = {'module': module, 'pvs': []}
            modules_dict[module.id]['pvs'].append(pv)
        
        modules_data = []
        total_points = 0
        total_coef = 0
        
        for module_id, module_info in modules_dict.items():
            module = module_info['module']
            pvs_list = module_info['pvs']
            all_notes_for_module = []
            all_decisions_for_module = []
            for pv in pvs_list:
                exam_types_notes = [etn for etn in pv.exam_types_notes.all() if etn.bloc_id in bulletin_bloc_ids]
                exam_types_notes_set = set(exam_types_notes)
                notes = [n for n in pv.notes.all() if n.etudiant_id == student.id and n.type_note in exam_types_notes_set]
                all_notes_for_module.extend(notes)
                decision = next((d for d in pv.decisions.all() if d.etudiant_id == student.id), None)
                if decision:
                    all_decisions_for_module.append(decision)
            
            best_decision = None
            for decision in all_decisions_for_module:
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
            
            modules_data.append({
                'module': module,
                'decision': best_decision,
                'moy_coef': round(moy_coef, 2)
            })
            
        moyenne_semestre = round(total_points / total_coef, 2) if total_coef > 0 else 0
        deliberation = DeliberationEtudiant.objects.filter(session_line=session_line, etudiant=student).first()

        context_data = {
            'date_impression': timezone.now().date().strftime("%d/%m/%Y"),
            'entreprise': {
                'designation': getattr(request.tenant, 'nom', 'Institut'),
                'adresse': getattr(request.tenant, 'adresse', ''),
            },
            'etudiant': {
                'nom': student.nom,
                'prenom': student.prenom,
                'matricule': student.matricule or '',
                'date_naissance': student.date_naissance.strftime("%d/%m/%Y") if student.date_naissance else '',
                'lieu_naissance': student.lieu_naissance or ''
            },
            'session_line': {
                'session': {'nom_session': session_line.session.nom_session},
                'semestre': session_line.get_semestre_display() if hasattr(session_line, 'get_semestre_display') else session_line.semestre
            },
            'groupe': {'nom_groupe': session_line.groupe.nom if session_line.groupe else ''},
            'moyenne_semestre': str(moyenne_semestre),
            'total_points': str(round(total_points, 2)),
            'total_coef': str(total_coef),
            'deliberation': {'decision': deliberation.decision if deliberation else ''},
            'modules_data': []
        }
        
        for m_data in modules_data:
            module = m_data['module']
            decision = m_data['decision']
            context_data['modules_data'].append({
                'matiere': module.nom,
                'professeur': f"{module.professeur.nom} {module.professeur.prenom}" if module.professeur else '',
                'coef': module.coef or 1,
                'moyenne_matiere': str(round(decision.moyenne, 2)) if decision and decision.moyenne else '0',
                'total_points': str(m_data['moy_coef']),
                'observation': decision.observation if decision else ''
            })

        template = DocumentTemplate.objects.filter(template_type='bulletin', is_active=True).first()
        if not template:
            return HttpResponse("Modèle de bulletin introuvable. Veuillez le créer dans l'éditeur de documents.", status=404)
            
        html_content, error = render_template_with_context(template.content, context_data)
        if error:
            return HttpResponse(f"Erreur de rendu du modèle: {error}", status=500)
            
        try:
            from weasyprint import HTML
            from io import BytesIO
            from django.template.loader import render_to_string
            
            full_html = render_to_string('documents/pdf_base.html', {
                'content': html_content,
                'template': template,
                'entreprise': context_data['entreprise']
            })
            
            pdf_file = BytesIO()
            HTML(string=full_html, base_url=request.build_absolute_uri('/')).write_pdf(pdf_file)
            pdf_file.seek(0)
            
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="bulletin_{student.id}.pdf"'
            return response
            
        except ImportError:
            return HttpResponse(html_content)

    except Exception as e:
        return HttpResponse(f"Erreur: {str(e)}", status=500)
"""

with open(r"c:\Users\kheir\Documents\saldae\SCHOOL_SAAS\t_exam\f_views\builltins.py", "a", encoding="utf-8") as f:
    f.write(view_code)
print("Done appending")
