from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from .models import CustomUser,PasswordResetRequest,Tithe
from .forms import RegisterUserForm,TitheForm,PasswordResetRequestForm,ChangePasswordForm,UpdateUserform
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.forms import ValidationError
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

# from .models import send_register_email_token
# Create your views here.


def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # user.send_register_email_token()
            messages.success(request,"User registered successfully,Please check your email to activate your account")
            return redirect("tithe:login_user")
        else:
            # print("Form errors:", form.errors)
            return render(request,"tithe/signup.html",{"form":form})
    else:
        form = RegisterUserForm()
        return render(request,"tithe/signup.html",{"form":form})
    
    
# def activate_user_account(request,token):
#     try:
#         token = CustomUser.objects.get(tokne=token)
#     except CustomUser.DoesNotExist:
#         messages.error(request, "Invalid or expired token.")
#         return redirect("tithe:register_user")
    
#     if not token.is_valid():
#         messages.error(request, "Invalid or expired token.")
#         return redirect("tithe:register_user")
    
#     token.is_active == True
#     return redirect("tithe:login_user")
    
    
        
        

@login_required
def update_user(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must login before you can perform action")
        return redirect("tithe:login_user")

    if request.method == "POST":
        form = UpdateUserform(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully updated your profile")
            
            
            if request.user.role == "ADMIN":
                return redirect("tithe:admin-dashboard")
            else:
                return redirect("tithe:user-dashboard")  
            
        else:
            return render(request, "tithe/update_user.html", {"form": form})
    else:
        form = UpdateUserform(instance=request.user)  
        return render(request, "tithe/update_user.html", {"form": form})
            

def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not username or not password:
            messages.error(request, "Please provide both username and password")
            return render(request, "tithe/login.html")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
        
            if user.role == "ADMIN": # type: ignore
                return redirect("tithe:admin-dashboard")
            elif user.role == "REGULAR_USER":    # type: ignore
                return redirect("tithe:user-dashboard")
            else:
                messages.warning(request, "Your account role is not recognized.")
                return redirect("tithe:login_user")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, "tithe/login.html")
    else:
        return render(request, "tithe/login.html")
    
@login_required   
def logout_user(request):
    logout(request)
    messages.success(request,"User logged out successfully")
    return redirect("church:home")

@login_required
def add_tithe(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page")
        return redirect("tithe:login_user")
    
    if not request.user.role == "ADMIN":
        messages.error(request, "You don't have permission to add tithe records. Contact your administrator.")
        return redirect("tithe:home") 
    
    if request.method == "POST":
        form = TitheForm(request.POST)
        if form.is_valid():
            tithe = form.save()
            
          
            try:
              
                text_message = f"""
                            Hello {tithe.user.username},

                            You paid a tithe of ₵{tithe.amount} on {tithe.date}.

                            Thank you for your faithfulness!

                            May God bless you abundantly.

                            Best regards,
                            Church Administration
                        """
                
              
                html_message = f"""
                <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                        <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                            <div style="background-color: blue; color: white; padding: 20px; text-align: center;">
                                <h1>Tithe Receipt</h1>
                            </div>
                            
                            <div style="background-color: white; padding: 30px; margin-top: 20px;">
                                <p>Hello <strong>{tithe.user.username}</strong>,</p>
                                
                                <p>Thank you for your faithful tithe payment.</p>
                                
                                <h3>Payment Details:</h3>
                                <ul>
                                    <li><strong>Amount:</strong> <span style="color: #4CAF50; font-size: 20px;">₵{tithe.amount}</span></li>
                                    <li><strong>Date:</strong> {tithe.date}</li>
                                </ul>
                                
                                <p style="font-style: italic; color: #555;">
                                    "Bring the whole tithe into the storehouse, that there may be food in my house. 
                                    Test me in this," says the Lord Almighty, "and see if I will not throw open the 
                                    floodgates of heaven and pour out so much blessing that there will not be room 
                                    enough to store it." - Malachi 3:10
                                </p>
                                
                                <p>May God bless you abundantly!</p>
                                
                                <p>Best regards,<br>Church Administration</p>
                            </div>
                            
                            <div style="text-align: center; margin-top: 20px; color: #777; font-size: 12px;">
                                <p>This is an automated message. Please do not reply to this email.</p>
                            </div>
                        </div>
                    </body>
                </html>
                """
                
                subject = "Tithe Receipt"
                
               
                email = EmailMultiAlternatives(
                    subject,
                    text_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [tithe.user.email]
                )
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=True)
                
                messages.success(request, f"Tithe of ₵{tithe.amount} for {tithe.user.get_full_name() or tithe.user.username} added successfully. Email sent.")
            except Exception as e:
                messages.warning(request, f"Tithe added but email failed to send: {str(e)}")
            
            return redirect("tithe:admin-dashboard") 
    else:
        form = TitheForm()
    
    return render(request, "tithe/add_tithe.html", {"form": form})

@login_required
def edit_tithe(request,tithe_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page")
        return redirect("tithe:login_user")
    
    if not request.user.role == "ADMIN":
        messages.error(request, "You don't have permission to add tithe records. Contact your administrator.")
        return redirect("tithe:home") 
    
    tithe = get_object_or_404(Tithe,id=tithe_id)
    if request.method == 'POST':
        form = TitheForm(request.POST,instance=tithe)
        if form.is_valid():
            form.save()
            messages.success(request,"You have successfully update the tithe")
            return redirect("tithe:admin-dashboard")
    else:
        return render(request,"tithe/edit-tithe.html")
    
@login_required    
def delete_tithe(request,tithe_id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page")
        return redirect("tithe:login_user")
    
    if not request.user.role == "ADMIN":
        messages.error(request, "You don't have permission to add tithe records. Contact your administrator.")
        return redirect("tithe:home") 
    
    tithe = get_object_or_404(Tithe,id=tithe_id)
    tithe.delete()
    messages.success(request,"You have successfully deleted a tithe")
    return redirect("tithe:admin-dashboard")
    

def request_password_reset(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            password_reset_request = form.save()
            password_reset_request.send_reset_email()
            messages.success(request,"Password reset email sent successfully")
            return redirect("tithe:login_user")
        else:
            return render(request,"tithe/request_password_reset.html",{"form":form})
    else:
        form = PasswordResetRequestForm()
        return render(request,"tithe/request_password_reset.html",{"form":form})
    
def reset_password(request, token):
    try:
        password_reset_request = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        messages.error(request, "Invalid or expired password reset token.")
        return redirect("tithe:login_user")

    if not password_reset_request.is_valid():
        messages.error(request, "Invalid or expired password reset token.")
        return redirect("tithe:login_user")

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not new_password or not confirm_password:
            messages.error(request, "Please provide both password fields.")
            return render(request, "tithe/reset_password.html", {"token": token})

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "tithe/reset_password.html", {"token": token})

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "tithe/reset_password.html", {"token": token})

        user = password_reset_request.user
        user.set_password(new_password)
        user.save()

        password_reset_request.is_used = True
        password_reset_request.save()

        messages.success(request, "Password reset successfully. You can now log in with your new password.")
        return redirect("tithe:login_user")
    else:
        return render(request, "tithe/reset_password.html", {"token": token})
 
@login_required      
def change_password(request):
    if not request.user.is_authenticated:
        raise PermissionDenied("You are not authorized to perform this action")

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']

           
            if not request.user.check_password(current_password):
                messages.error(request, "Your current password is incorrect.")
                return render(request, "tithe/change_password.html", {"form": form})

        
            request.user.set_password(new_password)
            request.user.save()

          
            update_session_auth_hash(request, request.user)

            messages.success(request, "Your password has been changed successfully.")
            if request.user.role == "ADMIN":
                return redirect("tithe:admin-dashboard")
            else:
                return redirect("tithe:admin-dashboard")  
    else:
        form = ChangePasswordForm()

    return render(request, "tithe/change_password.html", {"form": form})

@login_required  
def list_tithe(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page")
        return redirect("tithe:login_user")
    
    if not request.user.role == "ADMIN":
        messages.error(request, "You don't have permission to add tithe records. Contact your administrator.")
        return redirect("tithe:user-dashboard") 
    
    tithes = Tithe.objects.all().order_by("-date")
    paginator = Paginator(tithes,50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,"tithe/list-tithe.html",{"page_obj":page_obj})

@login_required  
def list_related_user(request):
    user = request.user
    tithe = Tithe.objects.filter(user=user).all()
    return render(request,"tithe/user-tithe.html",{"tithe":tithe})


@login_required  
def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != "ADMIN":
        messages.error(request, "You don't have permission to access this page")
        return redirect("tithe:login_user")  

    members = CustomUser.objects.count()
    today = timezone.now().date()
    total_tithe_today = Tithe.objects.filter(date=today).aggregate(total=Sum('amount'))['total'] or 0
    total_tithe_all_time = Tithe.objects.aggregate(total=Sum('amount'))['total'] or 0  # ← ADD THIS

    tithes = Tithe.objects.select_related('user').order_by("-date") 
    paginator = Paginator(tithes, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    users = CustomUser.objects.all()

    return render(request, "tithe/admin_dashboard.html", {
        "members": members,
        "total_tithe_today": total_tithe_today,
        "total_tithe_all_time": total_tithe_all_time, 
        "page_obj": page_obj,
        "users": users
    })


@login_required   
def user_dashboard(request):  
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page")
        return redirect("tithe:login_user")  
    
    tithe = Tithe.objects.filter(user=request.user)
    paginator = Paginator(tithe, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    total_amount = tithe.aggregate(total=Sum('amount'))['total'] or 0
    
    return render(request, "tithe/user_dashboard.html", {
        "page_obj": page_obj,
        "total_amount": total_amount
    })
    
@login_required  
def list_tithe_related_user_by_admin(request, user_id):
    if not request.user.is_authenticated or request.user.role != "ADMIN":
        messages.error(request, "You don't have permission to access this page")
        return redirect("tithe:login_user")  
    
    user = get_object_or_404(CustomUser, id=user_id)
    amount = Tithe.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    tithe = Tithe.objects.filter(user=user).order_by("-date")
    
    paginator = Paginator(tithe, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "tithe/user_tithe_admin_view.html", {
        "page_obj": page_obj,
        "viewed_user": user,
        "total_amount": amount
    })
    


