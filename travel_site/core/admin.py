from django.contrib import admin
from django.utils.html import format_html
from django.db.models.functions import Substr
from django.db.models import CharField
from .models import Countries


class FirstLetterFilter(admin.SimpleListFilter):
    title = 'First Letter'
    parameter_name = 'first_letter'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        letters = qs.annotate(first_letter=Substr('country_name', 1, 1, output_field=CharField(
        ))).values_list('first_letter', flat=True).distinct().order_by('first_letter')
        return [(letter, letter) for letter in letters]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country_name__istartswith=self.value())
        return queryset


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_photo', 'country_photo_preview')
    list_filter = (FirstLetterFilter,)
    search_fields = ('country_name',)

    def country_photo_preview(self, obj):
        if obj.country_photo:
            return format_html('<img src="{}" height="50" />'.format(obj.country_photo.url))
        else:
            return "-"
    country_photo_preview.short_description = "Photo Preview"
