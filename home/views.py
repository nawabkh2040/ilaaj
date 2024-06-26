from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect,get_object_or_404
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
from django.http import JsonResponse
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import * 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import smtplib
from django.shortcuts import render, get_object_or_404, redirect
from twilio.rest import Client
from token_values.token import *
from django.http import JsonResponse
import datetime

import stripe


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
        if city is not None:
            if city.lower() == "sagore":
                city = "Sagor"
            elif city.lower() == "mhow":
                city = "Mhow , pithampur"
        user_longitude = request.POST.get('longitude')
        user_latitude = request.POST.get('latitude')
        if user_longitude is not None and user_latitude is not None:
            print(f"{user_latitude} and {user_longitude}")
            user_latitude = float(user_latitude)  # Convert string to float
            user_longitude = float(user_longitude)  # Convert string to float
        if city is not None:
            user_latitude, user_longitude = get_coordinates(city=city)

        if search:
            search = search.rstrip()

        if user_latitude is not None and user_longitude is not None:
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
            return render(request, "home/search.html", context)
        else:
            error_message = 'Unable to retrieve coordinates for the specified city.'
            return render(request, "home/home.html", {'error_message': error_message})

    return render(request, "home/home.html")


def more_details(request):
    if request.method =="GET":
 
        service_id = request.GET.get('service_id')
        try:
            service = Service.objects.get(id=service_id)
            instant_discount=service.price-service.discounted_price
            context={
                'service' : service,
                'instant_discount':instant_discount,
            }
            return render(request, 'more_details.html',context)
        except Service.DoesNotExist:
            return HttpResponse("Invalid Service Id :-)")
    # Add your logic here to fetch more details
    else:
        return HttpResponse("Invalid Service Id. Access Denied")
        
def privacy_policy(request):
    return render(request,'home/privacy_policy.html')


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
                    return render(request, 'home/user/confirm_appointment.html', context)
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
        return render(request, "home/login.html", context)

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

        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return HttpResponse("Appointment does not exist", status=404)

        if payment_option == 'pay_at_place':
            # Handle payment at place option
            appointment.status = 'Pay at Place'
            appointment.save()
            return redirect('user-appointment')

        elif payment_option == 'pay_now':
            amount = appointment.service.discounted_price
            return HttpResponse("This Service Come Soon! ")
            stripe.api_key = settings.STRIPE_SECRET_KEY

            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(amount * 100),  # amount in cents
                    currency='INR',
                    payment_method_types=['card'],
                    description='Payment for appointment',
                    metadata={'appointment_id': appointment_id}
                )
                payment_instance = Payment.objects.create(
                    appointment=appointment, 
                    amount=amount, 
                    payment_method='stripe',
                    payment_intent_id=payment_intent.id
                )
                return render(request, 'home/user/stripe_payment.html', {'client_secret': payment_intent.client_secret})
            except stripe.error.StripeError as e:
                # Handle Stripe errors
                return HttpResponse(f"Stripe Error: {str(e)}", status=500)

    return HttpResponse("Invalid payment option")

def payment_success(request):
    return HttpResponse("Payment Success")
