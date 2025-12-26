from ..models import *
from ..forms import *
from django.contrib import messages
from django.db import transaction
from t_crm.models import *
from t_tresorerie.models import *
from django.db.models import Count, Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from t_documents_maker.models import DocumentTemplate
from t_documents_maker.services.template_processor import TemplateProcessor
from t_documents_maker.services.pdf_generator import PDFGenerator
import json
from io import BytesIO

@login_required(login_url="institut_app:login")
def StudentDetails(request, pk):
    
    student = Prospets.objects.get(id = pk)

    if not student.is_double:
        groupe = GroupeLine.objects.filter(student = student)
        current_groupe = GroupeLine.objects.get(student = student, groupe__etat = "inscription" )
        paiements = Paiements.objects.filter(prospect = student)
        documents = DocumentsDemandeInscription.objects.filter(prospect = student)
        notes = NotesProcpects.objects.filter(prospect = student, context="etudiant")
        rappels = RendezVous.objects.filter(prospect = student, context="etudiant" )
        echeanciers = DuePaiements.objects.filter(client = student, type='frais_f').order_by('ordre')
        remises = RemiseAppliquerLine.objects.filter(prospect = student, remise_appliquer__is_approuved = True,remise_appliquer__is_applicated = True)        
        montant_due = DuePaiements.objects.filter(client = student, is_done=False, type='frais_f').aggregate(total=Sum('montant_restant'))['total'] or 0
        montant_paye = Paiements.objects.filter(prospect= student, context="frais_f").aggregate(total=Sum('montant_paye'))['total'] or 0
        montant_total = DuePaiements.objects.filter(client = student, type='fras_f').aggregate(total=Sum('montant_due'))['total'] or 0
        specialite_simple = FicheDeVoeux.objects.get(prospect = student, is_confirmed=True)
        modele_contrat = ModelContrat.objects.get(formation = specialite_simple.specialite.formation, annee_scolaire = specialite_simple.promo.annee_academique, status = "act")
        entreprise_details = Entreprise.objects.get(id = specialite_simple.specialite.formation.entite_legal.id)
        echancier_standard = EcheancierPaiement.objects.get(formation = specialite_simple.specialite.formation, is_active = True, is_default=True, is_approuved=True)
        echeancier_line = EcheancierPaiementLine.objects.filter(echeancier = echancier_standard).values('id','value','montant_tranche','date_echeancier')

        documents_available = current_groupe.groupe.specialite.formation.documents.all()

        try:
            echeancier_special = EcheancierSpecial.objects.filter(prospect = student).first()
            echeancier_special_line = EcheancierPaiementLine.objects.filter(echeancier_id = echeancier_special.id).values('id','value','montant_tranche','date_echeancier')
        except:
            echeancier_special = 0
            echeancier_special_line = []

        montant_formation = specialite_simple.specialite.formation.prix_formation
        frais_incription = echancier_standard.frais_inscription
        branche = specialite_simple.specialite.branche
        dossier_inscription = DossierInscription.objects.filter(formation = specialite_simple.specialite.formation).values('label')
        try:
            logo_partenanire = Partenaires.objects.get(id = current_groupe.groupe.specialite.formation.partenaire.id)
        except:
            logo_partenanire = None

        context = {
            'pk' : pk,
            'etudiant' : student,
            'groupe' : groupe,
            'paiements' : paiements,
            'documents' : documents,
            'notes' : notes,
            'rappels' : rappels,
            'echeanciers' : echeanciers,
            'montant_due' : montant_due,
            'montant_paye' : montant_paye,
            'total_a_paye' : montant_total,
            'remises' : remises,
            'specialite_simple' : specialite_simple.specialite.label if not student.is_double else None,
            'formation' : specialite_simple.specialite.formation.nom,
            'modele_contrat' : modele_contrat,
            'qualification' : specialite_simple.specialite.formation.qualification,
            'entreprise_details' : entreprise_details,
            'echeancier_standart' : echancier_standard,
            'echeancier_line' : json.dumps(list(echeancier_line), cls=DjangoJSONEncoder),
            'echeancier_special_line' : json.dumps(list(echeancier_special_line)),
            'dossier_inscription' : json.dumps(list(dossier_inscription), cls=DjangoJSONEncoder),
            'montant_formation' : montant_formation,
            'frais_incription' : frais_incription,
            'annee_academique' : specialite_simple.promo.annee_academique,
            'branche' : branche,
            'date_debut' : current_groupe.groupe.start_date,
            'date_fin' : current_groupe.groupe.end_date,
            'type_formation' : current_groupe.groupe.specialite.formation.type_formation,
            'logo_partenaire' : logo_partenanire.logo.url if logo_partenanire.logo else "",
            'documents_available':documents_available,
        }
        return render(request, 'tenant_folder/student/profile_etudiant.html',context)


    else:

        groupe = GroupeLine.objects.filter(student = student)
        paiements = Paiements.objects.filter(prospect = student)
        documents = DocumentsDemandeInscription.objects.filter(prospect = student)
        notes = NotesProcpects.objects.filter(prospect = student, context="etudiant")
        rappels = RendezVous.objects.filter(prospect = student, context="etudiant" )
        echeanciers = DuePaiements.objects.filter(client = student, type='frais_f').order_by('ordre')
        remises = RemiseAppliquerLine.objects.filter(prospect = student, remise_appliquer__is_approuved = True,remise_appliquer__is_applicated = True)        
        montant_due = DuePaiements.objects.filter(client = student, is_done=False, type='frais_f').aggregate(total=Sum('montant_restant'))['total'] or 0
        montant_paye = Paiements.objects.filter(prospect= student, context="frais_f").aggregate(total=Sum('montant_paye'))['total'] or 0
        montant_total = DuePaiements.objects.filter(client = student, type='fras_f').aggregate(total=Sum('montant_due'))['total'] or 0
        specialite = FicheVoeuxDouble.objects.filter(prospect = student, is_confirmed=True).first()

        context = {
            'pk' : pk,
            'etudiant' : student,
            'groupe' : groupe,
            'paiements' : paiements,
            'documents' : documents,
            'notes' : notes,
            'rappels' : rappels,
            'echeanciers' : echeanciers,
            'montant_due' : montant_due,
            'montant_paye' : montant_paye,
            'total_a_paye' : montant_total,
            'remises' : remises,
            'specialite_double' : specialite.specialite.label if student.is_double else None,
        }
        return render(request, 'tenant_folder/student/profile_etudiant_double.html',context)




