# Generated by Django 4.1.7 on 2024-03-08 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_pathologylab_alter_appointment_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pathologylab',
            name='user',
            field=models.OneToOneField(limit_choices_to={'is_pathology': True}, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
