from django.db import models

# Create your models here.


class Etudiant(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)

    nom_arabe = models.CharField(max_length=255, null=True, blank=True)
    prenom_arabe = models.CharField(max_length=255, null=True, blank=True)

    prenom_pere = models.CharField(max_length=255, null=True, blank=True)

    date_naisance = models.DateField()
    lieu_naisance = models.CharField(max_length=255)

    adresse = models.TextField(null=True, blank=True)
    wilaya = models.CharField(max_length=255, null=True, blank=True)
    pays = models.CharField(max_length=255, null=True, blank=True)
    commune = models.CharField(max_length=255, null=True, blank=True)

    cin = models.CharField(max_length=255, null=True, blank=True)

    groupe_sanguin = models.CharField(max_length=5, null=True, blank=True, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    sexe = models.CharField(max_length=1, null=True, blank=True, choices=[('M', 'Masculin'), ('F', 'Feminin')])

    situation_familiale = models.CharField(max_length=255, null=True, blank=True, choices=[('C', 'Célibataire'), ('M', 'Marié(e)'), ('D', 'Divorcé(e)'), ('V', 'Veuf(ve)')])

    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, null=True, blank=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name="Etudiant"
        verbose_name_plural="Etudiants"

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    


