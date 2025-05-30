# Generated by Django 5.1.4 on 2025-04-27 07:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institut_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FraisInscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('montant', models.DecimalField(blank=True, decimal_places=2, max_digits=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': "Frais d'inscription",
                'verbose_name_plural': "Frais d'inscription",
            },
        ),
        migrations.CreateModel(
            name='PlansCours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Modules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('duree', models.IntegerField(blank=True, null=True)),
                ('coef', models.IntegerField(blank=True, null=True)),
                ('n_elimate', models.IntegerField(blank=True, null=True)),
                ('systeme_eval', models.CharField(blank=True, max_length=100, null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='module_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='module_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Module',
                'verbose_name_plural': 'Modules',
            },
        ),
        migrations.CreateModel(
            name='Partenaires',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('adresse', models.CharField(blank=True, max_length=255, null=True)),
                ('telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('site_web', models.URLField(blank=True, null=True)),
                ('type_partenaire', models.CharField(blank=True, choices=[('national', 'National'), ('etranger', 'Etranger')], max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_by_partenaire', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Partenaire',
                'verbose_name_plural': 'Partenaires',
            },
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('nom', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('duree', models.PositiveIntegerField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('type_formation', models.CharField(blank=True, choices=[('etrangere', 'Formation étrangere'), ('national', 'Formation Etatique')], default='national', max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('frais_inscription', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('frais_assurance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('updated', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('entite_legal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='institut_app.entreprise')),
                ('partenaire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='t_formations.partenaires', to_field='code')),
            ],
            options={
                'verbose_name': 'Formation',
                'verbose_name_plural': 'Formations',
            },
        ),
        migrations.CreateModel(
            name='PlansCadre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(blank=True, max_length=255, null=True)),
                ('objectifs', models.TextField(blank=True, null=True)),
                ('competences_visees', models.TextField(blank=True, null=True)),
                ('prerequis', models.TextField(blank=True, null=True)),
                ('contenus', models.TextField(blank=True, null=True)),
                ('volume_cours', models.PositiveIntegerField(default=0, help_text='Heures de cours magistral')),
                ('volume_td', models.PositiveIntegerField(default=0, help_text='Heures de travaux dirigés')),
                ('volume_tp', models.PositiveIntegerField(default=0, help_text='Heures de travaux pratiques')),
                ('methodes_pedagogiques', models.TextField(blank=True, null=True)),
                ('modalites_evaluation', models.TextField(blank=True, null=True)),
                ('bibliographie', models.TextField(blank=True, null=True)),
                ('responsable', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='t_formations.modules')),
            ],
            options={
                'verbose_name': 'Plan cadre',
                'verbose_name_plural': 'Plans cadre',
            },
        ),
        migrations.CreateModel(
            name='ProgrammeFormation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semestre', models.CharField(blank=True, max_length=10, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='t_formations.modules', to_field='code')),
            ],
            options={
                'verbose_name': 'Repartition du module',
                'verbose_name_plural': 'Repartition des modules',
            },
        ),
        migrations.CreateModel(
            name='ProgrammePlanCadre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('element_competence', models.TextField(blank=True, null=True)),
                ('criters_performance', models.TextField(blank=True, null=True)),
                ('contenu_pedagogique', models.TextField(blank=True, null=True)),
                ('plan_cadre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='t_formations.planscadre')),
            ],
        ),
        migrations.CreateModel(
            name='Promos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('session', models.CharField(blank=True, choices=[('octobre', 'Octobre'), ('mars', 'Mars')], max_length=255, null=True)),
                ('etat', models.CharField(blank=True, choices=[('active', 'Active'), ('inactive', 'Inactive')], default='inactive', max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Promo',
                'verbose_name_plural': 'Promos',
            },
        ),
        migrations.CreateModel(
            name='Specialites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('prix', models.DecimalField(blank=True, decimal_places=2, max_digits=100, null=True)),
                ('duree', models.CharField(blank=True, max_length=300, null=True)),
                ('nb_semestre', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1, null=True)),
                ('nb_tranche', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], max_length=1, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('version', models.CharField(blank=True, max_length=100, null=True)),
                ('condition_access', models.TextField(blank=True, max_length=1000, null=True)),
                ('dossier_inscription', models.TextField(blank=True, max_length=1000, null=True)),
                ('etat', models.CharField(blank=True, choices=[('last', 'A jour'), ('updated', 'Mis à jour')], default='last', max_length=10, null=True)),
                ('formation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='t_formations.formation', to_field='code')),
            ],
            options={
                'verbose_name': 'Spécialité',
                'verbose_name_plural': 'Spécialités',
            },
        ),
    ]
