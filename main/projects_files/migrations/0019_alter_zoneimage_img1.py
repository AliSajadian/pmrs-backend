# Generated by Django 3.2.19 on 2023-09-30 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects_files', '0018_alter_zoneimage_img1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zoneimage',
            name='img1',
            field=models.ImageField(blank=True, db_column='Img1', null=True, unique=True, upload_to='zone_images'),
        ),
    ]
