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
from django.template import Template, Context


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


class generate_student_pdf(LoginRequiredMixin, View):
    """Génère et imprime la fiche d'un étudiant en utilisant un template"""

    def get(self, request, pk, template_slug=None):
        # Récupération de l'étudiant et de sa fiche
        student = get_object_or_404(Prospets, pk=pk)
        fiche = get_object_or_404(FicheDeVoeux, prospect=student)
        logo = fiche.specialite.formation.entite_legal.entete_logo.url if fiche.specialite.formation.entite_legal.entete_logo else ''

        specialite = fiche.specialite.label
        formation = fiche.specialite.label
        annee_academique = fiche.promo.annee_academique

        # Récupération de l'échéancier et conversion des Decimals en float
        echeancier_qs = DuePaiements.objects.filter(client=student).order_by('date_echeance')
    
        echeancier = []

        for e in echeancier_qs:
            label = e.label

            if label == "Frais d'inscription":
                label = f"{label} (Non Remboursable)"

            echeancier.append({
                'label': label,
                'montant_due': float(e.montant_due) if e.montant_due is not None else 0.0,
                'date_echeance': e.date_echeance.isoformat() if e.date_echeance else ''
            })

        formation = FicheDeVoeux.objects.get(prospect = student)
        documents_qs = DossierInscription.objects.filter(formation  = formation.id)
        documents = []
        for i in documents_qs:
            documents.append({
                'label' : i.label
            })

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
        context_data = {
            
            'current_date': timezone.now().date().isoformat(),
            'pk': student.pk,
            'nom': student.nom,
            'prenom': student.prenom,
            'date_naissance': student.date_naissance.isoformat() if student.date_naissance else None,
            'lieu_naissance': student.lieu_naissance,
            'email': student.email or '',
            'telephone': student.telephone or '',
            'adresse': student.adresse or '',
            'logo': logo,
            'specialite': specialite,
            'annee_academique': annee_academique,
            'echeancier': echeancier,
            'documents' : documents,
        }

        # Rendu du template
        try:
            django_template = Template(template_obj.content)
            rendered_content = django_template.render(Context(context_data))

            # Enregistrer la génération
            doc_gen = DocumentGeneration.objects.create(
                template=template_obj,
                context_data=context_data,  # JSON serializable maintenant
                rendered_content=rendered_content,
                generated_by=request.user
            )

            return redirect('pdf_editor:document-preview', pk=doc_gen.pk)

        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Erreur lors du rendu: {str(e)}")
            return redirect('pdf_editor:document-preview', pk=pk)
