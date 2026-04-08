from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from t_tresorerie.models import PaymentCategory, OperationsBancaire
from t_crm.models import Opportunite, Prospets, ProspectBankAccount
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum, Q
from weasyprint import HTML
import os
from django.conf import settings
from .utils import num_to_words_fr
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from institut_app.decorators import ajax_required

@login_required(login_url='institut_app:login')
def ListeThematique(request):
    context = {
        'tenant' : request.tenant,
        'tvas': TvaConseil.objects.all().order_by('valeur'),
    }
    return render(request, 'tenant_folder/conseil/liste-des-thematiques.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadThematique(request):
    thematique = Thematiques.objects.filter(etat  = "active").values('id', 'label', 'description', 'prix', 'created_at', 'billing_type', 'default_tva', 'categorie')
    return JsonResponse(list(thematique), safe=False)

@login_required(login_url='institut_app:login')
def ApiSaveThematique(request):
    label = request.POST.get('label')
    prix = request.POST.get('prix')
    description = request.POST.get('description')
    billing_type = request.POST.get('billing_type', 'heure')
    default_tva = request.POST.get('default_tva', 19.00)
    categorie = request.POST.get('categorie', 'service')

    Thematiques.objects.create(
        label = label,
        description = description,
        prix = prix,
        billing_type = billing_type,
        default_tva = default_tva,
        categorie = categorie
    )

    return JsonResponse({'status': 'success', 'message': 'ThÃ©matique ajoutÃ©e avec succÃ¨s.'})

@login_required(login_url='institut_app:login')
def ApiLoadThematiqueDetails(request):
    id_thematique = request.GET.get('id_thematique')
    obj = Thematiques.objects.filter(id = id_thematique)
    data =[]
    for i in obj:
        data = {
            'id': i.id,
            'label': i.label,
            'description': i.description,
            'prix': i.prix,
            'default_tva': i.default_tva,
            'categorie': i.categorie
        }
    return JsonResponse(data, safe=False)

@login_required(login_url='institut_app:login')
def DetailsProspectConseil(request, slug):
    prospect = get_object_or_404(Prospets, slug=slug)
    
    context = {
        'tenant': request.tenant,
        'prospect': prospect,
        'pk': prospect.id,
        'slug': prospect.slug,
    }
    
    # Use dedicated template for Conseil/Executive Education
    return render(request, 'tenant_folder/conseil/prospect/details_prospect.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadProspectDevis(request):
    id_prospect = request.GET.get('id_prospect')
    devis = Devis.objects.filter(client_id=id_prospect).values('id', 'num_devis', 'montant', 'date_emission', 'etat')
    return JsonResponse(list(devis), safe=False)

@login_required(login_url='institut_app:login')
def ApiLoadProspectFactures(request):
    id_prospect = request.GET.get('id_prospect')
    factures = Facture.objects.filter(client_id=id_prospect)
    
    data = []
    for f in factures:
        data.append({
            'id': f.id,
            'num_facture': f.num_facture,
            'date_emission': f.date_emission,
            'etat': f.etat,
            'montant': f.total_ttc()
        })
    return JsonResponse(data, safe=False)

@login_required(login_url='institut_app:login')
def ApiLoadProspectFinancials(request):
    id_prospect = request.GET.get('id_prospect')
    factures = Facture.objects.filter(client_id=id_prospect)
    
    total_facture = 0
    total_paye = 0
    
    for f in factures:
        total_facture += f.total_ttc()
        # Sum payments for this facture
        payments_sum = f.paiements.filter(is_done=True).aggregate(Sum('montant'))['montant__sum'] or 0
        total_paye += payments_sum
        
    return JsonResponse({
        'total_invoiced': float(total_facture),
        'total_paid': float(total_paye),
        'balance': float(total_facture - total_paye)
    })

@login_required(login_url='institut_app:login')
def AddNewDevis(request):
    form = NewDevisForms()
    if request.method == "POST":
        form = NewDevisForms(request.POST)
        if form.is_valid():
            devis = form.save()
            
            # Create a new Opportunity for this manual Devis creation
            # Since the user explicitly creates a NEW quote, we assume a NEW opportunity unless specified otherwise.
            # (Ideally we'd let them pick an existing opportunity, but for now this fixes the "doesn't add to pipeline" issue)
            try:
                opp = Opportunite.objects.create(
                    prospect=devis.client,
                    nom=f"Devis #{devis.num_devis}",
                    stage='entrant', # Start at entrant or devis_envoye? If it's a draft, maybe just entrant or nego?
                    # Actually if it is just "Nouveau Devis" it is a draft. Let's say 'negociation' or keep 'entrant'.
                    # User complaint: "l'opportunitÃ© ne se rajoute pas".
                    budget=devis.montant or 0,
                    commercial=request.user # Assign current user as commercial?
                )
                devis.opportunite = opp
                devis.save()
            except Exception as e:
                # Log error but don't crash
                print(f"Error creating opportunity: {e}")

            messages.success(request, "Devis ajoutÃ© avec succÃ¨s.")
            return redirect('t_conseil:configure-devis', pk=form.instance.num_devis)
        else:
            messages.error(request, "Erreur lors de l'ajout du devis.")
            return redirect('t_conseil:AddNewDevis')

    context = {
        'form' : form,
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/conseil/nouveau-devis.html', context)

@login_required(login_url='institut_app:login')
def AddNewFacture(request):
    form = NewFactureForms()
    if request.method == "POST":
        form = NewFactureForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Facture ajoutÃ©e avec succÃ¨s.")
            return redirect('t_conseil:configure-facture', pk=form.instance.num_facture)
        else:
            messages.error(request, "Erreur lors de l'ajout de la facture.")
            return redirect('t_conseil:AddNewFacture')

    context = {
        'form' : form,
        'tenant' : request.tenant,
    }

    return render(request, 'tenant_folder/conseil/nouveau-facture.html', context)

@login_required(login_url='institut_app:login')
def ApiFetchEnterpriseTvas(request):
    ent_id = request.GET.get('enterprise_id')
    if not ent_id:
        return JsonResponse({'status': 'error', 'message': 'ID Entreprise manquant'}, status=400)
    
    tvas = TvaConseil.objects.all().order_by('valeur')
    data = [{'valeur': float(t.valeur), 'label': t.label, 'is_default': t.is_default} for t in tvas]
    return JsonResponse({'status': 'success', 'tvas': data})

@login_required(login_url='institut_app:login')
def configure_devis(request, pk):
    if pk is None or pk == '0':
        return redirect('t_conseil:AddNewDevis')
    else:
        devis = Devis.objects.get(num_devis=pk)
        lignes_devis = devis.lignes_devis.all()

        config = None
        if devis.entreprise:
            config = ConseilConfiguration.objects.filter(entreprise=devis.entreprise).first()
        
        if not config:
            config, _ = ConseilConfiguration.objects.get_or_create(entreprise=None)
        
        tvas = TvaConseil.objects.all().order_by('valeur')
        context = {
            'tenant' : request.tenant,
            'devis' : devis,
            'lignes_devis' : lignes_devis,
            'config': config,
            'tvas': tvas,
            'enterprises': Entreprise.objects.all(),
            'can_edit': devis.etat == 'brouillon'
        }

        return render(request, 'tenant_folder/conseil/configure-devis.html', context)

@login_required(login_url='institut_app:login')
def configure_facture(request, pk):
    if pk is None or pk == '0':
        return redirect('t_conseil:AddNewFacture')
    else:
        facture = Facture.objects.get(num_facture=pk)
        lignes_facture = facture.lignes_facture.all()

        config = None
        if facture.entreprise:
            config = ConseilConfiguration.objects.filter(entreprise=facture.entreprise).first()
        
        if not config:
            config, _ = ConseilConfiguration.objects.get_or_create(entreprise=None)
        
        tvas = TvaConseil.objects.all().order_by('valeur')
        context = {
            'tenant' : request.tenant,
            'facture' : facture,
            'lignes_facture' : lignes_facture,
            'config': config,
            'tvas': tvas,
            'enterprises': Entreprise.objects.all(),
            'can_edit': facture.etat == 'brouillon'
        }

        return render(request, 'tenant_folder/conseil/configure-facture.html', context)

@login_required(login_url="institut_app:login")
def ListeDesDevis(request):
    devis = Devis.objects.all().order_by('-created_at')
    
    # Calculate KPIs
    stats = {
        'total': devis.count(),
        'accepte': devis.filter(etat='accepte').count(),
        'attente': devis.filter(etat__in=['brouillon', 'envoye']).count(),
        'rejete': devis.filter(etat='rejete').count(),
    }
    
    context = {
        "devis" : devis,
        "stats": stats,
    }
    return render(request,'tenant_folder/conseil/liste_des_devis.html', context)

@login_required(login_url='institut_app:login')
def ArchiveThematique(request):
    context = {
        'tenant' : request.tenant
    }

    return render(request, 'tenant_folder/conseil/archive_thematique.html', context)

@login_required(login_url='institut_app:login')
def ApiLoadArchivedThematique(request):
    thematique = Thematiques.objects.filter(etat = "archive").values('id', 'label', 'prix', 'created_at', 'categorie', 'billing_type')
    return JsonResponse(list(thematique), safe=False)

@login_required(login_url='institut_app:login')
def ApiArchiveThematique(request):
    id_thematique = request.POST.get('id_thematique')
    thematique = Thematiques.objects.get(id=id_thematique)
    thematique.etat = "archive"
    thematique.save()
    return JsonResponse({'status': 'success', 'message': 'ThÃ©matique archivÃ©e avec succÃ¨s.'})   
    
@login_required(login_url='institut_app:login')
def ApiActivateThematique(request):
    id_thematique = request.POST.get('id_thematique')
    thematique = Thematiques.objects.get(id=id_thematique)
    thematique.etat = "active"
    thematique.save()
    return JsonResponse({'status': 'success', 'message': 'ThÃ©matique activÃ©e avec succÃ¨s.'})

@login_required(login_url='institut_app:login')
def ApiDeleteFinalThematique(request):
    id_thematique = request.POST.get('id_thematique')
    thematique = Thematiques.objects.get(id=id_thematique)
    thematique.delete()
    return JsonResponse({'status': 'success', 'message': 'ThÃ©matique supprimÃ©e dÃ©finitivement.'})

def make_prospect_client(request):
    pass

@login_required(login_url='institut_app:login')
def ApiUpdateThematique(request):
    id_thematique = request.POST.get('id_thematique')
    label = request.POST.get('label')
    prix = request.POST.get('prix')
    description = request.POST.get('description')
    default_tva = request.POST.get('default_tva')
    categorie = request.POST.get('categorie')

    try:
        thematique = Thematiques.objects.get(id=id_thematique)
        thematique.label = label
        thematique.categorie = categorie
        
        # Handle numeric fields safely
        if prix:
            thematique.prix = str(prix).replace(',', '.')
        else:
            thematique.prix = None
            
        if default_tva:
            thematique.default_tva = str(default_tva).replace(',', '.')
        else:
            thematique.default_tva = 19.00
            
        thematique.description = description
        thematique.save()
        return JsonResponse({'status': 'success', 'message': 'ThÃ©matique mise Ã  jour avec succÃ¨s.'})
    except Thematiques.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': f'ThÃ©matique introuvable (ID: {id_thematique})'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Erreur lors de la mise Ã  jour : {str(e)}'})



@login_required(login_url="institut_app:login")
def ListeProspectConseil(request):
    context ={
        'tenant' : request.tenant,
    }
    return render(request, "tenant_folder/conseil/prospect/liste_des_prospects.html",context)

@login_required(login_url="institut_app:login")
def ApiLoadProspect(request):
    pass

@login_required(login_url="institut_app:login")
def ListeDesClients(request):
    context = {
        'tenant': request.tenant,
    }
    return render(request, "tenant_folder/conseil/clients/liste_des_clients.html", context)

@login_required(login_url="institut_app:login")
def DetailsClient(request, slug):
    client = get_object_or_404(Prospets, slug=slug)
    context = {
        'tenant': request.tenant,
        'client': client,
        'pk': client.id,
    }
    return render(request, "tenant_folder/conseil/clients/details_client.html", context)

@login_required(login_url="institut_app:login")
def ApiListeClients(request):
    liste = Prospets.objects.filter(context='con', is_client=True).values(
        'id', 'slug', 'nom', 'prenom', 'entreprise', 'email', 'telephone', 'created_at', 'convertit_date'
    )
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def ApiTransformeToClient(request):
    id_prospect = request.POST.get('id_prospect')
    try:
        prospect = Prospets.objects.get(id=id_prospect)
        prospect.is_client = True
        prospect.statut = 'convertit'
        prospect.convertit_date = timezone.now().date()
        prospect.save()
        return JsonResponse({'status': 'success', 'message': 'Prospect converti en client.'})
    except Prospets.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Prospect non trouvÃ©.'})

@login_required(login_url="institut_app:login")
def ApiSaveLigneDevis(request):
    import decimal
    devis_id = request.POST.get('devis_id')
    thematique_id = request.POST.get('thematique_id')
    quantite = request.POST.get('quantite')
    description = request.POST.get('description')
    
    devis = Devis.objects.get(num_devis=devis_id)
    thematique = Thematiques.objects.get(id=thematique_id)
    
    try:
        qty = decimal.Decimal(quantite)
    except:
        qty = 0
        
    montant_ligne = (thematique.prix or 0) * qty

    LignesDevis.objects.create(
        devis=devis,
        thematique=thematique,
        description=description or thematique.label,
        quantite=qty,
        montant=montant_ligne 
    )
    
    # Recalculate devis total
    total = sum(l.montant for l in devis.lignes_devis.all() if l.montant)
    devis.montant = total
    devis.save()

    return JsonResponse({'status': 'success', 'message': 'Ligne ajoutÃ©e avec succÃ¨s.'})

@login_required(login_url="institut_app:login")
def ApiStartTransformationDevisToFacture(request):
    import decimal
    devis_id = request.POST.get('devis_id')
    tva_input = request.POST.get('tva', 19)
    try:
        tva = decimal.Decimal(str(tva_input).replace(',', '.'))
    except:
        tva = decimal.Decimal('19')
        
    try:
        devis = Devis.objects.get(num_devis=devis_id)
    except Devis.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Devis introuvable.'}, status=404)
    
    # Create Facture copying settings from Devis
    # Automatically accept the devis when converting to invoice
    devis.etat = 'accepte'
    devis.save()

    facture = Facture.objects.create(
        client=devis.client,
        entreprise=devis.entreprise,
        devis_source=devis,
        date_emission=timezone.now().date(),
        tva=tva, # Global TVA (kept for legacy/defaults, though lines manage their own)
        show_tva=devis.show_tva,
        show_remise=devis.show_remise,
        etat='brouillon',
        module_source='conseil',
        conditions_commerciales=devis.conditions_commerciales
    )
    
    for ligne in devis.lignes_devis.all():
        # Recalculate Unit Price: Montant = (UP * Qty) * (1 - Remise/100)
        # => UP = Montant / (Qty * (1 - Remise/100))
        qty = ligne.quantite if ligne.quantite and ligne.quantite > 0 else 1
        remise_val = ligne.remise_percent if ligne.remise_percent else 0
        remise_factor = decimal.Decimal(1) - (remise_val / decimal.Decimal(100))
        
        if remise_factor <= 0: remise_factor = 1 # Safety
        
        if ligne.prix_unitaire and ligne.prix_unitaire > 0:
            up = ligne.prix_unitaire
        elif ligne.montant:
            try:
                up = (ligne.montant / decimal.Decimal(qty)) / remise_factor
            except:
                up = 0
        else:
            up = 0

        LignesFacture.objects.create(
            facture=facture,
            thematique=ligne.thematique,
            specialite=ligne.specialite, # Support degree formations
            description=ligne.description,
            long_description=ligne.long_description,
            quantite=ligne.quantite,
            prix_unitaire=up,
            montant_ht=ligne.montant,
            remise_percent=ligne.remise_percent,
            tva_percent=ligne.tva_percent
        )
        
    # Update CRM Pipeline Stage
    if devis.opportunite:
        devis.opportunite.stage = 'facture'
        devis.opportunite.save()
    elif facture.client:
        # Check for related opportunity (linked to prospect) - Fallback
        opp = Opportunite.objects.filter(prospect=facture.client).order_by('-created_at').first()
        if opp:
            opp.stage = 'facture'
            opp.save()
        else:
             # Create new won opportunity?
             Opportunite.objects.create(
                 prospect=facture.client,
                 nom=f"Facture {facture.num_facture}",
                 stage='facture',
                 budget=facture.total_ttc or 0
             )
        
    # Carry over participants if any
    for part in Participant.objects.filter(devis=devis):
        Participant.objects.create(
            facture=facture,
            nom=part.nom,
            prenom=part.prenom,
            email=part.email,
            telephone=part.telephone,
            date_naissance=part.date_naissance,
            lieu_naissance=part.lieu_naissance,
            poste=part.poste,
            nin=part.nin
        )
        
    return JsonResponse({'status': 'success', 'message': 'Devis transformÃ© en facture avec succÃ¨s.', 'facture_num': facture.num_facture})

@login_required(login_url="institut_app:login")
def ApiSaveDevisItems(request):
    import json
    import decimal
    
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        devis_id = data.get('devis_id')
        items = data.get('items', [])
        show_tva = data.get('show_tva', True)
        show_remise = data.get('show_remise', False)
        
        devis = Devis.objects.get(num_devis=devis_id)
        devis.show_tva = show_tva
        devis.show_remise = show_remise
        
        # Associated enterprise if provided
        entreprise_id = data.get('entreprise_id')
        if entreprise_id:
            try:
                devis.entreprise = Entreprise.objects.get(id=entreprise_id)
            except Entreprise.DoesNotExist:
                pass
        
        # Conditions commerciales
        conditions = data.get('conditions_commerciales')
        if conditions is not None:
            devis.conditions_commerciales = conditions
        
        # Clear existing lines to replace with new ones (full sync) or append?
        # Usually full sync is safer for "Save" button unless we track IDs.
        # For simplicity, let's clear and re-create.
        from django.db import transaction
        
        with transaction.atomic():
            # Clear existing lines to replace with new ones (full sync)
            devis.lignes_devis.all().delete()
            
            total_montant = 0
            
            for item in items:
                thematique_id = item.get('thematique_id')
                specialite_id = item.get('specialite_id') # Support degree formations
                description = item.get('description')
                long_description = item.get('long_description', '')
                quantite = item.get('quantity')
                price = item.get('unitPrice')
                remise = item.get('remise_percent', 0)
                tva_l = item.get('tva_percent', 19.00)

                
                thematique = None
                if thematique_id:
                    try:
                        thematique = Thematiques.objects.get(id=thematique_id)
                    except Thematiques.DoesNotExist:
                        pass
                
                specialite = None
                if specialite_id:
                    try:
                        from t_formations.models import Specialites
                        specialite = Specialites.objects.get(id=specialite_id)
                    except Specialites.DoesNotExist:
                        pass
                
                try:
                    qty = decimal.Decimal(str(quantite))
                    unit_price = decimal.Decimal(str(price))
                    remise_percent = decimal.Decimal(str(remise))
                    tva_percent = decimal.Decimal(str(tva_l))
                except:
                    qty = 0
                    unit_price = 0
                    remise_percent = 0
                    tva_percent = 19
                    
                montant_ligne = (unit_price * qty) * (1 - (remise_percent / 100))
                total_montant += montant_ligne
                
                LignesDevis.objects.create(
                    devis=devis,
                    thematique=thematique,
                    specialite=specialite, # Support degree formations
                    description=description,
                    long_description=long_description,
                    quantite=qty,
                    prix_unitaire=unit_price,
                    montant=montant_ligne,
                    remise_percent=remise_percent,
                    tva_percent=tva_percent
                )
            
            devis.montant = total_montant
            devis.save()
            
            # Update linked Opportunity Budget
            if devis.opportunite:
                devis.opportunite.budget = total_montant
                devis.opportunite.save()

        return JsonResponse({'status': 'success', 'message': 'Devis enregistrÃ© avec succÃ¨s.'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url="institut_app:login")
def DetailsDevis(request, pk):
    devis = Devis.objects.get(num_devis=pk)
    lignes_devis = devis.lignes_devis.all()
    
    # Calculate totals for summary (since we have per-line TVA)
    total_ht = 0
    tva_breakdown = {}
    
    for ligne in lignes_devis:
        total_ht += ligne.montant
        if devis.show_tva:
            rate = float(ligne.tva_percent)
            amount = float(ligne.montant) * (rate / 100)
            if rate > 0:
                tva_breakdown[rate] = tva_breakdown.get(rate, 0) + amount
    
    total_tva = sum(tva_breakdown.values())
    total_ttc = float(total_ht) + total_tva
    
    # Sort breakdown for consistent display
    sorted_tva = sorted([{'rate': r, 'amount': a} for r, a in tva_breakdown.items()], key=lambda x: x['rate'], reverse=True)
    
    context = {
        'tenant' : request.tenant,
        'devis' : devis,
        'lignes_devis' : lignes_devis,
        'total_ht': total_ht,
        'total_tva': total_tva,
        'total_ttc': total_ttc,
        'tva_breakdown': sorted_tva,
        'has_facture': Facture.objects.filter(devis_source=devis).exists(),
        'participants': Participant.objects.filter(devis=devis)
    }
    return render(request, 'tenant_folder/conseil/details_devis.html', context)

@login_required(login_url='institut_app:login')
def ApiValidateDevis(request):
    if request.method == 'POST':
        devis_id = request.POST.get('devis_id')
        try:
            devis = Devis.objects.get(num_devis=devis_id)
            devis.etat = 'envoye'
            devis.save()
            
            # Update CRM Pipeline Stage
            if devis.opportunite:
                devis.opportunite.stage = 'devis_envoye'
                devis.opportunite.save()
            elif devis.client:
                 # Fallback for legacy devis without direct link
                opp = Opportunite.objects.filter(prospect=devis.client).order_by('-created_at').first()
                if opp:
                    opp.stage = 'devis_envoye'
                    opp.save()
                    # Link it for future
                    devis.opportunite = opp
                    devis.save()
                else:
                    new_opp = Opportunite.objects.create(
                        prospect=devis.client,
                        nom=f"Devis #{devis.num_devis}",
                        stage='devis_envoye',
                        budget=devis.montant or 0
                    )
                    devis.opportunite = new_opp
                    devis.save()

            return JsonResponse({'status': 'success', 'message': 'Devis validÃ© avec succÃ¨s.'})
        except Devis.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Devis non trouvÃ©.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='institut_app:login')
def ApiRevertDevisToDraft(request):
    if request.method == 'POST':
        devis_id = request.POST.get('devis_id')
        try:
            devis = Devis.objects.get(num_devis=devis_id)
            # Check if has facture
            if Facture.objects.filter(devis_source=devis).exists():
                return JsonResponse({'status': 'error', 'message': 'Impossible de repasser en brouillon : une facture est dÃ©jÃ  associÃ©e Ã  ce devis.'})
            
            devis.etat = 'brouillon'
            devis.save()
            return JsonResponse({'status': 'success', 'message': 'Devis repassÃ© en brouillon.'})
        except Devis.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Devis non trouvÃ©.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url="institut_app:login")
