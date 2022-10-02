# Generated by Django 3.2.15 on 2022-09-22 20:28
import csv
import os.path

from django.conf import settings
from django.db import migrations

from public_website.models import Theme


def populate_surveys(apps, schema_editor):
    Survey = apps.get_model("surveys", "Survey")
    SurveyQuestion = apps.get_model("surveys", "SurveyQuestion")
    themes = [theme for theme in Theme if theme not in ["EDUCATION", "SANTE"]]

    for theme in themes:
        Survey.objects.create(
            label=f"{theme.name}_1",
            hr_label=theme.label,
            theme=theme.name,
        )

    path = os.path.join(
        settings.BASE_DIR, "surveys/migrations/fixtures/20220922-questionnaires_CNR.csv"
    )
    with open(path) as file:
        data = csv.reader(file, delimiter=";")
        for row in data:

            survey_label = f"{row[0]}"

            survey = Survey.objects.get(label=survey_label)
            for i in range(1, len(row)):
                if "les trois mots" in row[i]:
                    answer_type = "THREE_TEXT_FIELD"
                elif "chantiers prioritaires" in row[i]:
                    answer_type = "FIVE_TEXT_FIELD"
                elif "une première proposition" in row[i]:
                    answer_type = "ONE_TEXT_FIELD"
                else:
                    print(survey_label, row[i])
                    raise Exception
                SurveyQuestion.objects.create(
                    survey=survey,
                    label=f"{survey_label}_Q_{i}",
                    hr_label=row[i],
                    answer_type=answer_type,
                )


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_surveys),
    ]
