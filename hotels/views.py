from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from admin import RoomAdminForm

# Create your views here.

@require_GET
def get_roomtypes(request):
    hotel_id = request.GET.get('hotels_id')
    if hotel_id:
        choices = RoomAdminForm().get_roomtype_choices(hotel_id)
        return JsonResponse({'choices': choices})
    else:
        return JsonResponse({'choices': []})