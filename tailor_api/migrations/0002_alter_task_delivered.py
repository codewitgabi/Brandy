# Generated by Django 3.2 on 2023-02-13 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailor_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
    ]
