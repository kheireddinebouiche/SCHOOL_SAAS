from django.shortcuts import render
from django.http import JsonResponse
from ..models import *
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from itertools import chain
from datetime import datetime
from django.db.models import F, Value,CharField, Q
from django.db.models.functions import Coalesce
from itertools import chain
from django.db.models.functions import Concat
from django.views.decorators.clickjacking import xframe_options_exempt



@login_required(login_url="institut_app:login")
def PageConfPenalite(request):
    entreprises = Entreprise.objects.all()
    payment_types = PaymentType.objects.all()
    penalty_config = PenaltyGlobalConfiguration.get_solo()
    return render(request,'tenant_folder/comptabilite/conf/liste_promo.html', locals())


@login_required(login_url="institut_app:login")
def ApiLoadPromo(request):
    if request.method == "GET":
        promo = Promos.objects.all()
        data = []
        for i in promo:
            data.append({
                'id': i.id,
                'begin_year' : i.begin_year,
                'end_year' : i.end_year,
                'session' : i.get_session_display(),
                'prix_rachat_credit' : i.prix_rachat_credit,
                'penalite_retard' : i.penalite_retard,
                'frais_duplicata' : i.frais_duplicata,
                'entite_id': i.entite.id if i.entite else None,
                'entite_label': i.entite.designation if i.entite else None,
                'code' : i.code if i.code else None,
            })
        return JsonResponse(data, safe=False)

    else:
        return JsonResponse({"status":"error"})

@login_required(login_url="institut_app:login")
def ApiUpdatePromoConfig(request):
    if request.method == 'POST':
        try:
            promo_id = request.POST.get('promo_id')
            prix_rachat_credit = request.POST.get('prix_rachat_credit')
            penalite_retard = request.POST.get('penalite_retard')
            frais_duplicata = request.POST.get('frais_duplicata')
            entite_id = request.POST.get('entite_id')

            promo = Promos.objects.get(id=promo_id)
            promo.prix_rachat_credit = Decimal(prix_rachat_credit) if prix_rachat_credit else Decimal('0.00')
            promo.penalite_retard = Decimal(penalite_retard) if penalite_retard else Decimal('0.00')
            promo.frais_duplicata = Decimal(frais_duplicata) if frais_duplicata else Decimal('0.00')
            
            if entite_id:
                promo.entite = Entreprise.objects.get(id=entite_id)
            else:
                promo.entite = None
                
            promo.save()

            return JsonResponse({'status': 'success', 'message': 'Promotion mise à jour avec succès.'})
        except Promos.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Promotion non trouvée.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@login_required(login_url="institut_app:login")
def ApiLoadPenaltyConfig(request):
    if request.method == "GET":
        config = PenaltyGlobalConfiguration.get_solo()
        return JsonResponse({
            'penalite_retard': str(config.penalite_retard),
            'penalite_retard_payment_type': config.penalite_retard_payment_type_id,
            'prix_rachat_credit': str(config.prix_rachat_credit),
            'prix_rachat_credit_payment_type': config.prix_rachat_credit_payment_type_id,
            'frais_duplicata': str(config.frais_duplicata),
            'frais_duplicata_payment_type': config.frais_duplicata_payment_type_id,
        })
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiUpdatePenaltyConfig(request):
    if request.method == 'POST':
        try:
            penalite_retard = request.POST.get('penalite_retard')
            penalite_retard_payment_type_id = request.POST.get('penalite_retard_payment_type')
            
            prix_rachat_credit = request.POST.get('prix_rachat_credit')
            prix_rachat_credit_payment_type_id = request.POST.get('prix_rachat_credit_payment_type')
            
            frais_duplicata = request.POST.get('frais_duplicata')
            frais_duplicata_payment_type_id = request.POST.get('frais_duplicata_payment_type')

            config = PenaltyGlobalConfiguration.get_solo()
            config.penalite_retard = Decimal(penalite_retard) if penalite_retard else Decimal('0.00')
            config.prix_rachat_credit = Decimal(prix_rachat_credit) if prix_rachat_credit else Decimal('0.00')
            config.frais_duplicata = Decimal(frais_duplicata) if frais_duplicata else Decimal('0.00')

            if penalite_retard_payment_type_id:
                config.penalite_retard_payment_type = PaymentType.objects.get(id=penalite_retard_payment_type_id)
            else:
                config.penalite_retard_payment_type = None

            if prix_rachat_credit_payment_type_id:
                config.prix_rachat_credit_payment_type = PaymentType.objects.get(id=prix_rachat_credit_payment_type_id)
            else:
                config.prix_rachat_credit_payment_type = None

            if frais_duplicata_payment_type_id:
                config.frais_duplicata_payment_type = PaymentType.objects.get(id=frais_duplicata_payment_type_id)
            else:
                config.frais_duplicata_payment_type = None

            config.save()
            return JsonResponse({'status': 'success', 'message': 'Configuration des pénalités mise à jour avec succès.'})
        except PaymentType.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Type de paiement spécifié introuvable.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


