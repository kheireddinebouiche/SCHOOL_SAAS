from django.db import models
from django.contrib.auth.models import User
from t_formations.models import *
from t_groupe.models import Groupe
from t_etudiants.models import *
from institut_app.models import SalleClasse
from t_timetable.models import Salle
from django.core.exceptions import ValidationError
from django.db.models import Sum


class SessionExam(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True, help_text="Code de la session d'examen")
    label = models.CharField(max_length=100, null=True, blank=True)
    type_session = models.CharField(max_length=11, null=True, blank=True, choices=[('normal' ,'Session Ordinaire'),('rattrapage', 'Session de rattrapage (Spéciale)')])
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
    salle = models.ForeignKey(Salle, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="exam_planification_salle")
    date = models.DateTimeField(null=True, blank=True, help_text="Date de l'examen")
    module = models.ForeignKey(Modules, null=True, on_delete=models.DO_NOTHING)
    heure_debut = models.TimeField(null=True, blank=True, help_text="Heure de début de l'examen")
    heure_fin = models.TimeField(null=True, blank=True, help_text="Heure de fin de l'examen")
    type_examen = models.CharField(max_length=100, null=True, blank=True, choices=[('normal','Ordinaire'),('rachat','Rachat de credit'),('rattrage','Rattrapage')])
    mode_examination = models.CharField(max_length=100, null=True, blank=True, choices=[('tr','Travail à remettre'),('exam','Examen'),('ligne','Examen en ligne')])

    statut = models.CharField(max_length=100, null=True, blank=True, choices=[('termine','Terminer'),('nabouti','Non abouti')])

    passed = models.BooleanField(default=False)

    comment = models.TextField(null=True, blank=True)

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
    
class BuiltinTypeNote(models.Model):
    builtin = models.ForeignKey(ModelBuilltins,on_delete=models.CASCADE,related_name="types_notes")
    code = models.CharField(max_length=30)
    libelle = models.CharField(max_length=100)
    max_note = models.FloatField()

    has_sous_notes = models.BooleanField(default=False)
    nb_sous_notes = models.PositiveIntegerField(default=0)

    is_rattrapage = models.BooleanField(default=False, help_text="Note concerner dans l'examen de rattrapage")
    is_rachat = models.BooleanField(default=False, help_text="Note faisant l'objet du rachat crédit")

    ordre = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.libelle} ({self.builtin})"
 
class BuiltinSousNote(models.Model):
    type_note = models.ForeignKey(BuiltinTypeNote,on_delete=models.CASCADE,related_name="sous_notes")
    label = models.CharField(max_length=50)
    ordre = models.PositiveIntegerField(default=0)
    max_note = models.FloatField(null=True)

    def clean(self):
        # Somme des autres sous-notes
        total = self.type_note.sous_notes.exclude(pk=self.pk)\
            .aggregate(s=Sum('max_note'))['s'] or 0

        if total + self.max_note > self.type_note.max_note:
            raise ValidationError(
                f"La somme des sous-notes ({total + self.max_note}) "
                f"dépasse la note maximale ({self.type_note.max_note})."
            )

    def save(self, *args, **kwargs):
        self.full_clean()  # force clean()
        super().save(*args, **kwargs)

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

class PvExamen(models.Model):
    exam_planification = models.OneToOneField(
        ExamPlanification,
        on_delete=models.CASCADE,
        related_name="pv"
    )

    est_valide = models.BooleanField(default=False)
    date_validation = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PV - {self.exam_planification.module}"
    
class ExamTypeNote(models.Model):
    pv = models.ForeignKey(PvExamen,on_delete=models.CASCADE,related_name="exam_types_notes")

    code = models.CharField(max_length=30)
    libelle = models.CharField(max_length=100)
    max_note = models.FloatField(null=True, blank=True)

    has_sous_notes = models.BooleanField(default=False)
    nb_sous_notes = models.PositiveIntegerField(default=0)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('pv', 'code')

    def __str__(self):
        return f"{self.libelle} ({self.pv})"

class ExamNote(models.Model):
    pv = models.ForeignKey(PvExamen,on_delete=models.CASCADE,related_name="notes")
    etudiant = models.ForeignKey(Prospets, on_delete=models.CASCADE)
    type_note = models.ForeignKey(ExamTypeNote, on_delete=models.CASCADE)
    valeur = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('pv', 'etudiant', 'type_note')

    def save(self, *args, **kwargs):
        if self.pv.est_valide:
            raise ValidationError("PV verrouillé : modification interdite")
        super().save(*args, **kwargs)

    def calculer_valeur(self):
        if self.sous_notes.exists():
            self.valeur = round(
                sum(sn.valeur for sn in self.sous_notes.all() if sn.valeur is not None),2)
            super().save(update_fields=['valeur'])

    def __str__(self):
        return f"{self.etudiant} - {self.type_note}"
    
class ExamSousNote(models.Model):
    note = models.ForeignKey(ExamNote, on_delete=models.CASCADE,related_name="sous_notes")
    valeur = models.FloatField()

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.note.pv.est_valide:
            raise ValidationError("PV verrouillé")
        super().save(*args, **kwargs)
        self.note.calculer_valeur()


