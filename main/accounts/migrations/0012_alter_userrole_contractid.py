# Generated by Django 3.2.19 on 2023-09-28 14:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0025_rename_tbljschedulefinancialdocument_schedulefinancialdocument'),
        ('accounts', '0011_auto_20230926_0751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='contractid',
            field=models.ForeignKey(blank=True, db_column='ContractID', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='Contract_UserRole', to='contracts.contract'),
        ),
    ]