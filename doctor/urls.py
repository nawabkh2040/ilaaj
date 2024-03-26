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
    path('Appointment-Details/<int:id>', views.appointment_details, name='Appointment-Details'),







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)