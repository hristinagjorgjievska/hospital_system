# Define your signal receivers here.
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from hospital_app.models import Appointment

# Доколку прегледот е додаден со статус завршен,
# но неговиот термин е за во иднина,
# системот автоматски ќе го промени статусот во закажан и обратно,
# доколку е додаден со статус закажан во минатото,
# тогаш автоматски ќе биде променет во завршен.
@receiver(pre_save, sender=Appointment)
def appointment_status_fix(sender, instance, **kwargs):

    if not instance.datetime:
        return

    now = timezone.now()

    if instance.status == "completed" and instance.datetime > now:
        instance.status = "scheduled"

    if instance.status == "scheduled" and instance.datetime < now:
        instance.status = "completed"

# Кога прегледот во тек ќе премине во статус завршен,
# потребно е само одговорниот лекар да го инкрементира бројот на успешно завршени прегледи.
@receiver(pre_save, sender=Appointment)
def increment_counter(sender, instance, **kwargs):

    if not instance.pk:
        return

    old = Appointment.objects.get(pk=instance.pk)

    if (
        old.status == "in_progress"
        and instance.status == "completed"
    ):
        doctor = instance.responsible_doctor
        doctor.completed_appointments += 1
        doctor.save()