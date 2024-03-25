# Generated by Django 5.0.3 on 2024-03-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_appointment_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='hospital_images/'),
        ),
        migrations.AddField(
            model_name='hospital',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='hospital_images/'),
        ),
        migrations.AddField(
            model_name='pathologylab',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='pathology_images/'),
        ),
        migrations.AddField(
            model_name='pathologylab',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='pathology_images/'),
        ),
    ]
