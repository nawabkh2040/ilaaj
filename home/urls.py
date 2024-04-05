from django.contrib import admin
from django.urls import path
from home import views
from ilaaj import settings
from django.conf.urls.static import static


urlpatterns = [
     path('', views.home, name='home'),
     path('contact/', views.contact, name='contact'),
     path('near-me/', views.near_me, name='near-me'),
     path('login/', views.login_user, name='login'),
     path('logout/', views.logout_user, name='logout'),
     path('sign-up/', views.sign_up, name='sign-up'),
     path('Success-user/', views.user_sign_up, name='Success-user'),
     path('basic-info/', views.basic_info, name='basic-info'),
     path('reset-password/', views.reset_password, name='reset-password'),
     # path('set-password/', views.set_password, name='set-password'),

     path('reset-password-user/<str:uidb64>/<str:token>/',views.reset_password_user,name="reset-password-user"),
     



     path('Book-Appointment/', views.book_appointment, name='Book-Appointment'),
     path('Appointment/', views.appointment, name='Appointment'),
     path('more-details/', views.more_details, name='More-Details'),
     path('search-services/', views.search_services, name='search-services'),
     path('activate-user/<str:uidb64>/<str:token>/',views.activate_user,name="activate-user"),
     path('verify-otp/', views.verify_otp, name='verify-otp'),



     path('User-Dashboard/', views.user_dashboard, name='User-Dashboard'),
     path('user-profile/', views.user_profile, name='user-profile'),
     path('user-appointment/', views.user_appointment, name='user-appointment'),
     path('user-report/<int:id>/', views.user_report, name='user-report'),

# For adding the data to the
     path('payment/<int:appointment_id>/',views.payment, name='payment'),
     path('payment/success/', views.payment_success, name='payment_success'),
     path('payment-process/', views.payment_process, name='payment-process'),
   







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
