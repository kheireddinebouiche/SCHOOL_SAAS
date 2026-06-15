from institut_app.decorators import module_permission_required
from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PageDepenses(request):
    return render(request,'tenant_folder/comptabilite/depenses/liste_des_depenses.html')

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiListeDepenses(request):
    liste = Depenses.objects.all().values('id','label','montant_ht','tva','montant_ttc','date_paiement','client__prenom','client__nom','fournisseur__designation','etat','created_at', 'mode_paiement', 'entite__id', 'entite__designation', 'reference', 'reference_document').order_by('-id')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadEntites(request):
    if request.method == "GET":
        # Fetch all enterprises/entities
        # You might want to filter this based on user permissions if necessary
        entites = Entreprise.objects.all().values('id', 'designation', 'entite_afficher')
        return JsonResponse(list(entites), safe=False)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PageNouvelleDepense(request):
    entites = Entreprise.objects.all()
    return render(request, "tenant_folder/comptabilite/depenses/nouvelle_depense.html", {'entites': entites})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadTypeDepense(request):
    if request.method == 'GET':
        types = TypeDepense.objects.all()
        data = []
        for t in types:
           
            sous_types = SousTypeDepense.objects.filter(type=t).values(
                'id', 'label', 'description',
            )

            data.append({
                'id': t.id,
                'label': t.label,
                'description': t.description,
                'created_at': t.created_at,
                'sous_types': list(sous_types)  # ajoute les sous-types
            })

        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status":"error",'message':'methode non autoriser'})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'add')
def ApiStoreNewType(request):
    if request.method == "POST":
        typeName = request.POST.get('typeName')
        typeDescription = request.POST.get('typeDescription')
        typeCategory = request.POST.get('typeCategory')

        ##Crée une catégorie et sous-catégorie
        if typeCategory != "":
            SousTypeDepense.objects.create(
                type = TypeDepense.objects.get(id = typeCategory),
                label = typeName,
            )
            return JsonResponse({"status":"success",'message':"La catégorie et sous-catégorie ont été crée avec succès"})
        

        TypeDepense.objects.create(
            label = typeName,
            description = typeDescription,
        )
        return JsonResponse({"status":"success",'message':"La catégorie a été crée avec succès"})

    else:
        return JsonResponse({"status":"error",'message':"methode non autoriser"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'add')
def ApiAddCategorieComptable(request):
    if request.method == "POST":
        label = request.POST.get('label')
        categorie = TypeDepense.objects.create(
            label = label
        )
        return JsonResponse({
            "status": "success",
            "message": "Créé avec succès",
            "category": {
                "id": categorie.id,
                "label": categorie.label
            }
        })
    else:
        return JsonResponse({"status":"error",'message':"methode non autoriser"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiLoadCategories(request):
    liste = TypeDepense.objects.all().values('id','label')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetCategorie(request):
    if request.method == "GET":
        liste = TypeDepense.objects.all().values('id','label')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiFilterSousCategrorie(request):
    if request.method == "GET":
        option = request.GET.get('option')
        liste=SousTypeDepense.objects.filter(type_id = option).values('id','label','type__id')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error"})

import json
from django.shortcuts import render, get_object_or_404

@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def PageDetailDepense(request, id):
    depense = get_object_or_404(Depenses, id=id)
    lignes = DepenseLigne.objects.filter(depense=depense)
    return render(request, "tenant_folder/comptabilite/depenses/details_depense.html", {
        'depense': depense,
        'lignes': lignes
    })

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'add')
def ApiStoreDepense(request):
    if request.method == "POST":
        label = request.POST.get('label')
        fournisseur = request.POST.get('fournisseur')
        date = request.POST.get('date_depense')
        piece = request.FILES.get('piece')
        description = request.POST.get('description')
        mode_paiement = request.POST.get('mode_paiement')
        reference_paiement = request.POST.get('reference_paiement')
        reference_document = request.POST.get('reference_document')
        entite_id = request.POST.get('entite')

        lignes_json = request.POST.get('lignes')
        lignes = []
        if lignes_json:
            try:
                lignes = json.loads(lignes_json)
            except:
                pass

        total_ht = Decimal('0.00')
        total_tva = Decimal('0.00')
        total_ttc = Decimal('0.00')
        
        for ligne in lignes:
            qte = Decimal(str(ligne.get('quantite', 1)))
            pu_ht = Decimal(str(ligne.get('prix_unitaire_ht', 0)))
            tva_rate = Decimal(str(ligne.get('tva', 0)))
            
            l_ht = qte * pu_ht
            l_tva = l_ht * (tva_rate / Decimal('100.00'))
            l_ttc = l_ht + l_tva
            
            total_ht += l_ht
            total_tva += l_tva
            total_ttc += l_ttc

        # Calcul Timbre
        timbre_val = Decimal('0.00')
        if mode_paiement == 'esp':
            param = ParametreFinancier.get_instance()
            if param.activer_timbre and param.timbre_cash_only:
                timbre_calc = total_ttc * (param.taux_timbre / Decimal('100.00'))
                if timbre_calc < param.timbre_min:
                    timbre_val = param.timbre_min
                elif timbre_calc > param.timbre_max:
                    timbre_val = param.timbre_max
                else:
                    timbre_val = timbre_calc

        depense = Depenses.objects.create(
            label=label,
            fournisseur_id=fournisseur,
            date_depense=date,
            montant_ht=total_ht,
            tva=str(total_tva), # Conserver pour la compatibilité
            montant_ttc=total_ttc,
            timbre=timbre_val,
            piece=piece,
            description=description,
            mode_paiement=mode_paiement,
            reference=reference_paiement,
            reference_document=reference_document,
            entite_id=entite_id
        )

        for ligne in lignes:
            qte = Decimal(str(ligne.get('quantite', 1)))
            pu_ht = Decimal(str(ligne.get('prix_unitaire_ht', 0)))
            tva_rate = Decimal(str(ligne.get('tva', 0)))
            
            l_ht = qte * pu_ht
            l_tva = l_ht * (tva_rate / Decimal('100.00'))
            l_ttc = l_ht + l_tva

            cat_id = ligne.get('category')
            if cat_id == '0' or cat_id == '':
                cat_id = None

            DepenseLigne.objects.create(
                depense=depense,
                designation=ligne.get('designation', 'Ligne'),
                category_id=cat_id,
                quantite=qte,
                prix_unitaire_ht=pu_ht,
                tva=tva_rate,
                montant_ht=l_ht,
                montant_tva=l_tva,
                montant_ttc=l_ttc
            )

        messages.success(request, 'Les informations ont été enregistrer avec succès')
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"error"})
    