@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdate_etudiant(request):
    
    id = request.POST.get('id_etudiant')
    etu = Prospets.objects.get(id=id)
    etu.nom = request.POST.get('nom')
    etu.prenom = request.POST.get('prenom')
    etu.date_naissance = request.POST.get('date_naissance') or None
    etu.lieu_naissance = request.POST.get('lieu_naissance')
    etu.nationnalite = request.POST.get('nationalite')
    etu.email = request.POST.get('email')
    etu.telephone = request.POST.get('telephone')
    etu.adresse = request.POST.get('adresse')
    etu.niveau_scolaire = request.POST.get('niveau_etude')
    etu.diplome = request.POST.get('dernier_diplome')
    etu.etablissement = request.POST.get('etablissement_origine')
    etu.prenom_pere = request.POST.get('nom_pere')
    etu.tel_pere = request.POST.get('tel_pere')
    etu.nom_mere = request.POST.get('nom_mere')
    etu.prenom_mere = request.POST.get('prenom_mere')
    etu.tel_mere = request.POST.get('tel_mere')
    # Tu peux aussi stocker les indicatifs :
    etu.indic1 = request.POST.get('indicatif_pere')
    etu.indic2 = request.POST.get('indicatif_mere')
    etu.save()
    print(id,request.POST.get('nationalite'))

    messages.success(request,'Information mises à jours')
    return JsonResponse({'status': 'success'})

  

