from django.contrib import admin
from home.models import *
# Register your models here.


class CustomUserAdmin_by(admin.ModelAdmin):
    list_display=('name','id','email','number','date','is_active','is_staff','is_hospital','is_pathology','password')
admin.site.register(CustomUser,CustomUserAdmin_by)


admin.site.register(Doctor)
admin.site.register(Payment)

class hospital_kyc_Admin(admin.ModelAdmin):
    list_display = ('name', 'user','address','owner_name','id_proof','id_proof_hospital')
admin.site.register(Hospital_kyc,hospital_kyc_Admin)
class pathology_kyc_Admin(admin.ModelAdmin):
    list_display = ('name', 'user','address','owner_name','id_proof','id_proof_pathology')
admin.site.register(PathologyLab_kyc,pathology_kyc_Admin)



class Contact_Admin(admin.ModelAdmin):
    list_display = ('name','id', 'number','email','message','date_time')
admin.site.register(Contact,Contact_Admin)

class  Appointment_admin(admin.ModelAdmin):
    list_display= ('id','patient','service','date_time','Appointment_date','status','hospital','pathology_lab','done','doctor','online_payment','note','payment_id')
admin.site.register(Appointment,Appointment_admin)

class Services_admin(admin.ModelAdmin):
    list_display = ('id','name','description','price','off_percentage','actual_price','discounted_price','image')
admin.site.register(Service,Services_admin)

class hospitals_admin(admin.ModelAdmin):
    list_display = ('Hospitals_name','user','address','zipcode','location','latitude','longitude','verified','image1','image2')
admin.site.register(Hospital,hospitals_admin)


class pathology_admin(admin.ModelAdmin):
    list_display = ('Pathology_name','user','address','zipcode','location','latitude','longitude','verified','image1','image2')
admin.site.register(PathologyLab,pathology_admin)


