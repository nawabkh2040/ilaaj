# Generated by Django 5.0.3 on 2024-03-24 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_service_off_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
