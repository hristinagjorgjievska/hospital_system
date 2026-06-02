from datetime import date, datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Doctor(models.Model):
    SPECIALTY = [
        ("cardiologist", "cardiologist"),
        ("dermatologist", "dermatologist"),
        ("neurologist", "neurologist"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100, choices=SPECIALTY)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    institution = models.CharField(max_length=100)
    completed_appointments = models.IntegerField(default=0)
    email = models.EmailField()
    phone = models.CharField(max_length=100)

class Patient(models.Model):
    GENDER = [
        ("male", "MALE"),
        ("female", "FEMALE")
    ]

    full_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    gender = models.CharField(max_length=100, choices=GENDER)
    email = models.EmailField()
    institution = models.CharField(max_length=100)

class Appointment(models.Model):
    TYPE = [
        ("cardiological", "cardiological"),
        ("dermatological", "dermatological"),
        ("neurological", "neurological"),
    ]

    STATUS = [
        ("scheduled", "scheduled"),
        ("in_progress", "in_progress"),
        ("completed", "completed")
    ]

    responsible_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_type = models.CharField(max_length=100, choices=TYPE)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS, default='scheduled')
    datetime = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


class AppointmentAssignment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('appointment', 'doctor')



