# Generated by Django 3.2.19 on 2023-09-26 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0017_alter_tbladdendum_addendumamountdate'),
        ('projects', '0016_rename_tblwfinancialinfo_financialinfo'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TblwHse',
            new_name='Hse',
        ),
    ]
