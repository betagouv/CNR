# Generated by Django 3.2.15 on 2022-09-18 09:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Participant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Courriel"
                    ),
                ),
                ("first_name", models.CharField(max_length=100, verbose_name="Prénom")),
                (
                    "postal_code",
                    models.CharField(max_length=10, verbose_name="Code Postal"),
                ),
                (
                    "participant_type",
                    models.CharField(
                        choices=[
                            ("CITOYEN", "Citoyen"),
                            ("ELU", "Élu"),
                            ("ASSOCIATION", "Représentant d'une association"),
                        ],
                        max_length=30,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "theme",
                    models.CharField(
                        choices=[("EDUCATION", "Éducation"), ("SANTE", "Santé")],
                        max_length=30,
                    ),
                ),
                (
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="public_website.participant",
                    ),
                ),
            ],
        ),
    ]