from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import logout
from django.templatetags.static import static
from .models import Counties, Cover
from hotels.models import Hotels, HotelsImage
from blogs.models import Blogs

import random
from datetime import datetime


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

    # Extract amount of guests
    guests_parts = guests.split("·")
    guests_count = sum(int(part.split()[0]) for part in guests_parts)

    # Convert check-in and check-out strings to datetime objects
    checkin_date = datetime.strptime(checkin, '%d-%m-%Y').date()
    checkout_date = datetime.strptime(checkout, '%d-%m-%Y').date()

    # Create a Q object for searching hotels by destination and availability
    query = Q(hotel_county__county_name__contains=destination) & \
            Q(room__available=True) & \
            ~Q(room__bookings__check_in_date__lt=checkout_date, room__bookings__check_out_date__gt=checkin_date)


    # Filter hotels by destination
    hotels = Hotels.objects.filter(query)

    # Count number of hotels found
    num_hotels_found = hotels.count()

    # Calculate number of days of stay
    checkout_datetime = datetime.strptime(checkin, '%d-%m-%Y')
    checkin_datetime = datetime.strptime(checkout, '%d-%m-%Y')

    duration = checkin_datetime - checkout_datetime

    price_ranges = [
        {'value': '$0-$50', 'label': '$0 - $50', 'count': 0},
        {'value': '$50-$100', 'label': '$50 - $100', 'count': 0},
        {'value': '$100-$150', 'label': '$100 - $150', 'count': 0},
        {'value': '$150-$200', 'label': '$150 - $200', 'count': 0},
        {'value': '$200+', 'label': '$200+', 'count': 0},
    ]

    facilities  = [
        {'value': 'Free wifi', 'label': 'Free wifi', 'count': 0},
        {'value': 'Air Conditioning', 'label': 'Air Conditioning', 'count': 0},
        {'value': 'Parking available', 'label': 'Parking available', 'count': 0},
        {'value': 'Business Services', 'label': 'Business Services', 'count': 0},
        {'value': 'Swimming pool', 'label': 'Swimming pool', 'count': 0},
        {'value': 'Top rated in area', 'label': 'Top rated in area', 'count': 0},
        {'value': 'Flat-screen TV', 'label': 'Flat-screen TV', 'count': 0},
        {'value': '24-hour front desk', 'label': '24-hour front desk', 'count': 0},
        {'value': 'Non-smoking rooms', 'label': 'Non-smoking rooms', 'count': 0},
        {'value': 'Fitness center', 'label': 'Fitness center', 'count': 0},
        {'value': 'Room service', 'label': 'Room service', 'count': 0},
        {'value': 'Restaurant', 'label': 'Restaurant', 'count': 0},
        {'value': 'Pet friendly', 'label': 'Pet friendly', 'count': 0},
        {'value': 'Facilities for disabled guests', 'label': 'Facilities for disabled guests', 'count': 0},
        {'value': 'Room service', 'label': 'Room service', 'count': 0},
        {'value': 'Family rooms', 'label': 'Family rooms', 'count': 0},
        {'value': 'Airport shuttle', 'label': 'Airport shuttle', 'count': 0},
        {'value': 'Electric vehicle charging station', 'label': 'Electric vehicle charging station', 'count': 0},
        {'value': 'Free cancellation', 'label': 'Free cancellation', 'count': 0},
        {'value': 'Beach front', 'label': 'Beach front', 'count': 0},
        {'value': 'Hot tub/jacuzzi', 'label': 'Hot tub/jacuzzi', 'count': 0},
        {'value': 'Book without credit card', 'label': 'Book without credit card', 'count': 0},
        {'value': 'No prepayment', 'label': 'No prepayment', 'count': 0},
    ]

    activities = [
        {'value': 'Fishing', 'label': 'Fishing', 'count': 0},
        {'value': 'Hiking', 'label': 'Hiking', 'count': 0},
        {'value': 'Beach', 'label': 'Beach', 'count': 0},
        {'value': 'Cycling', 'label': 'Cycling', 'count': 0},
        {'value': 'Sauna', 'label': 'Sauna', 'count': 0},
        {'value': 'Night lights', 'label': 'Night lights', 'count': 0},
        {'value': 'Tennis', 'label': 'Tennis', 'count': 0},
        {'value': 'Yoga', 'label': 'Yoga', 'count': 0},
        {'value': 'Scuba diving', 'label': 'Scuba diving', 'count': 0},
        {'value': 'Rafting', 'label': 'Rafting', 'count': 0},
        {'value': 'Guided nature walks', 'label': 'Guided nature walks', 'count': 0},
        {'value': 'Skiing or snowboarding', 'label': 'Skiing or snowboarding', 'count': 0},
        {'value': 'Golfing', 'label': 'Golfing', 'count': 0},
        {'value': 'Surfing', 'label': 'Surfing', 'count': 0},
    ]

    hotel_results = []

    for hotel in hotels:
        rooms = hotel.room_set.all()
        total_capacity = sum(room.max_guests for room in rooms)
        if guests_count <= total_capacity:
            cheapest_room = hotel.hotel_rooms.order_by('price_per_night').first()
            price_per_night = cheapest_room.price_per_night if cheapest_room else 0
            num_days = (datetime.strptime(checkout, '%d-%m-%Y') -
                        datetime.strptime(checkin, '%d-%m-%Y')).days
    
            price_discount = cheapest_room.price_discount if cheapest_room else 0
            special_discount = cheapest_room.special_discount if cheapest_room else 0
    
            total_price = price_per_night * num_days
    
            if price_discount != 0:
                total_price_with_discount = total_price - total_price/100*price_discount
            else:
                total_price_with_discount = 0
    
            hotel_search_info = hotel.hotel_search_info.first()


            # Create a dictionary for each hotel's result
            hotel_result = {
                'hotel_search_info_title': hotel_search_info.hotel_search_info_title,
                'hotel_search_info_text': hotel_search_info.hotel_search_info_text,
                'hotel_name': hotel.hotel_name,
                'hotel_type': hotel.hotel_type,
                'hotel_cover_photo': hotel.hotel_cover_photo,
                'price_per_night': price_per_night,
                'total_price': total_price,
                'total_price_with_discount': total_price_with_discount,
                'price_discount': price_discount,
                'special_discount': special_discount,
                'facilities': {
                    'Free wifi': hotel.hotel_facilities.first().hotel_has_free_wifi if hotel.hotel_facilities.exists() else False,
                    'Air Conditioning': hotel.hotel_facilities.first().hotel_has_air_conditioning if hotel.hotel_facilities.exists() else False,
                    'Parking available': hotel.hotel_facilities.first().hotel_has_parking_available if hotel.hotel_facilities.exists() else False,
                    'Business Services': hotel.hotel_facilities.first().hotel_has_business_services if hotel.hotel_facilities.exists() else False,
                    'Swimming pool': hotel.hotel_facilities.first().hotel_has_swimming_pool if hotel.hotel_facilities.exists() else False,
                    'Top rated in area': hotel.hotel_facilities.first().hotel_has_top_rated_in_area if hotel.hotel_facilities.exists() else False,
                    'Flat-screen TV': hotel.hotel_facilities.first().hotel_has_flat_screen_tv if hotel.hotel_facilities.exists() else False,
                    '24-hour front desk': hotel.hotel_facilities.first().hotel_has_24_hour_front_desk if hotel.hotel_facilities.exists() else False,
                    'Non-smoking rooms': hotel.hotel_facilities.first().hotel_has_non_smoking_rooms if hotel.hotel_facilities.exists() else False,
                    'Fitness center': hotel.hotel_facilities.first().hotel_has_fitness_center if hotel.hotel_facilities.exists() else False,
                    'Room service': hotel.hotel_facilities.first().hotel_has_room_service if hotel.hotel_facilities.exists() else False,
                    'Restaurant': hotel.hotel_facilities.first().hotel_has_restaurant if hotel.hotel_facilities.exists() else False,
                    'Pet friendly': hotel.hotel_facilities.first().hotel_is_pet_friendly if hotel.hotel_facilities.exists() else False,
                    'Facilities for disabled guests': hotel.hotel_facilities.first().hotel_has_facilities_for_disabled_guests if hotel.hotel_facilities.exists() else False,
                    'Family rooms': hotel.hotel_facilities.first().hotel_has_family_rooms if hotel.hotel_facilities.exists() else False,
                    'Spa': hotel.hotel_facilities.first().hotel_has_spa if hotel.hotel_facilities.exists() else False,
                    'Airport shuttle': hotel.hotel_facilities.first().hotel_has_airport_shuttle if hotel.hotel_facilities.exists() else False,
                    'Electric vehicle charging station': hotel.hotel_facilities.first().hotel_has_electric_vehicle_charging_station if hotel.hotel_facilities.exists() else False,
                    'Free cancellation': hotel.hotel_facilities.first().hotel_has_free_cancellation if hotel.hotel_facilities.exists() else False,
                    'Beach front': hotel.hotel_facilities.first().hotel_has_beach_front if hotel.hotel_facilities.exists() else False,
                    'Hot tub/jacuzzi': hotel.hotel_facilities.first().hotel_has_jacuzzi if hotel.hotel_facilities.exists() else False,
                    'Book without credit card': hotel.hotel_facilities.first().hotel_has_without_credit_card if hotel.hotel_facilities.exists() else False,
                    'No prepayment': hotel.hotel_facilities.first().hotel_has_no_prepayment if hotel.hotel_facilities.exists() else False,
                    },
                'activities': {
                    'Fishing': hotel.hotel_activities.first().hotel_has_fishing if hotel.hotel_activities.exists() else False,
                    'Hiking': hotel.hotel_activities.first().hotel_has_hiking if hotel.hotel_activities.exists() else False,
                    'Beach': hotel.hotel_activities.first().hotel_has_beach if hotel.hotel_activities.exists() else False,
                    'Cycling': hotel.hotel_activities.first().hotel_has_cycling if hotel.hotel_activities.exists() else False,
                    'Sauna': hotel.hotel_activities.first().hotel_has_sauna if hotel.hotel_activities.exists() else False,
                    'Night lights': hotel.hotel_activities.first().hotel_has_night_lights if hotel.hotel_activities.exists() else False,
                    'Tennis': hotel.hotel_activities.first().hotel_has_tennis if hotel.hotel_activities.exists() else False,
                    'Yoga': hotel.hotel_activities.first().hotel_has_yoga if hotel.hotel_activities.exists() else False,
                    'Scuba diving': hotel.hotel_activities.first().hotel_has_scuba_diving if hotel.hotel_activities.exists() else False,
                    'Rafting': hotel.hotel_activities.first().hotel_has_rafting if hotel.hotel_activities.exists() else False,
                    'Guided nature walks': hotel.hotel_activities.first().hotel_has_guided_nature_walks if hotel.hotel_activities.exists() else False,
                    'Skiing or snowboarding': hotel.hotel_activities.first().hotel_has_skiing if hotel.hotel_activities.exists() else False,
                    'Golfing': hotel.hotel_activities.first().hotel_has_golfing if hotel.hotel_activities.exists() else False,
                    'Surfing': hotel.hotel_activities.first().hotel_has_surfing if hotel.hotel_activities.exists() else False,
                    },
                }
    
            # Append the dictionary to the list of hotel results
            hotel_results.append(hotel_result)

    for hotel_result in hotel_results:
        price_per_night = hotel_result['price_per_night']
        if price_per_night <= 50:
            price_ranges[0]['count'] += 1
        elif price_per_night <= 100:
            price_ranges[1]['count'] += 1
        elif price_per_night <= 150:
            price_ranges[2]['count'] += 1
        elif price_per_night <= 200:
            price_ranges[3]['count'] += 1
        else:
            price_ranges[4]['count'] += 1
    
        facilities_present = hotel_result['facilities']
        for facility in facilities:
            facility_value = facility['value']
            if facilities_present.get(facility_value, False):
                facility['count'] += 1
    
        activities_present = hotel_result['activities']
        for activity in activities:
            activity_value = activity['value']
            if activities_present.get(activity_value, False):
                activity['count'] += 1

    

    # Create a context dictionary with query parameters
    context = {
            'destination': destination,
            'num_hotels_found': num_hotels_found,
            'duration': duration.days,
            'checkin': checkin,
            'checkout': checkout,
            'guests': guests.split("·")[1].strip(),
            'price_ranges': price_ranges,
            'facilities': facilities,
            'activities': activities,
            'hotel_results': hotel_results
        }
    
    # Render the search results page with context
    return render(request, 'core/search_results.html', context)

