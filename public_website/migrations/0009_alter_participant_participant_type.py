# Generated by Django 3.2.15 on 2022-09-28 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_website", "0008_auto_20220924_1547"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="participant_type",
            field=models.CharField(
                choices=[
                    ("PARTICULIER", "Particulier"),
                    ("ELU", "Élu(e)"),
                    ("ASSOCIATION", "Représentant(e) d'un corps intermédiaire"),
                ],
                max_length=11,
                null=True,
            ),
        ),
    ]
