# Generated by Django 5.1.4 on 2025-05-22 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_tresorerie', '0013_paiements_mode_paiement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paiements',
            name='reference_paiement',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