def near_me(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude
        context = {
            'latitude':latitude,
            'longitude':longitude,
        }

        return render(request,'home/Again_search.html',context)
    return HttpResponse("Location is not picked please refresh the page ")

    
def show_services(request,services):
    pass


def sign_up(request):
    service_id = request.GET.get('service_id')
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        if CustomUser.objects.filter(number=number):
            context={
                'error_message':"Number  Already Exists"
            }
            return render(request,"home/sign-up.html",context)
        elif CustomUser.objects.filter(email=email):
            context={
                'error_message':"Email Id already exists"
            }
            return render(request,"home/sign-up.html",context)
        new_user = CustomUser.objects.create_user(
            name=name,
            email=email,
            number=number,
            password=password,
        )
        new_user.is_active=False
        new_user.save()
        # otp_code = generate_otp()
        # send_otp_via_sms(number, otp_code)
        # request.session['otp_code'] = otp_code
        # request.session['user_id'] = new_user.id
        # return redirect('verify-otp')
    
        subject="Email Verification by Treat Now"
        from_email=settings.EMAIL_HOST_USER
        to_list = [new_user.email]
        current_site = get_current_site(request)
        uidb64 = urlsafe_base64_encode(force_bytes(new_user.id))
        token = default_token_generator.make_token(new_user)
        context_email={
            'name':new_user.name,
            'domain':current_site.domain,
            'uidb64': uidb64,
            'token': token,
        }
        messages=render_to_string('home/email_confirmation.html',context_email)
        try:
            send_mail(subject,messages,from_email,to_list,fail_silently=True)
            context={
                'success_message':"Please Verify Your Email. Go to mail and Click the link Blow And Verify yourself",
            }
            return render(request,"home/sign-up.html",context)
        except Exception as e:
            context= {
                    'error': 'Your Account Create Successfully. There is a problem to sending E-mail in Back-end Our Team is Working on it please Contact us as soon as Possible :-) '
                    }
            return render(request,"home/sign-up.html",context)
    else:
        next_url = reverse('Book-Appointment')  # URL to return to this view after signup
        if service_id:
            next_url += f'?service_id={service_id}'
        context = {'next': next_url}
        response= render(request,"home/sign-up.html",context)
        response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups https://auth.phone.email' 
        response.delete_cookie('ph_email_jwt')
        return response


from django.contrib import messages

def verify_otp(request):
    max_wrong_attempts = 4
    if request.method == "POST":
        otp_entered = request.POST.get('otp')
        otp_code = request.session.get('otp_code')
        user_id = request.session.get('user_id')

        wrong_attempts = request.session.get('wrong_attempts', 0)

        if wrong_attempts >= max_wrong_attempts:
            # Too many wrong attempts, render an error message
            messages.error(request, "You have exceeded the maximum number of wrong attempts.")
            return redirect('home')  # Redirect to the home page or any appropriate page

        if otp_entered == otp_code:
            # Activate the user account
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            # Clear the OTP-related session data and wrong attempts counter
            del request.session['otp_code']
            del request.session['user_id']
            request.session.pop('wrong_attempts', None)

            messages.success(request, "Email verified successfully. Now You Can Login")
            return redirect('home')  # Redirect to the home page or any appropriate page

        else:
            # Increment the wrong attempts counter
            request.session['wrong_attempts'] = wrong_attempts + 1

            context = {
                'error': "Invalid OTP. Please try again."
            }
            return render(request, "home/verify-otp.html", context)

    return render(request, "home/verify-otp.html")


import random
def generate_otp():
    # Generate a random 6-digit OTP
    
    return ''.join(random.choices('0123456789', k=6))


def send_otp_via_sms(phone_number, otp_code):
    # Replace these placeholders with your Twilio credentials
    account_sid = n_account_sid
    auth_token = n_auth_token
    from_number = my_number

    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=f"Your OTP for verification is: {otp_code}",
            from_=from_number,
            to=phone_number
        )
        print("OTP sent successfully via Twilio")
    except Exception as e:
        print(f"Error sending OTP via Twilio: {e}")


def render_with_message(request, message):
    context = {'message': message}
    return render(request, "home/login.html", context)




def activate_user(request, uidb64, token):
    try:
        uidb64 = force_str(urlsafe_base64_decode(uidb64))
        my_user = CustomUser.objects.get(id=uidb64)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        my_user = None
    if my_user is not None and default_token_generator.check_token(my_user,token):
        my_user.is_active = True
        my_user.save()
        login(request,my_user)
        return redirect('home')
    else:
         return render(request,'home/email_activation_failed.html')

def user_sign_up(request):
    access_token = request.GET.get('access_token')
    next_url = request.GET.get('next')
    url = "https://eapi.phone.email/getuser"
    CLIENT_ID = '16373631537064049441'  # Replace with your client id

    postData = {
        'access_token': access_token,
        'client_id': CLIENT_ID
    }
    try:
        response = requests.post(url, data=postData, verify=True)  # Use verify=False to ignore SSL certificate verification (not recommended in production)
        response.raise_for_status()  # Raise exception for non-200 status codes
        json_data = response.json()

        if json_data['status'] != 200:
            context={
                'error_message':"Error occurred while fetching user data"
            }
            response= render(request,"home/sign-up.html",context)
            response.delete_cookie('ph_email_jwt')
            return  response

        country_code = json_data['country_code']
        phone_no = json_data['phone_no']
        ph_email_jwt = json_data['ph_email_jwt']

        user_info = {
            'country_code': country_code,
            'phone_no': phone_no,
            'ph_email_jwt': ph_email_jwt,
            'next_url':next_url
        }

        return render(request, 'home/user_info.html',user_info)
    except requests.RequestException as e:
        context={
                'error_message':str(e)
            }
        return render(request,"home/sign-up.html",context)
        # return JsonResponse({'error': str(e)})
    
