from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Event(models.Model):
    name = models.CharField(_("Event Name"), max_length=250)
    image = models.ImageField(_("Event Image"), upload_to="uploads/event/")
    # Added auto_now_add to support views filtering by '.latest()' or '.order_by("-id")' safely
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(_("Group Name"), max_length=250)
    description = models.TextField(_("Description"))
    image = models.ImageField(_("Group Image"), upload_to="uploads/group/")
    is_second = models.BooleanField(_("Is Second Group"), default=False)

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")

    def __str__(self):
        return self.name


class Leadership(models.Model):
    name = models.CharField(_("Full Name"), max_length=250)
    bio = models.TextField(_("Biography"))
    image = models.ImageField(_("Profile Image"), upload_to="uploads/leadership/")
    role = models.CharField(_("Role / Position"), max_length=250)

    class Meta:
        verbose_name = _("Leadership Record")
        verbose_name_plural = _("Leadership Records")

    def __str__(self):
        return f"{self.name} ({self.role})"


class Attendee(models.Model):
    name = models.CharField(_("Full Name"), max_length=250)
    occupation = models.CharField(_("Occupation"), max_length=250, blank=True, null=True)
    # 20-30 characters is standard practice for phone configurations globally
    phone_number = models.CharField(_("Phone Number"), max_length=30)
    fellowship = models.CharField(_("Fellowship / Cell Group"), max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")

    def __str__(self):
        return self.name


class EventAttendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendances")
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE, related_name="events_attended")
    checked_in_at = models.DateTimeField(_("Checked In At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Event Attendance")
        verbose_name_plural = _("Event Attendances")
        unique_together = ("event", "attendee")

    def __str__(self):
        return f"{self.attendee.name} - {self.event.name}"