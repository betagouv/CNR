# Generated by Django 3.2.15 on 2022-09-22 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_website', '0005_auto_20220920_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='postal_code',
            field=models.CharField(max_length=5, null=True, verbose_name='Code postal'),
        ),
    ]