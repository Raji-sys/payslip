import django_filters
from .models import Profile


class ProfileFilter(django_filters.FilterSet):
    ippis_no = django_filters.NumberFilter(label="IPPIS NUMBER", field_name='ippis_no',lookup_expr='exact')
    file_no = django_filters.NumberFilter(label="FILE NUMBER", field_name='flie_no',lookup_expr='exact')
    department = django_filters.NumberFilter(label="DEPARTMENT", field_name='dept_or_unit',lookup_expr='iexact')
   
    class Meta:
        model = Profile