def basic_info(request):
    next_url = request.GET.get('next')
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('number')
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        if CustomUser.objects.filter(number=number):
            context={
                'error_message':"Number  Already Exists"
            }
            response= render(request,"home/sign-up.html",context)
            response.delete_cookie('ph_email_jwt')
            return  response

        elif CustomUser.objects.filter(email=email):
            context={
                'error_message':"Email Already Exists"
            }
            response= render(request,"home/sign-up.html",context)
            response.delete_cookie('ph_email_jwt')
            return  response
        else:
            new_user = CustomUser.objects.create_user(
                name=name,number=number,email=email,password=password,is_active=True
            )
            new_user.save()
            if next_url:  # If "next" URL exists, redirect to it after successful signup
                return redirect(next_url)
            else:
                context = {"success_message": "Registration Successful! Please Login to Continue."}
                return render(request, "home/login.html", context)
    else:
        context = {
            'error_message':"Access Denied Continue From Here !"
        }
        response= render(request,"home/sign-up.html",context)
        response.delete_cookie('ph_email_jwt')
        return  response

def login_user(request):
    if request.user.is_authenticated:
        return redirect('User-Dashboard')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get("next")
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            # print(next_url)
            if next_url:
                return redirect(next_url)  # Redirect to the next URL if it exists
            else:
                return redirect('User-Dashboard')  # Redirect to the dashboard if no next URL
        else:
            context = {'error_message': 'Invalid email or password'}
            return render(request, "home/login.html", context)
    else:
        
        response = render(request, "home/login.html")
        response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups https://auth.phone.email' 
        return response

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            send_success = send_reset_link(request, user)
            if send_success:
                context = {
                    'success_message': "Password Reset Link has been sent to your email. Please check your inbox."
                }
            else:
                context = {
                    'error_message': "There was a problem sending the email. Please try again later or contact us."
                }
            return render(request, "home/reset_password_email.html", context)
            
        except CustomUser.DoesNotExist:
            context = {
                'error_message': "Email is not registered. Please sign up."
            }
            return render(request, "home/reset_password_email.html", context)
    return render(request, "home/reset_password_email.html")

def send_reset_link(request, user):
    subject = "Password Reset Link by Treat Now"
    from_email = settings.EMAIL_HOST_USER
    to_list = [user.email]
    current_site = get_current_site(request)
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    reset_link = f"http://{current_site.domain}/reset-password-user/{uidb64}/{token}/"
    context_email = {
        'name': user.name,
        'reset_link': reset_link,
    }
    message = render_to_string('home/reset_confirmation.html', context_email)
    try:
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return True
    except Exception as e:
        # print(e)  # Log the error for debugging purposes
        return False  
        
    
def reset_password_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        my_user = CustomUser.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        my_user = None

    if my_user is not None and default_token_generator.check_token(my_user, token):
        if request.method == "POST":
            new_password = request.POST.get('password')
            my_user.set_password(new_password)
            my_user.save()
            login(request, my_user)
            return redirect("home")
        else:
            context = {'uidb64': uidb64, 'token': token}
            return render(request, "home/new_password.html", context)
    else:
        return render(request, 'home/email_activation_failed.html')

def logout_user(request):
    logout(request)
    response = redirect('home')
    response.delete_cookie('ph_email_jwt')  # Delete the cookie named 'ph_email_jwt'
    return response



def user_dashboard(request):
    if request.user.is_authenticated:
        user=request.user
        if user.is_patient:
            # print(f"{request.user}")
            appointments = Appointment.objects.filter(patient=user).order_by('Appointment_date')
            context={
                'user':user,
                'appointments':appointments,
            }
            return render(request,"home/user/appointment.html",context)
        else:
            return HttpResponse("You Are Not User ")
    else:
        return redirect('/login/')

def user_profile(request):
    
    if request.user.is_authenticated:
        user=request.user
        if user.is_patient:
            # print(f"{request.user}")
            context={
                'user':user,
            }
            return render(request,"home/user/profile.html",context)
        else:
            return HttpResponse("You Are Not User ")
    else:
        return redirect('/login/')

def user_appointment(request):
    
    if request.user.is_authenticated:
        user=request.user
        if user.is_patient:
            # print(f"{request.user}")

            appointments = Appointment.objects.filter(patient=user).order_by('Appointment_date')
            context={
                'user':user,
                'appointments':appointments,
            }
            return render(request,"home/user/appointment.html",context)
        else:
            return HttpResponse("You Are Not User ")
    else:
        return redirect('/login/')

def user_report(request,id):
    
    if request.user.is_authenticated:
        user=request.user
        if user.is_patient:
            # print(f"{request.user}")
            try:
                appointment = get_object_or_404(Appointment, id=id)
                if  appointment.patient != user :
                    return HttpResponse("Its Not Your Report. Access Denied !")
                context={
                    'appointment':appointment,
                }
                return render(request,"home/user/reports.html",context)
            except Exception as e:
                return HttpResponse(str(e)) 
        else:
            return HttpResponse("You Are Not User ")
    else:
        return redirect('/login/')

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
#okk