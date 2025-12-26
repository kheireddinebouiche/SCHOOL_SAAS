# Étapes pour utiliser le modèle de documents pour imprimer des documents spécifiques par spécialité

## 1. Gestion des modèles spécifiques par spécialité

### Étape 1.1 : Création d'une structure de gestion des modèles par spécialité
- Créer des modèles dans l'éditeur de documents accessible via le menu "Éditeur PDF"
- Chaque modèle est stocké dans la table DocumentTemplate avec les champs html_content et variables
- Le champ html_content contient le code HTML du document avec les emplacements de texte
- Le champ variables contient la liste des variables à remplacer par des valeurs dynamiques

### Étape 1.2 : Création des modèles spécifiques
Pour chaque spécialité, créer les modèles nécessaires :
- Certificat de scolarité spécifique à la spécialité
- Attestation d'inscription spécifique
- Contrat de formation spécifique
- Autres documents spécifiques à la spécialité

### Étape 1.3 : Insertion des variables dynamiques dans le modèle
Lors de la création d'un modèle dans l'éditeur :
- Utiliser le bouton "Variable" pour insérer des variables dynamiques
- L'éditeur détecte automatiquement les variables dans le html_content
- Les variables sont stockées dans le champ variables du modèle
- Exemples de variables communes à tous les modèles :
  - `{{ etudiant_nom }}` - Nom de l'étudiant
  - `{{ etudiant_prenom }}` - Prénom de l'étudiant
  - `{{ etudiant_matricule }}` - Matricule de l'étudiant
  - `{{ etudiant_date_naissance }}` - Date de naissance
  - `{{ etudiant_lieu_naissance }}` - Lieu de naissance
  - `{{ etudiant_specialite }}` - Spécialité de l'étudiant
  - `{{ etudiant_niveau }}` - Niveau d'étude
  - `{{ date_document }}` - Date d'émission du document
  - `{{ responsable_ecole }}` - Responsable de l'établissement
  - `{{ adresse_ecole }}` - Adresse de l'établissement

Variables spécifiques à certaines spécialités :
- `{{ specialite_duree }}` - Durée de la formation
- `{{ specialite_diplome }}` - Diplôme obtenu
- `{{ specialite_programme }}` - Programme spécifique
- `{{ specialite_stage }}` - Informations sur les stages
- `{{ specialite_modalites }}` - Modalités spécifiques à la formation

### Étape 1.4 : Configuration des marges
- Utiliser les contrôles de marges dans l'éditeur de documents
- Marges haut: 2cm (par défaut)
- Marges bas: 2.5cm (par défaut)
- Marges gauche: 1.5cm (par défaut)
- Marges droite: 1.5cm (par défaut)

### Étape 1.5 : Sauvegarde du modèle
- Donner un nom explicite au modèle (ex: "Certificat de scolarité - Informatique")
- Cliquer sur le bouton "Sauvegarder" dans l'éditeur
- Le modèle est enregistré avec son html_content et ses variables détectées
- Le modèle est maintenant disponible pour utilisation

## 2. Association des modèles aux formations

### Étape 2.1 : Configuration des documents pour une formation
- Accéder à la page de détails de la formation
- Cliquer sur le bouton "Documents d'impression"
- Dans la modal qui s'ouvre, cocher les documents à associer à la formation
- Cliquer sur "Imprimer les documents" pour enregistrer les associations

### Étape 2.2 : Affichage des modèles selon les documents affectés à la formation
Modifier le template `profile_etudiant.html` pour afficher les documents en fonction des associations avec la formation de l'étudiant :

```html
<!-- Dans le menu déroulant impression -->
{% if type_formation == "etrangere" %}
    <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'admission' %}" target="_blank">
        <i class="ri-file-line me-2"></i>Certificat d'admission
    </a></li>
    <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'contrat' %}" target="_blank">
        <i class="ri-file-text-line me-2"></i>Contrat de formation
    </a></li>
{% else %}
    <!-- Documents spécifiques à la formation de l'étudiant -->
    {% for template in formation_documents %}
        <li>
            <a class="dropdown-item" href="{% url 'generate_certificate_by_template' etudiant.id template.id %}" target="_blank">
                <i class="ri-file-line me-2"></i>{{ template.name }}
            </a>
        </li>
    {% endfor %}

    <!-- Documents génériques -->
    <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'inscription' %}" target="_blank">
        <i class="ri-file-line me-2"></i>Attestation d'inscription
    </a></li>
    <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'etudiant' %}" target="_blank">
        <i class="ri-id-card-line me-2"></i>Carte étudiant
    </a></li>
{% endif %}
```

### Étape 2.3 : Mise à jour du contexte de la vue
Modifier la vue qui gère le profil de l'étudiant pour inclure les modèles associés à la formation de l'étudiant :

