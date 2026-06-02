from django.contrib import admin
from django.db.models import Q

from .models import *

# Register your models here.
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    ...

    # Лекари и пациенти може да бидат додадени само од супер-корисници.
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    ...

    # Лекари и пациенти може да бидат додадени само од супер-корисници.
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    ...

    # Корисникот што го додава прегледот автоматски станува одговорен лекар
    def save_model(self, request, obj, form, change):

        if not change:
            obj.responsible_doctor = Doctor.objects.get(user=request.user)

        super().save_model(request, obj, form, change)

    # Прегледите може да бидат додадени од сите корисници - лекари,
    def has_add_permission(self, request, obj=None):
        if hasattr(request.user, 'doctor') or request.user.is_superuser:
            return True
        return False

    # Преглед може да се избрише само ако е незапочнат
    def has_delete_permission(self, request, obj=None):

        if obj.status == 'scheduled':
            return True

        return False

    from django.db.models import Q

    # Лекарите може да ги гледаат само прегледите на кои тие се одговорни или се доделени како асистенти
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        doctor = Doctor.objects.get(user=request.user)

        return qs.filter(
            Q(responsible_doctor=doctor) |
            Q(appointmentassignment__doctor=doctor)
        ).distinct()


    # Прегледите може да се менуваат само од лекар што е одговорен за нив или од супер-корисник
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True

        if request.user == obj.responsible_doctor.user:
            return True
        return False
