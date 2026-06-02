from datetime import date, datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# Секој лекар се карактеризира со име и презиме, специјалност (кардиолог, дерматолог или невролог),
# слика, институција од која доаѓа, број на успешно извршени прегледи, контакт е-пошта и телефон.
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

#  Секој пациент се карактеризира со име и презиме, датум на раѓање, пол и е-пошта за контакт.
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

# Секој преглед се карактеризира со тип на преглед (кардиолошки, дерматолошки или невролошки),
# опис на симптоми, статус (закажан, во тек, завршен), термин (датум и време), и забелешка.
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

    # Еден преглед мора да има еден одговорен лекар
    responsible_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_type = models.CharField(max_length=100, choices=TYPE)
    description = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS, default='scheduled')
    datetime = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    # Еден пациент може да има повеќе прегледи во различни термини (1 ПАЦИЕНТ - ПОВЕЌЕ ПРЕГЛЕДИ)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)


# Еден преглед мора да има еден одговорен лекар, но може да има и дополнителни асистенти (други лекари).
# еден преглед - повеќе лекари
# Еден лекар може да учествува на повеќе прегледи (еден лекар - повеќе прегледи)
class AppointmentAssignment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('appointment', 'doctor')



