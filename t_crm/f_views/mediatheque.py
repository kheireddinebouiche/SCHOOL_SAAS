import os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.conf import settings
from datetime import datetime
from ..models import DocumentsDemandeInscription, Prospets, UserActionLog, FicheDeVoeux, FicheVoeuxDouble
from t_formations.models import DossierInscription
from institut_app.decorators import module_permission_required, role_required
from django.core.paginator import Paginator

def format_size(bytes):
    if bytes == 0: return '0 B'
    k = 1024
    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
    import math
    i = int(math.floor(math.log(bytes) / math.log(k)))
    return str(round(bytes / math.pow(k, i), 2)) + ' ' + sizes[i]

@login_required(login_url='institut_app:login')
@module_permission_required('crm', 'view')
@role_required('crm', ['Administrateur', 'Superviseur'])
def mediatheque_list(request):
    """
    Shows exclusively physical files (FS orphans) from 'documents_demande_inscription'.
    """
    schema_name = request.tenant.schema_name
    target_subdir = "documents_demande_inscription"
    tenant_media_dir = os.path.join(settings.MEDIA_ROOT, schema_name, target_subdir)
    
    search_query = request.GET.get('search', '')
    physical_orphans = []

    if os.path.exists(tenant_media_dir):
        physical_files = []
        for root, _, files in os.walk(tenant_media_dir):
            for f in files:
                abs_f = os.path.join(root, f)
                rel_base_dir = os.path.join(settings.MEDIA_ROOT, schema_name)
                rel_f = os.path.relpath(abs_f, rel_base_dir).replace('\\', '/')
                db_path = f"{schema_name}/{rel_f}"
                physical_files.append({
                    'db_path': db_path,
                    'rel_path': rel_f,
                    'name': f,
                    'size': os.path.getsize(abs_f),
                    'size_formatted': format_size(os.path.getsize(abs_f)),
                    'mtime': datetime.fromtimestamp(os.path.getmtime(abs_f)).strftime('%d/%m/%Y %H:%M')
                })

        # Registered files in DB
        registered_files = set(DocumentsDemandeInscription.objects.filter(file__isnull=False).values_list('file', flat=True))
        prospects = Prospets.objects.filter(Q(photo__isnull=False) | Q(logo_entreprise__isnull=False)).values('photo', 'logo_entreprise')
        for p in prospects:
            if p['photo']: registered_files.add(str(p['photo']))
            if p['logo_entreprise']: registered_files.add(str(p['logo_entreprise']))

        # Filtering
        for f_info in physical_files:
            if f_info['db_path'] not in registered_files:
                if not search_query or search_query.lower() in f_info['name'].lower():
                    physical_orphans.append(f_info)

    # Sort by mtime (newest first)
    physical_orphans.sort(key=lambda x: x['mtime'], reverse=True)

    # Pagination
    fs_paginator = Paginator(physical_orphans, 15)
    fs_page_number = request.GET.get('fs_page')
    fs_page_obj = fs_paginator.get_page(fs_page_number)

    stats = {
        'fs_orphaned_count': len(physical_orphans),
        'total_docs': DocumentsDemandeInscription.objects.count(),
    }

    context = {
        'page_title': 'Médiathèque des Fichiers Inconnus',
        'fs_page_obj': fs_page_obj,
        'stats': stats,
        'search_query': search_query,
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/crm/mediatheque.html', context)

@login_required(login_url='institut_app:login')
def ApiSearchProspects(request):
    term = request.GET.get('term', '')
    prospects = Prospets.objects.filter(
        Q(nom__icontains=term) | 
        Q(prenom__icontains=term) |
        Q(email__icontains=term) |
        Q(id__icontains=term)
    ).order_by('nom')[:20]
    
    data = []
    for p in prospects:
        # Try to find promo from standard or double wish
        promo_label = "Sans Promo"
        try:
            if p.is_double:
                wish = FicheVoeuxDouble.objects.filter(prospect=p, is_confirmed=True).first()
            else:
                wish = FicheDeVoeux.objects.filter(prospect=p, is_confirmed=True).first()
                if not wish: # fallback to unconfirmed
                    wish = FicheDeVoeux.objects.filter(prospect=p).first()
            
            if wish and wish.promo:
                promo_label = wish.promo.label
        except Exception:
            pass

        data.append({
            'id': p.id, 
            'text': f"{p.nom} {p.prenom} (Promo: {promo_label}) (ID: {p.id})"
        })
        
    return JsonResponse({'results': data})

@login_required(login_url='institut_app:login')
def ApiListPreinscritsJSON(request):
    """Returns a full list of pre-enrolled and pending payment students for the selection table modal."""
    prospects = Prospets.objects.filter(statut__in=['prinscrit', 'instance']).order_by('-created_at')
    
    data = []
    for p in prospects:
        promo_label = "N/A"
        try:
            if p.is_double:
                wish = FicheVoeuxDouble.objects.filter(prospect=p, is_confirmed=True).first()
            else:
                wish = FicheDeVoeux.objects.filter(prospect=p, is_confirmed=True).first()
                if not wish:
                    wish = FicheDeVoeux.objects.filter(prospect=p).first()
            
            if wish and wish.promo:
                promo_label = wish.promo.label
        except Exception:
            pass

        data.append({
            'id': p.id,
            'nom': p.nom,
            'prenom': p.prenom,
            'full_name': f"{p.nom} {p.prenom}",
            'promo': promo_label,
            'tele': p.telephone or "N/A",
            'email': p.email or "N/A",
            'statut': p.statut
        })
        
    return JsonResponse({'data': data})

@login_required(login_url='institut_app:login')
def ApiAssignDocument(request):
    """Assigns an EXISTING DB document to a prospect."""
    if request.method == 'POST':
        document_id = request.POST.get('document_id')
        prospect_id = request.POST.get('prospect_id')
        dossier_id = request.POST.get('dossier_id')
        label = request.POST.get('label')

        try:
            doc = DocumentsDemandeInscription.objects.get(id=document_id)
            prospect = Prospets.objects.get(id=prospect_id)
            dossier_type = DossierInscription.objects.get(id=dossier_id)

            # Find the active fiche
            fiche_v = None
            fiche_vd = None
            if prospect.is_double:
                fiche_vd = FicheVoeuxDouble.objects.filter(prospect=prospect, is_confirmed=True).first()
                if not fiche_vd: fiche_vd = FicheVoeuxDouble.objects.filter(prospect=prospect).first()
            else:
                fiche_v = FicheDeVoeux.objects.filter(prospect=prospect, is_confirmed=True).first()
                if not fiche_v: fiche_v = FicheDeVoeux.objects.filter(prospect=prospect).first()

            doc.prospect = prospect
            doc.id_document = dossier_type
            doc.fiche_voeux = fiche_v
            doc.fiche_voeux_double = fiche_vd
            doc.label = label if label else dossier_type.label
            doc.save()

            UserActionLog.objects.create(
                user=request.user, action_type='UPDATE', target_model='Document', target_id=str(doc.id),
                details=f"Document affecté au prospect {prospect.nom} {prospect.prenom}. Type: {dossier_type.label}",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

@login_required(login_url='institut_app:login')
def ApiImportPhysicalFile(request):
    """Creates a DB record for a physical file and assigns it to a prospect."""
    if request.method == 'POST':
        db_path = request.POST.get('db_path') # e.g. "tenant_2/files/scan.pdf"
        prospect_id = request.POST.get('prospect_id')
        dossier_id = request.POST.get('dossier_id')
        label = request.POST.get('label')

        try:
            prospect = Prospets.objects.get(id=prospect_id)
            dossier_type = DossierInscription.objects.get(id=dossier_id)

            # Find the active fiche
            fiche_v = None
            fiche_vd = None
            if prospect.is_double:
                fiche_vd = FicheVoeuxDouble.objects.filter(prospect=prospect, is_confirmed=True).first()
                if not fiche_vd: fiche_vd = FicheVoeuxDouble.objects.filter(prospect=prospect).first()
            else:
                fiche_v = FicheDeVoeux.objects.filter(prospect=prospect, is_confirmed=True).first()
                if not fiche_v: fiche_v = FicheDeVoeux.objects.filter(prospect=prospect).first()

            # Create the record
            doc = DocumentsDemandeInscription.objects.create(
                prospect=prospect,
                fiche_voeux=fiche_v,
                fiche_voeux_double=fiche_vd,
                id_document=dossier_type,
                label=label if label else dossier_type.label,
                file=db_path # Django will handle this if the path is relative to MEDIA_ROOT
            )

            UserActionLog.objects.create(
                user=request.user, action_type='CREATE', target_model='Document', target_id=str(doc.id),
                details=f"Importation et affectation du fichier physique {db_path} au prospect {prospect.nom}.",
                ip_address=request.META.get('REMOTE_ADDR')
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})