def ListeDesFactures(request):
    factures = Facture.objects.filter(module_source='conseil').order_by('-created_at')
    
    # Calculate stats
    stats = {
        'total': factures.count(),
        'payee': factures.filter(etat='payee').count(),
        'envoye': factures.filter(etat='envoye').count(),
        'brouillon': factures.filter(etat='brouillon').count(),
    }
    
    config, _ = ConseilConfiguration.objects.get_or_create(id=1)
    tvas = TvaConseil.objects.all().order_by('valeur')
    
    # Get all enterprises for tabs
    enterprises = Entreprise.objects.all()

    context = {
        "tenant": request.tenant,
        "factures": factures,
        "stats": stats,
        "config": config,
        "tvas": tvas,
        "enterprises": enterprises,
    }
    return render(request, 'tenant_folder/conseil/liste_des_factures.html', context)


@login_required(login_url="institut_app:login")
def ApiQuickCreateProspect(request):
    if request.method != "POST":
         return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    nom = request.POST.get('nom')
    prenom = request.POST.get('prenom')
    email = request.POST.get('email')
    telephone = request.POST.get('telephone')
    type_prospect = request.POST.get('type_prospect', 'particulier')
    entreprise_nom = request.POST.get('entreprise')
    poste = request.POST.get('poste')
    
    if not nom or not telephone:
         return JsonResponse({'status': 'error', 'message': 'Nom et TÃ©lÃ©phone sont obligatoires.'})
         
    try:
        # Check for duplicates? For now, we assume standard creation.
        
        prospect = Prospets.objects.create(
            nom=nom,
            prenom=prenom,  # Keep prenom for both types - it's the contact person name
            email=email,
            telephone=telephone,
            type_prospect=type_prospect,
            context='con', # Conseil
            indic='+213', # Default
            # Enterprise specific fields - only populated for entreprise type
            entreprise=entreprise_nom if type_prospect == 'entreprise' else None,
            poste_dans_entreprise=poste if type_prospect == 'entreprise' else None,
        )
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Prospect créé avec succès.',
            'prospect': {
                'id': prospect.id,
                'nom': prospect.nom,
                'prenom': prospect.prenom,
                'type': prospect.type_prospect,
                'entreprise': prospect.entreprise
            }
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required(login_url="institut_app:login")
@ajax_required
def ApiDeleteOpportunite(request):
    if request.method == "POST":
        id_opp = request.POST.get('id')
        try:
            opp = Opportunite.objects.get(id=id_opp)
            opp.delete()
            return JsonResponse({'status': 'success', 'message': 'OpportunitÃ© supprimÃ©e.'})
        except Opportunite.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'OpportunitÃ© non trouvÃ©e.'})
    return JsonResponse({'status': 'error', 'message': 'MÃ©thode non autorisÃ©e.'})

