from django.db import models
from .forms import *
from django.contrib.auth.models import User


class SessionExam(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True, help_text="Code de la session d'examen")
    label = models.CharField(max_length=100, null=True, blank=True)
    type_session = models.CharField(max_length=11, null=True, blank=True, choices=[('normal' ,'Session Normal'),('rattrapage', 'Session de rattrapage')])
    date_debut = models.DateTimeField(null=True, blank=True)
    date_fin = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="session_exam_updated_by")

    class Meta:
        verbose_name = "Session d'examen"
        verbose_name_plural = "Sessions d'examen"

    def __str__(self):
        return self.label
    

class SessionExamLine(models.Model):
    pass


class Exam(models.Model):
    pass


