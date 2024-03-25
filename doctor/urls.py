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
    path('Doctor-Dashboard/', views.doctor_dashboard, name='Doctor-Dashboard'),






]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)