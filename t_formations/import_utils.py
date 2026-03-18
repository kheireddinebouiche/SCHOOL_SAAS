import json
from django.core.exceptions import ValidationError
import openpyxl
from .models import Partenaires, Formation, Specialites, Modules, Formateurs, ProgrammeFormation
from django.db.models import Q

def parse_dispo_string(dispo_str):
    if not dispo_str:
        return {'disponibilites': []}
    
    # Check if it's already JSON
    if isinstance(dispo_str, str) and dispo_str.strip().startswith('{'):
        try:
            data = json.loads(dispo_str)
            if isinstance(data, dict) and 'disponibilites' in data:
                return data
        except:
            pass

    disponibilites = []
    # Format: Jour:HH:mm-HH:mm, Jour2:HH:mm-HH:mm
    parts = [p.strip() for p in str(dispo_str).split(',') if p.strip()]
    for part in parts:
        if ':' in part and '-' in part:
            try:
                # Part might be "Lundi:08:00-12:00"
                first_colon = part.find(':')
                jour = part[:first_colon].strip().lower()
                times = part[first_colon+1:].strip()
                if '-' in times:
                    heure_debut, heure_fin = times.split('-', 1)
                    disponibilites.append({
                        'jour': jour,
                        'heure_debut': heure_debut.strip(),
                        'heure_fin': heure_fin.strip()
                    })
            except:
                continue
    return {'disponibilites': disponibilites}


def handle_uploaded_file(file):
    """
    Parses the uploaded file (Excel or JSON) and returns a list of dictionaries.
    """
    data = []
    filename = file.name.lower()

    try:
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active
            headers = [cell.value for cell in sheet[1]]
            
            for row in sheet.iter_rows(min_row=2, values_only=True):
                # Skip empty rows
                if not any(row):
                    continue
                row_data = dict(zip(headers, row))
                data.append(row_data)

        elif filename.endswith('.json'):
            content = file.read().decode('utf-8')
            data = json.loads(content)
            if not isinstance(data, list):
                raise ValidationError("Le fichier JSON doit contenir une liste d'objets.")
        else:
             raise ValidationError("Format de fichier non supporté. Veuillez utiliser .xlsx, .xls ou .json")
    
    except Exception as e:
        raise ValidationError(f"Erreur lors de la lecture du fichier : {str(e)}")

    return data

