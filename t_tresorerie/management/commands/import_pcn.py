from django.core.management.base import BaseCommand
from django_tenants.utils import tenant_context
from institut_app.models import Institut  # Adapter selon ton modèle tenant
from t_tresorerie.models import PlanComptable

# Définition complète du plan comptable algérien
PLAN_COMPTABLE = [
    ("10", "Capital", "1", "passif"),
    ("11", "Primes liées au capital", "1", "passif"),
    ("12", "Écarts de réévaluation", "1", "passif"),
    ("13", "Réserves", "1", "passif"),
    ("14", "Résultats reportés", "1", "passif"),
    ("15", "Subventions d’investissement", "1", "passif"),
    ("16", "Provisions et amortissements", "1", "passif"),
    ("17", "Dettes financières", "1", "passif"),
    ("18", "Comptes de liaison interne", "1", "passif"),
    ("20", "Immobilisations incorporelles", "2", "actif"),
    ("21", "Immobilisations corporelles", "2", "actif"),
    ("22", "Immobilisations en concession", "2", "actif"),
    ("23", "Immobilisations en cours", "2", "actif"),
    ("24", "Immobilisations de participation", "2", "actif"),
    ("25", "Autres immobilisations financières", "2", "actif"),
    ("28", "Amortissements des immobilisations", "2", "actif"),
    ("30", "Matières premières", "3", "actif"),
    ("31", "Fournitures consommables", "3", "actif"),
    ("32", "Produits en cours", "3", "actif"),
    ("33", "Produits intermédiaires", "3", "actif"),
    ("34", "Produits finis", "3", "actif"),
    ("35", "Stocks commerciaux", "3", "actif"),
    ("37", "Stocks en transit", "3", "actif"),
    ("39", "Dépréciations des stocks", "3", "actif"),
    ("40", "Fournisseurs", "4", "passif"),
    ("41", "Clients", "4", "actif"),
    ("42", "Personnel", "4", "passif"),
    ("43", "CNAS / CSS", "4", "passif"),
    ("44", "État - Impôts et taxes", "4", "passif"),
    ("45", "Associés", "4", "passif"),
    ("46", "Débiteurs / créanciers divers", "4", "actif"),
    ("47", "Comptes d’attente", "4", "actif"),
    ("48", "Comptes transitoires", "4", "actif"),
    ("49", "Dépréciations comptes tiers", "4", "actif"),
    ("51", "Banques", "5", "actif"),
    ("53", "Caisse", "5", "actif"),
    ("54", "Régies d’avance", "5", "actif"),
    ("55", "Virements internes", "5", "actif"),
    ("58", "Opérations diverses", "5", "actif"),
    ("59", "Dépréciations financières", "5", "actif"),
    ("60", "Achats consommés", "6", "charge"),
    ("61", "Services extérieurs", "6", "charge"),
    ("62", "Impôts et taxes", "6", "charge"),
    ("63", "Charges de personnel", "6", "charge"),
    ("64", "Charges financières", "6", "charge"),
    ("65", "Charges diverses", "6", "charge"),
    ("66", "Charges exceptionnelles", "6", "charge"),
    ("68", "Dotations aux amortissements", "6", "charge"),
    ("69", "Impôts sur les bénéfices", "6", "charge"),
    ("70", "Ventes de biens", "7", "produit"),
    ("706", "Prestations de services", "7", "produit"),
    ("71", "Production vendue", "7", "produit"),
    ("75", "Autres produits", "7", "produit"),
    ("76", "Produits financiers", "7", "produit"),
    ("77", "Produits exceptionnels", "7", "produit"),
    ("78", "Reprises sur amortissements", "7", "produit"),
    ("79", "Transferts de charges", "7", "produit"),
    ("80", "Engagements reçus", "8", "hors_bilan"),
    ("81", "Engagements donnés", "8", "hors_bilan"),
    ("88", "Comptes de liaison hors bilan", "8", "hors_bilan"),
]

class Command(BaseCommand):
    help = "Importe le Plan Comptable Algérien pour tous les tenants"

    def handle(self, *args, **kwargs):
        tenants = Institut.objects.all()  # Tous les tenants
        for tenant in tenants:
            self.stdout.write(f"Importation pour le tenant : {tenant.schema_name}")
            with tenant_context(tenant):
                for numero, intitule, classe, type_compte in PLAN_COMPTABLE:
                    PlanComptable.objects.update_or_create(
                        numero=numero,
                        defaults={
                            "intitule": intitule,
                            "classe": classe,
                            "type_compte": type_compte,
                        }
                    )
        self.stdout.write(self.style.SUCCESS("Plan comptable importé pour tous les tenants !"))
