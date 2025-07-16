from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect, get_object_or_404   
from .models import User, Profile, Profession, Job
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.shortcuts import redirect
from .forms import SignUpForm, JobForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.paginator import Paginator


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
from django.utils import timezone


from django.db.models import Q

from django.core.mail import send_mail

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm

from django.shortcuts import get_object_or_404

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

# Chatbot imports
import json
from django.views.decorators.csrf import csrf_exempt
from .chatbot.chat_engine import ask_question
from django.http import JsonResponse


load_dotenv()


# Create your views here.

def index(request):
    return render(request, 'homepage/index.html', {})

def home(request):
    users = User.objects.exclude(id=request.user.id).order_by('first_name')  # Exclude current user
    paginator = Paginator(users, 6)  # Show 6 users per page

    page_number = request.GET.get('page')
    paginator_userdb = paginator.get_page(page_number)

    return render(request, 'homepage/home.html', {
        'paginator_userdb': paginator_userdb
    })

@login_required
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
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email1 = form.cleaned_data.get('email')

            user = authenticate(username=username, password=raw_password)
            login(request, user)

            # Personalized welcome HTML
            html_content = f"""
                            <div style="font-family: Arial, sans-serif; font-size:14px; line-height:1.6; color:#333;">
                                <!-- Logo at the top -->
                                <div style="text-align: center; margin-bottom: 20px;">
                                    <img src="https://images.squarespace-cdn.com/content/v1/52742948e4b0c2eac22b888e/1383594624830-QFRNTFEY4CJ8HY4I0QZQ/LIFi.jpg?format=1500w" alt="Latinos in Finance" style="width: 150px;">
                                </div>

                                <p><strong>Welcome to Latinos in Finance, {first_name} {last_name}!</strong></p>
                                <p>We’re excited to have you as part of our growing community of Latino professionals in finance.</p>
                                <p>To access the full benefits of your membership — including networking opportunities, event invitations, and member-only resources — please take a moment to 
                                    <a href="https://crmproject-9f4q.onrender.com" target="_blank">update your profile</a>.
                                </p>
                                <p>This helps us personalize your experience and connect you with the right people and opportunities.</p>
                                <p>Bienvenidos — we look forward to growing with you!</p>
                                <br>
                                <p>Follow us:</p>
                                <!-- Social media links -->
                                <div style="margin-top: 30px; text-align: left;">
                                    <a href="https://instagram.com/latinosinfinance" target="_blank" style="margin-right: 10px;">
                                        <img src="https://cdn-icons-png.flaticon.com/512/1384/1384063.png" alt="Instagram" style="width: 24px; height: 24px;">
                                    </a>
                                    <a href="https://www.linkedin.com/company/latinos-in-finance" target="_blank" style="margin-right: 10px;">
                                        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="width: 24px; height: 24px;">
                                    </a>
                                    <a href="https://www.youtube.com/@LatinosInFinance" target="_blank">
                                        <img src="https://cdn-icons-png.flaticon.com/512/1384/1384060.png" alt="YouTube" style="width: 24px; height: 24px;">
                                    </a>
                                </div>
                            </div>
                        """

            # Send a welcome email
            message = Mail(
                from_email='Latinos in Finance <membership@latinosinfinance.org>',  # Replace with a verified email
                to_emails=email1,  # Replace with the recipient's email
                subject='Welcome to Latinos in Finance',
                html_content=html_content,         
                )

            try:
                # Get the API key from the environment variable
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY').strip())
                
                # Send the email
                response = sg.send(message)

                messages.success(request, 'You have successfully registered.')
                return redirect('update_profile')  # Redirect to profile update page after registration
        
            except Exception as e:
                print(f"Error: {str(e)}")
                
            
        else:
            messages.error(request, 'Unsuccessful registration. Invalid information.')
    else:
        form = SignUpForm()
        return render(request, 'homepage/register_user.html', {'form': form})
    return render(request, 'homepage/index.html', {'form': form})

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
        profile.gender = request.POST.get("gender", profile.gender)
        user.email = request.POST.get("email", user.email)

        # Second Card
        profession.career_stage = request.POST.get("career_stage", profession.career_stage)
        profession.industry = request.POST.get("industry", profession.industry)
        profession.industry_interest = request.POST.get("industry_interest", profession.industry_interest)
        profession.school = request.POST.get("school", profession.school)
        profession.major_minor = request.POST.get("major_minor", profession.major_minor)
        profession.graduation_year = request.POST.get("graduation_year", profession.graduation_year)
        gpa = request.POST.get("gpa")
        profession.gpa = float(gpa) if gpa not in [None, ''] else 0.0

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


