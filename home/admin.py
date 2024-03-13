from django.contrib import admin
from home.models import *
# Register your models here.


class CustomUserAdmin_by(admin.ModelAdmin):
    list_display=('name','id','email','number','date','is_active','is_staff','is_hospital','is_pathology','password')
admin.site.register(CustomUser,CustomUserAdmin_by)

admin.site.register(Hospital)
admin.site.register(Service)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Payment)


class Contact_Admin(admin.ModelAdmin):
    list_display = ('name','id', 'number','email','message','date_time')
admin.site.register(Contact,Contact_Admin)



