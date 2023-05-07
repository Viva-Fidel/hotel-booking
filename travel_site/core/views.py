from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import logout
from .models import Counties, Cover
from hotels.models import Hotels, HotelsImage
from blogs.models import Blogs

import random


# Create your views here.

def index(request):
    # Get a list of unique county names from the Hotels model
    counties = Hotels.objects.values_list(
        'hotel_county__county_name', flat=True).distinct()

    # Choose 4 random county names from the unique list
    selected_counties = random.sample(list(counties), 4)

    # Create a dictionary to store the data for each random county
    random_counties_list = {}

    # Loop through the selected counties
    for county_name in selected_counties:

        # Get the County object for the current county name
        county = Counties.objects.get(county_name=county_name)

        # Get the number of hotels in the current county
        hotel_count = Hotels.objects.filter(hotel_county=county).count()

        # Get the county photo for the current county
        county_photo = county.county_photo

        # Add the current county's data to the random_counties_list dictionary
        random_counties_list[county] = {
            'hotel_count': hotel_count, 'county_photo': county_photo}

    # Get the latest 3 published blog posts
    blog_info = Blogs.objects.filter(
        is_published=True).order_by('-time_create')[:3]

    # Get the 4 most popular published hotels
    popular_hotels = Hotels.objects.filter(
        is_published=True).order_by('-hotel_popularity')[:4]

    # Create a dictionary to store the images for each popular hotel
    popular_hotels_images = {}
    for hotel in popular_hotels:
        # Get all images for the current hotel
        popular_hotels_images[hotel.id] = HotelsImage.objects.filter(
            hotel=hotel)

    # Get the first Cover object (if any)
    cover = Cover.objects.first()

    # Create a dictionary to pass to the index.html template
    context = {'random_counties_list': random_counties_list,
               'popular_hotels': popular_hotels,
               'popular_hotels_images': popular_hotels_images,
               'blog_info': blog_info,
               'cover': cover}

    # Render the index.html template with the context dictionary
    return render(request, 'core/index.html', context)


def logout_view(request):
    # Log out the user
    logout(request)
    # Redirect the user to the home page
    return redirect('home')


def search_address(request):
    # Get the search query from the GET request
    address = request.GET.get('address')

    # Initialize an empty list to store the real addresses
    payload = []

    # Check if the search query is not empty
    if address:
        # Filter the counties that contain the search query in their name
        real_addresses = Counties.objects.filter(
            county_name__icontains=address)[:5]

        # Add the county names to the payload list
        for real_address in real_addresses:
            payload.append(real_address.county_name)

    # Return a JSON response with the status code and payload data
    return JsonResponse({'status': 200, 'data': payload})


def search_hotels(request):
    # Get query parameters from request
    destination = request.GET.get('destination')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    guests = request.GET.get('guests')

    # Create a Q object for searching hotels by destination
    query = Q(hotel_county__county_name__contains=destination)

    # Filter hotels by destination
    hotels = Hotels.objects.filter(query)

    # Create a context dictionary with query parameters
    context = {
        'destination': destination,
        'checkin': checkin,
        'checkout': checkout,
        'guests': guests,
    }

    # Render the search results page with context
    return render(request, 'core/search_results.html', context)
