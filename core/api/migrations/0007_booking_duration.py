# Generated by Django 4.2.1 on 2023-06-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_booking_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='duration',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
