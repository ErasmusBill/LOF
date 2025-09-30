from django import forms
from .models import CustomUser,PasswordResetRequest,Tithe
from django.core.exceptions import ValidationError
from django.utils import timezone

class RegisterUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "password", "username", "email", "avatar", "phone_number"]
       
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        return password
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
    
class UpdateUserform(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name","last_name","username","email","phone_number","avatar"]
    
class TitheForm(forms.ModelForm):
    class Meta:
        model = Tithe
        fields = ["user", "amount", "date"]  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01', 'placeholder': 'Enter amount'}),
        }
        labels = {
            'user': 'Church Member',
            'amount': 'Tithe Amount',
            'date': 'Payment Date',
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise ValidationError("Amount must be greater than 0")
        return amount
    
    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date and date > timezone.now().date():
            raise ValidationError("Date cannot be in the future")
        return date

    
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not CustomUser.objects.filter(email=email).exists():
            raise ValidationError("No account is registered with this email.")
        return email

    def save(self):
        email = self.cleaned_data['email']
        user = CustomUser.objects.get(email=email)
        return PasswordResetRequest.objects.create(user=user)
    
class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput,label="Current password")
    new_password = forms.CharField(widget=forms.PasswordInput,label="New password")
    confirm_password = forms.CharField(widget=forms.PasswordInput,label="Confirm password")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        if new_password and len(new_password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        return cleaned_data
