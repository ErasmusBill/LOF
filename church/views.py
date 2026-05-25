from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import re
from django.conf import settings
from .forms import EventAttendanceForm
from django.shortcuts import render, redirect
from .forms import EventAttendanceForm


# Create your views here.

def home(request):
    events = Event.objects.all()
    groups = Group.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        #phonenumber = request.POST.get('phonenumber')
        message = request.POST.get('message')
        subject = request.POST.get('subject')

        if not email or not name or not message or not subject:
            messages.error(request, "All fields are required.")
            return redirect('church:home')


        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            messages.error(request, "Invalid email address. Please enter a valid email.")
            return redirect('church:home')

      
        try:
            email_message = EmailMessage(
                subject=f"Message from {name}",
                body=f"""
                Name: {name}
                Email: {email}
                Message: {message}
                """,
                from_email=email,
                to=["fruitfulyouth01@gmail.com"],
            )
            
            email_message.send()
            messages.success(request, "Email sent successfully!")
            return redirect('church:home')  
        
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")
            return redirect('church:home')
    
    return render(request, 'church/index.html', {'events': events, 'groups': groups})
   


def about(request):
    leaders = Leadership.objects.all()
    return render(request, 'church/about.html', {'leaders':leaders})  


def history(request):
    return render(request, 'church/history.html', {})

def church_service(request):
    return render(request,'church/church_service.html', {})

def vision(request):
    return render(request, 'church/vision.html', {})

def mission(request):
    return render(request, 'church/mission.html', {})


def create_event_attendance(request):
    event_id = request.GET.get("event")
    form = EventAttendanceForm(request.POST or None, initial={"event": event_id})

    if request.method == "POST" and form.is_valid():
        attendance = form.save()
        messages.success(
            request,
            f"Attendance recorded for {attendance.attendee.name}!"
        )
        return redirect("church:create-attendance")

    return render(request, "church/create_attendance.html", {"form": form})


def event_attendance_list(request, event_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page")
        return redirect("tithe:login_user")

    if request.user.role != "ADMIN":
        messages.error(
            request,
            "You don't have permission to view attendance records. Contact your administrator."
        )
        return redirect("tithe:home")

    event = get_object_or_404(Event, id=event_id)

    attendances_qs = EventAttendance.objects.filter(
        event=event
    ).select_related("attendee").order_by("-checked_in_at")

    paginator = Paginator(attendances_qs, 30)
    page = request.GET.get("page")

    try:
        attendances = paginator.page(page)
    except PageNotAnInteger:
        attendances = paginator.page(1)
    except EmptyPage:
        attendances = paginator.page(paginator.num_pages)

    context = {
        "event": event,
        "attendances": attendances
    }

    return render(request, "tithe/event_attendance_list.html", context)