```python
def profile_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)

    # Récupérer la formation de l'étudiant
    formation = etudiant.specialite.formation if etudiant.specialite else None

    # Récupérer les modèles associés à la formation
    formation_documents = []
    if formation:
        # Supposons que vous avez un champ JSON ou une relation pour stocker les documents sélectionnés
        # selon la logique implémentée dans la section "Documents d'impression" des formations
        selected_document_names = formation.selected_documents if hasattr(formation, 'selected_documents') else []

        # Récupérer les modèles correspondants
        formation_documents = DocumentTemplate.objects.filter(
            name__in=selected_document_names,
            author=request.user
        )

    context = {
        'etudiant': etudiant,
        'formation_documents': formation_documents,
        # ... autres variables
    }
    return render(request, 'tenant_folder/student/profile_etudiant.html', context)
```

## 3. Création des vues nécessaires pour la gestion spécifique

### Étape 3.1 : Vue pour générer un document spécifique à la spécialité
Créer une vue dans `views.py` pour gérer la génération de documents en fonction de la spécialité :

```python
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import DocumentTemplate, GeneratedDocument, Etudiant
from .services.pdf_generator import PDFGenerator
from .services.template_processor import TemplateProcessor
from django.core.files.base import ContentFile
from django.utils import timezone
import json

def generate_certificate_by_specialty(request, etudiant_id, document_type):
    if request.method == 'GET':
        try:
            # Récupérer les données de l'étudiant
            etudiant = get_object_or_404(Etudiant, id=etudiant_id)

            # Déterminer le modèle approprié en fonction de la spécialité et du type de document
            template_name = f"{document_type.title()} - {etudiant.specialite.label if etudiant.specialite else 'Générique'}"

            # Essayer de trouver un modèle spécifique à la spécialité
            try:
                template = DocumentTemplate.objects.get(
                    name=template_name,
                    author=request.user
                )
            except DocumentTemplate.DoesNotExist:
                # Si pas de modèle spécifique, utiliser un modèle générique
                template = DocumentTemplate.objects.get(
                    name=f"{document_type.title()} - Générique",
                    author=request.user
                )

            # Préparer les données pour le template
            data = prepare_certificate_data(etudiant, document_type)

            # Traiter le template avec les données
            processor = TemplateProcessor(template.html_content)
            rendered_html = processor.render(data)

            # Générer le PDF
            pdf_gen = PDFGenerator(rendered_html, {
                'page_size': template.page_size,
                'page_orientation': template.page_orientation
            })
            pdf_bytes, success, error = pdf_gen.generate()

            if success:
                # Sauvegarder le document généré
                generated_doc = GeneratedDocument.objects.create(
                    template=template,
                    data=data,
                    pdf_file=ContentFile(pdf_bytes, name=f'{document_type}_{etudiant.matricule_interne}.pdf'),
                    author=request.user
                )

                # Retourner le PDF
                response = HttpResponse(pdf_bytes, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{document_type}_{etudiant.nom}_{etudiant.prenom}.pdf"'
                return response
            else:
                return JsonResponse({'error': error}, status=500)

        except DocumentTemplate.DoesNotExist:
            return JsonResponse({'error': f'Modèle de {document_type} non trouvé'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def generate_certificate_by_template(request, etudiant_id, template_id):
    if request.method == 'GET':
        try:
            # Récupérer les données de l'étudiant
            etudiant = get_object_or_404(Etudiant, id=etudiant_id)
            template = get_object_or_404(DocumentTemplate, id=template_id, author=request.user)

            # Préparer les données pour le template
            data = prepare_certificate_data(etudiant, template.name)

            # Traiter le template avec les données
            processor = TemplateProcessor(template.html_content)
            rendered_html = processor.render(data)

            # Générer le PDF
            pdf_gen = PDFGenerator(rendered_html, {
                'page_size': template.page_size,
                'page_orientation': template.page_orientation
            })
            pdf_bytes, success, error = pdf_gen.generate()

            if success:
                # Sauvegarder le document généré
                generated_doc = GeneratedDocument.objects.create(
                    template=template,
                    data=data,
                    pdf_file=ContentFile(pdf_bytes, name=f'{template.name}_{etudiant.matricule_interne}.pdf'),
                    author=request.user
                )

                # Retourner le PDF
                response = HttpResponse(pdf_bytes, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{template.name}_{etudiant.nom}_{etudiant.prenom}.pdf"'
                return response
            else:
                return JsonResponse({'error': error}, status=500)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

def prepare_certificate_data(etudiant, document_type):
    """Préparer les données pour le template en fonction de l'étudiant et du type de document"""
    data = {
        'etudiant_nom': etudiant.nom,
        'etudiant_prenom': etudiant.prenom,
        'etudiant_matricule': etudiant.matricule_interne,
        'etudiant_date_naissance': etudiant.date_naissance.strftime('%d/%m/%Y') if etudiant.date_naissance else '',
        'etudiant_lieu_naissance': etudiant.lieu_naissance,
        'etudiant_specialite': etudiant.specialite.label if etudiant.specialite else '',
        'etudiant_niveau': etudiant.get_niveau_scolaire_display(),
        'date_document': timezone.now().strftime('%d/%m/%Y'),
        'responsable_ecole': 'Directeur de l\'établissement',  # à adapter
        'adresse_ecole': 'Adresse de l\'établissement',  # à adapter
    }

    # Ajouter des données spécifiques selon la spécialité
    if etudiant.specialite:
        # Données spécifiques à la spécialité (à adapter selon votre modèle de données)
        data['specialite_duree'] = getattr(etudiant.specialite, 'duree_formation', 'Non spécifiée')
        data['specialite_diplome'] = getattr(etudiant.specialite, 'diplome_obtenu', 'Non spécifié')
        data['specialite_programme'] = getattr(etudiant.specialite, 'programme', 'Non spécifié')
        data['specialite_modalites'] = getattr(etudiant.specialite, 'modalites', 'Non spécifié')

    return data

### Étape 3.2 : Ajouter les URLs
Ajouter les URLs dans `urls.py` :

```python
from django.urls import path
from . import views

