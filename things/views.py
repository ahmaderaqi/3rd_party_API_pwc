from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
import requests
from django.utils import timezone
from .models import Event,Flight
import math

def event_list_view(request):
    
    
    country = request.GET.get('country')
    
    
    try:
        event = Event.objects.get(country=country)
        if timezone.now() - event.last_updated <= timezone.timedelta(hours=6):
            return JsonResponse(event.data, safe=False)
    except Event.DoesNotExist:
        pass
    
    # Make the API request with the country query parameter
    response = requests.get(
        url="https://api.predicthq.com/v1/events/",
        headers={
            "Authorization": "Bearer EqpJf87ypBIW6cbbhkXRj_HOyxkNezMRw66NdI86",
            "Accept": "application/json"
        },
        params={
            "country": country,
            "rank": "rank"  # Sort events by rank
        }
    )
    
    # Extract the top 10 events from the API response
    if response.status_code == 200:
        events = response.json().get('results', [])[:10]
    else:
        events = []
    
    # Save the data in the database for future queries
    Event.objects.update_or_create(
        country_code=country,
        defaults={
            'data': events,
        }
    )
    
    # Return the list of events as JSON response
    return JsonResponse(events, safe=False)


def weather_view(request):
    event_id = request.GET.get('id')
    
    try:
        event = Event.objects.get(id=event_id)
        
        # Check if weather data is already available for the event and not more than 6 hours old
        if event.temperature is not None and event.humidity is not None and timezone.now() - event.last_updated <= timezone.timedelta(hours=6):
            return JsonResponse({
                'temperature': event.temperature,
                'humidity': event.humidity
            })
        
        # Retrieve the latitude and longitude of the event
        lat = event.location[1]
        lon = event.location[0]
        
        
        api_key = 'f22892654725839a44ff6db985f0b151'
        url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=part&appid={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            weather_data = response.json()
            # Extract the required weather information from the response
            temperature = weather_data['current']['temp']
            humidity = weather_data['current']['humidity']
            
            
            event.temperature = temperature
            event.humidity = humidity
            event.save()
            
            return JsonResponse({
                'temperature': temperature,
                'humidity': humidity
            })
        
    except Event.DoesNotExist:
        pass
    
    return JsonResponse({'error': 'Event not found or failed to fetch weather data'})


def flights_view(request):
    event_id = request.GET.get('eventId')
    user_airport_code = request.GET.get('reg_number')

    try:
        event = Event.objects.get(id=event_id)

        # Check if flights data is already available and not more than 6 hours old
        flights = Flight.objects.filter(event=event)
        if flights.exists() and (timezone.now() - flights.first().last_updated).seconds < 21600:
            # Retrieve flights from the database
            flights_data = list(flights.values())
        else:
            # Retrieve the latitude and longitude of the event
            event_lat = event.latitude
            event_lon = event.longitude

            # Make a call to the AirLabs flights API
            api_key = '1c211297-65e3-4ada-b6ed-73f7c25e2391'
            url = f"https://airlabs.co/api/v9/flights?api_key={api_key}"
            response = requests.get(url)

            if response.status_code == 200:
                flights_data = response.json()
                # Process and filter the flights data based on event location and user's airport code

                # Example: Filtering flights within 200km of the event location
                filtered_flights = []
                for flight in flights_data:
                    if calculate_distance(event_lat, event_lon, flight['lat'], flight['lng']) <= 200:
                        filtered_flights.append(flight)

                # Example: Filtering flights based on user's airport code
                user_flights = [flight for flight in filtered_flights if flight['departure_airport_code'] == user_airport_code]

                # Save flights data to the database for future requests
                Flight.objects.filter(event=event).delete()  # Delete existing flights for the event
                Flight.objects.bulk_create([Flight(event=event, **flight_data) for flight_data in user_flights])

                flights_data = user_flights

        return JsonResponse({
            'flights': flights_data
        })

    except Event.DoesNotExist:
        pass

    return JsonResponse({'error': 'Event not found or failed to fetch flights data'})




def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate the differences in latitude and longitude
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Apply the Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance

