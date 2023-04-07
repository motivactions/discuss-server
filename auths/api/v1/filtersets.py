from django_filters.rest_framework import filters, filterset


class UserAPIFilterset(filterset.FilterSet):
    is_active = filters.BooleanFilter(field_name="is_active")