@login_required(login_url="institut_app:login")
@module_permission_required('tre', 'view')
def ApiGetDepenseDetails(request):
    if request.method == "GET":
        id = request.GET.get('id')
        obj = Depenses.objects.get(id = id)
        
        lignes = []
        for l in obj.lignes.all():
            lignes.append({
                'id': l.id,
                'designation': l.designation,
                'category': l.category.id if l.category else '',
                'category_name': l.category.name if l.category else '',
                'quantite': str(l.quantite),
                'prix_unitaire_ht': str(l.prix_unitaire_ht),
                'tva': str(l.tva),
                'montant_ht': str(l.montant_ht),
                'montant_tva': str(l.montant_tva),
                'montant_ttc': str(l.montant_ttc),
            })

        data = {
            'id' : obj.id,
            'label' : obj.label,
            'fournisseur' : obj.fournisseur.id if obj.fournisseur else None,
            'fournisseur_designation' : obj.fournisseur.designation if obj.fournisseur else None,
            'client_nom' : obj.client.nom if obj.client else None,
            'client_prenom' : obj.client.prenom if obj.client else None,
            'date' : obj.date_depense,
            'date_paiement' : obj.date_paiement,
            'montant_ht': obj.montant_ht,
            'montant_ttc' : obj.montant_ttc,
            'timbre': obj.timbre,
            'piece' : obj.piece.url if obj.piece else None,
            'description' : obj.description,
            'reference_document': obj.reference_document,
            'tva'  : obj.tva,
            'entite' : obj.entite.id if obj.entite else None,
            'mode_paiement' : obj.mode_paiement,
            'reference' : obj.reference,
            'etat': obj.etat,
            'lignes': lignes
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"status":"error"})
    
@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'change')
def ApiUpdateDepense(request):
    if request.method == "POST":
        id = request.POST.get('id')
        edit_label = request.POST.get('edit_label')
        edit_fournisseur = request.POST.get('edit_fournisseur')
        edit_date = request.POST.get('edit_date')
        edit_description = request.POST.get('edit_description')
        edit_piece = request.FILES.get('edit_piece')
        edit_entite = request.POST.get('edit_entite')
        edit_mode_paiement = request.POST.get('edit_mode_paiement')
        edit_reference = request.POST.get('edit_reference')
        edit_reference_document = request.POST.get('edit_reference_document')
        obj = Depenses.objects.get(id = id)
             
        lignes_json = request.POST.get('edit_lignes')
        lignes = []
        if lignes_json:
            try:
                lignes = json.loads(lignes_json)
            except:
                pass

        total_ht = Decimal('0.00')
        total_tva = Decimal('0.00')
        total_ttc = Decimal('0.00')
        
        # Calculate totals from lignes
        for ligne in lignes:
            qte = Decimal(str(ligne.get('quantite', 1)))
            pu_ht = Decimal(str(ligne.get('prix_unitaire_ht', 0)))
            tva_rate = Decimal(str(ligne.get('tva', 0)))
            
            l_ht = qte * pu_ht
            l_tva = l_ht * (tva_rate / Decimal('100.00'))
            l_ttc = l_ht + l_tva
            
            total_ht += l_ht
            total_tva += l_tva
            total_ttc += l_ttc

        # Recalcul Timbre
        timbre_val = Decimal('0.00')
        if edit_mode_paiement == 'esp':
            param = ParametreFinancier.get_instance()
            if param.activer_timbre and param.timbre_cash_only:
                timbre_calc = total_ttc * (param.taux_timbre / Decimal('100.00'))
                if timbre_calc < param.timbre_min:
                    timbre_val = param.timbre_min
                elif timbre_calc > param.timbre_max:
                    timbre_val = param.timbre_max
                else:
                    timbre_val = timbre_calc
        
        obj.label = edit_label
        obj.fournisseur_id = edit_fournisseur
        obj.date_depense = edit_date
        obj.montant_ht = total_ht
        obj.tva = str(total_tva)
        obj.montant_ttc = total_ttc
        obj.timbre = timbre_val
        if edit_piece:
            obj.piece = edit_piece
        obj.reference_document = edit_reference_document
        obj.description = edit_description
        obj.entite_id = edit_entite
        if edit_mode_paiement:
            obj.mode_paiement = edit_mode_paiement
        obj.reference = edit_reference

        obj.save()
        
        # Sync Lignes
        # Delete existing lignes and recreate for simplicity, or sync
        # Here we just delete and recreate
        obj.lignes.all().delete()
        for ligne in lignes:
            qte = Decimal(str(ligne.get('quantite', 1)))
            pu_ht = Decimal(str(ligne.get('prix_unitaire_ht', 0)))
            tva_rate = Decimal(str(ligne.get('tva', 0)))
            
            l_ht = qte * pu_ht
            l_tva = l_ht * (tva_rate / Decimal('100.00'))
            l_ttc = l_ht + l_tva

            cat_id = ligne.get('category')
            if cat_id == '0' or cat_id == '':
                cat_id = None

            DepenseLigne.objects.create(
                depense=obj,
                designation=ligne.get('designation', 'Ligne'),
                category_id=cat_id,
                quantite=qte,
                prix_unitaire_ht=pu_ht,
                tva=tva_rate,
                montant_ht=l_ht,
                montant_tva=l_tva,
                montant_ttc=l_ttc
            )
        
        # Update OperationsBancaire if it exists
        from t_tresorerie.models import OperationsBancaire
        op = OperationsBancaire.objects.filter(depense=obj).first()
        if op:
            if obj.mode_paiement in ['che', 'vir']:
                op.montant = obj.montant_ttc # or ttc + timbre depending on logic. Bank is usually just TTC
                op.reference_bancaire = obj.reference
                op.save()
            else:
                # If mode_paiement changed to something else (e.g. esp), delete the bank operation
                op.delete()

        return JsonResponse({"status":"success"})

    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'approuv')
def ApiValidateDepense(request):
    if request.method == "GET":
        id = request.GET.get('id')
        obj = Depenses.objects.get(id = id)
        obj.etat = True
        obj.save()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"error"})


@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'delete')
def ApiDeleteDepense(request):
    if request.method == "GET":
        id = request.GET.get('id')
        obj = Depenses.objects.get(id = id)
        obj.delete()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
@module_permission_required('tre', 'view')
def ApiRecordExpensePayment(request):
    if request.method == "POST":
        try:
            id = request.POST.get('id')
            payment_date = request.POST.get('payment_date')
            payment_mode = request.POST.get('payment_mode')
            payment_reference = request.POST.get('payment_reference')
            
            if not id or not payment_date:
                return JsonResponse({"status":"error", "message":"ID et date de paiement requis"})
            
            obj = Depenses.objects.get(id=id)
            obj.date_paiement = payment_date
            if payment_mode:
                obj.mode_paiement = payment_mode
            if payment_reference is not None:
                obj.reference = payment_reference
                
            obj.etat = True  # Mark as validated when payment is recorded
            obj.save()
            
            # Ensure OperationsBancaire exists for bank payments so it shows up in Imputation Bancaire
            if obj.mode_paiement in ['che', 'vir']:
                from t_tresorerie.models import OperationsBancaire
                op, created = OperationsBancaire.objects.get_or_create(
                    operation_type="sortie",
                    depense=obj,
                    defaults={
                        'montant': obj.montant_ttc,
                        'reference_bancaire': obj.reference,
                        'date_operation': payment_date
                    }
                )
                if not created:
                    op.montant = obj.montant_ttc
                    op.reference_bancaire = obj.reference
                    op.date_operation = payment_date
                    op.save()
            else:
                # If changed to esp and a bank operation existed, remove it
                from t_tresorerie.models import OperationsBancaire
                OperationsBancaire.objects.filter(operation_type="sortie", depense=obj).delete()
            
            return JsonResponse({"status":"success", "message":"Paiement enregistré avec succès"})
        except Depenses.DoesNotExist:
            return JsonResponse({"status":"error", "message":"Dépense introuvable"})
        except Exception as e:
            return JsonResponse({"status":"error", "message":str(e)})
    else:
        return JsonResponse({"status":"error", "message":"Méthode non autorisée"})