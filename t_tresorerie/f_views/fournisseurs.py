import json
from institut_app.decorators import module_permission_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from institut_app.models import Fournisseur  # Import the Fournisseur model from institut_app


@login_required(login_url='institut_app:login')
@module_permission_required('tre', 'view')
def PageFournisseur(request):
    return render(request,'tenant_folder/comptabilite/fournisseurs/liste_des_fournisseurs.html')

@login_required(login_url='institut_app:login')
@module_permission_required('tre', 'view')
def ApiListeFournisseurs(request):
    liste = Fournisseur.objects.all().values('id', 'designation','telephone','code','email')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url='institut_app:login')
@module_permission_required('tre', 'view')
def PageNouveauFournisseur(request):
    return render(request,'tenant_folder/comptabilite/fournisseurs/nouveau_fournisseur.html')

@login_required(login_url='institut_app:login')
@transaction.atomic
@module_permission_required('tre', 'view')
def enregistrer_fournisseur(request):
    try:
        designation = request.POST.get('designation', '').strip()
        adresse = request.POST.get('adresse', '').strip()
        commune = request.POST.get('commune', '').strip()
        wilaya = request.POST.get('wilaya', '').strip()
        pays = request.POST.get('pays', '').strip()
        rc = request.POST.get('rc', '').strip()
        nif = request.POST.get('nif', '').strip()
        art = request.POST.get('art_impot', '').strip()
        nis = request.POST.get('nis', '').strip()
        code = request.POST.get('code','').strip()
        telephone = request.POST.get('telephone','').strip()
        email = request.POST.get('email','').strip()
        site_web = request.POST.get('site_web','').strip()

        fournisseur = Fournisseur.objects.create(
            designation=designation,
            adresse=adresse,
            commune=commune,
            wilaya=wilaya,
            pays=pays,
            rc=rc,
            nif=nif,
            art=art,
            nis=nis,
            code = code,
            telephone = telephone,
            email = email,
            site_web = site_web
        )
        return JsonResponse({"status": "success","message": "Le fournisseur a été enregistré avec succès.", "id": fournisseur.id})
    except Exception as e:
        return JsonResponse({"status": "error", "message": f"Erreur lors de l'enregistrement du fournisseur : {str(e)}"}, status=500)

@login_required(login_url='institut_app:login')
@module_permission_required('tre', 'view')
def PageDetailsFournisseur(request, pk):
    if not pk:
        return redirect('t_tresorerie:PageFournisseur')
    
    fournisseur = Fournisseur.objects.get(id = pk)
    depenses = Depenses.objects.filter(fournisseur=fournisseur).order_by('-created_at')
    
    total_achete = sum(d.montant_ttc for d in depenses if d.montant_ttc)
    
    reglements = ReglementFournisseur.objects.filter(fournisseur=fournisseur)
    total_paye = sum(r.total_paye for r in reglements if r.total_paye)
    
    anciennes_sans_reglement = depenses.filter(etat=True).filter(reglements__isnull=True)
    total_paye += sum(d.montant_ttc for d in anciennes_sans_reglement if d.montant_ttc)
    
    total_reste = total_achete - total_paye
    
    context = {
        'fournisseur' : fournisseur,
        'depenses' : depenses,
        'total_achete': total_achete,
        'total_paye': total_paye,
        'total_reste': total_reste
    }
    return render(request, 'tenant_folder/comptabilite/fournisseurs/details_fournisseur.html',context)

@login_required(login_url='institut_app:login')
@module_permission_required('tre', 'view')
def ApiLoadFournisseur(request):
    if request.method == "GET":
        liste = Fournisseur.objects.all().values('id','designation')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error","message":"méthode non autorisée"})

@login_required(login_url='institut_app:login')
@transaction.atomic
@module_permission_required('tre', 'change')
def UpdateFournisseur(request):
    if request.method =="POST":
        id = request.POST.get('id')
        code = request.POST.get('code')
        designation = request.POST.get('designation')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        adresse = request.POST.get('adresse')
        commune = request.POST.get('commune')
        wilaya = request.POST.get('wilaya')
        pays = request.POST.get('pays')
        rc = request.POST.get('rc')
        nif = request.POST.get('nif')
        art = request.POST.get('art')
        nis = request.POST.get('nis')
        banque = request.POST.get('banque')
        num_compte = request.POST.get('num_compte')
        code_banque = request.POST.get('code_banque')
        observation = request.POST.get('observation')
        site_web = request.POST.get('site_web')

        fournisseur = Fournisseur.objects.get(id = id)
        
        fournisseur.code = code
        fournisseur.designation = designation
        fournisseur.telephone = telephone
        fournisseur.adresse = adresse
        fournisseur.commune = commune
        fournisseur.wilaya = wilaya
        fournisseur.pays = pays
        fournisseur.rc = rc
        fournisseur.nif = nif
        fournisseur.art = art
        fournisseur.nis = nis
        fournisseur.banque = banque
        fournisseur.num_compte = num_compte
        fournisseur.code_banque = code_banque
        fournisseur.observation = observation
        fournisseur.email = email
        fournisseur.site_web = site_web

        fournisseur.save()
        messages.success(request, "Les informations du fournisseur ont été modifiées.")
        return JsonResponse({"status":"success"})

    else:
        return JsonResponse({"status":"error","message":"methode non autoriser"})

