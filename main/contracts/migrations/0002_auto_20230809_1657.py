# Generated by Django 3.2.19 on 2023-08-09 12:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblcontract',
            name='coordinatorid',
            field=models.ForeignKey(blank=True, db_column='CoordinatorID', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Coordinator_Contract', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tblcontract',
            name='projectmanagerid',
            field=models.ForeignKey(db_column='ProjectManagerID', on_delete=django.db.models.deletion.CASCADE, related_name='ProjectManager_Contract', to=settings.AUTH_USER_MODEL),
        ),
    ]