def verify_data(data, data_type):
    """
    Verifies the data against the database constraints and logic.
    Returns a report with valid rows and errors.
    """
    report = {
        'valid_rows': [],
        'errors': [],
        'summary': {'new': 0, 'update': 0}
    }

    if not data:
        return report

    for index, row in enumerate(data):
        row_num = index + 2  # Assuming 1-based index + header for Excel
        error_msg = []
        is_update = False
        
        # Normalize keys to lowercase for consistency if needed, but assuming strict headers for now
        # You might want to strip whitespace from keys and values
    
        try:
            if data_type == 'Partenaires':
                code = row.get('Code') or row.get('code')
                nom = row.get('Nom') or row.get('nom')
                if not code:
                    error_msg.append("Code manquant")
                else:
                    if Partenaires.objects.filter(code=code).exists():
                         is_update = True
                
                # Handling type_partenaire choice field mapping
                raw_type = row.get('type_partenaire')
                if raw_type is not None:
                    valid_keys = [k for k, v in Partenaires._meta.get_field('type_partenaire').choices]
                    valid_labels = {v.lower().strip(): k for k, v in Partenaires._meta.get_field('type_partenaire').choices}
                    clean_raw = str(raw_type).lower().strip()
                    if str(raw_type) in valid_keys:
                        pass # Already a valid key
                    elif clean_raw in valid_labels:
                        row['type_partenaire'] = valid_labels[clean_raw]
                    else:
                        error_msg.append(f"Type de partenaire invalide: '{raw_type}'")
                
                # Basic validation
                if not nom: error_msg.append("Nom manquant")

            elif data_type == 'Formation':
                # New hierarchical headers:
                # Code Formation, Nom Formation, Description Formation, Durée Formation, Partenaire, Type de formation, Frais Inscription, Prix Formation
                # Code Spécialité, Label Spécialité, Durée Spécialité, Branche, Prix Spécialité
                # Code Module, Code Interne Module, Label Module, Durée Module, Coefficient
                
                # Check for alternative headers (backward compatibility or new export format)
                code_form = row.get('Code Formation') or row.get('code')
                nom_form = row.get('Nom Formation') or row.get('nom')
                duree_form = row.get('Durée Formation') or row.get('duree')
                partenaire_code = row.get('Partenaire') or row.get('partenaire_code')
                type_form = row.get('Type de formation') or row.get('type_formation')
                
                # Specialite and Module fields
                code_spec = row.get('Code Spécialité') or row.get('specialite_code')
                label_spec = row.get('Label Spécialité') or row.get('specialite_label')
                abr_spec = row.get('Abréviation Spécialité') or row.get('specialite_abr')
                
                qualification_form = row.get('Qualification Formation') or row.get('qualification')
                
                version_spec = row.get('Version Spécialité') or row.get('specialite_version')
                semestres_spec = row.get('Semestres Spécialité') or row.get('specialite_nb_semestre')
                tranches_spec = row.get('Tranches Spécialité') or row.get('specialite_nb_tranche')
                prix_double_spec = row.get('Prix Double Diplomation') or row.get('specialite_prix_double')
                conditions_spec = row.get("Conditions d'accès") or row.get('specialite_conditions')

                code_mod = row.get('Code Module') or row.get('module_code')
                label_mod = row.get('Label Module') or row.get('module_label')
                semestre_mod = row.get('Semestre Module') or row.get('module_semestre')
                
                if not code_form: 
                    error_msg.append("Code Formation manquant")
                else:
                    if Formation.objects.filter(code=code_form).exists():
                        is_update = True
                
                if not nom_form: error_msg.append("Nom Formation manquant")
                if not duree_form: error_msg.append("Durée Formation manquante")
                
                # Handling type_formation choice field mapping
                raw_type = type_form
                if raw_type is not None and str(raw_type).strip() != '':
                    valid_keys = [k for k, v in Formation._meta.get_field('type_formation').choices]
                    valid_labels = {v.lower().strip(): k for k, v in Formation._meta.get_field('type_formation').choices}
                    clean_raw = str(raw_type).lower().strip()
                    if str(raw_type) in valid_keys:
                        row['Type de formation'] = str(raw_type) # Keep valid key
                    elif clean_raw in valid_labels:
                        row['Type de formation'] = valid_labels[clean_raw]
                    else:
                        error_msg.append(f"Type de formation invalide: '{raw_type}'")
                
                if partenaire_code:
                     if not Partenaires.objects.filter(code=partenaire_code).exists():
                         error_msg.append(f"Le Partenaire avec le code '{partenaire_code}' n'existe pas en base de données. Veuillez d'abord l'importer dans la section Partenaires.")
                
                # If a Specialite is provided on this row, check mandatory fields
                if code_spec:
                    if not label_spec:
                        error_msg.append(f"Label Spécialité manquant pour la spécialité '{code_spec}'")
                
                # If a Module is provided on this row, it requires a Specialite, and mandatory fields
                if code_mod:
                    if not code_spec:
                        error_msg.append(f"Un Module ('{code_mod}') ne peut pas être importé sans une Spécialité parente sur la même ligne")
                    if not label_mod:
                        error_msg.append(f"Label Module manquant pour le module '{code_mod}'")

            elif data_type == 'Specialites':
                code = row.get('code')
                formation_code = row.get('formation_code')

                if not code: error_msg.append("Code manquant")
                else:
                    if Specialites.objects.filter(code=code).exists():
                        is_update = True
                
                if not row.get('label'): error_msg.append("Label manquant")
                
                if formation_code:
                    if not Formation.objects.filter(code=formation_code).exists():
                        error_msg.append(f"Formation avec code '{formation_code}' introuvable")
                else:
                    error_msg.append("Code formation manquant")

            elif data_type == 'Modules':
                code = row.get('code')
                specialite_code = row.get('specialite_code')

                if not code: error_msg.append("Code manquant")
                else:
                    if Modules.objects.filter(code=code).exists():
                         is_update = True
                
                if not row.get('label'): error_msg.append("Label manquant")
                
                if specialite_code:
                    if not Specialites.objects.filter(code=specialite_code).exists():
                         error_msg.append(f"Spécialité avec code '{specialite_code}' introuvable")
                else:
                     error_msg.append("Code spécialité manquant")

            elif data_type == 'Formateurs':
                # Formateurs don't essentially have a strict 'code', usually email or nom/prenom key
                # Assuming unique identifier is email or creating new if not found
                email = row.get('Email') or row.get('email')
                nom = row.get('Nom') or row.get('nom')
                prenom = row.get('Prénom') or row.get('prenom')
                nin = row.get('NIN') or row.get('nin')
                
                if not email:
                     error_msg.append("Email manquant")
                else:
                    if Formateurs.objects.filter(email=email).exists():
                        is_update = True
                
                if not nom: error_msg.append("Nom manquant")
                if not prenom: error_msg.append("Prénom manquant")

                # Availability check (optional but validate format if present)
                dispo_val = row.get('Disponibilité') or row.get('disponibilite') or row.get('dispo')
                if dispo_val:
                    parsed = parse_dispo_string(dispo_val)
                    if not parsed['disponibilites'] and str(dispo_val).strip() != '':
                         # If there was something but we couldn't parse any entry
                         pass # Could add warning, but let's be lenient for now

            
        except Exception as e:
            error_msg.append(f"Erreur inattendue: {str(e)}")

        if error_msg:
            report['errors'].append({'row': row_num, 'data': row, 'errors': ", ".join(error_msg)})
        else:
            row['is_update'] = is_update # Internal flag
            report['valid_rows'].append(row)
            if is_update:
                report['summary']['update'] += 1
            else:
                report['summary']['new'] += 1

    return report