@login_required
@require_http_methods(["POST"])
def generate_student_pdf(request):
    """Génère le PDF - NOM + PRENOM"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        student_id = data.get('student_id')

        template = get_object_or_404(DocumentTemplate, id=template_id, author=request.user)
        etudiant = get_object_or_404(Prospets, pk=student_id)

        print(f"\n{'='*80}")
        print(f"DÉBUT GÉNÉRATION PDF")
        print(f"{'='*80}")

        # ✅ DONNÉES
        student_data = {
            'nom': str(etudiant.nom or '') or 'Non renseigné',
            'prenom': str(etudiant.prenom or '') or 'Non renseigné',
            'nom_complet': f"{str(etudiant.nom or '')} {str(etudiant.prenom or '')}".strip() or 'Non renseigné',
        }

        print(f"\n1️⃣ DONNÉES PRÊTES: {student_data}")

        # ✅ PROCESS ALL PAGES WITH STUDENT DATA
        from t_documents_maker.services.pdf_generator import MultiPagePDFGenerator

        if template.pages:
            # Process all pages with the student data
            processed_pages = []
            for page in template.pages:
                content = page.get('content', '')
                processor = TemplateProcessor(content)
                rendered_content = processor.render(student_data)

                # Create a processed page object
                processed_page = {
                    'content': rendered_content,
                    'page_size': page.get('page_size', template.page_size),
                    'orientation': page.get('orientation', template.page_orientation)
                }
                processed_pages.append(processed_page)

            print(f"\n2️⃣ PROCESSING {len(processed_pages)} PAGES...")

            # Use MultiPagePDFGenerator for multi-page documents
            pdf_gen = MultiPagePDFGenerator(processed_pages, {
                'page_size': template.page_size,
                'page_orientation': template.page_orientation,
                'header_footer': template.get_header_footer_config()
            })
            pdf_bytes, success, error = pdf_gen.generate()
        else:
            # Fallback to single page processing if no pages exist
            print(f"\n2️⃣ PROCESSING SINGLE PAGE...")
            print(f"HTML ORIGINAL (500 chars):\n{template.get_first_page_content()[:500]}")

            # ✅ NETTOIE ET REND
            processor = TemplateProcessor(template.get_first_page_content())
            rendered_html = processor.render(student_data)

            print(f"\n3️⃣ VÉRIFICATION HTML RENDU:")
            if rendered_html and rendered_html.strip():
                print(f"   ✅ HTML NON-VIDE ({len(rendered_html)} chars)")
                print(f"   Contenu (200 chars): {rendered_html[:200]}")
            else:
                print(f"   ❌ ERREUR: HTML VIDE!")
                return JsonResponse({'error': 'HTML template vide après rendu'}, status=500)

            # ✅ GÉNÈRE PDF
            print(f"\n4️⃣ GÉNÉRATION PDF...")
            pdf_gen = PDFGenerator(rendered_html, {
                'page_size': template.page_size,
                'page_orientation': template.page_orientation
            })
            pdf_bytes, success, error = pdf_gen.generate()

        if not success:
            print(f"   ❌ ERREUR PDF: {error}")
            return JsonResponse({'error': error}, status=500)

        print(f"   ✅ PDF généré ({len(pdf_bytes)} bytes)")

        pdf_buffer = BytesIO(pdf_bytes)

        print(f"\n{'='*80}")
        print(f"✅ SUCCÈS!")
        print(f"{'='*80}\n")

        return FileResponse(
            pdf_buffer,
            as_attachment=False,
            filename=f"document_{etudiant.id}_{template_id}.pdf",
            content_type='application/pdf'
        )

    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ ERREUR: {e}")
        print(f"{'='*80}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': str(e)}, status=500)