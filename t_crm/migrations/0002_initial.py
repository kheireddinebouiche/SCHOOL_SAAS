# Generated by Django 5.1.4 on 2025-04-27 07:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('t_crm', '0001_initial'),
        ('t_formations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='demandeinscription',
            name='formation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='t_formations.formation'),
        ),
        migrations.AddField(
            model_name='demandeinscription',
            name='promo',
            field=models.ForeignKey(blank=True, limit_choices_to={'etat': 'active'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='promo_demande_inscription', to='t_formations.promos'),
        ),
        migrations.AddField(
            model_name='demandeinscription',
            name='specialite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='t_formations.specialites'),
        ),
        migrations.AddField(
            model_name='demandeinscription',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_by_demande_inscription', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='visiteurs',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='demandeinscription',
            name='visiteur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='t_crm.visiteurs'),
        ),
    ]
