# Generated by Django 3.2.15 on 2022-10-04 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0007_alter_survey_theme"),
    ]

    operations = [
        migrations.AlterField(
            model_name="survey",
            name="theme",
            field=models.CharField(
                choices=[
                    ("CLIMAT", "Climat et biodiversité"),
                    ("VIEILLISSEMENT", "Bien vieillir"),
                    ("SOUVERAINETE", "Souveraineté économique"),
                    ("TRAVAIL", "Futur du travail"),
                    ("SANTE", "Notre santé"),
                    ("EDUCATION", "Notre école"),
                    ("LOGEMENT", "Logement"),
                    ("JEUNESSE", "Jeunesse"),
                    ("NUMERIQUE", "Numérique"),
                ],
                max_length=14,
                null=True,
            ),
        ),
    ]
