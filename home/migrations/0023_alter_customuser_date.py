# Generated by Django 5.0.3 on 2024-03-29 18:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_appointment_report'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]