@login_required(login_url="institut_app:login")
@ajax_required
def ApiAddPaiement(request):
    if request.method == "POST":
        facture_id = request.POST.get('facture_id')
        montant = request.POST.get('montant')
        date_p = request.POST.get('date_paiement')
        mode = request.POST.get('mode_paiement')
        ref = request.POST.get('reference', '')
        note = request.POST.get('note', '')

        try:
            facture = Facture.objects.get(num_facture=facture_id)
            
            paiement = Paiement.objects.create(
                facture=facture,
                montant=montant,
                date_paiement=date_p,
                mode_paiement=mode,
                reference=ref,
                note=note
            )

            if mode in ['virement', 'cheque']:
                OperationsBancaire.objects.create(
                    operation_type='entree',
                    conseil_paiement=paiement,
                    montant=montant,
                    reference_bancaire=ref,
                )

            # Update Facture Status
            total_ttc = facture.total_ttc()
            total_paye = sum(p.montant for p in facture.paiements.all())

            if total_paye >= total_ttc:
                facture.etat = 'paye'
            elif total_paye > 0:
                facture.etat = 'battente'
            
            facture.save()

            return JsonResponse({
                'status': 'success', 
                'message': 'Paiement enregistrÃ© avec succÃ¨s.',
                'new_status': facture.get_etat_display(),
                'total_paye': float(total_paye)
            })

        except Facture.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Facture non trouvÃ©e.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'MÃ©thode non autorisÃ©e.'})

