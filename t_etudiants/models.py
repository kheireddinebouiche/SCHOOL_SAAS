from django.db import models
from t_crm.models import Prospets
from t_groupe.models import Groupe
from t_formations.models import *
from django.utils import timezone

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
    
class RegistrePresence(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    semestre = models.CharField(max_length=100, null=True, blank=True, choices=[('1','Semestre 1'),('2','Semestre 2'),('3','Semestre 3'),('4','Semestre 4')])
    groupe = models.ForeignKey(Groupe, null=True, blank=True, on_delete=models.CASCADE)
    context = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label
    
class LigneRegistrePresence(models.Model):
    module = models.ForeignKey(Modules, on_delete=models.CASCADE, null=True, blank=True, related_name="module_presence")
    teacher = models.ForeignKey(Formateurs, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    room = models.CharField(max_length=100, null=True, blank=True)
    registre = models.ForeignKey(RegistrePresence, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.module.label} - {self.teacher.nom}"
    
class HistoriqueAbsence(models.Model):
    ligne_presence = models.ForeignKey("LigneRegistrePresence", on_delete=models.CASCADE, null=True, blank=True)
    etudiant = models.ForeignKey(Prospets, null=True, blank=True, on_delete=models.CASCADE)
    historique = models.JSONField(default=list, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.etudiant.nom} - {self.ligne_presence.module.label}" if self.etudiant and self.ligne_presence else "Historique Absence"

    def ajouter_entree(self, date, module, heure, etat):
        """Ajoute ou met à jour une entrée dans le champ JSON"""
        if not date:
            date = timezone.now().date()

        date_str = date.strftime("%d/%m/%Y")

        if self.historique is None:
            self.historique = []

        new_entry = {"module": module, "heure": heure, "etat": etat}

        # Cherche si cette date existe déjà
        existing_date = next((item for item in self.historique if item["date"] == date_str), None)

        if existing_date:
            existing_module = next((m for m in existing_date["data"] if m["module"] == module), None)
            if existing_module:
                existing_module.update(new_entry)
            else:
                existing_date["data"].append(new_entry)
        else:
            self.historique.append({"date": date_str,"data": [new_entry]})

        self.save()


