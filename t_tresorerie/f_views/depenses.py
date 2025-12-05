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
    liste = Depenses.objects.all().values('id','label','categorie__label','sous_categorie__label','montant_ht','montant_ttc','tva','date_paiement','fournisseur__designation','etat').order_by('id')
    return JsonResponse(list(liste), safe=False)

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
        categorie = request.POST.get('typeSelect')
        sous_categorie = request.POST.get('typeSelectSousCategorie')
        date = request.POST.get('date_depense')
        montant_ht = request.POST.get('montant_ht')
        tva = request.POST.get('tva')
        montant_ttc = request.POST.get('montant_ttc')
        piece = request.FILES.get('piece')
        description = request.POST.get('description')
        mode_paiement = request.POST.get('mode_paiement')
        reference_paiement = request.POST.get('reference_paiement')

        Depenses.objects.create(
            label = label,
            fournisseur_id = fournisseur,
            categorie_id = categorie,
            sous_categorie_id = sous_categorie,
            date_paiement = date,
            montant_ht = montant_ht,
            tva = tva,
            montant_ttc = montant_ttc,
            piece = piece,
            description = description,
            mode_paiement = mode_paiement,
            reference = reference_paiement
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
            'fournisseur' : obj.fournisseur.id,
            'fournisseur_designation' : obj.fournisseur.designation,
            'date' : obj.date,
            'categorie': obj.categorie.id,
            'categorie_label': obj.categorie.label,
            'sous_categorie' : obj.sous_categorie.id,
            'sous_categorie_label' : obj.sous_categorie.label,
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

        obj.label = edit_label
        obj.fournisseur.id = edit_fournisseur
        obj.categorie.id = edit_categorie
        obj.sous_categorie.id = edit_sous_categorie
        obj.date = edit_date
        obj.montant_ht = edit_montant_ht
        obj.tva = edit_tva
        obj.montant_ttc = edit_montant_ttc
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