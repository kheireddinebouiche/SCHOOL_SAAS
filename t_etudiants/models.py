from django.db import models
from t_crm.models import *


class Etudiant(models.Model):
    
    relation = models.ForeignKey(Prospets, on_delete=models.DO_NOTHING, null=True, blank=True)

    nom_arabe = models.CharField(max_length=255, null=True, blank=True)
    prenom_arabe = models.CharField(max_length=255, null=True, blank=True)

    prenom_pere = models.CharField(max_length=255, null=True, blank=True)

    nom_mere = models.CharField(max_length=255, null=True, blank=True)
    prenom_mere = models.CharField(max_length=255, null=True, blank=True)

    tel_pere = models.CharField(max_length=15, null=True, blank=True)
    tel_mere = models.CharField(max_length=15, null=True, blank=True)


    adresse = models.TextField(null=True, blank=True)
    wilaya = models.CharField(max_length=255, null=True, blank=True)
    pays = models.CharField(max_length=255, null=True, blank=True)
    commune = models.CharField(max_length=255, null=True, blank=True)
    
    groupe_sanguin = models.CharField(max_length=5, null=True, blank=True, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    sexe = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Masculin'), ('F', 'Feminin')])

    situation_familiale = models.CharField(max_length=255, null=True, blank=True, choices=[('C', 'Célibataire'), ('M', 'Marié(e)'), ('D', 'Divorcé(e)'), ('V', 'Veuf(ve)')])

    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    alreeady_paied = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name="Etudiant"
        verbose_name_plural="Etudiants"

    def __str__(self):
        return f"{self.relation.nom} {self.relation.prenom}"
    


