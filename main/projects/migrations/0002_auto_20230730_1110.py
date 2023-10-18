# Generated by Django 3.2.19 on 2023-07-30 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tblwbudgetcost',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_BudgetCost', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwcontractdox',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_ContractDox', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwcriticalaction',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_CriticalAction', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwcriticalaction',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_CriticalAction', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwfinancialinfo',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_Financialinfo', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwfinancialinfo',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_Financialinfo', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwfinancialinfo',
            name='lastclaimedinvoice_r',
            field=models.BigIntegerField(blank=True, db_column='LastClaimedInvoice_r', null=True),
        ),
        migrations.AlterField(
            model_name='tblwhse',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_Hse', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwhse',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_Hse', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwinvoice',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_Invoice', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwinvoice',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_Invoice', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwinvoicedox',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_Invoicedox', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwinvoicedox',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_Invoicedox', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwinvoiceex',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_InvoiceEx', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwinvoiceex',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_InvoiceEx', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwmachinary',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_Machinery', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwmachinary',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_Machinery', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwpmsprogress',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_Pmsprogress', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwpmsprogress',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_Pmsprogress', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwproblem',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_Problem', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwproblem',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_Problem', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwprogressstate',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_ProgressState', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwprogressstate',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_ProgressState', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwprojectpersonel',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_ProjectPersonal', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwprojectpersonel',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_ProjectPersonal', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwreportconfirm',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_ReportConfirm', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwreportconfirm',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_ReportConfirm', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwreportdox',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_ReportDox', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwreportdox',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_ReportDox', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwreportvisit',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_ReportVisit', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwreportvisit',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_ReportVisit', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwtimeprogressstate',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_TimeProgressState', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwtimeprogressstate',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_TimeProgressState', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwworkvolume',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_WorkVolume', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwworkvolume',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate_WorkVolume', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwzone',
            name='contractid',
            field=models.ForeignKey(db_column='ContractID', on_delete=django.db.models.deletion.PROTECT, related_name='Contract_Zone', to='contracts.tblcontract'),
        ),
        migrations.AlterField(
            model_name='tblwzoneimage',
            name='dateid',
            field=models.ForeignKey(db_column='DateID', on_delete=django.db.models.deletion.PROTECT, related_name='ReportDate', to='projects.tblwreportdate'),
        ),
        migrations.AlterField(
            model_name='tblwzoneimage',
            name='zoneid',
            field=models.ForeignKey(db_column='ZoneID', on_delete=django.db.models.deletion.DO_NOTHING, to='projects.tblwzone'),
        ),
    ]