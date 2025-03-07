# Generated by Django 5.1.4 on 2025-02-16 14:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('t_formations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NouveauVisiteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('prenom', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('telephone', models.CharField(blank=True, max_length=15, null=True)),
                ('adresse', models.TextField(blank=True, null=True)),
                ('type_visiteur', models.CharField(blank=True, choices=[('particulier', 'Particulier'), ('entreprise', 'Entreprise')], max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('has_paied', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('formation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='t_formations.formation')),
            ],
            options={
                'verbose_name': 'Visiteur',
                'verbose_name_plural': 'Visiteurs',
            },
        ),
    ]
