from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
import requests
from django.http import JsonResponse
from home.token import *
# Create your views here.
import requests
from django.db.models import Q
from home.models import *
from datetime import datetime
from django.contrib.auth import authenticate, login , logout
from django.views.decorators.csrf import csrf_exempt
import razorpay


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

            # Filter hospitals and pathology labs within 20 km range
            nearby_hospitals = Hospital.objects.filter(
                latitude__range=(user_latitude - 0.2, user_latitude + 0.2),
                longitude__range=(user_longitude - 0.2, user_longitude + 0.2)
            )
            nearby_pathology_labs = PathologyLab.objects.filter(
                latitude__range=(user_latitude - 0.2, user_latitude + 0.2),
                longitude__range=(user_longitude - 0.2, user_longitude + 0.2)
            )

            nearby_services = []  # List to store nearby services with hospital names
            nearby_services_pathology = []

            # Find hospitals with matching services
            for hospital in nearby_hospitals:
                matching_services = hospital.services.filter(name__icontains=search)
                for service in matching_services:
                    distance_km = calculate_distance(user_latitude, user_longitude, hospital.latitude, hospital.longitude)
                    if distance_km <= 20:
                        nearby_services.append((service, hospital, distance_km))  # Add service name, hospital name, and distance

            # Find pathology labs with matching services
            for pathology_lab in nearby_pathology_labs:
                matching_services = pathology_lab.services.filter(name__icontains=search)
                for service in matching_services:
                    distance_km = calculate_distance(user_latitude, user_longitude, pathology_lab.latitude, pathology_lab.longitude)
                    if distance_km <= 20:
                        nearby_services_pathology.append((service, pathology_lab, distance_km))

            nearby_services.sort(key=lambda x: x[2])  # Sort by distance (ascending)
            nearby_services_pathology.sort(key=lambda x: x[2])

            context = {
                'nearby_services': nearby_services,
                'nearby_services_pathology': nearby_services_pathology,
                'search': search,
            }
            # print(f"City: {city}, Search: {search}, Latitude: {user_latitude}, Longitude: {user_longitude}")
            return render(request, "home/hospitals.html", context)
        else:
            error_message = 'Unable to retrieve coordinates for the specified city.'
            return render(request, "home/home.html", {'error_message': error_message})

    return render(request, "home/home.html")



def book_appointment(request):
    service_id = request.GET.get('service_id')
    if request.user.is_authenticated:
        if request.method == 'GET':
            if service_id:
                try:
                    user = request.user
                    service = Service.objects.get(id=service_id)
                    instant_discount = service.price - service.discounted_price
                    # Render the booking page with the pre-filled form fields
                    context={
                        'service':service,
                        'user':user,
                        'instant_discount': instant_discount,
                    }
                    return render(request, 'Home/user/booking_appointment.html', context)
                    # return HttpResponse("Booking Page")
                except Service.DoesNotExist:
                    return render(request, 'error_page.html', {'error_message': 'Service not found'})
            else:
                # Handle case when no service ID is provided
                return render(request, 'error_page.html', {'error_message': 'Service ID not provided'})
        else:
            return HttpResponse("Book Appointment")
    else:
        # If the user is not logged in, redirect to the login page with next parameter
        next_url = reverse('Book-Appointment')  # URL to return to this view after login
        if service_id:
            next_url += f'?service_id={service_id}'
        context={
            'next': next_url,
        }
        return render(request, "Home/login.html", context)

def appointment(request):
    try:
        if request.user.is_authenticated:
            user = request.user
            if request.method == "POST":
                hospital = request.POST.get('hospital')
                doctor = request.POST.get('doctor')
                pathology_lab = request.POST.get('pathology_lab')
                service_name = request.POST.get('service')
                appointment_date = request.POST.get('Appointment_date')
                status = request.POST.get('status')
                note = request.POST.get('note')

                try:
                    hospitals = Hospital.objects.get(Hospitals_name=hospital)
                except Hospital.DoesNotExist:
                    hospitals = hospital
                
                try:
                    pathology = PathologyLab.objects.get(Pathology_name=pathology_lab)
                except PathologyLab.DoesNotExist:
                    pathology = pathology_lab
                
                if doctor:
                    try:
                        doctors = Doctor.objects.get(name=doctor)
                    except Doctor.DoesNotExist:
                        doctors = None
                else:
                    doctors = None
                
                services = Service.objects.filter(name=service_name)
                if services.exists():
                    service = services.first()
                else:
                    return HttpResponse("Service does not exist")
                   
                
                appointment = Appointment.objects.create(
                    patient=user, hospital=hospitals, doctor=doctors, pathology_lab=pathology, service=service, Appointment_date=appointment_date, status=status, note=note
                )

                return redirect('payment', appointment_id=appointment.id)
            else:
                return HttpResponse("Access Denied")
                
        else:
            return redirect('login')
    except Exception as e:
        return HttpResponse(f"Error occurred: {e}")

