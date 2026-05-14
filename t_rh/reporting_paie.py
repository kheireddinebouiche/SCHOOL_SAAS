import csv
import io
from django.http import HttpResponse
from decimal import Decimal

def generate_payroll_journal_csv(payroll_data, month, year):
    """
    Generates a CSV file for the Payroll Journal.
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    
    # Header
    writer.writerow(['Journal de Paie', f'{month}/{year}'])
    writer.writerow([])
    writer.writerow([
        'Matricule', 'Nom & Prenom', 'Salaire Base', 'Panier', 'Transport', 
        'HS', 'Base SS', 'Cotis. SS (9%)', 'Imposable', 'IRG', 'Net a Payer'
    ])
    
    for data in payroll_data:
        emp = data['employee']
        res = data['result']
        vars = data['variables']
        
        writer.writerow([
            emp.id,
            f"{emp.nom} {emp.prenom}",
            res['salaire_base_calcule'],
            res['prime_panier'],
            res['prime_transport'],
            vars['heures_sup'],
            res['base_ss'],
            res['montant_ss'],
            res['salaire_imposable'],
            res['irg'],
            res['net_a_payer']
        ])
        
    return output.getvalue()

def generate_bank_transfer_csv(payroll_data):
    """
    Generates a CSV file for Bank Transfer (Virement).
    Format: Nom;RIB;Montant
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    
    writer.writerow(['Nom et Prenom', 'RIB / CCP', 'Banque', 'Montant Net'])
    
    for data in payroll_data:
        emp = data['employee']
        res = data['result']
        
        # Use RIB if available, otherwise CCP
        compte = emp.rib if emp.rib else emp.ccp
        
        writer.writerow([
            f"{emp.nom} {emp.prenom}",
            compte if compte else 'N/A',
            emp.bank if emp.bank else 'N/A',
            res['net_a_payer']
        ])
        
    return output.getvalue()
