from ..models import *
from ..forms import *
from django.contrib import messages
from django.db import transaction
from t_crm.models import *
from t_tresorerie.models import *
from django.db.models import Count, Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from io import BytesIO
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views import View  
from django.template import Template, Context
from django.urls import reverse


@login_required(login_url="institut_app:login")
def StudentDetails(request, pk):
    
    student = Prospets.objects.get(id = pk)

    if not student.is_double:
        groupe = GroupeLine.objects.filter(student=student)
        
        # Determine current group (default to 'inscription', otherwise the most recent one)
        current_groupe = GroupeLine.objects.filter(student=student, groupe__etat="inscription").first()
        if not current_groupe:
            current_groupe = GroupeLine.objects.filter(student=student).first()
            
        # Basic student info (Generic)
        paiements = []
        documents = DocumentsDemandeInscription.objects.filter(prospect=student)
        notes = NotesProcpects.objects.filter(prospect=student, context="etudiant")
        rappels = RendezVous.objects.filter(prospect=student, context="etudiant")
        echeanciers = []
        remises = []
        montant_due = 0
        montant_paye = 0
        montant_total = 0
        rachat_due_paiement = []
        autre_paiements = []
        
        # Payment logic (Skip for Conseil participants: student.context == "con")
        if student.context != "con":
            paiements = Paiements.objects.filter(prospect=student)
            echeanciers = DuePaiements.objects.filter(client=student, type='frais_f').order_by('ordre')
            remises = RemiseAppliquerLine.objects.filter(prospect=student, remise_appliquer__is_approuved=True, remise_appliquer__is_applicated=True)
            
            montant_due = DuePaiements.objects.filter(client=student, is_done=False, type='frais_f').aggregate(total=Sum('montant_restant'))['total'] or 0
            montant_paye = Paiements.objects.filter(prospect=student, context="frais_f").aggregate(total=Sum('montant_paye'))['total'] or 0
            montant_total = DuePaiements.objects.filter(client=student, type='frais_f').aggregate(total=Sum('montant_due'))['total'] or 0
            
            rachat_due_paiement = DuePaiements.objects.filter(client=student, type='rach')
            # Fix: Model AutreProduit does not have 'compte' field
            autre_paiements = AutreProduit.objects.filter(client=student).select_related('payment_type')

        # Handle Specialite and Formation (FicheDeVoeux is only for standard students)
        specialite_simple = FicheDeVoeux.objects.filter(prospect=student, is_confirmed=True).first()
        
        if specialite_simple:
            formation = specialite_simple.specialite.formation
            specialite_label = specialite_simple.specialite.label
            qualification = formation.qualification
            annee_academique = specialite_simple.promo.annee_academique
            branche = specialite_simple.specialite.branche
            montant_formation = formation.prix_formation
        elif current_groupe:
            formation = current_groupe.groupe.specialite.formation
            specialite_label = current_groupe.groupe.specialite.label
            qualification = formation.qualification if formation else "N/A"
            annee_academique = current_groupe.groupe.promotion.annee_academique if current_groupe.groupe.promotion else "N/A"
            branche = current_groupe.groupe.specialite.branche
            montant_formation = formation.prix_formation if formation else 0
        else:
            formation = None
            specialite_label = "N/A"
            qualification = "N/A"
            annee_academique = "N/A"
            branche = None
            montant_formation = 0

        # Legal entity and Echeancier
        try:
            entreprise_details = Entreprise.objects.get(id=formation.entite_legal.id) if formation and formation.entite_legal else None
        except:
            entreprise_details = None
            
        echancier_standard = EcheancierPaiement.objects.filter(formation=formation, is_active=True, is_default=True, is_approuved=True).first()
        if echancier_standard:
            echeancier_line = EcheancierPaiementLine.objects.filter(echeancier=echancier_standard).values('id', 'value', 'montant_tranche', 'date_echeancier')
            frais_inscription = echancier_standard.frais_inscription
        else:
            echeancier_line = []
            frais_inscription = 0
            
        documents_available = formation.documents.all() if formation else []
        
        # Historique Absence
        from t_etudiants.models import HistoriqueAbsence
        historique_absence = HistoriqueAbsence.objects.filter(etudiant=student).select_related('ligne_presence__module')
        
        attendance_summary = {}
        for record in historique_absence:
            if record.historique:
                for entry in record.historique:
                    for d in entry.get('data', []):
                        code = d.get('code')
                        etat = d.get('etat')
                        module_label = record.ligne_presence.module.label if record.ligne_presence and record.ligne_presence.module else d.get('module')
                        if code:
                            if code not in attendance_summary:
                                attendance_summary[code] = {'label': module_label, 'code': code, 'P': 0, 'A': 0, 'J': 0, 'details': []}
                            if etat in ['P', 'A', 'J']:
                                attendance_summary[code][etat] += 1
                            attendance_summary[code]['details'].append({'date': entry.get('date'), 'etat': etat})

        try:
            echeancier_special = EcheancierSpecial.objects.filter(prospect=student).first()
            echeancier_special_line = EcheancierPaiementLine.objects.filter(echeancier_id=echeancier_special.id).values('id','value','montant_tranche','date_echeancier') if echeancier_special else []
        except:
            echeancier_special = None
            echeancier_special_line = []

        dossier_inscription = DossierInscription.objects.filter(formation=formation).values('label') if formation else []
        
        try:
            logo_partenaire = Partenaires.objects.get(id=current_groupe.groupe.specialite.formation.partenaire.id) if current_groupe and current_groupe.groupe.specialite.formation.partenaire else None
        except:
            logo_partenaire = None

        context = {
            'pk': pk,
            'etudiant': student,
            'groupe': groupe,
            'paiements': paiements,
            'documents': documents,
            'notes': notes,
            'rappels': rappels,
            'echeanciers': echeanciers,
            'montant_due': montant_due,
            'montant_paye': montant_paye,
            'total_a_paye': montant_total,
            'remises': remises,
            'specialite_simple': specialite_label,
            'formation': formation.nom if formation else "N/A",
            'qualification': qualification,
            'entreprise_details': entreprise_details,
            'echeancier_standart': echancier_standard,
            'echeancier_line': json.dumps(list(echeancier_line), cls=DjangoJSONEncoder),
            'echeancier_special_line': json.dumps(list(echeancier_special_line)),
            'dossier_inscription': json.dumps(list(dossier_inscription), cls=DjangoJSONEncoder),
            'montant_formation': montant_formation,
            'frais_incription': frais_inscription,
            'annee_academique': annee_academique,
            'branche': branche,
            'date_debut': current_groupe.groupe.start_date if current_groupe else None,
            'date_fin': current_groupe.groupe.end_date if current_groupe else None,
            'type_formation': formation.type_formation if formation else "N/A",
            'logo_partenaire': logo_partenaire.logo.url if logo_partenaire and logo_partenaire.logo else "",
            'documents_available': documents_available,
            'rachat_due_paiement': rachat_due_paiement,
            'autre_paiements': autre_paiements,
            'historique_absence': attendance_summary.values(),
        }
        return render(request, 'tenant_folder/student/profile_etudiant.html', context)


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
        montant_total = DuePaiements.objects.filter(client = student, type='frais_f').aggregate(total=Sum('montant_due'))['total'] or 0
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

    messages.success(request,'Informations mises à jour')
    return JsonResponse({'status': 'success'})


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdateStudentPhoto(request):
    """Mise à jour de la photo de l'étudiant via AJAX"""
    if request.method == 'POST':
        student_id = request.POST.get('id_etudiant')
        photo = request.FILES.get('photo')
        
        if not student_id or not photo:
            return JsonResponse({'status': 'error', 'message': 'Données manquantes'})
            
        try:
            student = Prospets.objects.get(id=student_id)
            student.photo = photo
            student.save()
            return JsonResponse({'status': 'success'})
        except Prospets.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Étudiant introuvable'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'})