from t_conseil.models import TvaConseil

@login_required(login_url="institut_app:login")
def ListePenalite(request):
    tvas = TvaConseil.objects.all().order_by('valeur')
    return render(request,'tenant_folder/comptabilite/penalite_rachat/demande_paiements.html', {'tvas': tvas})


@login_required(login_url="institut_app:login")
def ApiListeDuePenalite(request):
    if request.method == 'GET':
        due_paiements = DuePaiements.objects.filter(type__in=['rach', 'dette', 'autre']).select_related('client', 'payment_type')
        data = []
        for due in due_paiements:
            # Check if a payment exists for this due
            paiement = Paiements.objects.filter(due_paiements=due).first()
            data.append({
                'id': due.id,
                'client': f"{due.client.nom} {due.client.prenom}" if due.client else "Client Inconnu",
                'label': due.label,
                'montant_due': due.montant_due,
                'is_done': due.is_done,
                'type': due.payment_type.name if due.payment_type else due.get_type_display(),
                'paiement_id': paiement.id if paiement else None,
                'date_echeance': due.date_echeance,
                'date_paiement': paiement.date_paiement if paiement else None,
            })
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@login_required(login_url="institut_app:login")
def ApiDeleteDuePenalite(request):
    if request.method == 'POST':
        try:
            id_paiement = request.POST.get('id')
            if not id_paiement:
                return JsonResponse({'status': 'error', 'message': 'ID manquant.'}, status=400)

            due_paiement = DuePaiements.objects.get(id=id_paiement)
            due_paiement.delete()

            return JsonResponse({'status': 'success', 'message': 'Paiement dû supprimé avec succès.'})
        except DuePaiements.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paiement dû introuvable.'}, status=404)


@login_required(login_url="institut_app:login")
@transaction.atomic
def ApiPayDuePenalite(request):
    if request.method == 'POST':
        try:
            id_paiement = request.POST.get('id')
            mode_paiement = request.POST.get('mode_paiement', 'esp')
            date_paiement_str = request.POST.get('date_paiement')
            generate_invoice = request.POST.get('generate_invoice', 'false').lower() == 'true'
            
            if not id_paiement:
                return JsonResponse({'status': 'error', 'message': 'ID manquant.'}, status=400)

            due_paiement = DuePaiements.objects.get(id=id_paiement)
            if due_paiement.is_done:
                 return JsonResponse({'status': 'info', 'message': 'Ce paiement a déjà été effectué.'})
            
            # Parse effective date
            if date_paiement_str:
                try:
                    date_paiement = datetime.strptime(date_paiement_str, "%Y-%m-%d").date()
                except ValueError:
                    date_paiement = datetime.now().date()
            else:
                date_paiement = datetime.now().date()

            reference_paiement = request.POST.get('reference_paiement', '').strip()

            # Create the actual Payment record
            paiement = Paiements.objects.create(
                due_paiements=due_paiement,
                prospect=due_paiement.client,
                montant_paye=due_paiement.montant_due,
                date_paiement=date_paiement,
                mode_paiement=mode_paiement,
                reference_paiement=reference_paiement,
                paiement_label=f"Paiement: {due_paiement.label}",
                context='rach' if due_paiement.type == 'rach' else 'autre',
                is_done=(mode_paiement == 'esp'),
                payment_type=due_paiement.payment_type,
            )
            
            due_paiement.is_done = True
            due_paiement.save()

            if mode_paiement in ['che', 'vir']:
                OperationsBancaire.objects.create(
                    operation_type='entree',
                    paiement=paiement,
                    montant=due_paiement.montant_due,
                    reference_bancaire=reference_paiement,
                )

            # Optional invoice generation
            if generate_invoice:
                tva_percent = request.POST.get('tva_percent')
                show_tva = request.POST.get('show_tva', 'true').lower() == 'true'
                skip_timbre = request.POST.get('skip_timbre', 'false').lower() == 'true'
                
                from .invoice_generation import create_invoice_from_payment_object
                create_invoice_from_payment_object(paiement, tva_percent, show_tva, skip_timbre)

            return JsonResponse({
                'status': 'success', 
                'message': 'Paiement effectué et facture générée avec succès.' if generate_invoice else 'Paiement effectué avec succès.',
                'paiement_id': paiement.id
            })
        except DuePaiements.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Paiement dû introuvable.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée.'}, status=405)


@xframe_options_exempt
@login_required(login_url="institut_app:login")
def PrintReceipt(request, paiement_id):
    try:
        paiement = Paiements.objects.get(id=paiement_id)
        return render(request, 'tenant_folder/comptabilite/penalite_rachat/print_receipt.html', {'paiement': paiement})
    except Paiements.DoesNotExist:
        messages.error(request, "Paiement introuvable.")
        return render(request, 'tenant_folder/404.html') # Or redirect back