def import_data(data, data_type, user=None):
    """
    Saves the data to the database.
    """
    success_count = 0
    
    for row in data:
        try:
            if data_type == 'Partenaires':
                code = row.get('Code') or row.get('code')
                nom = row.get('Nom') or row.get('nom')
                adresse = row.get('Adresse') or row.get('adresse')
                telephone = row.get('Téléphone') or row.get('telephone')
                email = row.get('Email') or row.get('email')
                site_web = row.get('Site Web') or row.get('site_web')
                type_p = row.get('Type de partenaire') or row.get('type_partenaire')

                Partenaires.objects.update_or_create(
                    code=code,
                    defaults={
                        'nom': nom,
                        'adresse': adresse,
                        'telephone': telephone,
                        'email': email,
                        'site_web': site_web,
                        'type_partenaire': type_p,
                        'created_by': user
                    }
                )
            
            elif data_type == 'Formation':
                code_form = row.get('Code Formation') or row.get('code')
                nom_form = row.get('Nom Formation') or row.get('nom')
                desc_form = row.get('Description Formation') or row.get('description')
                duree_form = row.get('Durée Formation') or row.get('duree', 0)
                type_form = row.get('Type de formation') or row.get('type_formation', 'national')
                frais_form = row.get('Frais Inscription') or row.get('frais_inscription')
                prix_form = row.get('Prix Formation') or row.get('prix_formation')
                partenaire_code = row.get('Partenaire') or row.get('partenaire_code')
                qualification_form = row.get('Qualification Formation') or row.get('qualification')
                
                # Specialite and Module fields
                code_spec = row.get('Code Spécialité') or row.get('specialite_code')
                label_spec = row.get('Label Spécialité') or row.get('specialite_label')
                duree_spec = row.get('Durée Spécialité') or row.get('specialite_duree')
                branche_spec = row.get('Branche') or row.get('specialite_branche')
                prix_spec = row.get('Prix Spécialité') or row.get('specialite_prix')
                
                code_mod = row.get('Code Module') or row.get('module_code')
                int_mod = row.get('Code Interne Module') or row.get('module_code_interne')
                label_mod = row.get('Label Module') or row.get('module_label')
                duree_mod = row.get('Durée Module') or row.get('module_duree')
                coef_mod = row.get('Coefficient') or row.get('module_coef')
                semestre_mod = row.get('Semestre Module') or row.get('module_semestre')

                version_spec = row.get('Version Spécialité') or row.get('specialite_version')
                semestres_spec = row.get('Semestres Spécialité') or row.get('specialite_nb_semestre')
                tranches_spec = row.get('Tranches Spécialité') or row.get('specialite_nb_tranche')
                prix_double_spec = row.get('Prix Double Diplomation') or row.get('specialite_prix_double')
                abr_spec = row.get('Abréviation Spécialité') or row.get('specialite_abr')
                conditions_spec = row.get("Conditions d'accès") or row.get('specialite_conditions')
                
                partenaire = None
                if partenaire_code:
                    partenaire = Partenaires.objects.filter(code=partenaire_code).first()
                
                formation, _ = Formation.objects.update_or_create(
                    code=code_form,
                    defaults={
                        'nom': nom_form,
                        'description': desc_form,
                        'duree': duree_form,
                        'type_formation': type_form,
                        'frais_inscription': frais_form,
                        'prix_formation': prix_form,
                        'partenaire': partenaire,
                        'qualification': qualification_form,
                        'created_by': user
                    }
                )
                
                # Create or Update Specialite if provided
                if code_spec:
                    specialite, _ = Specialites.objects.update_or_create(
                         code=code_spec,
                         defaults={
                             'label': label_spec,
                             'duree': duree_spec,
                             'branche': branche_spec,
                             'prix': prix_spec,
                             'version': version_spec,
                             'nb_semestre': semestres_spec,
                             'nb_tranche': tranches_spec,
                             'prix_double_diplomation': prix_double_spec,
                             'abr': abr_spec,
                             'condition_access': conditions_spec,
                             'formation': formation,
                             'updated_by': user
                         }
                    )
                    
                    # Create or Update Module if provided
                    if code_mod:
                        module, _ = Modules.objects.update_or_create(
                            code=code_mod,
                            defaults={
                                'code_interne': int_mod,
                                'label': label_mod,
                                'duree': duree_mod,
                                'coef': coef_mod,
                                'specialite': specialite,
                                'created_by': user
                            }
                        )
                        if semestre_mod:
                            ProgrammeFormation.objects.update_or_create(
                                module=module,
                                specialite=specialite,
                                defaults={
                                    'semestre': str(semestre_mod).strip(),
                                    'created_by': user
                                }
                            )

            elif data_type == 'Specialites':
                formation = Formation.objects.filter(code=row['formation_code']).first()
                if formation:
                    Specialites.objects.update_or_create(
                        code=row['code'],
                        defaults={
                            'label': row.get('label'),
                            'prix': row.get('prix'),
                            'prix_double_diplomation': row.get('prix_double_diplomation') or row.get('prix_double'),
                            'duree': row.get('duree'),
                            'nb_semestre': row.get('nb_semestre') or row.get('semestres'),
                            'nb_tranche': row.get('nb_tranche') or row.get('tranches'),
                            'branche': row.get('branche'),
                            'abr': row.get('abr'),
                            'version': row.get('version'),
                            'condition_access': row.get('condition_access') or row.get('conditions'),
                            'formation': formation,
                            'updated_by': user
                        }
                    )

            elif data_type == 'Modules':
                specialite = Specialites.objects.filter(code=row.get('specialite_code')).first()
                if specialite:
                    Modules.objects.update_or_create(
                        code=row['code'],
                        defaults={
                            'label': row.get('label'),
                            'duree': row.get('duree'),
                            'coef': row.get('coef'),
                            'systeme_eval': row.get('systeme_eval'),
                            'specialite': specialite,
                            'created_by': user
                        }
                    )

            elif data_type == 'Formateurs':
                email = row.get('Email') or row.get('email')
                nom = row.get('Nom') or row.get('nom')
                prenom = row.get('Prénom') or row.get('prenom')
                telephone = row.get('Téléphone') or row.get('telephone')
                diplome = row.get('Diplôme') or row.get('diplome')
                nin = row.get('NIN') or row.get('nin')
                nin = row.get('NIN') or row.get('nin')
                
                if email:
                    dispo_val = row.get('Disponibilité') or row.get('disponibilite') or row.get('dispo')
                    dispo_data = parse_dispo_string(dispo_val) if dispo_val else None

                    Formateurs.objects.update_or_create(
                        email=email,
                        defaults={
                            'prenom': prenom,
                            'nom': nom, # Also update nom if provided
                            'telephone': telephone,
                            'diplome': diplome,
                            'nin': nin,
                            'dispo': dispo_data
                        }
                    )

            
            success_count += 1
            
        except Exception as e:
            # Should be caught by validation ideally, but just in case
            print(f"Error importing row {row}: {e}")
            pass

    return success_count
