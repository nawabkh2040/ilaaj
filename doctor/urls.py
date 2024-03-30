from django.contrib import admin
from django.urls import path, include
from ilaaj import settings
from doctor import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='doctor'),
    path('login/', views.login_doctor, name='doctor-login'),
    path('logout/', views.logout_doctor, name='doctor-logout'),
    path('sign-up/', views.sign_up, name='doctor-sign-up'),
    path('activate-doctor/<str:uidb64>/<str:token>/',views.activate_doctor,name="activate-doctor"),
    path('Doctor-Dashboard/', views.doctor_dashboard, name='Doctor-Dashboard'),
    path('Doctor-Profile/', views.doctor_profile, name='Doctor-Profile'),
    path('Doctor-place/', views.doctor_place, name='Doctor-Place'),
    path('Doctor-Services/', views.doctor_services, name='Doctor-Services'),
    path('Add-Services/', views.add_services, name='Add-Services'),
    path('reset-password-doctor/', views.reset_password, name='reset-password-doctor'),
     path('reset-password-doctor/<str:uidb64>/<str:token>/',views.reset_password_doctor,name="reset-password-doctor"),





    path('Appointment-Details/<int:id>/', views.appointment_details, name='Appointment-Details'),







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)