# Generated by Django 3.2.19 on 2023-09-14 20:15

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_tblwreportdox_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblwreportdox',
            name='file',
            field=models.FileField(db_column='File', null=True, storage=django.core.files.storage.FileSystemStorage(location='D:/projects/cost_control/files/projectsDox/hseDox'), upload_to=''),
        ),
    ]