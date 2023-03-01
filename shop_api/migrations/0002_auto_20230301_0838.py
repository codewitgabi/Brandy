# Generated by Django 3.2 on 2023-03-01 07:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothrating',
            name='feedback',
            field=models.TextField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clothrating',
            name='rating',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default='2', max_length=1),
        ),
        migrations.CreateModel(
            name='ClothRatingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='cloth_rating')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_api.clothrating')),
            ],
        ),
    ]
