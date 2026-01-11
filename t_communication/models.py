from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Reminder(models.Model):
    CATEGORY_CHOICES = [
        ('bg-primary', 'Travail (Bleu)'),
        ('bg-success', 'Personnel (Vert)'),
        ('bg-danger', 'Important (Rouge)'),
        ('bg-warning', 'A faire (Jaune)'),
        ('bg-info', 'Autre (Ciel)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders', verbose_name=_("Utilisateur"))
    title = models.CharField(max_length=255, verbose_name=_("Titre"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='bg-primary', verbose_name=_("Catégorie"))
    participants = models.ManyToManyField(User, related_name='participating_reminders', blank=True, verbose_name=_("Participants"))
    start_time = models.DateTimeField(verbose_name=_("Heure de début"))
    end_time = models.DateTimeField(blank=True, null=True, verbose_name=_("Heure de fin"))
    is_completed = models.BooleanField(default=False, verbose_name=_("Complété"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Rappel")
        verbose_name_plural = _("Rappels")
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class ChatGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nom du groupe"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    members = models.ManyToManyField(User, related_name='chat_groups', verbose_name=_("Membres"))
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administered_groups', verbose_name=_("Administrateur"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Groupe de discussion")
        verbose_name_plural = _("Groupes de discussion")
        
    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name=_("Expéditeur"))
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name=_("Destinataire"), null=True, blank=True)
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, related_name='messages', verbose_name=_("Groupe"), null=True, blank=True)
    content = models.TextField(verbose_name=_("Contenu"), blank=True, null=True)
    file = models.FileField(upload_to='chat_files/%Y/%m/%d/', blank=True, null=True, verbose_name=_("Fichier joint"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Horodatage"))
    is_read = models.BooleanField(default=False, verbose_name=_("Lu"))

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ['timestamp']

    def __str__(self):
        if self.group:
             return f"De {self.sender.username} dans {self.group.name} le {self.timestamp}"
        return f"De {self.sender.username} à {self.receiver.username} le {self.timestamp}"
