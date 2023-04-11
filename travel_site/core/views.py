from django.shortcuts import render
from django.db.models import Count
from hotel_list.models import Hotel_list

import random

# Create your views here.


def index(request):
    hotel_countries = Hotel_list.objects.filter(
        is_published=True).values_list('hotel_country', flat=True).distinct()
    random_countries = random.sample(list(hotel_countries), 4)

    destinations = Hotel_list.objects.filter(is_published=True, hotel_country__in=random_countries)
    counts = destinations.values('hotel_country').annotate(count=Count('id')).order_by('-count')

    available_destinations = []
    for country in random_countries:
        count = counts.filter(hotel_country=country).first()['count']
        available_destinations.append({'country': country, 'count': count})
   
    random_countries = random.sample(list(hotel_countries), 3)

    available_destinations2 = []
    for country in random_countries:
        count = counts.filter(hotel_country=country).first()['count']
        available_destinations2.append({'country': country, 'count': count})



    context = {'available_destinations': available_destinations,
               'available_destinations2': available_destinations2,
               }
    

    return render(request, 'core/index.html', context)