def payment(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        return render(request, 'home/user/payment.html', {'appointment': appointment})
    except Appointment.DoesNotExist:
        return HttpResponse("Appointment not found")

def payment_process(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        payment_option = request.POST.get('payment_option')

        if payment_option == 'pay_at_place':
            # Handle payment at place option
            # You can update the appointment status or perform any other action as needed
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = 'Paid at Place'
            appointment.save()
            return redirect('user-report')

        elif payment_option == 'pay_now':
            appointment = Appointment.objects.get(id=appointment_id)
            amount = appointment.service.discounted_price
            
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            payment = client.order.create({'amount': amount * 100, 'currency': 'INR', 'payment_capture': '1'})

            payment_instance = Payment.objects.create(
                appointment=appointment, amount=amount, payment_method='razorpay'
            )

            return render(request, 'home/user/razorpay_payment.html', {'payment': payment})

    return HttpResponse("Invalid payment option")

def razorpay_success(request):
    if request.method == 'POST':
        # Capture the payment details from the POST request
        payment_id = request.POST.get('razorpay_payment_id')
        appointment_id = request.POST.get('appointment_id')
        
        # Retrieve the appointment instance
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return HttpResponse("Appointment not found")
        
        # Update the appointment status to 'Paid'
        appointment.status = 'Paid'
        appointment.save()
        
        # Redirect to a success page
        return render(request, 'home/user/payment_success.html')
    else:
        return HttpResponseNotAllowed(['POST'])

def initiate_payment(request):
    if request.method == "POST":
        appointment_id = request.POST.get('appointment_id')
        amount = request.POST.get('amount')

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return JsonResponse({'error': 'Invalid appointment ID'}, status=400)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment_data = {
            'amount': int(float(amount) * 100),  # Convert to paisa
            'currency': 'INR',
            'receipt': 'appointment_payment_' + str(appointment_id),
            'payment_capture': 1  # Auto capture payment after successful payment
        }

        try:
            payment = client.order.create(data=payment_data)
            return JsonResponse(payment)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return HttpResponseBadRequest('Invalid request')

@csrf_exempt
def capture_payment(request):
    if request.method == "POST":
        data = request.POST
        appointment_id = data['appointment_id']
        razorpay_payment_id = data['razorpay_payment_id']
        razorpay_order_id = data['razorpay_order_id']
        razorpay_signature = data['razorpay_signature']

        # Verify the payment signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        attributes = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        try:
            client.utility.verify_payment_signature(attributes)

            # Update payment details
            payment_method = data.get('payment_method')
            payment_details = data.get('payment_details')

            # Create Payment instance
            payment = Payment.objects.create(
                appointment_id=appointment_id,
                amount=float(data.get('amount')),
                payment_method=payment_method,
                payment_details=payment_details
            )

            # Update appointment status to Paid or any other relevant action
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.status = 'Paid'
            appointment.save()

            return HttpResponse("Payment successful")
        except Exception as e:
            return HttpResponse("Payment failed")


def near_me(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        # latitude = float(latitude)
        # longitude = float(longitude)
        print(f"{longitude} and {latitude}")
        # return render(request,"home/")
        # search ="blood test"
        # nearby_services = [] 
        # for hospital in Hospital.objects.all():
        #         matching_services = hospital.services.filter(name__icontains=search)
        #         if matching_services.exists():
        #             distance_km = calculate_distance(latitude, longitude, hospital.latitude, hospital.longitude)
        #             if distance_km <= 20:
        #                 for service in matching_services:
        #                     nearby_services.append((service, hospital, distance_km))  # Add service name, hospital name, and 
        # nearby_services.sort(key=lambda x: x[2])  # Sort by distance (ascending)
        # context = {
        #     'nearby_services': nearby_services,
        # }
        return HttpResponse("Location is picked")
    return HttpResponse("Location is not picked please refresh the page ")

    
def show_services(request,services):
    pass


def sign_up(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        if CustomUser.objects.filter(number=number):
            context={
                'error_message':"Number  Already Exists"
            }
            return render(request,"Home/sign-up.html",context)
        elif CustomUser.objects.filter(email=email):
            context={
                'error_message':"Email Id already exists"
            }
            return render(request,"Home/sign-up.html",context)
        new_hospital = CustomUser.objects.create_user(
            name=name,
            email=email,
            number=number,
            password=password,
        )
        new_hospital.save()
        context={
            'success_message':"Please Verify Your Email. Go to You mail and Click the link Blow And Verify yourself",
        }
        return render(request,"Home/login.html",context)
    return render(request,"Home/sign-up.html")


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get("next")
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            print(next_url)
            if next_url:
                return redirect(next_url)  # Redirect to the next URL if it exists
            else:
                return redirect('User-Dashboard')  # Redirect to the dashboard if no next URL
        else:
            context = {'error_message': 'Invalid email or password'}
            return render(request, "Home/login.html", context)
    else:
        return render(request, "Home/login.html")


def logout_user(request):
    logout(request)
    return redirect('home')



def user_dashboard(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_patient:
            print(f"{request.user}")
            context={
                'user':user,
            }
            return render(request,"Home/user/profile.html",context)
        else:
            return HttpResponse("You Are Not User ")
    else:
        return redirect('/login/')

def user_profile(request):
    
    if request.user.is_authenticated:
        user=request.user
        if user.is_patient:
            print(f"{request.user}")
            context={
                'user':user,
            }
            return render(request,"Home/user/profile.html",context)
        else:
            return HttpResponse("You Are Not User ")
    else:
        return redirect('/login/')

def user_appointment(request):
    
    if request.user.is_authenticated:
        user=request.user
        if user.is_patient:
            print(f"{request.user}")
            context={
                'user':user,
            }
            return render(request,"Home/user/appointment.html",context)
        else:
            return HttpResponse("You Are Not User ")
    else:
        return redirect('/login/')

def user_report(request):
    
    if request.user.is_authenticated:
        user=request.user
        if user.is_patient:
            print(f"{request.user}")
            context={
                'user':user,
            }
            return render(request,"Home/user/reports.html",context)
        else:
            return HttpResponse("You Are Not User ")
    else:
        return redirect('/login/')



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
        content={
            'success_message':"Your Information is saved Successfully. We will Reach  out to you soon",
        }
        return render(request,"home/contact.html",content)
    else :
        content = {
            'error_message':'Your Information is not  Saved Please Try Again Later',
        }
        return render(request,"home/contact.html",content)
