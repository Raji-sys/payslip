from django.db import models
from django.contrib.auth.models import User
from django.db import models 
from django.urls import reverse


    
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    middle_name=models.CharField(max_length=300, blank=True, null=True)
    ippis_no=models.PositiveIntegerField('IPPIS Number', null=True, unique=True, blank=True)
    file_no = models.PositiveIntegerField('File Number', null=True, unique=True, blank=True)
    phone_no = models.PositiveIntegerField('Phone Number', null=True, blank=True, unique=True)

    dep=(('ADMINISTRATION','ADMINISTRATION'),('ACCOUNT','ACCOUNT'),('BIO-MEDICAL ENGINEERING','BIO-MEDICAL ENGINEERING'),('CLINICAL SERVICES','CLINICAL SERVICES'),
        ('CATERING','CATERING'),('DISCIPLINE','DISCIPLINE'),('ENGINEERING','ENGINEERING'),('INFORMATION TECHNOLOGY','INFORMATION TECHNOLOGY'),
        ('INTERNAL AUDIT','INTERNAL AUDIT'),('LEGAL','LEGAL'),('LIBRARY','LIBRARY'),('MEDICAL RECORD','MEDICAL RECORD'),('MEDICAL ILLUSTRATION','MEDICAL ILLUSTRATION'),
        ('NURSING EDUCATION','NURSING EDUCATION'),('NURSING SERVICES','NURSING SERVICES'),('PATHOLOGY','PATHOLOGY'),('PHARMACY','PHARMACY'),
        ('PHYSIOTHERAPHY','PHYSIOTHERAPHY'),('PROSTHETIC AND ORTHOTICS','PROSTHETIC AND ORTHOTICS'),('PROCUMENT','PROCUMENT'),('PUBLIC HEALTH','PUBLIC HEALTH'),
        ('OCCUPATIONAL THERAPHY','OCCUPATIONAL THERAPHY'),('RADIOLOGY','RADIOLOGY'),('SERVICOM','SERVICOM'),('SOCIAL WELFARE','SOCIAL WELFARE'),
        ('STORE','STORE'),('TELEPHONE','TELEPHONE'),('TRANSPORT','TRANSPORT'),)
    dept_or_unit=models.CharField('Department or Unit', choices=dep, blank=True, null=True, max_length=300)

    def get_absolute_url(self):
        return reverse('profile_page', args=[self.user])

    def full_name(self):
        return f"{self.user.get_full_name()} {self.middle_name}"
    
    def __str__(self):
        return self.user.username


class Payslip(models.Model):
    profile=models.OneToOneField(Profile, on_delete=models.CASCADE)
    month=models.DateField()
    year=models.DateField()

    def __str__(self):
        return f"{self.profile.full_name} - {self.profile.ippis_no} - {self.month.strftime('%B %Y')}"