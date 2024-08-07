# Generated by Django 3.2.19 on 2023-11-30 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects_files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportvisit',
            name='budget',
            field=models.BooleanField(db_column='Budget', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='criticalactions',
            field=models.BooleanField(db_column='CriticalActions', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='dashboard_fc',
            field=models.BooleanField(db_column='Dashboard_FC', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='dashboard_r',
            field=models.BooleanField(db_column='Dashboard_R', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='durationdox',
            field=models.BooleanField(db_column='DurationDox', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='financialinfo',
            field=models.BooleanField(db_column='FinancialInfo', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='financialinvoice',
            field=models.BooleanField(db_column='FinancialInvoice', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='hse',
            field=models.BooleanField(db_column='HSE', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='imagereport',
            field=models.BooleanField(db_column='ImageReport', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='invoice',
            field=models.BooleanField(db_column='Invoice', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='machinary',
            field=models.BooleanField(db_column='Machinary', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='personel',
            field=models.BooleanField(db_column='Personel', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='pmsprogress',
            field=models.BooleanField(db_column='PMSProgress', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='problems',
            field=models.BooleanField(db_column='Problems', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='progressstate',
            field=models.BooleanField(db_column='ProgressState', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='projectdox',
            field=models.BooleanField(db_column='ProjectDox', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='timeprogressstate',
            field=models.BooleanField(db_column='TimeProgressState', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='workvolume',
            field=models.BooleanField(db_column='WorkVolume', default=False),
        ),
        migrations.AlterField(
            model_name='reportvisit',
            name='zoneimages',
            field=models.BooleanField(db_column='ZoneImages', default=False),
        ),
    ]
