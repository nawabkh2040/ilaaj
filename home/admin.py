from django.contrib import admin
from home.models import *
# Register your models here.


class CustomUserAdmin_by(admin.ModelAdmin):
    list_display=('name','id','email','number','date','is_active','is_staff','is_hospital','is_pathology','password')
admin.site.register(CustomUser,CustomUserAdmin_by)

admin.site.register(Hospital)
admin.site.register(PathologyLab)
admin.site.register(Service)
admin.site.register(Doctor)
admin.site.register(Payment)


class Contact_Admin(admin.ModelAdmin):
    list_display = ('name','id', 'number','email','message','date_time')
admin.site.register(Contact,Contact_Admin)

class  Appointment_admin(admin.ModelAdmin):
    list_display= ('id','patient','service','date_time','Appointment_date','status','hospital','pathology_lab','doctor','note')
admin.site.register(Appointment,Appointment_admin)