# --- NOUVELLES APIS POUR REGLEMENTS ET CHEQUES ---

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'add')
def ApiCreerReglementFournisseur(request):
    if request.method == "POST":
        try:
            fournisseur_id = request.POST.get('fournisseur_id')
            date_reglement = request.POST.get('date_reglement')
            observation = request.POST.get('observation', '')
            reference = request.POST.get('reference', '')
            
            depenses_data = json.loads(request.POST.get('depenses', '[]'))
            paiements_data = json.loads(request.POST.get('paiements', '[]'))
            
            if not fournisseur_id or not date_reglement or not depenses_data or not paiements_data:
                return JsonResponse({"status": "error", "message": "Données incomplètes."})
                
            fournisseur = Fournisseur.objects.get(id=fournisseur_id)
            
            total_paye = sum([Decimal(str(p['montant'])) for p in paiements_data])
            
            reglement = ReglementFournisseur.objects.create(
                fournisseur=fournisseur,
                date_reglement=date_reglement,
                reference=reference,
                observation=observation,
                total_paye=total_paye
            )
            
            # Affecter les montants aux dépenses
            for d_data in depenses_data:
                depense = Depenses.objects.get(id=d_data['id'])
                montant_affecte = Decimal(str(d_data['montant']))
                
                ReglementDepense.objects.create(
                    reglement=reglement,
                    depense=depense,
                    montant_affecte=montant_affecte
                )
                
                # Check if expense is fully paid to mark it etat=True
                # But actually, the total paid on an expense is the sum of all its ReglementDepense
                total_affecte = sum([rd.montant_affecte for rd in depense.reglements.all()])
                if total_affecte >= depense.montant_ttc:
                    depense.etat = True
                    # Let's keep date_paiement as the last payment date
                    depense.date_paiement = date_reglement
                    depense.save()
                    
            # Créer les modes de paiement
            for p_data in paiements_data:
                mode = p_data['mode_paiement']
                pm = PaiementFournisseurMode.objects.create(
                    reglement=reglement,
                    mode_paiement=mode,
                    montant=Decimal(str(p_data['montant'])),
                    banque=p_data.get('banque', ''),
                    reference_paiement=p_data.get('reference_paiement', '')
                )
                
                if mode == 'che':
                    pm.etat_cheque = 'emis'
                    pm.date_emission = date_reglement
                    pm.save()
                    
            return JsonResponse({"status": "success", "message": "Le règlement a été enregistré avec succès."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée."})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetReglementsFournisseur(request):
    fournisseur_id = request.GET.get('fournisseur_id')
    if not fournisseur_id:
        return JsonResponse({"status": "error"})
        
    reglements = ReglementFournisseur.objects.filter(fournisseur_id=fournisseur_id).order_by('-date_reglement', '-id')
    
    data = []
    for r in reglements:
        depenses_affectees = [f"{rd.depense.reference_document or rd.depense.label} ({rd.montant_affecte} DA)" for rd in r.depenses_payees.all()]
        modes_paiement = []
        for m in r.modes_paiement.all():
            modes_paiement.append({
                'id': m.id,
                'mode': m.get_mode_paiement_display(),
                'mode_code': m.mode_paiement,
                'montant': str(m.montant),
                'banque': m.banque,
                'reference': m.reference_paiement,
                'etat_cheque': m.get_etat_cheque_display(),
                'etat_cheque_code': m.etat_cheque,
                'dates_cheque': {
                    'emis': m.date_emission.strftime('%d/%m/%Y') if m.date_emission else None,
                    'signature': m.date_signature.strftime('%d/%m/%Y') if m.date_signature else None,
                    'remis': m.date_remise.strftime('%d/%m/%Y') if m.date_remise else None,
                    'decaisse': m.date_encaissement.strftime('%d/%m/%Y') if m.date_encaissement else None,
                }
            })
            
        data.append({
            'id': r.id,
            'date': r.date_reglement,
            'reference': r.reference,
            'total': str(r.total_paye),
            'depenses': depenses_affectees,
            'modes': modes_paiement
        })
        
    return JsonResponse(data, safe=False)

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiUpdateChequeStatus(request):
    if request.method == "POST":
        try:
            mode_id = request.POST.get('mode_id')
            new_status = request.POST.get('etat_cheque')
            status_date = request.POST.get('date_status')
            
            pm = PaiementFournisseurMode.objects.get(id=mode_id, mode_paiement='che')
            
            pm.etat_cheque = new_status
            if new_status == 'signature':
                pm.date_signature = status_date
            elif new_status == 'remis':
                pm.date_remise = status_date
            elif new_status == 'decaisse':
                pm.date_encaissement = status_date
            
            pm.save()
            return JsonResponse({"status": "success", "message": "Le statut du chèque a été mis à jour."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Méthode non autorisée."})