urlpatterns = [
    # ... autres URLs
    path('generate-certificate/<int:etudiant_id>/<str:document_type>/',
         views.generate_certificate_by_specialty,
         name='generate_certificate_by_specialty'),
    path('generate-certificate-template/<int:etudiant_id>/<int:template_id>/',
         views.generate_certificate_by_template,
         name='generate_certificate_by_template'),
]
```

## 4. Amélioration de l'interface utilisateur

### Étape 4.1 : Affichage conditionnel des documents
Dans le template `profile_etudiant.html`, afficher uniquement les documents disponibles pour la formation de l'étudiant :

```html
<!-- Action Buttons -->
<div class="d-flex gap-2">
    <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#editStudentModal">
        <i class="ri-edit-line me-1"></i> Modifier
    </button>
    <div class="dropdown">
        <button class="btn btn-info dropdown-toggle" type="button" id="impressionDropdown" data-bs-toggle="dropdown" aria-expanded="false">
            <i class="ri-printer-line me-1"></i> Impression
        </button>
        <ul class="dropdown-menu" aria-labelledby="impressionDropdown">
            {% if type_formation == "etrangere" %}
                <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'admission' %}" target="_blank">
                    <i class="ri-file-line me-2"></i>Certificat d'admission
                </a></li>
                <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'contrat' %}" target="_blank">
                    <i class="ri-file-text-line me-2"></i>Contrat de formation
                </a></li>
            {% else %}
                <!-- Documents spécifiques à la formation de l'étudiant -->
                {% for template in formation_documents %}
                    <li>
                        <a class="dropdown-item" href="{% url 'generate_certificate_by_template' etudiant.id template.id %}" target="_blank">
                            <i class="ri-file-line me-2"></i>{{ template.name }}
                        </a>
                    </li>
                {% endfor %}

                <!-- Documents génériques -->
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'scolarite' %}" target="_blank">
                    <i class="ri-file-line me-2"></i>Certificat de scolarité
                </a></li>
                <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'inscription' %}" target="_blank">
                    <i class="ri-file-line me-2"></i>Attestation d'inscription
                </a></li>
            {% endif %}

            <li><a class="dropdown-item" href="{% url 'generate_certificate_by_specialty' etudiant.id 'etudiant' %}" target="_blank">
                <i class="ri-id-card-line me-2"></i>Carte étudiant
            </a></li>
        </ul>
    </div>
</div>
```

## 5. Tests et validation

### Étape 5.1 : Tester la génération
- Créer des modèles de documents dans l'éditeur de documents
- Associer ces modèles aux formations via la fonctionnalité "Documents d'impression"
- Accéder à la page de profil d'un étudiant inscrit à une formation
- Vérifier que seuls les documents associés à la formation sont affichés
- Cliquer sur les documents disponibles et vérifier que le PDF est généré correctement

### Étape 5.2 : Vérification des données
- S'assurer que les variables spécifiques à la spécialité sont correctement remplies
- Vérifier le formatage du PDF
- Valider que les marges sont correctement appliquées
- Confirmer que le document est sauvegardé dans la base de données

## 6. Personnalisation avancée (optionnel)

### Étape 6.1 : Gestion des droits d'accès
- Créer des permissions pour limiter l'accès à certains types de documents
- Gérer les droits selon le rôle de l'utilisateur (administrateur, enseignant, etc.)

### Étape 6.2 : Système de catégorisation des modèles
- Ajouter un modèle de catégorie pour organiser les modèles
- Permettre la recherche de modèles par spécialité, type de document ou période

### Étape 6.3 : Génération automatique de documents
- Créer des workflows pour générer automatiquement certains documents
- Planifier la génération de documents à des dates spécifiques

## Conclusion

Avec cette approche, les modèles de documents apparaissent selon la liste des documents affectés à la formation de l'étudiant. Le système permet une gestion centralisée des documents par formation, ce qui assure une cohérence dans les documents disponibles pour chaque spécialité. Cela permet une gestion plus efficace et personnalisée des documents pour chaque formation.