def dashboard_view(request):
    total_users = User.objects.count()

    gender_dist = list(Profile.objects.values('gender').annotate(count=Count('id')))
    city_dist = list(Profile.objects.values('city').annotate(count=Count('id')))
    state_dist = list(Profile.objects.values('state').annotate(count=Count('id')))
    industry_dist = list(Profile.objects.values('user__profession__industry').annotate(count=Count('id')))
    career_stage_dist = list(Profile.objects.values('user__profession__career_stage').annotate(count=Count('id')))
    position_dist = list(Profile.objects.values('user__profession__position').annotate(count=Count('id')))

    context = {
        'total_users': total_users,
        'gender_dist': gender_dist,
        'industry_dist': industry_dist,
        'city_dist': city_dist,
        'state_dist': state_dist,
        'career_stage_dist': career_stage_dist,
        'position_dist': position_dist,
    }

    return render(request, 'homepage/dashboard.html', context)

def member_profile(request, id):
    user = get_object_or_404(User, id=id)
    # Try to get the profile, or handle the case where it doesn't exist
    try:
        profile = user.profile  # Assuming a OneToOne relationship with Profile
    except Profile.DoesNotExist:
        profile = None  # If no profile exists, set profile to None

    # Get the associated Profession information (it should exist for each user)
    profession = user.profession if hasattr(user, 'profession') else None

    # Pass the user, profile, and profession to the context
    context = {
        'user1': user,
        'profile1': profile,
        'profession1': profession,
    }

    return render(request, 'homepage/member_profile.html', context)

def jobboard(request):
    # Get the current date
    current_date = timezone.now().date()

    # Fetch only jobs with a future application deadline
    job_list = Job.objects.filter(application_deadline__gt=current_date)

    # Paginate the filtered job list
    paginator = Paginator(job_list, 10)  # Show 10 jobs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get the logged-in user
    current_user = request.user if request.user.is_authenticated else None

    return render(request, 'homepage/jobs.html', {
        'page_obj': page_obj,
        'user': current_user,
    })

@login_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user  # Link the job to the logged-in user
            job.save()
            return redirect('jobboard')
    else:
        form = JobForm()

    return render(request, 'homepage/add_job.html', {'form': form})


def chat_view(request):
    history = request.session.get('chat_history', [])
    return render(request, 'chatbot/chat.html', {'history': history})

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')
        bot_response = ask_question(user_message)

        # If bot_response is a dictionary, extract the 'result' field
        if isinstance(bot_response, dict) and 'result' in bot_response:
            bot_reply = bot_response['result']
        else:
            bot_reply = str(bot_response)

        # Store in session history
        chat_entry = {'user': user_message, 'bot': bot_reply}
        history = request.session.get('chat_history', [])
        history.append(chat_entry)
        request.session['chat_history'] = history

        return JsonResponse({'response': bot_reply})
    
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        html_content = request.POST.get('message')

        message = Mail(
                from_email='Contact Message LIF CRM <membership@latinosinfinance.org>',  # Replace with a verified email
                to_emails='membership@latinosinfinance.org',  # Replace with the recipient's email
                subject=f'Conact Form Submission from {name}',
                html_content=f"""
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Message:</strong><br>{html_content}</p>
                """,         
                )

        try:
            # Get the API key from the environment variable
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY').strip())
                
            # Send the email
            response = sg.send(message)

            messages.success(request, 'Your message was sent successfully.')
            return redirect('home')  # Redirect to profile update page after registration
        
        except Exception as e:
            print(f"Error: {str(e)}")

    else:

        return render(request, 'homepage/contact.html')


def scholarship(request):
    return render(request, 'homepage/scholarship.html', {})