def update_search_results(request):
    # Get the search parameters from the query parameters
    destination = request.GET.get('destination')
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')
    guests = request.GET.get('guests')
    hotel_name = request.GET.get('hotel_name')


     # Extract amount of guests
    guests_parts = guests.split("·")
    guests_count = sum(int(part.split()[0]) for part in guests_parts)

    # Convert check-in and check-out strings to datetime objects
    checkin_date = datetime.strptime(checkin, '%d-%m-%Y').date()
    checkout_date = datetime.strptime(checkout, '%d-%m-%Y').date()


    # Perform the database query based on the search parameters
    query = Q(hotel_county__county_name__contains=destination) & \
            Q(room__available=True) & \
            ~Q(room__bookings__check_in_date__lt=checkout_date, room__bookings__check_out_date__gt=checkin_date)

    if hotel_name:
        query &= Q(hotel_name__icontains=hotel_name)

    
     # Filter hotels by destination
    hotels = Hotels.objects.filter(query)

    # Count number of hotels found
    num_hotels_found = hotels.count()

    # Calculate number of days of stay
    checkout_datetime = datetime.strptime(checkin, '%d-%m-%Y')
    checkin_datetime = datetime.strptime(checkout, '%d-%m-%Y')

    duration = checkin_datetime - checkout_datetime

    price_ranges = [
        {'value': '$0-$50', 'label': '$0 - $50', 'count': 0},
        {'value': '$50-$100', 'label': '$50 - $100', 'count': 0},
        {'value': '$100-$150', 'label': '$100 - $150', 'count': 0},
        {'value': '$150-$200', 'label': '$150 - $200', 'count': 0},
        {'value': '$200+', 'label': '$200+', 'count': 0},
    ]

    facilities  = [
        {'value': 'Free wifi', 'label': 'Free wifi', 'count': 0},
        {'value': 'Air Conditioning', 'label': 'Air Conditioning', 'count': 0},
        {'value': 'Parking available', 'label': 'Parking available', 'count': 0},
        {'value': 'Business Services', 'label': 'Business Services', 'count': 0},
        {'value': 'Swimming pool', 'label': 'Swimming pool', 'count': 0},
        {'value': 'Top rated in area', 'label': 'Top rated in area', 'count': 0},
        {'value': 'Flat-screen TV', 'label': 'Flat-screen TV', 'count': 0},
        {'value': '24-hour front desk', 'label': '24-hour front desk', 'count': 0},
        {'value': 'Non-smoking rooms', 'label': 'Non-smoking rooms', 'count': 0},
        {'value': 'Fitness center', 'label': 'Fitness center', 'count': 0},
        {'value': 'Room service', 'label': 'Room service', 'count': 0},
        {'value': 'Restaurant', 'label': 'Restaurant', 'count': 0},
        {'value': 'Pet friendly', 'label': 'Pet friendly', 'count': 0},
        {'value': 'Facilities for disabled guests', 'label': 'Facilities for disabled guests', 'count': 0},
        {'value': 'Room service', 'label': 'Room service', 'count': 0},
        {'value': 'Family rooms', 'label': 'Family rooms', 'count': 0},
        {'value': 'Airport shuttle', 'label': 'Airport shuttle', 'count': 0},
        {'value': 'Electric vehicle charging station', 'label': 'Electric vehicle charging station', 'count': 0},
        {'value': 'Free cancellation', 'label': 'Free cancellation', 'count': 0},
        {'value': 'Beach front', 'label': 'Beach front', 'count': 0},
        {'value': 'Hot tub/jacuzzi', 'label': 'Hot tub/jacuzzi', 'count': 0},
        {'value': 'Book without credit card', 'label': 'Book without credit card', 'count': 0},
        {'value': 'No prepayment', 'label': 'No prepayment', 'count': 0},
    ]

    activities = [
        {'value': 'Fishing', 'label': 'Fishing', 'count': 0},
        {'value': 'Hiking', 'label': 'Hiking', 'count': 0},
        {'value': 'Beach', 'label': 'Beach', 'count': 0},
        {'value': 'Cycling', 'label': 'Cycling', 'count': 0},
        {'value': 'Sauna', 'label': 'Sauna', 'count': 0},
        {'value': 'Night lights', 'label': 'Night lights', 'count': 0},
        {'value': 'Tennis', 'label': 'Tennis', 'count': 0},
        {'value': 'Yoga', 'label': 'Yoga', 'count': 0},
        {'value': 'Scuba diving', 'label': 'Scuba diving', 'count': 0},
        {'value': 'Rafting', 'label': 'Rafting', 'count': 0},
        {'value': 'Guided nature walks', 'label': 'Guided nature walks', 'count': 0},
        {'value': 'Skiing or snowboarding', 'label': 'Skiing or snowboarding', 'count': 0},
        {'value': 'Golfing', 'label': 'Golfing', 'count': 0},
        {'value': 'Surfing', 'label': 'Surfing', 'count': 0},
    ]

    hotel_results = []

    for hotel in hotels:
        rooms = hotel.room_set.all()
        total_capacity = sum(room.max_guests for room in rooms)
        if guests_count <= total_capacity:
            cheapest_room = hotel.hotel_rooms.order_by('price_per_night').first()
            price_per_night = cheapest_room.price_per_night if cheapest_room else 0
            num_days = (datetime.strptime(checkout, '%d-%m-%Y') -
                        datetime.strptime(checkin, '%d-%m-%Y')).days
    
            price_discount = cheapest_room.price_discount if cheapest_room else 0
            special_discount = cheapest_room.special_discount if cheapest_room else 0
    
            total_price = price_per_night * num_days
    
            if price_discount != 0:
                total_price_with_discount = total_price - total_price/100*price_discount
            else:
                total_price_with_discount = 0
    
            hotel_search_info = hotel.hotel_search_info.first()

            hotel_cover_photo_url = hotel.hotel_cover_photo.url
    
            # Create a dictionary for each hotel's result

            hotel_result = {
                'hotel_search_info_title': hotel_search_info.hotel_search_info_title,
                'hotel_search_info_text': hotel_search_info.hotel_search_info_text,
                'hotel_name': hotel.hotel_name,
                'hotel_type': hotel.hotel_type,
                'hotel_cover_photo': hotel_cover_photo_url,
                'price_per_night': price_per_night,
                'total_price': total_price,
                'total_price_with_discount': total_price_with_discount,
                'price_discount': price_discount,
                'special_discount': special_discount,
                'facilities': {
                    'Free wifi': hotel.hotel_facilities.first().hotel_has_free_wifi if hotel.hotel_facilities.exists() else False,
                    'Air Conditioning': hotel.hotel_facilities.first().hotel_has_air_conditioning if hotel.hotel_facilities.exists() else False,
                    'Parking available': hotel.hotel_facilities.first().hotel_has_parking_available if hotel.hotel_facilities.exists() else False,
                    'Business Services': hotel.hotel_facilities.first().hotel_has_business_services if hotel.hotel_facilities.exists() else False,
                    'Swimming pool': hotel.hotel_facilities.first().hotel_has_swimming_pool if hotel.hotel_facilities.exists() else False,
                    'Top rated in area': hotel.hotel_facilities.first().hotel_has_top_rated_in_area if hotel.hotel_facilities.exists() else False,
                    'Flat-screen TV': hotel.hotel_facilities.first().hotel_has_flat_screen_tv if hotel.hotel_facilities.exists() else False,
                    '24-hour front desk': hotel.hotel_facilities.first().hotel_has_24_hour_front_desk if hotel.hotel_facilities.exists() else False,
                    'Non-smoking rooms': hotel.hotel_facilities.first().hotel_has_non_smoking_rooms if hotel.hotel_facilities.exists() else False,
                    'Fitness center': hotel.hotel_facilities.first().hotel_has_fitness_center if hotel.hotel_facilities.exists() else False,
                    'Room service': hotel.hotel_facilities.first().hotel_has_room_service if hotel.hotel_facilities.exists() else False,
                    'Restaurant': hotel.hotel_facilities.first().hotel_has_restaurant if hotel.hotel_facilities.exists() else False,
                    'Pet friendly': hotel.hotel_facilities.first().hotel_is_pet_friendly if hotel.hotel_facilities.exists() else False,
                    'Facilities for disabled guests': hotel.hotel_facilities.first().hotel_has_facilities_for_disabled_guests if hotel.hotel_facilities.exists() else False,
                    'Family rooms': hotel.hotel_facilities.first().hotel_has_family_rooms if hotel.hotel_facilities.exists() else False,
                    'Spa': hotel.hotel_facilities.first().hotel_has_spa if hotel.hotel_facilities.exists() else False,
                    'Airport shuttle': hotel.hotel_facilities.first().hotel_has_airport_shuttle if hotel.hotel_facilities.exists() else False,
                    'Electric vehicle charging station': hotel.hotel_facilities.first().hotel_has_electric_vehicle_charging_station if hotel.hotel_facilities.exists() else False,
                    'Free cancellation': hotel.hotel_facilities.first().hotel_has_free_cancellation if hotel.hotel_facilities.exists() else False,
                    'Beach front': hotel.hotel_facilities.first().hotel_has_beach_front if hotel.hotel_facilities.exists() else False,
                    'Hot tub/jacuzzi': hotel.hotel_facilities.first().hotel_has_jacuzzi if hotel.hotel_facilities.exists() else False,
                    'Book without credit card': hotel.hotel_facilities.first().hotel_has_without_credit_card if hotel.hotel_facilities.exists() else False,
                    'No prepayment': hotel.hotel_facilities.first().hotel_has_no_prepayment if hotel.hotel_facilities.exists() else False,
                    },
                'activities': {
                    'Fishing': hotel.hotel_activities.first().hotel_has_fishing if hotel.hotel_activities.exists() else False,
                    'Hiking': hotel.hotel_activities.first().hotel_has_hiking if hotel.hotel_activities.exists() else False,
                    'Beach': hotel.hotel_activities.first().hotel_has_beach if hotel.hotel_activities.exists() else False,
                    'Cycling': hotel.hotel_activities.first().hotel_has_cycling if hotel.hotel_activities.exists() else False,
                    'Sauna': hotel.hotel_activities.first().hotel_has_sauna if hotel.hotel_activities.exists() else False,
                    'Night lights': hotel.hotel_activities.first().hotel_has_night_lights if hotel.hotel_activities.exists() else False,
                    'Tennis': hotel.hotel_activities.first().hotel_has_tennis if hotel.hotel_activities.exists() else False,
                    'Yoga': hotel.hotel_activities.first().hotel_has_yoga if hotel.hotel_activities.exists() else False,
                    'Scuba diving': hotel.hotel_activities.first().hotel_has_scuba_diving if hotel.hotel_activities.exists() else False,
                    'Rafting': hotel.hotel_activities.first().hotel_has_rafting if hotel.hotel_activities.exists() else False,
                    'Guided nature walks': hotel.hotel_activities.first().hotel_has_guided_nature_walks if hotel.hotel_activities.exists() else False,
                    'Skiing or snowboarding': hotel.hotel_activities.first().hotel_has_skiing if hotel.hotel_activities.exists() else False,
                    'Golfing': hotel.hotel_activities.first().hotel_has_golfing if hotel.hotel_activities.exists() else False,
                    'Surfing': hotel.hotel_activities.first().hotel_has_surfing if hotel.hotel_activities.exists() else False,
                    },
                }
    
            # Append the dictionary to the list of hotel results
            hotel_results.append(hotel_result)

    for hotel_result in hotel_results:
        price_per_night = hotel_result['price_per_night']
        if price_per_night <= 50:
            price_ranges[0]['count'] += 1
        elif price_per_night <= 100:
            price_ranges[1]['count'] += 1
        elif price_per_night <= 150:
            price_ranges[2]['count'] += 1
        elif price_per_night <= 200:
            price_ranges[3]['count'] += 1
        else:
            price_ranges[4]['count'] += 1
    
        facilities_present = hotel_result['facilities']
        for facility in facilities:
            facility_value = facility['value']
            if facilities_present.get(facility_value, False):
                facility['count'] += 1
    
        activities_present = hotel_result['activities']
        for activity in activities:
            activity_value = activity['value']
            if activities_present.get(activity_value, False):
                activity['count'] += 1
    


    for hotel_result in hotel_results:
        price_per_night = hotel_result['price_per_night']
        if price_per_night <= 50:
            price_ranges[0]['count'] += 1
        elif price_per_night <= 100:
            price_ranges[1]['count'] += 1
        elif price_per_night <= 150:
            price_ranges[2]['count'] += 1
        elif price_per_night <= 200:
            price_ranges[3]['count'] += 1
        else:
            price_ranges[4]['count'] += 1
    
        facilities_present = hotel_result['facilities']
        for facility in facilities:
            facility_value = facility['value']
            if facilities_present.get(facility_value, False):
                facility['count'] += 1
    
        activities_present = hotel_result['activities']
        for activity in activities:
            activity_value = activity['value']
            if activities_present.get(activity_value, False):
                activity['count'] += 1
    

    # Create a context dictionary with query parameters
    context = {
            'destination': destination,
            'num_hotels_found': num_hotels_found,
            'duration': duration.days,
            'checkin': checkin,
            'checkout': checkout,
            'guests': guests.split("·")[1].strip(),
            'price_ranges': price_ranges,
            'facilities': facilities,
            'activities': activities,
            'hotel_results': hotel_results
        }

    # Return the search results as JSON response
    return JsonResponse(context)




    # Return the search results as JSON response
    return JsonResponse(context)
