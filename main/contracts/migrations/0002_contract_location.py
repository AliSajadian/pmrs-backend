# Generated by Django 3.2.19 on 2024-05-08 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='location',
            field=models.CharField(db_column='Location', max_length=20, null=True),
        ),
    ]