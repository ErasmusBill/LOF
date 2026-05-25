from django import forms
from .models import EventAttendance, Event, Attendee


class EventAttendanceForm(forms.ModelForm):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    name = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter full name"
        })
    )

    occupation = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter occupation"
        })
    )

    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter phone number"
        })
    )

    fellowship = forms.CharField(
        max_length=250,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter fellowship"
        })
    )

    class Meta:
        model = EventAttendance
        fields = ["event"]

    def save(self, commit=True):
        attendee = Attendee.objects.create(
            name=self.cleaned_data["name"],
            phone_number=self.cleaned_data["phone_number"],
            occupation=self.cleaned_data["occupation"],
            fellowship=self.cleaned_data["fellowship"],
        )

        attendance = EventAttendance.objects.create(
            event=self.cleaned_data["event"],
            attendee=attendee
        )

        attendance.is_duplicate = False
        return attendance