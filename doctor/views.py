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
from home.models import *
from django.utils import timezone
from datetime import date


# for mail 
# form ilaaj.settings import *
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
# from django.utils.encoding import force_text


# Create your views here.
def home(request):
     return HttpResponse("Doctors Page")

def login_doctor(request):
     if request.method == "POST" or  request.method == "post":
          email = request.POST.get('email')
          password = request.POST.get('password')
          user = authenticate(request, email=email, password=password)
          if user is not None:
               if user.is_active:
                    if user.is_hospital or user.is_pathology:
                         login(request, user)
                         return redirect('Doctor-Dashboard')
                    else:
                         context={
                              'error':"You Are  Not Doctor"
                         }
                         return render(request,"doctor/html/login.html",context)
               else:
                    context = {
                    'error':"Email Is Not Verified. Please Check Your Mail And Verify it.",
                    }
                    return render(request,"doctor/html/login.html",context)
          else:
               context = {
                    'error':"Invalid Email Or Password",
               }
               return render(request,"doctor/html/login.html",context)
     else:
          return render(request,"doctor/html/login.html")
def logout_doctor(request):
    logout(request)
    return redirect('home')

def sign_up(request):
     if request.method == "POST" or  request.method == "post":
          name = request.POST.get('name')
          email = request.POST.get('email')
          number = request.POST.get('number')
          password = request.POST.get('password')
          is_hospital = request.POST.get('is_hospital')
          is_pathology = request.POST.get('is_pathology')
          # print(f"{name} {email} {number}")
          if CustomUser.objects.filter(number=number):
               context={
                    'error':'This phone number has already been registered.'
               }
               return render(request,"doctor/html/sign-up.html",context)
          elif CustomUser.objects.filter(email=email):
               context={
                    'error':'This Email has already been registered.'
               }
               return render(request,"doctor/html/sign-up.html",context)
          new_user = CustomUser.objects.create_user(
               name=name,email=email,number=number,password=password,
               is_hospital=bool(is_hospital),is_pathology=bool(is_pathology)
               )
          new_user.is_active=False
          new_user.save()
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
          messages=render_to_string('doctor/email_confirmation.html',context_email)
          try:
               send_mail(subject,messages,from_email,to_list,fail_silently=True)
               context = {
                    'success_message':"You Registration  Successfully. Please check your e-mail & verify yourself.",
               }
               return render(request,"doctor/html/sign-up.html",context)
          except Exception as e:
                    context= {
                         'error': 'Your Account Create Successfully. There is a problem to sending E-mail in Back-end Our Team is Working on it please Contact us as soon as Possible :-) '
                         }
                    return render(request,"doctor/html/sign-up.html",context)
     else:
          return render(request,"doctor/html/sign-up.html")


def activate_doctor(request, uidb64, token):
    try:
        uidb64 = force_str(urlsafe_base64_decode(uidb64))
        my_user = CustomUser.objects.get(id=uidb64)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        my_user = None
    if my_user is not None and default_token_generator.check_token(my_user,token):
        my_user.is_active = True
        my_user.save()
        login(request,my_user)
        return redirect('Doctor-Dashboard')
    else:
         return render(request,'doctor/email_activation_failed.html')
     
def doctor_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_hospital or user.is_pathology:
            try:
                hospital = Hospital.objects.get(user=user)
            except Hospital.DoesNotExist:
                hospital = None

            try:
                pathology = PathologyLab.objects.get(user=user)
            except PathologyLab.DoesNotExist:
                pathology = None
            today = date.today()
            appointments = []
            if hospital:
                try:
                    appointments = Appointment.objects.filter(hospital=hospital)
                    today_appointments = Appointment.objects.filter(hospital=hospital,Appointment_date=today)
                except Appointment.DoesNotExist:
                    pass
            elif pathology:
                try:
                    appointments = Appointment.objects.filter(pathology_lab=pathology)
                    today_appointments = Appointment.objects.filter(pathology_lab=pathology,Appointment_date=today)
                except Appointment.DoesNotExist:
                    pass

            context = {
                'hospital': hospital,
                'pathology': pathology,
                'appointments': appointments,
                'today_appointments':today_appointments,
            }
            return render(request, "doctor/html/dashboard.html", context)
        else:
            return HttpResponse("You are not a doctor.")
    else:
        return redirect('doctor-login')

def doctor_profile(request):
     if request.user.is_authenticated:
          user = request.user
          if user.is_hospital or user.is_pathology:
               # return HttpResponse("Doctor Dashboard")
               try:
                    hospital = Hospital.objects.get(user=user)
               except Hospital.DoesNotExist:
                    hospital = None
               try:
                    pathology = PathologyLab.objects.get(user=user)
               except PathologyLab.DoesNotExist:
                    pathology = None
               context = {
                    'user':user,
                    'hospital':hospital,
                    'pathology':pathology
               }
               return render(request,"doctor/html/profile.html",context)

          else:
               return HttpResponse("You Are Not Doctor")
     else:
          return redirect('doctor-login')
