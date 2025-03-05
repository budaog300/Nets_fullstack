import django_filters
from django.db import models
import json
from .models import Veterans


class VeteransFilter(django_filters.FilterSet):
    # achievements_filter = django_filters.CharFilter(method="filter_achievements", field_name="achievements")

    class Meta:
        model = Veterans
        fields = {
            "last_name": ["exact"],
            "first_name": ["exact"],
            "patronymic": ["exact"],
            "gender": ["exact"],
            "age_group": ["exact"],
            "sport": ["exact"],
            "club": ["exact"],
        }

    # def filter_achievements(self, queryset, name, value):
    #     try:
    #         search_value = json.loads(value)
    #         if "title" in search_value:
    #             queryset = queryset.filter(achievements__contains=[{"title": search_value["title"]}])
    #         if "year" in search_value:
    #             queryset = queryset.filter(achievements__contains=[{"year": search_value["year"]}])
    #
    #         return queryset.distinct()
    #     except json.JSONDecodeError:
    #         return queryset.none()