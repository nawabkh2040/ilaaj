from django.contrib import admin
from django.urls import path
from home import views
from ilaaj import settings
from django.conf.urls.static import static


urlpatterns = [
     path('', views.home, name='home'),
     path('contact/', views.contact, name='contact'),
     path('near-me/', views.near_me, name='near-me'),
     
     path('Hospital-login/', views.Hospital_login, name='Hospital-login'),
     path('Pathology-login/', views.Pathology_login, name='Pathology-login'),
     path('Hospital-sign-up/', views.Hospital_sign_up, name='Hospital-sign-up'),
     path('Pathology-sign-up/', views.Pathology_sign_up, name='Pathology-sign-up'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
