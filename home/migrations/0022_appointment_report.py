# Generated by Django 5.0.3 on 2024-03-26 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_appointment_payment_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='report',
            field=models.FileField(blank=True, null=True, upload_to='appointment_reports/'),
        ),
    ]