@login_required(login_url="institut_app:login")
def DetailsFacture(request, pk):
    facture = Facture.objects.get(num_facture=pk)
    lignes_facture = facture.lignes_facture.all()
    
    config = None
    if facture.entreprise:
        config = ConseilConfiguration.objects.filter(entreprise=facture.entreprise).first()
    
    if not config:
        config, _ = ConseilConfiguration.objects.get_or_create(entreprise=None)
        
    tvas = TvaConseil.objects.all().order_by('valeur')
    
    # Calculate totals and breakdown
    total_ht = 0
    tva_breakdown = {}
    
    for ligne in lignes_facture:
        total_ht += ligne.montant_ht
        if facture.show_tva:
            rate = float(ligne.tva_percent)
            amount = float(ligne.montant_ht) * (rate / 100)
            if rate > 0:
                tva_breakdown[rate] = tva_breakdown.get(rate, 0) + amount
            
    total_tva = sum(tva_breakdown.values())
    total_ttc = float(total_ht) + total_tva
    sorted_tva = sorted([{'rate': r, 'amount': a} for r, a in tva_breakdown.items()], key=lambda x: x['rate'], reverse=True)

    context = {
        "tenant": request.tenant,
        "facture": facture,
        "lignes_facture": lignes_facture,
        "config": config,
        "tvas": tvas,
        "total_ht": total_ht,
        "total_tva": total_tva,
        "total_ttc": total_ttc,
        "tva_breakdown": sorted_tva
    }
    return render(request, 'tenant_folder/conseil/details_facture.html', context)

@login_required(login_url="institut_app:login")
def ConseilDashboard(request):
    context = {
        'tenant': request.tenant,
    }
    return render(request, 'tenant_folder/conseil/dashboard.html', context)

@login_required(login_url="institut_app:login")
def PipelineConseil(request):
    from django.db.models import Sum, Q
    from django.db.models.functions import TruncMonth
    
    stages = [
        ('entrant', 'Entrant'),
        ('contacte', 'ContactÃ©'),
        ('negociation', 'NÃ©gociation'),
        ('devis_envoye', 'Devis envoyÃ©'),
        ('facture', 'FacturÃ©'),
        ('recouvrement', 'RECOUVREMENT'),
    ]
    
    view_type = request.GET.get('view', 'stage')  # 'stage' or 'closing'
    search_query = request.GET.get('search', '')
    commercial_id = request.GET.get('commercial', '')
    state_filter = request.GET.get('state', 'active') # 'active', 'inactive', 'all'
    
    prospects = Opportunite.objects.filter(prospect__context='con')
    
    # Apply Filters
    if search_query:
        prospects = prospects.filter(Q(prospect__nom__icontains=search_query) | Q(prospect__prenom__icontains=search_query) | Q(prospect__entreprise__icontains=search_query) | Q(nom__icontains=search_query))
    if commercial_id:
        prospects = prospects.filter(commercial_id=commercial_id)
    if state_filter == 'active':
        prospects = prospects.filter(is_active=True)
    elif state_filter == 'inactive':
        prospects = prospects.filter(is_active=False)

    pipeline_data = []
    
    if view_type == 'closing':
        # Group by closing month
        closing_months = prospects.filter(closing_date__isnull=False).annotate(month=TruncMonth('closing_date')).values('month').distinct().order_by('month')
        for m in closing_months:
            month_date = m['month']
            items = prospects.filter(closing_date__year=month_date.year, closing_date__month=month_date.month)
            total_budget = items.aggregate(total=Sum('budget'))['total'] or 0
            pipeline_data.append({
                'code': month_date.strftime('%Y-%m'),
                'label': month_date.strftime('%B %Y'),
                'items': items.order_by('closing_date'),
                'total_budget': total_budget,
                'count': items.count()
            })
        # Add a "Sans date" column if exists
        no_date_items = prospects.filter(closing_date__isnull=True)
        if no_date_items.exists():
             pipeline_data.append({
                'code': 'no-date',
                'label': 'Sans Date',
                'items': no_date_items.order_by('-updated_at'),
                'total_budget': no_date_items.aggregate(total=Sum('budget'))['total'] or 0,
                'count': no_date_items.count()
            })
    else:
        # Default Stage View
        for stage_code, stage_label in stages:
            stage_items = prospects.filter(stage=stage_code).order_by('-updated_at')
            total_budget = stage_items.aggregate(total=Sum('budget'))['total'] or 0
            pipeline_data.append({
                'code': stage_code,
                'label': stage_label,
                'items': stage_items,
                'total_budget': total_budget,
                'count': stage_items.count()
            })
    
    # Get all commercials for filtered list
    commercials = User.objects.filter(opportunites_conseil__isnull=False).distinct()
    
    # Get all active prospects for "New Opportunity" dropdown
    all_prospects = Prospets.objects.filter(context='con', conseil_is_active=True).order_by('nom')

    context = {
        'tenant': request.tenant,
        'pipeline_stages': pipeline_data,
        'view_type': view_type,
        'commercials': commercials,
        'all_prospects': all_prospects,
        'current_filters': {
            'search': search_query,
            'commercial': commercial_id,
            'state': state_filter
        }
    }
    return render(request, 'tenant_folder/conseil/pipeline.html', context)

@login_required(login_url="institut_app:login")
@ajax_required
def ApiToggleFavorite(request):
    prospect_id = request.POST.get('prospect_id')
    try:
        prospect = Prospets.objects.get(id=prospect_id)
        prospect.conseil_is_favorite = not prospect.conseil_is_favorite
        prospect.save()
        return JsonResponse({'status': 'success', 'is_favorite': prospect.conseil_is_favorite})
    except Prospets.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Prospect non trouvÃ©.'})

@login_required(login_url="institut_app:login")
def ExportPipelineCsv(request):
    import csv
    from django.http import HttpResponse
    
    prospects = Prospets.objects.filter(context='con', conseil_is_active=True)
    # Re-apply filters from session or GET if needed, simplicity for now:
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pipeline_conseil.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nom', 'PrÃ©nom', 'Entreprise', 'Ã‰tape', 'Budget', 'ProbabilitÃ©', 'Date Closing'])
    
    for p in prospects:
        writer.writerow([p.nom, p.prenom, p.entreprise, p.get_conseil_pipeline_stage_display(), p.conseil_budget, p.conseil_probability, p.conseil_closing_date])
        
    return response

@login_required(login_url="institut_app:login")
@ajax_required
def ApiConvertProspectToDevis(request):
    from django.urls import reverse
    # Note: 'prospect_id' parameter actually comes as opportunite_id from the new pipeline
    opp_id = request.POST.get('prospect_id') 
    try:
        opp = Opportunite.objects.get(id=opp_id)
        prospect = opp.prospect
        
        # Assign the first enterprise by default for the devis
        # In a multi-tenant set, Entreprise.objects.first() should be the correct one.
        entreprise = Entreprise.objects.first()
        
        new_devis = Devis.objects.create(
            client=prospect,
            opportunite=opp, # Link the devis to the opportunity
            date_emission=timezone.now().date(),
            entreprise=entreprise,
            etat='brouillon'
        )
        
        # Update Opportunity Stage
        opp.stage = 'devis_envoye'
        opp.save()
        
        redirect_url = reverse('t_conseil:configure-devis', kwargs={'pk': new_devis.num_devis})
        
        return JsonResponse({
            'status': 'success', 
            'message': 'OpportunitÃ© convertie en devis avec succÃ¨s.',
            'redirect_url': redirect_url
        })
    except Opportunite.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'OpportunitÃ© non trouvÃ©e.'})

