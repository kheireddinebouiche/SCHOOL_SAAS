import json
from django.core.exceptions import ValidationError
import openpyxl
from .models import Partenaires, Formation, Specialites, Modules, Formateurs
from django.db.models import Q

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
                code = row.get('code')
                if not code:
                    error_msg.append("Code manquant")
                else:
                    if Partenaires.objects.filter(code=code).exists():
                         is_update = True
                
                # Basic validation
                if not row.get('nom'): error_msg.append("Nom manquant")

            elif data_type == 'Formation':
                code = row.get('code')
                partenaire_code = row.get('partenaire_code')
                
                if not code: error_msg.append("Code manquant")
                else:
                    if Formation.objects.filter(code=code).exists():
                        is_update = True
                
                if not row.get('nom'): error_msg.append("Nom manquant")
                if not row.get('duree'): error_msg.append("Durée manquante")
                
                if partenaire_code:
                     if not Partenaires.objects.filter(code=partenaire_code).exists():
                         error_msg.append(f"Partenaire avec code '{partenaire_code}' introuvable")

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
                email = row.get('email')
                if not email:
                     error_msg.append("Email manquant")
                else:
                    if Formateurs.objects.filter(email=email).exists():
                        is_update = True
                
                if not row.get('nom'): error_msg.append("Nom manquant")
                if not row.get('prenom'): error_msg.append("Prénom manquant")
            
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
                Partenaires.objects.update_or_create(
                    code=row['code'],
                    defaults={
                        'nom': row.get('nom'),
                        'adresse': row.get('adresse'),
                        'telephone': row.get('telephone'),
                        'email': row.get('email'),
                        'site_web': row.get('site_web'),
                        'type_partenaire': row.get('type_partenaire'),
                        'created_by': user
                    }
                )
            
            elif data_type == 'Formation':
                partenaire = None
                if row.get('partenaire_code'):
                    partenaire = Partenaires.objects.filter(code=row['partenaire_code']).first()
                
                Formation.objects.update_or_create(
                    code=row['code'],
                    defaults={
                        'nom': row.get('nom'),
                        'description': row.get('description'),
                        'duree': row.get('duree', 0),
                        'type_formation': row.get('type_formation', 'national'),
                        'frais_inscription': row.get('frais_inscription'),
                        'prix_formation': row.get('prix_formation'),
                        'partenaire': partenaire,
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
                            'duree': row.get('duree'),
                            'branche': row.get('branche'),
                            'abr': row.get('abr'),
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
                Formateurs.objects.update_or_create(
                    email=row['email'],
                    defaults={
                        'nom': row.get('nom'),
                        'prenom': row.get('prenom'),
                        'telephone': row.get('telephone'),
                        'diplome': row.get('diplome')
                    }
                )
            
            success_count += 1
            
        except Exception as e:
            # Should be caught by validation ideally, but just in case
            print(f"Error importing row {row}: {e}")
            pass

    return success_count
