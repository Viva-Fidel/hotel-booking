from django.shortcuts import render
from django.db.models import Count, Q
from django.http import JsonResponse

from .models import Countries
from hotel_list.models import Hotel_list
from blog.models import Blog_post

import random

# Create your views here.


from django.db.models import Count

import random

def index(request):
    # get a list of all available countries
    available_countries = Hotel_list.objects.values_list('hotel_country__country_name', flat=True).distinct()
    
    # randomly select 4 unique countries
    selected_countries = random.sample(list(available_countries), 4)

    # create a dictionary to hold the hotel count and country photos
    available_destinations = {}
    
    # loop through selected countries to get hotel count and country photo
    for country_name in selected_countries:
        # get the country object for the selected country
        country = Countries.objects.get(country_name=country_name)
        
        # get the count of hotels for the selected country
        hotel_count = Hotel_list.objects.filter(hotel_country=country).count()
        
        # get the country photo for the selected country
        country_photo = country.country_photo
        
        # add the hotel count and country photo to the dictionary
        available_destinations[country] = {'hotel_count': hotel_count, 'country_photo': country_photo}
    

    # get the latest 3 published blog posts
    blog_info = Blog_post.objects.filter(is_published=True).order_by('-time_create')[:3]

    context = {'available_destinations': available_destinations, 'blog_info': blog_info}
    
    return render(request, 'core/index.html', context)







def search_address(request):
    address = request.GET.get('address')
    payload = []

    if address:
        real_addresses = Hotel_list.objects.filter(hotel_country__icontains = address)[:5]

        for real_address in real_addresses:
            payload.append(real_address.hotel_country)

    return JsonResponse({'status': 200, 'data': payload})

def search_hotels(request):
    destination = request.GET.get('destination')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    guests = request.GET.get('guests')

    query = Q(hotel_country__icontains=destination)
    hotels = Hotel_list.objects.filter(query)

    context = {
        'destination': destination,
    }

    return render(request, 'core/search_results.html', context)