def doctor_place(request):
     if request.user.is_authenticated:
          user = request.user
          if user.is_hospital or user.is_pathology:
               try:
                    hospital = Hospital.objects.get(user=user)
               except Hospital.DoesNotExist:
                    hospital = None
               try:
                    pathology = PathologyLab.objects.get(user=user)
               except PathologyLab.DoesNotExist:
                    pathology = None
               if request.method == "POST":
                    Hospitals_name = request.POST.get('Hospitals_name')
                    pathology_name = request.POST.get('pathology_name')
                    address = request.POST.get('address')
                    location = request.POST.get('location')
                    zipcode = request.POST.get('zip_code')
                    image1 = request.FILES.get('image1')
                    image2 = request.FILES.get('image2')
                    latitude = request.POST.get('latitude')
                    longitude = request.POST.get('longitude')
                    if hospital is not None:
                         context ={
                              'user' : user,
                              'error_message':"You Already have a Hospital"
                         }
                         return render(request,"doctor/html/place.html",context)
                    if pathology is not None:
                         context ={
                              'user' : user,
                              'error_message':"You Already have a Pathology"
                         }
                         return render(request,"doctor/html/place.html",context)
                    if user.is_hospital:
                         new_hospital = Hospital.objects.create(
                              Hospitals_name=Hospitals_name,address=address,zipcode=zipcode,location=location,latitude=latitude,longitude=longitude,image1=image1,image2=image2,user=user
                         )
                         new_hospital.save()
                         context = {
                              'user':user,
                              'new_hospital':new_hospital,
                              'success_message':"Hospital add  Successfully!"
                         }
                         return render(request,"doctor/html/place.html",context)
                    elif user.is_pathology:
                         new_pathology = PathologyLab.objects.create(
                              Hospitals_name=Hospitals_name,address=address,zipcode=zipcode,location=location,latitude=latitude,longitude=longitude,image1=image1,image2=image2,user=user
                         )
                         new_pathology.save()
                         context = {
                              'user':user,
                              'new_pathology':new_pathology,
                              'success_message':"Pathology add  Successfully!"
                         }
                         return render(request,"doctor/html/place.html",context)

               context = {
                    'user':user,
                    'hospital':hospital,
                    'pathology':pathology
               }
               return render(request,"doctor/html/place.html",context)

          else:
               return HttpResponse("You Are Not Doctor")
     else:
          return redirect('doctor-login')

def appointment_details(request,id):
     if request.user.is_authenticated:
          user = request.user
          if user.is_hospital or user.is_pathology:
               # return HttpResponse("Doctor Dashboard")

               appointment = get_object_or_404(Appointment, id=id)
               if request.method == 'POST':
                    new_status = request.POST.get('status')
                    new_done = request.POST.get('done')
                    report_file = request.FILES.get('report')
                    # print(report_file)
                    appointment.status = new_status
                    appointment.done = new_done
                    if report_file:  
                         appointment.report = report_file
                    appointment.save()
                    context = {
                         'appointment':appointment,
                         'success_message':"Update Success Full"
                    }
                    return render(request,"doctor/html/appointment_details.html",context)
               context={
                    'appointment':appointment
               }
               return render(request,"doctor/html/appointment_details.html",context)

          else:
               return HttpResponse("You Are Not Doctor")
     else:
          return redirect('doctor-login')

def doctor_services(request):
    if request.user.is_authenticated:
        user = request.user
        if user.is_hospital or user.is_pathology:
            hospital = None
            pathology = None
            services = []

            if user.is_hospital:
                try:
                    hospital = Hospital.objects.get(user=user)
                    hospital_services = Service.objects.filter(hospitals=hospital)
                    services.extend(hospital_services)
                except Hospital.DoesNotExist:
                    pass

            if user.is_pathology:
                try:
                    pathology = PathologyLab.objects.get(user=user)
                    pathology_services = Service.objects.filter(pathology_labs=pathology)
                    services.extend(pathology_services)
                except PathologyLab.DoesNotExist:
                    pass

            context = {
                'user': user,
                'hospital': hospital,
                'pathology': pathology,
                'services': services,
            }
            return render(request, "doctor/html/service.html", context)
        else:
            return HttpResponse("You Are Not a Doctor")
    else:
        return redirect('doctor-login')
def add_services(request):
     if request.user.is_authenticated:
          user = request.user
          if user.is_hospital or user.is_pathology:
               try:
                    hospital = Hospital.objects.get(user=user)
                    services = Service.objects.filter(hospitals=hospital).order_by('id')
                    # print(services)
               except Hospital.DoesNotExist:
                    hospital = None
                    services = None
               try:
                    pathology = PathologyLab.objects.get(user=user)
                    services = Service.objects.filter(pathology_labs=pathology).order_by('id')

               except PathologyLab.DoesNotExist:
                    pathology = None
                    services = None
               if request.method == "POST":
                    name = request.POST.get('name')
                    description = request.POST.get('description')
                    price = request.POST.get('price')
                    off_percentage = request.POST.get('off_percentage')
                    actual_price = request.POST.get('actual_price')
                    discounted_price = request.POST.get('discounted_price')
                    image = request.FILES.get('image')
                    new_service = Service.objects.create(
                         name=name,description=description,price=int(price),
                         off_percentage=int(off_percentage),actual_price=int(actual_price),
                         discounted_price=int(discounted_price),image=image,
                    )
                    if hospital:
                         new_service.hospitals.add(hospital)
                    elif pathology:
                         new_service.pathology_labs.add(pathology)
                    new_service.save()
                    return redirect('Doctor-Services')
               context = {
                    'user':user,
                    'hospital':hospital,
                    'pathology':pathology,
                    'services':services,
               }
               return render(request,"doctor/html/add-service.html",context)

          else:
               return HttpResponse("You Are Not Doctor")
     else:
          return redirect('doctor-login')

