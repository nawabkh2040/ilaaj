# Generated by Django 5.0.3 on 2024-03-26 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_hospital_image1_hospital_image2_pathologylab_image1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='online_payment',
            field=models.BooleanField(default=False),
        ),
    ]
