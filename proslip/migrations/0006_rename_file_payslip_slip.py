# Generated by Django 4.2.7 on 2023-12-18 19:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proslip', '0005_payslip_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payslip',
            old_name='file',
            new_name='slip',
        ),
    ]