from django.contrib import admin
from .models import Profile

admin.site.site_header="PRO PAYSLIP ADMIN"
admin.site.index_title="PRO PAYSLIP"
admin.site.site_title="PRO PAYSLIP"


# class ProfileForm(forms.ModelForm):
#     pass
    # class Meta:
    #     model = Profile
    #     fields = []  

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # form=ProfileForm
    readonly_fields=['ippis_no',]
    list_display = ['full_name','file_no','ippis_no','dept_or_unit','phone_no']
    list_filter = ['dept_or_unit']
    search_fields = ['dept_or_unit']
    list_per_page = 10