# Generated by Django 4.1.7 on 2024-03-08 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_service_hospitals_alter_service_pathology_labs'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='is_user',
            new_name='is_patient',
        ),
    ]
