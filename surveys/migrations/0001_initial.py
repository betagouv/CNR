# Generated by Django 3.2.15 on 2022-09-22 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("public_website", "0007_auto_20220922_1420"),
    ]

    operations = [
        migrations.CreateModel(
            name="Survey",
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
                ("label", models.CharField(max_length=100, unique=True)),
                ("hr_label", models.TextField(blank=True, null=True)),
                (
                    "theme",
                    models.CharField(
                        choices=[
                            ("CLIMAT", "Climat"),
                            ("VIEILLISSEMENT", "Générations et vieillissement"),
                            ("SOUVERAINETE", "Souveraineté économique"),
                            ("TRAVAIL", "Futur du travail"),
                            ("SANTE", "Santé"),
                            ("EDUCATION", "Éducation"),
                            ("LOGEMENT", "Logement"),
                            ("JEUNESSE", "Jeunesse"),
                            ("NUMERIQUE", "Numérique"),
                        ],
                        max_length=14,
                        null=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="SurveyQuestion",
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
                ("label", models.CharField(max_length=100, unique=True)),
                ("hr_label", models.TextField(blank=True, null=True)),
                ("rank", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "answer_type",
                    models.CharField(
                        choices=[
                            ("ONE_TEXT_FIELD", "1 large text input"),
                            ("THREE_TEXT_FIELD", "3 small text inputs"),
                            ("FIVE_TEXT_FIELD", "5 small text inputs"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "survey",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="surveys.survey",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SurveyParticipation",
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
                    "participant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participations",
                        to="public_website.participant",
                    ),
                ),
                (
                    "survey",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="participants",
                        to="surveys.survey",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SurveyAnswer",
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
                ("rank", models.IntegerField(blank=True, null=True)),
                ("answer", models.TextField(blank=True)),
                (
                    "postal_code",
                    models.CharField(max_length=5, verbose_name="Code postal"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "survey_question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="surveys.surveyquestion",
                    ),
                ),
            ],
        ),
    ]
