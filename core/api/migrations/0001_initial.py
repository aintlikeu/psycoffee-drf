# Generated by Django 4.2.1 on 2023-06-06 16:39

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.IntegerField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU')),
                ('comment', models.TextField()),
                ('spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.spot')),
            ],
        ),
    ]
