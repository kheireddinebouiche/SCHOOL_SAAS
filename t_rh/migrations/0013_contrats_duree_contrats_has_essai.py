# Generated by Django 5.1.4 on 2025-03-31 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_rh', '0012_rename_salaire_contrats_salaire_base_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrats',
            name='duree',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contrats',
            name='has_essai',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
