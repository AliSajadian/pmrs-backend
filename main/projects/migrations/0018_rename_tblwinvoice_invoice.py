# Generated by Django 3.2.19 on 2023-09-26 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0017_alter_tbladdendum_addendumamountdate'),
        ('projects', '0017_rename_tblwhse_hse'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TblwInvoice',
            new_name='Invoice',
        ),
    ]