@login_required(login_url="institut_app:login")
@ajax_required
def ApiDeleteDevis(request):
    num_devis = request.POST.get('num_devis')
    try:
        devis = Devis.objects.get(num_devis=num_devis)
        devis.delete()
        return JsonResponse({'status': 'success', 'message': 'Devis supprimÃ© avec succÃ¨s.'})
    except Devis.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Devis non trouvÃ©.'})

@login_required(login_url="institut_app:login")
@login_required(login_url="institut_app:login")
@ajax_required
def ApiUpdatePipelineStage(request):
    if request.method == "POST":
        # 'prospect_id' coming from frontend is actually Opportunite ID now
        opp_id = request.POST.get('prospect_id') 
        new_stage = request.POST.get('new_stage')
        
        try:
            opp = Opportunite.objects.get(id=opp_id)
            opp.stage = new_stage
            opp.save()
            return JsonResponse({'status': 'success', 'message': 'Statut mis Ã  jour.'})
        except Opportunite.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'OpportunitÃ© non trouvÃ©e.'})
    return JsonResponse({'status': 'error', 'message': 'MÃ©thode non autorisÃ©e.'})

@login_required(login_url="institut_app:login")
@ajax_required
def ApiCreateOpportunite(request):
    if request.method == "POST":
        prospect_id = request.POST.get('prospect_id')
        nom = request.POST.get('nom')
        budget = request.POST.get('budget', 0)
        
        if not prospect_id or not nom:
            return JsonResponse({'status': 'error', 'message': 'Prospect et Nom sont obligatoires.'})
            
        try:
            prospect = Prospets.objects.get(id=prospect_id)
            
            opp = Opportunite.objects.create(
                prospect=prospect,
                nom=nom,
                budget=budget,
                stage='entrant',
                commercial=request.user
            )
            
            # Get initials
            initials = ""
            if prospect.nom: initials += prospect.nom[0].upper()
            if prospect.prenom: initials += prospect.prenom[0].upper()

            return JsonResponse({
                'status': 'success', 
                'message': 'OpportunitÃ© crÃ©Ã©e avec succÃ¨s.', 
                'id': opp.id,
                'slug': prospect.slug,
                'initials': initials,
                'nom_complet': f"{prospect.nom} {prospect.prenom or ''}".strip(),
                'entreprise': prospect.entreprise or ''
            })
            
        except Prospets.DoesNotExist:
             return JsonResponse({'status': 'error', 'message': 'Prospect non trouvÃ©.'})
             
    return JsonResponse({'status': 'error', 'message': 'MÃ©thode non autorisÃ©e.'})

@login_required(login_url="institut_app:login")
def ApiGetOpportunite(request):
    opp_id = request.GET.get('id')
    try:
        opp = Opportunite.objects.get(id=opp_id)
        return JsonResponse({
            'status': 'success',
            'data': {
                'id': opp.id,
                'nom': opp.nom,
                'budget': opp.budget,
                'probability': opp.probability,
                'closing_date': opp.closing_date.strftime('%Y-%m-%d') if opp.closing_date else '',
                'stage': opp.stage,
                'prospect_name': f"{opp.prospect.nom} {opp.prospect.prenom or ''}".strip()
            }
        })
    except Opportunite.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'OpportunitÃ© non trouvÃ©e.'})

@login_required(login_url="institut_app:login")
@ajax_required
def ApiUpdateOpportunite(request):
    if request.method == "POST":
        opp_id = request.POST.get('id')
        nom = request.POST.get('nom')
        budget = request.POST.get('budget')
        probability = request.POST.get('probability')
        closing_date = request.POST.get('closing_date')
        
        try:
            opp = Opportunite.objects.get(id=opp_id)
            opp.nom = nom
            opp.budget = budget or 0
            opp.probability = probability or 0
            if closing_date:
                opp.closing_date = closing_date
            else:
                opp.closing_date = None
            
            opp.save()
            return JsonResponse({'status': 'success', 'message': 'OpportunitÃ© mise Ã  jour.'})
        except Opportunite.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'OpportunitÃ© non trouvÃ©e.'})
            
    return JsonResponse({'status': 'error', 'message': 'MÃ©thode non autorisÃ©e.'})

def ConfigurationConseil(request):
    enterprise_id = request.GET.get('enterprise_id') or request.POST.get('enterprise_id')
    enterprise = None
    if enterprise_id:
        try:
            enterprise = Entreprise.objects.get(id=enterprise_id)
        except Entreprise.DoesNotExist:
            pass
    
    if not enterprise:
        # Fallback to first enterprise for convenience in the UI? 
        # Or keep it None (Global). Let's say we prefer selecting an enterprise.
        enterprise = Entreprise.objects.first()

    config, created = ConseilConfiguration.objects.get_or_create(entreprise=enterprise)
    # Global TVAs
    tvas = TvaConseil.objects.all().order_by('valeur')
    enterprises = Entreprise.objects.all()
    
    if request.method == "POST":
        action = request.POST.get('action')
        
        if action == 'save_config' or not action: # Default fallback if action missing
            try:
                config.default_tva_percent = request.POST.get('default_tva_percent') or 19.00
                config.show_tva_on_devis = request.POST.get('show_tva_on_devis') == 'on'
                config.show_tva_on_facture = request.POST.get('show_tva_on_facture') == 'on'
                
                config.enable_remise_global = request.POST.get('enable_remise_global') == 'on'
                config.default_remise_percent = request.POST.get('default_remise_percent') or 0.00
                config.show_remise_on_devis = request.POST.get('show_remise_on_devis') == 'on'
                config.show_remise_on_facture = request.POST.get('show_remise_on_facture') == 'on'
                
                # Numbering Configuration
                config.devis_prefix = request.POST.get('devis_prefix', 'DEV')
                config.devis_counter_width = request.POST.get('devis_counter_width') or 4
                config.facture_prefix = request.POST.get('facture_prefix', 'FAC')
                config.facture_counter_width = request.POST.get('facture_counter_width') or 4
                
                config.default_conditions_commerciales = request.POST.get('default_conditions_commerciales', '')
                config.payment_methods = request.POST.get('payment_methods', '')
                
                # Stamp Duty Configuration
                config.enable_stamp_duty = request.POST.get('enable_stamp_duty') == 'on'
                config.stamp_duty_rate = request.POST.get('stamp_duty_rate') or 1.00
                config.stamp_duty_min = request.POST.get('stamp_duty_min') or 5.00
                config.stamp_duty_max = request.POST.get('stamp_duty_max') or 10000.00
                config.apply_stamp_duty_on_cash_only = request.POST.get('apply_stamp_duty_on_cash_only') == 'on'
                
                config.save()
                messages.success(request, "Configuration mise Ã  jour avec succÃ¨s.")
            except Exception as e:
                messages.error(request, f"Erreur lors de la mise Ã  jour : {e}")
                
        elif action == 'add_tva':
            label = request.POST.get('tva_label')
            valeur = request.POST.get('tva_valeur')
            if label and valeur:
                try:
                    TvaConseil.objects.create(label=label, valeur=valeur)
                    messages.success(request, f"TVA '{label}' ajoutÃ©e avec succÃ¨s.")
                except Exception as e:
                    messages.error(request, f"Erreur : {e}")
            else:
                messages.warning(request, "Veuillez remplir le libellÃ© et la valeur.")
                
        elif action == 'delete_tva':
            tva_id = request.POST.get('tva_id')
            if tva_id:
                TvaConseil.objects.filter(id=tva_id).delete()
                messages.success(request, "TVA supprimÃ©e.")
            
        return redirect('t_conseil:ConfigurationConseil')

    context = {
        "tenant": request.tenant,
        "config": config,
        "tvas": tvas,
        "enterprises": enterprises,
        "current_enterprise": enterprise,
    }
    return render(request, 'tenant_folder/conseil/configuration.html', context)
