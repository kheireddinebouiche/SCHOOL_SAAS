# Generated by Django 5.1.4 on 2025-02-18 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_formations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modules',
            name='coef',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='modules',
            name='n_elimate',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
