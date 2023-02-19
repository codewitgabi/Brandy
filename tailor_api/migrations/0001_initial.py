# Generated by Django 3.2 on 2023-02-19 16:40

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tailor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('skill', models.CharField(choices=[('Tailor', 'Tailor'), ('Fashion Designer', 'Fashion Designer'), ('Tailor and Designer', 'Both')], default='Tailor', max_length=19)),
                ('business_name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=14)),
                ('wallet_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('money_earned', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('pending_money', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('experience', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('location', models.TextField()),
                ('bank', models.CharField(max_length=20)),
                ('account_number', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.TimeField(auto_now_add=True)),
                ('due_date', models.DateField()),
                ('charge', models.DecimalField(decimal_places=2, max_digits=12)),
                ('delivered', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tailor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tailor_api.tailor')),
            ],
        ),
        migrations.CreateModel(
            name='WalletNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('message', models.TextField()),
                ('wallet', models.CharField(choices=[('Credit', 'Credit'), ('Withdrawal', 'Withdrawal'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('paid_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('tailor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tailor_api.tailor')),
            ],
        ),
        migrations.CreateModel(
            name='TaskReminder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('tailor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tailor_api.tailor')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tailor_api.task')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.CharField(choices=[('0.5', '0.5'), ('1.0', '1.0'), ('1.5', '1.5'), ('2.0', '2.0'), ('2.5', '2.5'), ('3.0', '3.0'), ('3.5', '3.5'), ('4.0', '4.0'), ('4.5', '4.5'), ('5.0', '5.0')], default='5.0', max_length=3)),
                ('tailor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tailor_api.tailor')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crotch_length', models.IntegerField(default=1)),
                ('center_length', models.IntegerField(default=1)),
                ('out_seam', models.IntegerField(default=1)),
                ('waist', models.IntegerField(default=1)),
                ('In_seam', models.IntegerField(default=1)),
                ('hip', models.IntegerField(default=1)),
                ('ankle', models.IntegerField(default=1)),
                ('bust', models.IntegerField(default=1)),
                ('height', models.IntegerField(default=1)),
                ('hight_bust', models.IntegerField(default=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('duration', models.CharField(choices=[('7am - 8am', '7am - 8am'), ('10am - 11am', '10am - 11am'), ('1pm - 2pm', '1pm - 2pm'), ('4pm - 5pm', '4pm - 5pm'), ('7pm - 8pm', '7pm - 8pm'), ('9pm - 10pm', '9pm - 10pm')], default='7am - 8am', max_length=11)),
                ('accepted', models.BooleanField(default=False)),
                ('declined', models.BooleanField(default=False)),
                ('tailor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tailor_api.tailor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['accepted'],
            },
        ),
    ]
