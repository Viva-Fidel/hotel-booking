from django.shortcuts import get_object_or_404, render
from .models import Hotels

import random


def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotels, slug=slug)
    facilities = hotel.hotel_facilities.all()

    facility_data = []

    hotel.hotel_popularity += 1
    hotel.save()

    for facility in facilities:
        if facility.hotel_has_free_wifi:
            facility_data.append({'name': 'Free wifi', 'icon': '/static/images/hotels/icons/hotel_has_free_wifi.png'})
        if facility.hotel_has_air_conditioning:
            facility_data.append({'name': 'Air Conditioning', 'icon': '/static/images/hotels/icons/hotel_has_air_conditioning'})
        if facility.hotel_has_parking_available:
            facility_data.append({'name': 'Parking available', 'icon': '/static/images/hotels/icons/hotel_has_parking_available.png'})
        if facility.hotel_has_business_services:
            facility_data.append({'name': 'Business Services', 'icon': '/static/images/hotels/icons/hotel_has_business_services.png'})
        if facility.hotel_has_swimming_pool:
            facility_data.append({'name': 'Swimming pool', 'icon': '/static/images/hotels/icons/hotel_has_swimming_pool.png'})
        if facility.hotel_has_top_rated_in_area:
            facility_data.append({'name': 'Top rated in area', 'icon': '/static/images/hotels/icons/hotel_has_top_rated_in_area.png'})
        if facility.hotel_has_flat_screen_tv:
            facility_data.append({'name': 'Flat-screen TV', 'icon': '/static/images/hotels/icons/hotel_has_flat_screen_tv.png'})
        if facility.hotel_has_24_hour_front_desk:
            facility_data.append({'name': '24-hour front desk', 'icon': '/static/images/hotels/icons/hotel_has_24_hour_front_desk.png'})
        if facility.hotel_has_non_smoking_rooms:
            facility_data.append({'name': 'Non-smoking rooms', 'icon': '/static/images/hotels/icons/hotel_has_non_smoking_rooms.png'})
        if facility.hotel_has_fitness_center:
            facility_data.append({'name': 'Fitness center', 'icon': '/static/images/hotels/icons/hotel_has_fitness_center.png'})
        if facility.hotel_has_room_service:
            facility_data.append({'name': 'Room service', 'icon': '/static/images/hotels/icons/hotel_has_room_service.png'})
        if facility.hotel_has_restaurant:
            facility_data.append({'name': 'Restaurant', 'icon': '/static/images/hotels/icons/hotel_has_restaurant.png'})
        if facility.hotel_has_pet_friendly:
            facility_data.append({'name': 'Pet friendly', 'icon': '/static/images/hotels/icons/hotel_has_pet_friendly.png'})
        if facility.hotel_has_facilities_for_disabled_guests:
            facility_data.append({'name': 'Facilities for disabled guests', 'icon': '/static/images/hotels/icons/hotel_has_facilities_for_disabled_guests.png'})
        if facility.hotel_has_family_rooms:
            facility_data.append({'name': 'Family rooms', 'icon': '/static/images/hotels/icons/hotel_has_family_rooms.png'})
        if facility.hotel_has_spa:
            facility_data.append({'name': 'Spa', 'icon': '/static/images/hotels/icons/hotel_has_spa.png'})
        if facility.hotel_has_airport_shuttle:
            facility_data.append({'name': 'Airport shuttle', 'icon': '/static/images/hotels/icons/hotel_has_airport_shuttle.png'})
        if facility.hotel_has_electric_vehicle_charging_station:
            facility_data.append({'name': 'Electric vehicle charging station', 'icon': '/static/images/hotels/icons/hotel_has_electric_vehicle_charging_station.png'})
        if facility.hotel_has_free_cancellation:
            facility_data.append({'name': 'Free cancellation', 'icon': '/static/images/hotels/icons/hotel_has_free_cancellation.png'})
        if facility.hotel_has_beach_front:
            facility_data.append({'name': 'Beach front', 'icon': '/static/images/hotels/icons/hotel_has_beach_front.png'})
        if facility.hotel_has_jacuzzi:
            facility_data.append({'name': 'Hot tub/jacuzzi', 'icon': '/static/images/hotels/icons/hotel_has_jacuzzi.png'})
        if facility.hotel_has_without_credit_card:
            facility_data.append({'name': 'Book without credit card', 'icon': '/static/images/hotels/icons/hotel_has_without_credit_card.png'})
        if facility.hotel_has_no_prepayment:
            facility_data.append({'name': 'No prepayment', 'icon': '/static/images/hotels/icons/hotel_has_no_prepayment.png'})
    
    if len(facility_data) > 6:
        facility_data = random.sample(facility_data, 6)
    
    address = str(hotel.hotel_street)+ ", " + str(hotel.hotel_city) + ", " + str(hotel.hotel_county) + " OR" 

    context = {'hotel': hotel, 
               'facility_data': facility_data, 
               'address': address,
            }
    return render(request, 'hotels/hotel_detail.html', context)