@login_required(login_url="institut_app:login")
def DetailsFacture(request, pk):
    facture = get_object_or_404(Facture, num_facture=pk)
    lignes_facture = facture.lignes_facture.all()
    config = ConseilConfiguration.objects.filter(entreprise=facture.entreprise).first() if facture.entreprise else ConseilConfiguration.objects.filter(entreprise=None).first()
    
    total_ht = 0
    tva_breakdown = {}
    for l in lignes_facture:
        total_ht += float(l.montant_ht)
        if facture.show_tva:
            rate = float(l.tva_percent)
            amt = float(l.montant_ht) * (rate / 100)
            tva_breakdown[rate] = tva_breakdown.get(rate, 0) + amt
            
    total_tva = sum(tva_breakdown.values())
    total_ttc = total_ht + total_tva
    sorted_tva = sorted([{'rate': r, 'amount': a} for r, a in tva_breakdown.items()], key=lambda x: x['rate'], reverse=True)
    
    # Amount in words
    total_in_words = ""
    try:
        total_in_words = num_to_words_fr(total_ttc)
    except Exception as e:
        print(f"Error converting: {e}")

    context = {
        "tenant": request.tenant,
        "facture": facture,
        "lignes_facture": lignes_facture,
        "total_ht": total_ht,
        "total_tva": total_tva,
        "total_ttc": total_ttc,
        "tva_breakdown": sorted_tva,
        "total_in_words": total_in_words,
        "config": config,
    }
    return render(request, 'tenant_folder/conseil/details_facture.html', context)

@login_required(login_url="institut_app:login")
def AddNewFacture(request):
    if request.method == "POST":
        form = NewFactureForms(request.POST)
        if form.is_valid():
            facture = form.save()
            return redirect('t_conseil:configure-facture', pk=facture.num_facture)
    else:
        form = NewFactureForms()
    
    context = {
        "tenant": request.tenant,
        "form": form,
        "prospects": Prospets.objects.filter(context='con'),
        "enterprises": Entreprise.objects.all(),
    }
    return render(request, 'tenant_folder/conseil/nouveau-facture.html', context)

@login_required(login_url="institut_app:login")
def configure_facture(request, pk):
    facture = get_object_or_404(Facture, num_facture=pk)
    lignes_facture = facture.lignes_facture.all()
    
    # Get configuration for specific enterprise if set, otherwise first or default
    config = None
    if facture.entreprise:
        config = ConseilConfiguration.objects.filter(entreprise=facture.entreprise).first()
    
    if not config:
        config, _ = ConseilConfiguration.objects.get_or_create(entreprise=None)
        
    tvas = TvaConseil.objects.all().order_by('valeur')
    if facture.entreprise:
        tvas = tvas.filter(entreprise=facture.entreprise)
        
    # Check if we can edit
    can_edit = (facture.etat == 'brouillon')
    
    context = {
        "tenant": request.tenant,
        "facture": facture,
        "lignes_facture": lignes_facture,
        "config": config,
        "tvas": tvas,
        "enterprises": Entreprise.objects.all(),
        "can_edit": can_edit
    }
    return render(request, 'tenant_folder/conseil/configure-facture.html', context)

@login_required(login_url='institut_app:login')
@ajax_required
def ApiSaveFactureItems(request):
    import json
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        
    try:
        data = json.loads(request.body)
        facture_id = data.get('facture_id')
        items_data = data.get('items', [])
        show_tva = data.get('show_tva', False)
        show_remise = data.get('show_remise', False)
        entreprise_id = data.get('entreprise_id')
        conditions = data.get('conditions_commerciales', '')
        mode_paiement = data.get('mode_paiement', 'virement')
        date_emission = data.get('date_emission')
        date_echeance = data.get('date_echeance')
        
        facture = Facture.objects.get(num_facture=facture_id)
        
        if facture.etat != 'brouillon':
            return JsonResponse({'status': 'error', 'message': 'Modification impossible : la facture n\'est plus en brouillon.'})

        # Update global fields
        facture.show_tva = show_tva
        facture.show_remise = show_remise
        facture.conditions_commerciales = conditions
        facture.mode_paiement = mode_paiement
        
        if date_emission:
            facture.date_emission = date_emission
        if date_echeance:
            facture.date_echeance = date_echeance
            
        if entreprise_id:
            facture.entreprise = Entreprise.objects.get(id=entreprise_id)
        facture.save()
        
        # Clear existing items and recreate
        facture.lignes_facture.all().delete()
        
        total_ttc = 0
        total_ht = 0
        
        for item in items_data:
            t_id = item.get('thematique_id')
            description = item.get('description', '')
            long_description = item.get('long_description', '')
            qty = float(item.get('quantity', 0))
            unit_price = float(item.get('unitPrice', 0))
            remise_percent = float(item.get('remise_percent', 0))
            tva_percent = float(item.get('tva_percent', 0))
            
            thematique = None
            if t_id:
                thematique = Thematiques.objects.get(id=t_id)
                
            montant_ht = (qty * unit_price) * (1 - (remise_percent / 100))
            tva_amount = montant_ht * (tva_percent / 100)
            
            LignesFacture.objects.create(
                facture=facture,
                thematique=thematique,
                description=description,
                long_description=long_description,
                quantite=qty,
                montant_ht=montant_ht,
                remise_percent=remise_percent,
                tva_percent=tva_percent
            )
            
            total_ht += montant_ht
            total_ttc += (montant_ht + tva_amount)
            
        facture.total_ttc = total_ttc
        facture.save()
        
        return JsonResponse({'status': 'success', 'message': 'Facture enregistrÃ©e avec succÃ¨s.'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url='institut_app:login')
def ApiValidateFacture(request):
    if request.method == 'POST':
        facture_id = request.POST.get('facture_id')
        try:
            facture = Facture.objects.get(num_facture=facture_id)
            
            # Update Facture Status to 'En attente de paiement'
            facture.etat = 'battente'
            facture.save()
            
            # Update Related Prospect Pipeline Stage
            if facture.client:
                facture.client.conseil_pipeline_stage = 'recouvrement'
                facture.client.save()

            # Update Linked Opportunity Stage to 'recouvrement'
            if facture.devis_source and hasattr(facture.devis_source, 'opportunite'):
                opp = facture.devis_source.opportunite
                if opp:
                    opp.stage = 'recouvrement'
                    opp.save()
            
            return JsonResponse({'status': 'success', 'message': 'Facture validÃ©e et en attente de paiement.'})
        except Facture.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Facture non trouvÃ©e.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='institut_app:login')
def ApiRevertFactureToDraft(request):
    if request.method == 'POST':
        facture_id = request.POST.get('facture_id')
        try:
            facture = Facture.objects.get(num_facture=facture_id)
            facture.etat = 'brouillon'
            facture.save()
            return JsonResponse({'status': 'success', 'message': 'Facture repassÃ©e en brouillon.'})
        except Facture.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Facture non trouvÃ©e.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='institut_app:login')
@ajax_required
def ApiDeleteFacture(request):
    facture_id = request.POST.get('facture_id')
    try:
        facture = Facture.objects.get(num_facture=facture_id)
        if facture.etat != 'brouillon':
            return JsonResponse({'status': 'error', 'message': 'Seules les factures en brouillon peuvent Ãªtre supprimÃ©es.'})
        facture.delete()
        return JsonResponse({'status': 'success', 'message': 'Facture supprimÃ©e avec succÃ¨s.'})
    except Facture.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Facture non trouvÃ©e.'})

@ajax_required
def ApiFetchEnterpriseTvas(request):
    enterprise_id = request.GET.get('enterprise_id')
    if not enterprise_id:
        return JsonResponse({'status': 'error', 'message': 'ID Entreprise manquant.'})
    
    tvas = TvaConseil.objects.all().values('valeur', 'label', 'is_default')
    return JsonResponse({'status': 'success', 'tvas': list(tvas)})


@login_required(login_url='institut_app:login')
def ListeDAS(request):
    """
    Renders the page to manage DAS mappings (Products/Services to PaymentCategory).
    """
    context = {
        'tenant': request.tenant,
        'mappings': DASMapping.objects.all().select_related('thematique', 'payment_category'),
        'thematiques': Thematiques.objects.filter(etat='active'),
        'payment_categories': PaymentCategory.objects.all(),
    }
    return render(request, 'tenant_folder/conseil/liste_das.html', context)


@login_required(login_url='institut_app:login')
@ajax_required
def ApiSaveDAS(request):
    """
    API to create or update a DAS mapping.
    """
    if request.method == "POST":
        das_id = request.POST.get('das_id')
        designation = request.POST.get('designation')
        thematique_id = request.POST.get('thematique_id')
        category_id = request.POST.get('category_id')

        if not designation or not thematique_id or not category_id:
            return JsonResponse({'status': 'error', 'message': 'Tous les champs sont obligatoires.'})

        try:
            thematique = Thematiques.objects.get(id=thematique_id)
            category = PaymentCategory.objects.get(id=category_id)

            if das_id:
                mapping = DASMapping.objects.get(id=das_id)
                mapping.designation = designation
                mapping.thematique = thematique
                mapping.payment_category = category
                mapping.save()
                message = "Mapping DAS mis Ã  jour avec succÃ¨s."
            else:
                DASMapping.objects.create(
                    designation=designation,
                    thematique=thematique,
                    payment_category=category
                )
                message = "Nouveau mapping DAS crÃ©Ã© avec succÃ¨s."

            return JsonResponse({'status': 'success', 'message': message})

        except (Thematiques.DoesNotExist, PaymentCategory.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Produit ou catÃ©gorie introuvable.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'MÃ©thode non autorisÃ©e.'})


