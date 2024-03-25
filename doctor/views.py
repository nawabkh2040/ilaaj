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
from home.models import *

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
          print(f"{name} {email} {number}")
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
               is_active=False,is_staff=False,is_superuser=False,
               is_hospital=bool(is_hospital),is_pathology=bool(is_pathology)
               )
          new_user.save()
          context = {
               'success_message':"You Registration  Successfully. Please check your e-mail & verify yourself.",
          }
          return render(request,"doctor/html/sign-up.html",context)
     else:
          return render(request,"doctor/html/sign-up.html")
     
def doctor_dashboard(request):
     if request.user.is_authenticated:
          user = request.user
          if user.is_hospital or user.is_pathology:
               return HttpResponse("Doctor Dashboard")
          else:
               return HttpResponse("You Are Not Doctor")
     else:
          return redirect('doctor-login')