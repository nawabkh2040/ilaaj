# Generated by Django 5.0.3 on 2024-03-30 11:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_alter_customuser_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]