class generate_student_pdf(LoginRequiredMixin, View):
    """Génère et imprime la fiche d'un étudiant en utilisant un template"""

    def get(self, request, pk, template_slug=None):
        # Récupération de l'étudiant et de sa fiche
        # Sélection du template
        if template_slug:
            template_obj = get_object_or_404(DocumentTemplate, slug=template_slug, is_active=True)
        else:
            template_obj = DocumentTemplate.objects.filter(is_active=True).first()
            if not template_obj:
                from django.contrib import messages
                messages.error(request, "Aucun template de fiche étudiant disponible.")
                return redirect('school:student-detail', pk=pk)

        # Préparer les données de contexte
        from ..utils import get_student_context
        context_data = get_student_context(pk)

        # Rendu du template
        try:
            # ✅ MODIFICATION 1 : Convertir les commentaires <!-- pagebreak --> en divs
            raw_content = template_obj.content
            import re

            # Remplace <!-- pagebreak --> par <div class="pagebreak"></div>
            # Accepte les variantes : espaces, casse différente
            raw_content = re.sub(
                r'<!--\s*pagebreak\s*-->',
                '<div class="pagebreak"></div>',
                raw_content,
                flags=re.IGNORECASE
            )

            django_template = Template(raw_content)
            rendered_content = django_template.render(Context(context_data))

            # Enregistrer la génération
            doc_gen = DocumentGeneration.objects.create(
                template=template_obj,
                context_data=context_data,  # JSON serializable maintenant
                rendered_content=rendered_content,
                generated_by=request.user
            )

            # Check for AJAX/Modal request
            if request.GET.get('modal') == 'true':
                return JsonResponse({
                    'status': 'success',
                    'preview_html': rendered_content,
                    'custom_css': template_obj.custom_css,
                    'download_url': reverse('pdf_editor:document-export', args=[doc_gen.pk])
                })

            return redirect('pdf_editor:document-preview', pk=doc_gen.pk)

        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Erreur lors du rendu: {str(e)}")
            return redirect('pdf_editor:document-preview', pk=pk)
