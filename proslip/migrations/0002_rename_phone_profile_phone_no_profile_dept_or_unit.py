# Generated by Django 4.2.7 on 2023-12-15 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proslip', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='phone',
            new_name='phone_no',
        ),
        migrations.AddField(
            model_name='profile',
            name='dept_or_unit',
            field=models.CharField(blank=True, choices=[('ADMINISTRATION', 'ADMINISTRATION'), ('ACCOUNT', 'ACCOUNT'), ('BIO-MEDICAL ENGINEERING', 'BIO-MEDICAL ENGINEERING'), ('CLINICAL SERVICES', 'CLINICAL SERVICES'), ('CATERING', 'CATERING'), ('DISCIPLINE', 'DISCIPLINE'), ('ENGINEERING', 'ENGINEERING'), ('INFORMATION TECHNOLOGY', 'INFORMATION TECHNOLOGY'), ('INTERNAL AUDIT', 'INTERNAL AUDIT'), ('LEGAL', 'LEGAL'), ('LIBRARY', 'LIBRARY'), ('MEDICAL RECORD', 'MEDICAL RECORD'), ('MEDICAL ILLUSTRATION', 'MEDICAL ILLUSTRATION'), ('NURSING EDUCATION', 'NURSING EDUCATION'), ('NURSING SERVICES', 'NURSING SERVICES'), ('PATHOLOGY', 'PATHOLOGY'), ('PHARMACY', 'PHARMACY'), ('PHYSIOTHERAPHY', 'PHYSIOTHERAPHY'), ('PROSTHETIC AND ORTHOTICS', 'PROSTHETIC AND ORTHOTICS'), ('PROCUMENT', 'PROCUMENT'), ('PUBLIC HEALTH', 'PUBLIC HEALTH'), ('OCCUPATIONAL THERAPHY', 'OCCUPATIONAL THERAPHY'), ('RADIOLOGY', 'RADIOLOGY'), ('SERVICOM', 'SERVICOM'), ('SOCIAL WELFARE', 'SOCIAL WELFARE'), ('STORE', 'STORE'), ('TELEPHONE', 'TELEPHONE'), ('TRANSPORT', 'TRANSPORT')], max_length=300, null=True, verbose_name='Department or Unit'),
        ),
    ]
