from django.contrib import admin
from django.utils.html import format_html
from django.db.models.functions import Substr
from django.db.models import CharField
from .models import Counties, Cover


# Define a custom filter class that filters a queryset by the first letter of the county name
class FirstLetterFilter(admin.SimpleListFilter):
    # Set the title and parameter name for the filter
    title = 'First Letter'
    parameter_name = 'first_letter'

    # Define a method that returns the filter options to display in the admin UI
    def lookups(self, request, model_admin):
        # Get the queryset for the model being filtered
        qs = model_admin.get_queryset(request)
        # Annotate each county name with its first letter
        letters = qs.annotate(
            first_letter=Substr('county_name', 1, 1, output_field=CharField())).values_list('first_letter', flat=True).distinct().order_by('first_letter')
        # Return the unique first letters as filter options
        return [(letter, letter) for letter in letters]

    # Define a method that applies the selected filter to the queryset
    def queryset(self, request, queryset):
        # If a filter value was selected, filter the queryset by county names that start with that value
        if self.value():
            return queryset.filter(county_name__istartswith=self.value())
        # If no filter value was selected, return the unfiltered queryset
        return queryset


@admin.register(Counties)
class CountiesAdmin(admin.ModelAdmin):
    # Define the fields to display in the admin UI
    list_display = ('county_name', 'county_photo', 'county_photo_preview')
    # Add the custom filter to the admin UI
    list_filter = (FirstLetterFilter,)
    # Enable searching by county name
    search_fields = ('county_name',)

    # Define a method that returns a preview of the county photo in the admin UI
    def county_photo_preview(self, obj):
        # If a photo is present, display a thumbnail
        if obj.county_photo:
            return format_html('<img src="{}" height="50" />'.format(obj.county_photo.url))
        # If no photo is present, display a placeholder
        else:
            return "-"
    # Set a user-friendly name for the county photo preview column
    county_photo_preview.short_description = "Photo Preview"


@admin.register(Cover)
class CoverAdmin(admin.ModelAdmin):
    # Define the fields to display in the change list
    list_display = ('cover_title', 'cover_text',
                    'cover_photo', 'cover_photo_preview')

    # Define whether the add permission should be granted
    def has_add_permission(self, request):
        # Only allow adding a Cover if there are no existing covers in the database
        return Cover.objects.count() == 0

    # Define whether the delete permission should be granted
    def has_delete_permission(self, request, obj=None):
        # Only allow deleting a Cover if there is exactly one existing cover in the database
        return Cover.objects.count() == 1

    # Define what happens when a Cover is saved
    def save_model(self, request, obj, form, change):
        # If this is an update (change), delete all existing Cover objects
        if change:
            Cover.objects.all().delete()
        # Call the default save_model method to save the new Cover object
        super().save_model(request, obj, form, change)

    # Define a custom function to display a preview of the cover photo in the change list
    def cover_photo_preview(self, obj):
        if obj.cover_photo:
            # Return an HTML string containing the cover photo thumbnail
            return format_html('<img src="{}" height="50" />'.format(obj.cover_photo.url))
        else:
            # If there is no cover photo, return a dash
            return "-"
    # Set a custom name for the cover photo preview column
    cover_photo_preview.short_description = "Photo Preview"
