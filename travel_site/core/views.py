from django.shortcuts import render, redirect
from django.db.models import Count, Q
from django.http import JsonResponse

from .models import Counties, Cover
from hotels.models import Hotels, HotelsImage
from blogs.models import Blogs
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test

import random


# Create your views here.

def index(request):
    available_counties = Hotels.objects.values_list(
        'hotel_county__county_name', flat=True).distinct()

    selected_counties = random.sample(list(available_counties), 4)

    available_destinations = {}

    for county_name in selected_counties:

        county = Counties.objects.get(county_name=county_name)

        hotel_count = Hotels.objects.filter(hotel_county=county).count()

        county_photo = county.county_photo

        available_destinations[county] = {
            'hotel_count': hotel_count, 'county_photo': county_photo}

    blog_info = Blogs.objects.filter(
        is_published=True).order_by('-time_create')[:3]
    
    popular_hotels = Hotels.objects.filter(is_published=True).order_by('-hotel_popularity')[:4]
    popular_hotels_images = {}
    for hotel in popular_hotels:
        popular_hotels_images[hotel.id] = HotelsImage.objects.filter(hotel=hotel)
    

    cover = Cover.objects.first()

    context = {'available_destinations': available_destinations,
               'popular_hotels': popular_hotels,
               'popular_hotels_images': popular_hotels_images,
               'blog_info': blog_info,
               'cover': cover}

    return render(request, 'core/index.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')


def search_address(request):
    address = request.GET.get('address')
    payload = []

    if address:
        real_addresses = Counties.objects.filter(
            county_name__icontains=address)[:5]

        for real_address in real_addresses:
            payload.append(real_address.county_name)

    return JsonResponse({'status': 200, 'data': payload})


def search_hotels(request):
    destination = request.GET.get('destination')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    guests = request.GET.get('guests')

    query = Q(hotel_county__county_name__contains=destination)
    hotels = Hotels.objects.filter(query)

    context = {
        'destination': destination,
        'checkin': checkin,
        'checkout': checkout,
        'guests': guests,
    }

    return render(request, 'core/search_results.html', context)
