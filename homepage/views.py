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
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Send registration email
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail
            load_dotenv()
            message = Mail(
                from_email='membership@latinosinfinance.org',
                to_emails= request.user.email
                subject='Regisration Successful',
                html_content='<strong>Thanks for registering with us!!!</strong>')
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e.message)


            
            recipient = user.email
            subject = "You have successfully registered"
            body = "Thanks for registerig with us"
            send_email(recipient, subject, body)


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

        # Ensure profile exists
        profile, _ = Profile.objects.get_or_create(user=user)
        
        # Ensure profession exists
        profession, _ = Profession.objects.get_or_create(user=user)

        # Update fields from the form
        # First Card
        profession.position = request.POST.get("position", profession.position or "")
        profession.company = request.POST.get("company", profession.company or "")
        profile.city = request.POST.get("city", profile.city or "")
        profile.state = request.POST.get("state", profile.state or "")
        profile.country = request.POST.get("country", profile.country or "")
        profile.phone = request.POST.get("phone", profile.phone or "")
        user.email = request.POST.get("email", user.email or "")
        # Second Card
        profession.career_stage = request.POST.get("career_stage", profession.career_stage or "")
        profession.industry = request.POST.get("industry", profession.industry or "")
        profession.industry_interest = request.POST.get("industry_interest", profession.industry_interest or "")
        
        profession.school = request.POST.get("school", profession.school or "")
        profession.major_minor = request.POST.get("major_minor", profession.major_minor or "")
        profession.graduation_year = request.POST.get("graduation_year", profession.graduation_year or "1900")
        profession.gpa = request.POST.get("gpa", profession.gpa or "0.00")
        # Third Card
        profession.linkedin = request.POST.get("linkedin", profession.linkedin or "")
        profession.volunteer_interest = request.POST.get("volunteer_interest", profession.volunteer_interest or "")




        # Handle image upload
        if "image" in request.FILES:
            profile.image = request.FILES["image"]

        # Save updates
        profession.save()
        profile.save()
        user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile")

    return render(request, "homepage/update_profile.html", {"user": request.user})


def resumeboard(request):
    userdb = User.objects.all()
    return render(request, 'resumeboard.html', {'userdb': userdb})