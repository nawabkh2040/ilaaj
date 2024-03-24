from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model 
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )

    name = models.CharField(max_length=25,default="None")
    email = models.EmailField(unique=True)
    number = models.CharField(unique=True,max_length=15)
    password = models.CharField(max_length=500)
    date = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)
    is_pathology = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True) 
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'number']

    def __str__(self):
        return self.email

    username = models.CharField(max_length=70, null=True, blank=True)



class Hospital(models.Model):
     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'is_hospital': True})
     Hospitals_name = models.CharField(max_length=200)
     address = models.CharField(max_length=500)
     zipcode = models.IntegerField(default=0,null=True)
     location = models.CharField(max_length=255, blank=True)  
     latitude = models.FloatField(blank=True, null=True)  
     longitude = models.FloatField(blank=True, null=True)
     def __str__(self):
        return self.Hospitals_name

class PathologyLab(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True,limit_choices_to={'is_pathology': True})
    Pathology_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    zipcode = models.IntegerField(default=0,null=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.Pathology_name


class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='services/%Y/%m/%d/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Add price field
    off_percentage  = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    hospitals = models.ManyToManyField(Hospital, related_name='services', blank=True)
    pathology_labs = models.ManyToManyField(PathologyLab, related_name='services', blank=True)  

    def __str__(self):
        return self.name




class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    hospitals = models.ManyToManyField(Hospital, related_name='doctors')

    def __str__(self):
        return self.name + " (" + self.specialization + ")"

class Appointment(models.Model):
    

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to logged-in user
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, blank=True, null=True)  # Optional for pathology labs
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, blank=True, null=True)  # Optional for pathology labs
    pathology_lab = models.ForeignKey(PathologyLab, on_delete=models.CASCADE, blank=True, null=True)  # Optional for hospitals
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField(default=datetime.now) 
    Appointment_date = models.DateTimeField(default=datetime.now) # Appointment date and time
    status = models.CharField(max_length=100,  default="PENDING")  # Status of appointment: Pending, Cancelled, Accepted
    note = models.TextField(blank=True)  # Optional note for the appointment

    def __str__(self):
        return f"Appointment for {self.patient.username}"


class Payment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
        ('wallet', 'Wallet'),
        ('other', 'Other')
    ])
    payment_details = models.TextField(blank=True) 

    def __str__(self):
        return f"Payment of {self.amount} for appointment {self.appointment.id}"


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.CharField(max_length=15)
    message = models.TextField(max_length=500)
    date_time = models.DateTimeField(default=datetime.now) 