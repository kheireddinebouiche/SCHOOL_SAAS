# Generated by Django 5.1.4 on 2025-03-30 09:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t_formations', '0004_alter_promos_etat'),
        ('t_groupe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupe',
            name='promotion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='t_formations.promos'),
        ),
    ]