@login_required(login_url='institut_app:login')
@ajax_required
def ApiDeleteDAS(request):
    """
    API to delete a DAS mapping.
    """
    if request.method == "POST":
        das_id = request.POST.get('das_id')
        try:
            mapping = DASMapping.objects.get(id=das_id)
            mapping.delete()
            return JsonResponse({'status': 'success', 'message': 'Mapping supprimÃ© avec succÃ¨s.'})
        except DASMapping.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Mapping introuvable.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'MÃ©thode non autorisÃ©e.'})

@login_required(login_url="institut_app:login")
def DownloadFacturePDF(request, pk):
    try:
        facture = get_object_or_404(Facture, num_facture=pk)
        lignes = facture.lignes_facture.all()
        
        # Calculate totals
        total_ht = sum(ligne.montant_ht for ligne in lignes)
        total_tva = sum(ligne.montant_ht * (ligne.tva_percent / 100) for ligne in lignes)
        total_ttc = total_ht + total_tva
        
        # Convert total to words
        amount_in_words = num_to_words_fr(float(total_ttc))
        
        # Logo URL for WeasyPrint
        logo_url = ""
        if facture.entreprise and facture.entreprise.logo:
            logo_url = request.build_absolute_uri(facture.entreprise.logo.url)
            
        context = {
            'facture': facture,
            'total_ht': total_ht,
            'total_tva': total_tva,
            'total_ttc': total_ttc,
            'amount_in_words': amount_in_words,
            'logo_url': logo_url,
        }
        
        html_string = render_to_string('pdf/facture_pdf.html', context)
        
        # Create PDF
        html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
        pdf = html.write_pdf()
        
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Facture_{facture.num_facture}.pdf"'
        return response
        
    except Exception as e:
        return HttpResponse(f"Erreur lors de la gÃ©nÃ©ration du PDF: {str(e)}", status=500)

@login_required(login_url="institut_app:login")
def ApiSaveParticipants(request):
    import json
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        devis_id = data.get('devis_id')
        facture_id = data.get('facture_id')
        participants = data.get('participants', [])
        
        devis = None
        if devis_id:
            devis = Devis.objects.get(num_devis=devis_id)
        
        facture = None
        if facture_id:
            facture = Facture.objects.get(num_facture=facture_id)
            
        # Full sync: delete existing for this doc and re-add
        from django.db import transaction
        with transaction.atomic():
            if devis:
                Participant.objects.filter(devis=devis).delete()
            if facture:
                Participant.objects.filter(facture=facture).delete()
                
            for p in participants:
                Participant.objects.create(
                    devis=devis,
                    facture=facture,
                    nom=p.get('nom'),
                    prenom=p.get('prenom'),
                    email=p.get('email'),
                    telephone=p.get('telephone'),
                    date_naissance=p.get('date_naissance') if p.get('date_naissance') else None,
                    lieu_naissance=p.get('lieu_naissance'),
                    poste=p.get('poste'),
                    nin=p.get('nin')
                )
            
        return JsonResponse({'status': 'success', 'message': 'Participants enregistrÃ©s avec succÃ¨s.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url="institut_app:login")
def ApiGetDegreeFormations(request):
    from t_formations.models import Specialites
    specialites = Specialites.objects.all().values('id', 'label', 'prix', 'code', 'created_at', 'formation__nom')
    return JsonResponse(list(specialites), safe=False)

@login_required(login_url='institut_app:login')
def ApiLoadDegreeFormationsList(request):
    from t_formations.models import Formation
    formations = Formation.objects.all().values('id', 'nom', 'description', 'prix_formation', 'code', 'date_creation')
    return JsonResponse(list(formations), safe=False)

@login_required(login_url='institut_app:login')
def ApiGetSpecialiteDetails(request):
    """
    Returns full details for a specific specialty, including associated modules.
    """
    spec_id = request.GET.get('id')
    if not spec_id:
        return JsonResponse({'status': 'error', 'message': 'Specialite ID required'}, status=400)
    
    from t_formations.models import Specialites, Modules
    try:
        spec = Specialites.objects.get(id=spec_id)
        
        # Fetch associated modules
        modules = Modules.objects.filter(specialite=spec, is_archived=False).values('id', 'code', 'label', 'coef', 'duree')
        
        data = {
            'id': spec.id,
            'label': spec.label,
            'code': spec.code,
            'prix': str(spec.prix),
            'prix_double': str(spec.prix_double_diplomation) if spec.prix_double_diplomation else None,
            'duree': spec.duree,
            'nb_semestre': spec.nb_semestre,
            'branche': spec.branche,
            'abr': spec.abr,
            'formation_nom': spec.formation.nom if spec.formation else '-',
            'nb_tranche': spec.nb_tranche,
            'condition_access': spec.condition_access,
            'etat': spec.get_etat_display() if hasattr(spec, 'get_etat_display') else spec.etat,
            'modules': list(modules)
        }
        return JsonResponse({'status': 'success', 'data': data})
    except Specialites.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'SpÃ©cialitÃ© introuvable'}, status=404)

@login_required(login_url="institut_app:login")
def ApiEnrollToGroup(request):
    from t_groupe.models import Groupe, GroupeLine
    from t_crm.models import Prospets
    import json
    
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        participant_id = data.get('participant_id') # From Participant model
        prospect_id = data.get('prospect_id') # From Prospets model
        groupe_id = data.get('groupe_id')
        
        groupe = Groupe.objects.get(id=groupe_id)
        
        prospect = None
        if prospect_id:
            prospect = Prospets.objects.get(id=prospect_id)
        elif participant_id:
            p = Participant.objects.get(id=participant_id)
            prospect = Prospets.objects.filter(nom=p.nom, prenom=p.prenom, email=p.email).first()
            if not prospect:
                prospect = Prospets.objects.create(
                    nom=p.nom,
                    prenom=p.prenom,
                    email=p.email,
                    telephone=p.telephone,
                    date_naissance=p.date_naissance,
                    lieu_naissance=p.lieu_naissance,
                    nin=p.nin,
                    type_prospect='particulier',
                    statut='convertit',
                    context='con'
                )
        
        if prospect:
            from django.db import transaction
            with transaction.atomic():
                if not GroupeLine.objects.filter(groupe=groupe, student=prospect).exists():
                    GroupeLine.objects.create(groupe=groupe, student=prospect)
                    prospect.statut = 'convertit'
                    prospect.save()
                    return JsonResponse({'status': 'success', 'message': f'{prospect.nom} {prospect.prenom} inscrit au groupe {groupe.nom} avec succÃ¨s.'})
                else:
                    return JsonResponse({'status': 'error', 'message': 'DÃ©jÃ  inscrit Ã  ce groupe.'})
        
        return JsonResponse({'status': 'error', 'message': 'Participant ou prospect introuvable.'})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url='institut_app:login')
@ajax_required
def ApiGetGroups(request):
    """
    Returns groups for a specific specialty.
    """
    specialite_id = request.GET.get('specialite_id')
    if not specialite_id:
        return JsonResponse({'status': 'error', 'message': 'Specialite ID required'}, status=400)
    
    from t_groupe.models import Groupe
    groups = Groupe.objects.filter(specialite_id=specialite_id).values('id', 'nom', 'promotion__label', 'etat')
    return JsonResponse({'status': 'success', 'groups': list(groups)})

@login_required(login_url="institut_app:login")
def ApiLoadProspectParticipants(request):
    prospect_id = request.GET.get('prospect_id')
    if not prospect_id:
        return JsonResponse({'status': 'error', 'message': 'Prospect ID required'}, status=400)
    
    participants = Participant.objects.filter(prospect_id=prospect_id).values(
        'id', 'nom', 'prenom', 'email', 'telephone', 'date_naissance', 'lieu_naissance', 'poste', 'nin'
    )
    return JsonResponse({'status': 'success', 'participants': list(participants)})

@login_required(login_url="institut_app:login")
@ajax_required
def ApiSaveParticipant(request):
    import json
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        p_id = data.get('id')
        prospect_id = data.get('prospect_id')
        
        if not prospect_id and not p_id:
            return JsonResponse({'status': 'error', 'message': 'Prospect ID required'}, status=400)
            
        if p_id:
            participant = Participant.objects.get(id=p_id)
        else:
            participant = Participant(prospect_id=prospect_id)
            
        participant.nom = data.get('nom')
        participant.prenom = data.get('prenom')
        participant.email = data.get('email')
        participant.telephone = data.get('telephone')
        participant.date_naissance = data.get('date_naissance') if data.get('date_naissance') else None
        participant.lieu_naissance = data.get('lieu_naissance')
        participant.poste = data.get('poste')
        participant.nin = data.get('nin')
        participant.save()
        
        return JsonResponse({'status': 'success', 'message': 'Participant enregistrÃ© avec succÃ¨s.', 'id': participant.id})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url="institut_app:login")
