# Generated by Django 3.2.15 on 2022-09-18 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("public_website", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="participant",
            name="registration_success",
            field=models.BooleanField(default=False),
        ),
    ]
