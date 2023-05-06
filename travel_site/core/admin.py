from django.contrib import admin
from django.utils.html import format_html
from django.db.models.functions import Substr
from django.db.models import CharField
from .models import Counties, Cover


class FirstLetterFilter(admin.SimpleListFilter):
    title = 'First Letter'
    parameter_name = 'first_letter'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        letters = qs.annotate(first_letter=Substr('county_name', 1, 1, output_field=CharField(
        ))).values_list('first_letter', flat=True).distinct().order_by('first_letter')
        return [(letter, letter) for letter in letters]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(county_name__istartswith=self.value())
        return queryset


@admin.register(Counties)
class CountiesAdmin(admin.ModelAdmin):
    list_display = ('county_name', 'county_photo', 'county_photo_preview')
    list_filter = (FirstLetterFilter,)
    search_fields = ('county_name',)

    def county_photo_preview(self, obj):
        if obj.county_photo:
            return format_html('<img src="{}" height="50" />'.format(obj.county_photo.url))
        else:
            return "-"
    county_photo_preview.short_description = "Photo Preview"

@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    list_display = ('cover_title', 'cover_text', 'cover_photo')
    
    def has_add_permission(self, request):
        return Cover.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        return Cover.objects.count() == 1

    def save_model(self, request, obj, form, change):
        if change:
            Cover.objects.all().delete()
        super().save_model(request, obj, form, change)
