# Generated by Django 3.2.15 on 2022-09-29 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_website", "0011_participant_sante_participant_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="education_participant_type",
            field=models.CharField(
                choices=[
                    ("PARENT", "Parent d’élève"),
                    ("PROFESSEUR", "Professeur(e)"),
                    (
                        "ASSOCIATION",
                        "Association ou entreprise ayant un lien avec l’école",
                    ),
                    ("ELU", "Elu(e) local"),
                    ("MAIRE", "Maire ou président(e) d’exécutif"),
                ],
                max_length=11,
                null=True,
            ),
        ),
    ]
