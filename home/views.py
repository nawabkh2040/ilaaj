from django.shortcuts import render, HttpResponse, redirect
import requests
from django.http import JsonResponse
from home.token import *
# Create your views here.
import requests
from home.models import *
from datetime import datetime
from django.contrib.auth import authenticate, login , logout


from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance in kilometers between two sets of coordinates.
    """
    R = 6371  # Earth's radius in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def get_coordinates(city):
    access_token = token_key  
    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{city}.json?country=in&access_token={access_token}'
    response = requests.get(url)
    data = response.json()
    if 'features' in data and data['features']:
        latitude = data['features'][0]['center'][1]
        longitude = data['features'][0]['center'][0]
        return latitude, longitude
    else:
        return None, None

def home(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        search = request.POST.get('search')
        user_latitude, user_longitude = get_coordinates(city=city)

        if user_latitude is not None and user_longitude is not None:
            print(f"City: {city}, Search: {search}, Latitude: {user_latitude}, Longitude: {user_longitude}")
            nearby_services = []  # List to store nearby services with hospital names

            # Find hospitals with matching services and calculate distance
            for hospital in Hospital.objects.all():
                matching_services = hospital.services.filter(name__icontains=search)
                if matching_services.exists():
                    distance_km = calculate_distance(user_latitude, user_longitude, hospital.latitude, hospital.longitude)
                    if distance_km <= 20:
                        for service in matching_services:
                            nearby_services.append((service, hospital, distance_km))  # Add service name, hospital name, and distance
            # Sort by distance
            nearby_services.sort(key=lambda x: x[2])  # Sort by distance (ascending)

            context = {
                'nearby_services': nearby_services,
                'search': search,
            }
            print(f"City: {city}, Search: {search}, Latitude: {user_latitude}, Longitude: {user_longitude}")
            return render(request, "home/search.html", context)
        else:
            error_message = 'Unable to retrieve coordinates for the specified city.'
            return render(request, "home/home.html", {'error_message': error_message})

    return render(request, "home/home.html")

def near_me(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        latitude = float(latitude)
        longitude = float(longitude)
        print(f"{longitude} and {latitude}")
        search ="blood test"
        nearby_services = [] 
        for hospital in Hospital.objects.all():
                matching_services = hospital.services.filter(name__icontains=search)
                if matching_services.exists():
                    distance_km = calculate_distance(latitude, longitude, hospital.latitude, hospital.longitude)
                    if distance_km <= 20:
                        for service in matching_services:
                            nearby_services.append((service, hospital, distance_km))  # Add service name, hospital name, and 
        nearby_services.sort(key=lambda x: x[2])  # Sort by distance (ascending)
        context = {
            'nearby_services': nearby_services,
        }
        return HttpResponse("Location is picked")
    return HttpResponse("Location is not picked")
def show_services(request,services):
    pass

def contact(request):
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        message = request.POST.get('message')
        new_contact = Contact.objects.create(
            name=name,
            email=email,
            number=number,
            message=message,
        )
        new_contact.save()
        return HttpResponse("Your Information is saved Successfully ")
    return HttpResponse("Your Information is not saved ")


def Hospital_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            if user.is_active:
               login(request,user)
               return redirect('Dashboard')
            else:
                 context={
                      'error_message':"You are not a Author"
                 }
                 return HttpResponse("Login page")
        else:
            context = {'error_message': 'Invalid email or password'}
            return HttpResponse("Login page")
    else:
        return HttpResponse("Hospital Login page")

def sign_up(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        Hospital_name = request.POST.get( 'Hospital_name' )
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        new_hospital = CustomUser.objects.create_user(
            name=name,
            email=email,
            number=number,
            password=password,
        )
        new_hospital.save()
        return HttpResponse("Sign up success")
    return HttpResponse("sign_up")


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request,email=email,password=password)
        if user is not None:
            if user.is_active:
               login(request,user)
               return redirect('Dashboard')
            else:
                 context={
                      'error_message':"You are not a Author"
                 }
                 return HttpResponse("Login page")
        else:
            context = {'error_message': 'Invalid email or password'}
            return HttpResponse("Login page")
    else:
        return HttpResponse("Login page")

    



def Hospital_sign_up(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        Hospital_name = request.POST.get( 'Hospital_name' )
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        new_hospital = CustomUser.objects.create_user(
            name=name,
            email=email,
            number=number,
            password=password,
        )
        new_hospital.is_hospital=True
        new_hospital.save()
        return HttpResponse("Sign up success")
    return HttpResponse("Hospital_sign_up")


def Pathology_login(request):
    return HttpResponse("Pathology_login")

def Pathology_sign_up(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        Hospital_name = request.POST.get( 'Hospital_name' )
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        new_hospital = CustomUser.objects.create_user(
            name=name,
            email=email,
            number=number,
            password=password,
        )
        new_hospital.is_pathology=True
        new_hospital.save()
        return HttpResponse("Pathology_sign_up success")
    return HttpResponse("Pathology_sign_up")
