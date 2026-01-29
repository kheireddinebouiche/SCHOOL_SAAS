from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required(login_url="institut_app:login")
def PageDepenses(request):
    return render(request,'tenant_folder/comptabilite/depenses/liste_des_depenses.html')

@login_required(login_url="institut_app:ApiListeDepenses")
def ApiListeDepenses(request):
    liste = Depenses.objects.all().values('id','label', 'category__name', 'category__parent__name','montant_ht','tva','date_paiement','client__prenom','client__nom','fournisseur__designation','etat','created_at', 'mode_paiement', 'entite__id', 'entite__designation').order_by('-id')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def ApiLoadEntites(request):
    if request.method == "GET":
        # Fetch all enterprises/entities
        # You might want to filter this based on user permissions if necessary
        entites = Entreprise.objects.all().values('id', 'designation', 'entite_afficher')
        return JsonResponse(list(entites), safe=False)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed"})

@login_required(login_url="institut_app:login")
def PageNouvelleDepense(request):
    return render(request, "tenant_folder/comptabilite/depenses/nouvelle_depense.html")

@login_required(login_url="institut_app:login")
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
def ApiLoadCategories(request):
    liste = TypeDepense.objects.all().values('id','label')
    return JsonResponse(list(liste), safe=False)

@login_required(login_url="institut_app:login")
def ApiGetCategorie(request):
    if request.method == "GET":
        liste = TypeDepense.objects.all().values('id','label')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def ApiFilterSousCategrorie(request):
    if request.method == "GET":
        option = request.GET.get('option')
        liste=SousTypeDepense.objects.filter(type_id = option).values('id','label','type__id')
        return JsonResponse(list(liste), safe=False)
    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="insitut_app:login")
@transaction.atomic
def ApiStoreDepense(request):
    if request.method == "POST":
        label = request.POST.get('label')
        fournisseur = request.POST.get('fournisseur')
        date = request.POST.get('date_depense')
        montant_ht = request.POST.get('montant_ht')
        tva = request.POST.get('tva')
        montant_ttc = request.POST.get('montant_ttc')
        piece = request.FILES.get('piece')
        description = request.POST.get('description')
        mode_paiement = request.POST.get('mode_paiement')
        reference_paiement = request.POST.get('reference_paiement')

        categoryId = request.POST.get('category')
        
        # Handle '0' or empty string for category
        if categoryId == '0' or categoryId == '':
            categoryId = None

        depense = Depenses.objects.create(
            label = label,
            fournisseur_id = fournisseur,
            category_id = categoryId,
            date_paiement = date,
            montant_ht = montant_ht,
            tva = tva,
            montant_ttc = montant_ttc,
            piece = piece,
            description = description,
            mode_paiement = mode_paiement,
            reference = reference_paiement
        )

        if mode_paiement == "che" or mode_paiement == "vir":
            OperationsBancaire.objects.create(
                operation_type = "sortie",
                depense = depense,
                montant = montant_ttc,
                reference_bancaire = reference_paiement,
            )

        messages.success(request, 'Les informations ont été enregistrer avec succès')
        return JsonResponse({"status":"success"})

    else:
        return JsonResponse({"status":"error"})
    
@login_required(login_url="institut_app:login")
def ApiGetDepenseDetails(request):
    if request.method == "GET":
        id = request.GET.get('id')
        obj = Depenses.objects.get(id = id)
        data = {
            'id' : obj.id,
            'label' : obj.label,
            'fournisseur' : obj.fournisseur.id if obj.fournisseur else None,
            'fournisseur_designation' : obj.fournisseur.designation if obj.fournisseur else None,
            'client_nom' : obj.client.nom if obj.client else None,
            'client_prenom' : obj.client.prenom if obj.client else None,
            'date' : obj.date_paiement,
            'category': obj.category.id if obj.category else None,
            'category_name': obj.category.name if obj.category else None,
            'category_parent_name': obj.category.parent.name if obj.category and obj.category.parent else None,
            'montant_ht': obj.montant_ht,
            'montant_ttc' : obj.montant_ttc,
            'piece' : obj.piece.url if obj.piece else None,
            'description' : obj.description,
            'tva'  : obj.tva,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"status":"error"})
    
@login_required(login_url="institut_app")
@transaction.atomic
def ApiUpdateDepense(request):
    if request.method == "POST":
        id = request.POST.get('id')
        edit_label = request.POST.get('edit_label')
        edit_fournisseur = request.POST.get('edit_fournisseur')
        edit_montant_ht = request.POST.get('edit_montant_ht')
        edit_tva = request.POST.get('edit_tva')
        edit_montant_ttc = request.POST.get('edit_montant_ttc')
        edit_date = request.POST.get('edit_date')
        edit_categorie = request.POST.get('edit_categorie')
        edit_sous_categorie = request.POST.get('edit_sous_categorie')
        edit_description = request.POST.get('edit_description')
        edit_piece = request.FILES.get('edit_piece')
        obj = Depenses.objects.get(id = id)

        if request.POST.get('edit_category'):
             obj.category_id = request.POST.get('edit_category')
        
        obj.label = edit_label
        obj.fournisseur_id = edit_fournisseur
        obj.date_paiement = edit_date # Adjusted field name match model
        obj.montant_ht = edit_montant_ht
        obj.tva = edit_tva
        obj.montant_ttc = edit_montant_ttc
        if edit_piece:
            obj.piece = edit_piece
        obj.description = edit_description

        obj.save()
        return JsonResponse({"status":"success"})
                

    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
@transaction.atomic
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
def ApiRecordExpensePayment(request):
    if request.method == "POST":
        try:
            id = request.POST.get('id')
            payment_date = request.POST.get('payment_date')
            
            if not id or not payment_date:
                return JsonResponse({"status":"error", "message":"ID et date de paiement requis"})
            
            obj = Depenses.objects.get(id=id)
            obj.date_paiement = payment_date
            obj.etat = True  # Mark as validated when payment is recorded
            obj.save()
            
            return JsonResponse({"status":"success", "message":"Paiement enregistré avec succès"})
        except Depenses.DoesNotExist:
            return JsonResponse({"status":"error", "message":"Dépense introuvable"})
        except Exception as e:
            return JsonResponse({"status":"error", "message":str(e)})
    else:
        return JsonResponse({"status":"error", "message":"Méthode non autorisée"})