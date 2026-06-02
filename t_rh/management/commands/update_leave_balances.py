from django.core.management.base import BaseCommand
from t_rh.models import Employees
from t_rh.utils import accrue_monthly_leave
from django.db import connection

class Command(BaseCommand):
    help = 'Met à jour le solde de congé (ajoute 2.5 jours) pour tous les employés actifs'

    def handle(self, *args, **kwargs):
        if getattr(connection, 'schema_name', None) == 'public':
            self.stdout.write('Skipping public schema...')
            return

        try:
            employes_actifs = Employees.objects.filter(etat="en cours")
            count = 0
            for emp in employes_actifs:
                if emp.date_recrutement:
                    accrue_monthly_leave(emp)
                    count += 1
            
            self.stdout.write(self.style.SUCCESS(f'Succès: Les soldes de congé ont été mis à jour pour {count} employés.'))
        except Exception as e:
            self.stderr.write(f"Erreur lors de l'exécution sur le schéma {getattr(connection, 'schema_name', 'inconnu')}: {e}")
