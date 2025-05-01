from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect   
from .models import User, Profile, Profession
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from django.core.files.storage import default_storage

import io
from django.shortcuts import render, redirect
from django.conf import settings


from django.db.models import Q

from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

from django.shortcuts import get_object_or_404



# Create your views here.

def index(request):
    return render(request, 'homepage/index.html', {})

def home(request):
    return render(request, 'homepage/home.html', {})

def profile(request):
    return render(request, 'homepage/profile.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")  # Use get() to avoid KeyError
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log in the user
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")  # Show error message
            return redirect('home')  # Redirect back to login page

    return redirect('home')   # Render login page for GET requests

   
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and log user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email1 = form.cleaned_data.get('email')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # Send a welcome email
            send_mail(
                subject='Welcome to Latinos in Finance!',
                message=(
                f"Hi {user.first_name} {user.last_name},\n\n"
                "Thank you for registering with Latinos in Finance.\n"
                "We're excited to have you on board!\n\n"
                "Visit your profile to update your resume and explore opportunities.\n\n"
                "Best,\n"
                "The LIF Team"
                ),
                from_email='membership@latinosinfinance.org',
                recipient_list=[email1],
                fail_silently=False
            )
            messages.success(request, 'You have successfully registered.')
            return redirect('home')
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = SignUpForm()
        return render(request, 'homepage/register_user.html', {'form': form})
    return render(request, 'homepage/register_user.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == "POST":
        user = request.user

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile(user=user)
            profile.save()

        # Check if the profession exists, if not, create it
        profile, _ = Profile.objects.get_or_create(user=user)
        profession, _ = Profession.objects.get_or_create(user=user)

        # Update fields from the form
        # First Card
        profession.position = request.POST.get("position", profession.position)
        profession.company = request.POST.get("company", profession.company)
        profile.city = request.POST.get("city", profile.city)
        profile.state = request.POST.get("state", profile.state)
        profile.country = request.POST.get("country", profile.country)
        profile.phone = request.POST.get("phone", profile.phone)
        user.email = request.POST.get("email", user.email)

        # Second Card
        profession.career_stage = request.POST.get("career_stage", profession.career_stage)
        profession.industry = request.POST.get("industry", profession.industry)
        profession.industry_interest = request.POST.get("industry_interest", profession.industry_interest)
        profession.school = request.POST.get("school", profession.school)
        profession.major_minor = request.POST.get("major_minor", profession.major_minor)
        profession.graduation_year = request.POST.get("graduation_year", profession.graduation_year)
        profession.gpa = request.POST.get("gpa", profession.gpa)

        # Third Card
        profession.linkedin = request.POST.get("linkedin", profession.linkedin)
        profession.volunteer_interest = request.POST.get("volunteer_interest", profession.volunteer_interest)
        profile.resume = request.FILES.get("resume", profile.resume)

        # Image upload
        if "image" in request.FILES:
            profile.image = request.FILES["image"]

        # Check if the resume file is uploaded
        if profile.resume and hasattr(profile.resume, 'url'):
            resume_url = profile.resume.url
        else:
            resume_url = None

        # Save all updates
        profession.save()
        profile.save()
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "homepage/update_profile.html", {"user": request.user})

@login_required
def resumeboard(request):
    userdb = User.objects.all()
    return render(request, "homepage/resumeboard.html", {'userdb': userdb})

@login_required
def search_members(request):
    search_query = request.GET.get('search', '')    

    userdb = Profession.objects.select_related('user', 'user__profile').filter(
        Q(career_stage__icontains=search_query) |
        Q(position__icontains=search_query) |
        Q(industry__icontains=search_query) |
        Q(company__icontains=search_query) |
        Q(user__profile__city__icontains=search_query) |  # Searching in Profile model's city
        Q(user__profile__state__icontains=search_query) |  # Searching in Profile model's state
        Q(user__profile__country__icontains=search_query)  # Searching in Profile model's country
    )

    return render(request, 'homepage/search_members.html', {'userdb': userdb})

    
@login_required
def delete_user(request, id):
    user = get_object_or_404(User, id=id)
    if request.user == user:
        user.delete()
        return redirect('home')
 



def custom_password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse('custom_password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )
            subject = "Reset Your Password"
            message = f"""
                Hi {user.first_name},

                You requested a password reset. Click the link below to reset your password:
                {reset_url}

                If you didn't request this, you can ignore this email.

                Best,
                Latinos in Finance Team
            """
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.success(request, 'A password reset link has been sent to your email.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
        return redirect('custom_password_reset')
    return render(request, 'homepage/password_reset_request.html')

def custom_password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password reset successfully.")
                return redirect('login-user')
        else:
            form = SetPasswordForm(user)
        return render(request, 'homepage/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect('custom_password_reset')