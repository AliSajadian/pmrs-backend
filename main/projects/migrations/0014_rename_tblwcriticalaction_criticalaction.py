# Generated by Django 3.2.19 on 2023-09-26 03:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0017_alter_tbladdendum_addendumamountdate'),
        ('projects', '0013_rename_tbljcontractreportdate_contractreportdate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TblwCriticalaction',
            new_name='Criticalaction',
        ),
    ]
