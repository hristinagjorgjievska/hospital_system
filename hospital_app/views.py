from django.utils import timezone

from django.shortcuts import render, get_object_or_404

from .models import *

# Create your views here.
def index(request):
    cardiologists = Doctor.objects.filter(specialty='cardiologist')
    dermatologists = Doctor.objects.filter(specialty='dermatologist')
    neurologists = Doctor.objects.filter(specialty='neurologist')

    return render(request, "index.html", {
        "cardiologists": cardiologists,
        "dermatologists": dermatologists,
        "neurologists": neurologists,
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import AppointmentForm


def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)

    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            appointment = form.save(commit=False)

            appointment.responsible_doctor = doctor

            appointment.appointment_type = doctor.specialty

            appointment.save()

            AppointmentAssignment.objects.create(
                appointment=appointment,
                doctor=doctor
            )

            return redirect("doctor_detail", doctor_id=doctor.id)

    else:
        form = AppointmentForm()

    today = date.today()

    past_appointments = Appointment.objects.filter(
        responsible_doctor=doctor,
        datetime__date__lt=today
    )

    today_appointments = Appointment.objects.filter(
        responsible_doctor=doctor,
        datetime__date=today
    )

    future_appointments = Appointment.objects.filter(
        responsible_doctor=doctor,
        datetime__date__gt=today
    )

    return render(
        request,
        "doctor_detail.html",
        {
            "doctor": doctor,
            "form": form,
            "past_appointments": past_appointments,
            "today_appointments": today_appointments,
            "future_appointments": future_appointments,
        }
    )