@ajax_required
def ApiDeleteParticipant(request):
    import json
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        p_id = data.get('id')
        if not p_id:
            return JsonResponse({'status': 'error', 'message': 'Participant ID required'}, status=400)
            
        Participant.objects.filter(id=p_id).delete()
        return JsonResponse({'status': 'success', 'message': 'Participant supprimÃ© avec succÃ¨s.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required(login_url='institut_app:login')
@ajax_required
def ApiSaveEtsDetails(request):
    if request.method == 'POST':
        prospect_id = request.POST.get('prospect_id')
        try:
            prospect = Prospets.objects.get(id=prospect_id)
            prospect.entreprise = request.POST.get('entreprise')
            prospect.rc = request.POST.get('rc')
            prospect.nif = request.POST.get('nif')
            prospect.nis = request.POST.get('nis')
            prospect.art_imp = request.POST.get('art_imp')
            prospect.observation = request.POST.get('observation')
            prospect.save()
            return JsonResponse({'status': 'success', 'message': 'Informations entreprise mises Ã  jour.'})
        except Prospets.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Prospect non trouvÃ©.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required(login_url='institut_app:login')
@ajax_required
def ApiLoadBankAccounts(request):
    prospect_id = request.GET.get('id_prospect')
    accounts = ProspectBankAccount.objects.filter(prospect_id=prospect_id).values(
        'id', 'bank_name', 'rib', 'swift', 'bank_address', 'is_active'
    )
    return JsonResponse(list(accounts), safe=False)

@login_required(login_url='institut_app:login')
@ajax_required
def ApiSaveBankAccount(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        prospect_id = request.POST.get('prospect_id')
        
        if account_id:
            account = ProspectBankAccount.objects.get(id=account_id)
        else:
            prospect = Prospets.objects.get(id=prospect_id)
            account = ProspectBankAccount(prospect=prospect)
            
        account.bank_name = request.POST.get('bank_name')
        account.rib = request.POST.get('rib')
        account.swift = request.POST.get('swift')
        account.bank_address = request.POST.get('bank_address')
        account.save()
        
        return JsonResponse({'status': 'success', 'message': 'Compte bancaire enregistrÃ©.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required(login_url='institut_app:login')
@ajax_required
def ApiDeleteBankAccount(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        try:
            account = ProspectBankAccount.objects.get(id=account_id)
            account.delete()
            return JsonResponse({'status': 'success', 'message': 'Compte bancaire supprimÃ©.'})
        except ProspectBankAccount.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Compte non trouvÃ©.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@login_required(login_url='institut_app:login')
def GroupedParticipants(request):
    """
    Displays participants grouped by their thematics from confirmed quotes.
    Handles both explicit Participant objects and individual Prospect clients.
    """
    from .models import Thematiques, Participant
    from t_formations.models import Specialites, Promos
    from t_crm.models import Prospets

    # Get active thematics
    thematiques = Thematiques.objects.filter(etat='active')
    
    grouped_data = []
    for th in thematiques:
        # 1. Explicit participants linked to confirmed quotes with this thematic
        participants_explicit = Participant.objects.filter(
            devis__lignes_devis__thematique=th,
            devis__etat='accepte'
        ).select_related('prospect', 'devis').distinct()
        
        # 2. Individual prospects who are clients of confirmed thematic quotes
        prospects_as_clients = Prospets.objects.filter(
            client_devis__lignes_devis__thematique=th,
            client_devis__etat='accepte',
            type_prospect='particulier'
        ).distinct()

        unified_participants = []
        seen_emails = set()

        # Add explicit participants
        for p in participants_explicit:
            p_data = {
                'id': p.id,
                'nom': p.nom,
                'prenom': p.prenom,
                'email': p.email,
                'telephone': p.telephone,
                'poste': p.poste,
                'prospect': p.prospect,
                'devis': p.devis,
                'is_prospect_direct': False
            }
            unified_participants.append(p_data)
            if p.email: seen_emails.add(p.email)

        # Add prospect clients if not already added
        for p in prospects_as_clients:
            if p.email and p.email in seen_emails:
                continue
            
            # Find the first accepted devis with this thematic for context
            devis = p.client_devis.filter(lignes_devis__thematique=th, etat='accepte').first()
            
            p_data = {
                'id': f"prospect_{p.id}",
                'nom': p.nom,
                'prenom': p.prenom,
                'email': p.email,
                'telephone': p.telephone,
                'poste': getattr(p, 'poste', '') or '',
                'prospect': p,
                'devis': devis,
                'is_prospect_direct': True
            }
            unified_participants.append(p_data)

        if unified_participants:
            grouped_data.append({
                'thematique': th,
                'participants': unified_participants
            })

    context = {
        'tenant': request.tenant,
        'grouped_data': grouped_data,
        'specialites': Specialites.objects.all(),
        'promos': Promos.objects.filter(etat='active'),
    }
    return render(request, 'tenant_folder/conseil/grouped_participants.html', context)


@login_required(login_url='institut_app:login')
@ajax_required
def ApiCreateGroupFromParticipants(request):
    """
    API to create a group in t_groupe from selected participants.
    Handles both Participant IDs and prospect IDs (prefixed with prospect_).
    """
    import json
    from t_groupe.models import Groupe, GroupeLine
    from t_crm.models import Prospets
    from t_formations.models import Thematiques, Promos
    from .models import Participant
    
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
        
    try:
        data = json.loads(request.body)
        participant_ids = data.get('participant_ids', [])
        group_name = data.get('group_name')
        thematique_id = data.get('thematique_id')
        promo_id = data.get('promo_id')
        
        if not group_name or not thematique_id:
            return JsonResponse({'status': 'error', 'message': 'Nom du groupe et thématique sont obligatoires.'}, status=400)
            
        # Create the group
        groupe = Groupe.objects.create(
            nom=group_name,
            thematique_id=thematique_id,
            promotion_id=promo_id,
            etat='brouillon',
        )
        
        count = 0
        for pid_str in participant_ids:
            try:
                student = None
                if str(pid_str).startswith('prospect_'):
                    prospect_id = pid_str.replace('prospect_', '')
                    student = Prospets.objects.get(id=prospect_id)
                else:
                    participant = Participant.objects.get(id=pid_str)
                    # Find or create a Prospets record for the individual participant
                    if participant.email:
                        student = Prospets.objects.filter(email=participant.email, is_ets_prospect=False).first()
                    
                    if not student:
                        student = Prospets.objects.create(
                            nom=participant.nom,
                            prenom=participant.prenom,
                            email=participant.email,
                            telephone=participant.telephone,
                            date_naissance=participant.date_naissance,
                            lieu_naissance=participant.lieu_naissance,
                            nin=participant.nin,
                            context='con',
                            is_ets_prospect=False,
                            type_prospect='particulier',
                            entreprise=participant.prospect.nom if participant.prospect else None,
                        )
                
                if student:
                    if not GroupeLine.objects.filter(groupe=groupe, student=student).exists():
                        GroupeLine.objects.create(groupe=groupe, student=student)
                        count += 1
            except Exception as e:
                print(f"Error adding participant {pid_str}: {e}")
                continue
        
        return JsonResponse({
            'status': 'success', 
            'message': f'Groupe "{group_name}" créé avec succès. {count} participants ajoutés.',
            'group_id': groupe.id
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url="institut_app:login")
def ApiAcceptDevis(request):
    if request.method == 'POST':
        devis_id = request.POST.get('devis_id')
        try:
            from .models import Devis
            devis = Devis.objects.get(num_devis=devis_id)
            devis.etat = 'accepte'
            devis.save()
            
            # Update CRM Pipeline Stage
            if devis.opportunite:
                devis.opportunite.stage = 'facture'
                devis.opportunite.save()
            
            return JsonResponse({'status': 'success', 'message': 'Le devis a été accepté avec succès.'})
        except Devis.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Devis introuvable.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Mauvaise méthode.'}, status=405)

@login_required(login_url="institut_app:login")
def ApiRejectDevis(request):
    if request.method == 'POST':
        devis_id = request.POST.get('devis_id')
        try:
            from .models import Devis
            devis = Devis.objects.get(num_devis=devis_id)
            devis.etat = 'rejete'
            devis.save()
            
            # Update CRM Pipeline Stage
            if devis.opportunite:
                devis.opportunite.stage = 'perdu'
                devis.opportunite.save()

            return JsonResponse({'status': 'success', 'message': 'Le devis a été rejeté.'})
        except Devis.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Devis introuvable.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Mauvaise méthode.'}, status=405)
