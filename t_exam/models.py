from django.db import models
from django.contrib.auth.models import User
from t_formations.models import *
from t_groupe.models import Groupe
from t_etudiants.models import *
from institut_app.models import SalleClasse

class SessionExam(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True, help_text="Code de la session d'examen")
    label = models.CharField(max_length=100, null=True, blank=True)
    type_session = models.CharField(max_length=11, null=True, blank=True, choices=[('normal' ,'Session Normal'),('rattrapage', 'Session de rattrapage')])
    date_debut = models.DateTimeField(null=True)
    date_fin = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="session_exam_updated_by")

    class Meta:
        verbose_name = "Session d'examen"
        verbose_name_plural = "Sessions d'examen"

    def __str__(self):
        return self.label
    
class SessionExamLine(models.Model):
    session = models.ForeignKey(SessionExam, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="session_exam_lines")
    groupe = models.ForeignKey(Groupe, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="session_exam_groupe")
    semestre = models.CharField(max_length=100, null=True, choices=[('1',"1"),('2',"2"),('3',"3"),('4',"4")])

    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return f"{self.session} - {self.groupe}" if self.session and self.groupe else "Ligne de session d'examen non définie"
    
class ExamPlanification(models.Model):
    exam_line = models.ForeignKey(SessionExamLine, on_delete=models.CASCADE, null=True, blank=True, related_name="exam_planification")
    salle = models.ForeignKey(SalleClasse, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="exam_planification_salle")
    date = models.DateTimeField(null=True, blank=True, help_text="Date de l'examen")
    module = models.ForeignKey(Modules, null=True, on_delete=models.DO_NOTHING)
    heure_debut = models.TimeField(null=True, blank=True, help_text="Heure de début de l'examen")
    heure_fin = models.TimeField(null=True, blank=True, help_text="Heure de fin de l'examen")

    passed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return f"{self.exam_line} - {self.module}" if self.exam_line and self.module else "Planification d'examen non définie"

class ModelBuilltins(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True, help_text="Label du modèle de builtins")
    formation = models.ForeignKey(Formation, null=True, blank=True, on_delete=models.DO_NOTHING, related_name="model_builtin_formation")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.label if self.label else "Modèle de builtins non défini"
    
class TypeNote(models.Model):
    model_builtins = models.ForeignKey(ModelBuilltins, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="model_builtins")
    label = models.CharField(max_length=100, null=True, blank=True, help_text="Nom du type de note")
    affichage = models.CharField(max_length=100, null=True, blank=True, help_text="Quelle text afficher dans les PV's et builltins")
    eval = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)

    def __str__(self):
        return self.label if self.label else "Type de note non défini"
    
class PVNotes(models.Model):
    model_builtin = models.ForeignKey(ModelBuilltins, on_delete=models.DO_NOTHING, null=True)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    class Meta:
        unique_together = ('module', 'groupe')

    def __str__(self):
        return f"PV - {self.module.label} - {self.groupe.nom}"
    
class Note(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='notes')
    note_type = models.ForeignKey(TypeNote, on_delete=models.CASCADE)
    valeur = models.FloatField()
    pv = models.ForeignKey(PVNotes, on_delete=models.CASCADE, related_name='notes')

    class Meta:
        unique_together = ('etudiant', 'note_type', 'pv')

class Commissions(models.Model):
    label = models.CharField(max_length=100, null=True, blank=True)
    promo = models.ForeignKey(Promos, null=True, blank=True, on_delete=models.CASCADE)
    criters = models.TextField(null=True, blank=True)
    date_commission = models.DateField(null=True, blank=True)
    is_validated = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    comment = models.TextField(null=True, blank=True)
    
    participant = models.ManyToManyField(Employees)
    formateurs = models.ManyToManyField(Formateurs)
    groupes = models.ManyToManyField(Groupe)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.label

class CommisionResult(models.Model):
    commission = models.ForeignKey(Commissions, on_delete=models.CASCADE, null=True, blank=True)
    etudiants = models.ForeignKey(Prospets, on_delete=models.CASCADE, null=True, blank=True)
    result = models.CharField(max_length=100, null=True, blank=True, choices=[('exam','Examen'),('rach','Rachat'),('ajou','Ajourné(e)')])
    modules = models.ManyToManyField(Modules)
    commentaire = models.TextField(null=True, blank=True)

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.commission.label}'




