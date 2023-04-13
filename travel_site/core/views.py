from django.shortcuts import render
from django.db.models import Count
from django.http import JsonResponse
from hotel_list.models import Hotel_list
from blog.models import Blog_post

import random

# Create your views here.


def index(request):
    hotel_countries = Hotel_list.objects.filter(
        is_published=True).values_list('hotel_country', flat=True).distinct()
    random_countries = random.sample(list(hotel_countries), 4)

    destinations = Hotel_list.objects.filter(
        is_published=True, hotel_country__in=random_countries)
    counts = destinations.values('hotel_country').annotate(
        count=Count('id')).order_by('-count')

    available_destinations = []
    for country in random_countries:
        count = counts.filter(hotel_country=country).first()['count']
        available_destinations.append({'country': country, 'count': count})

    blog_info = Blog_post.objects.filter(
        is_published=True).order_by('-time_create')[:3]

    context = {'available_destinations': available_destinations,
               'blog_info': blog_info,
               }

    return render(request, 'core/index.html', context)


def search_address(request):
    address = request.GET.get('address')
    payload = []

    if address:
        real_addresses = Hotel_list.objects.filter(hotel_country__icontains = address)

        for real_address in real_addresses:
            payload.append(real_address.hotel_country)

    return JsonResponse({'status': 200, 'data': payload})

def search_hotels(request):
    if request.method == 'POST':
        destination = request.POST.get('destination')
        checkin_date = request.POST.get('checkin')
        checkout_date = request.POST.get('checkout')
        num_guests = request.POST.get('guests')

        # Use the form inputs to search for hotels
        hotels = Hotel_list.objects.filter(destination=destination, checkin_date=checkin_date,
                                       checkout_date=checkout_date, num_guests=num_guests)

        # Pass the search results to the template
        context = {'hotels': hotels}
        return render(request, 'hotel_search_results.html', context)

    # If the request method is not POST, render the search form
    return render(request, 'hotel_search.html')