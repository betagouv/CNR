# Generated by Django 3.2.15 on 2022-09-24 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0004_remove_surveyquestion_rank"),
    ]

    operations = [
        migrations.AlterField(
            model_name="surveyquestion",
            name="answer_type",
            field=models.CharField(
                choices=[
                    ("ONE_TEXT_FIELD", "1 large text input"),
                    ("THREE_TEXT_FIELD", "3 small text inputs"),
                    ("FIVE_TEXT_FIELD", "5 small text inputs"),
                ],
                default="ONE_TEXT_FIELD",
                max_length=50,
            ),
            preserve_default=False,
        ),
    ]