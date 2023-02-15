# Generated by Django 3.2 on 2023-02-15 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0004_auto_20230215_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloth',
            name='category',
            field=models.CharField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Babies', 'Babies'), ('Teenagers', 'Teenagers')], default='Men', max_length=9),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
