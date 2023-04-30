from django.shortcuts import render
from django.db.models import Count, Q
from django.http import JsonResponse

from .models import Countries, CoverPhoto
from hotels.models import Hotels, HotelsImage
from blogs.models import Blogs

import random


# Create your views here.

def index(request):
    available_countries = Hotels.objects.values_list(
        'hotel_country__country_name', flat=True).distinct()

    selected_countries = random.sample(list(available_countries), 4)

    available_destinations = {}

    for country_name in selected_countries:

        country = Countries.objects.get(country_name=country_name)

        hotel_count = Hotels.objects.filter(hotel_country=country).count()

        country_photo = country.country_photo

        available_destinations[country] = {
            'hotel_count': hotel_count, 'country_photo': country_photo}

    blog_info = Blogs.objects.filter(
        is_published=True).order_by('-time_create')[:3]
    
    popular_hotels = Hotels.objects.filter(is_published=True).order_by('-hotel_popularity')[:4]
    popular_hotels_images = {}
    for hotel in popular_hotels:
        popular_hotels_images[hotel.id] = HotelsImage.objects.filter(hotel=hotel)
    

    cover_photo = CoverPhoto.objects.first()

    context = {'available_destinations': available_destinations,
               'popular_hotels': popular_hotels,
               'popular_hotels_images': popular_hotels_images,
               'blog_info': blog_info,
               'cover_photo': cover_photo}

    return render(request, 'core/index.html', context)


def search_address(request):
    address = request.GET.get('address')
    payload = []

    if address:
        real_addresses = Countries.objects.filter(
            country_name__icontains=address)[:5]

        for real_address in real_addresses:
            payload.append(real_address.country_name)

    return JsonResponse({'status': 200, 'data': payload})


def search_hotels(request):
    destination = request.GET.get('destination')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    guests = request.GET.get('guests')

    query = Q(hotel_country__country_name__contains=destination)
    hotels = Hotels.objects.filter(query)

    context = {
        'destination': destination,
        'checkin': checkin,
        'checkout': checkout,
        'guests': guests,
    }

    return render(request, 'core/search_results.html', context)
