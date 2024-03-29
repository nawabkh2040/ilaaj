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
     path('payment/success/', views.razorpay_success, name='payment_success'),
     path('payment-process/', views.payment_process, name='payment-process'),
     path('initiate-payment/', views.initiate_payment, name='initiate_payment'),
     path('capture-payment/', views.capture_payment, name='capture_payment'),







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
