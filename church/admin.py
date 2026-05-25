from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Event)
admin.site.register(Group)
admin.site.register(Leadership)
admin.site.register(EventAttendance)
admin.site.register(Attendee)