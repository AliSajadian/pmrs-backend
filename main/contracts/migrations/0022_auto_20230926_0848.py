# Generated by Django 3.2.19 on 2023-09-26 05:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0021_auto_20230926_0841'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TblJcontractuser',
            new_name='ContractUser',
        ),
        migrations.RenameModel(
            old_name='TblCorporation',
            new_name='EpcCorporation',
        ),
    ]