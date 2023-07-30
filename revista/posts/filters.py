import django_filters
from accounts.models import CustomUser

class CustomUserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['username']