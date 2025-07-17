from django.shortcuts import render
from .forms import UserRegisterForm
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from article.models import Article
from newsletter.models import Newsletter
from django.core.mail import EmailMessage
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.forms import SetPasswordForm
import secrets
from hashlib import sha1
from .models import ResetToken

User = get_user_model()


# Create your views here.
def home_view(request):
    """
    Render the home page view.
    """
    
    articles = Article.objects.all()
    newsletters = Newsletter.objects.all()
    context = {
        'articles': articles,
        'newsletters': newsletters
    }
    return render(request, 'accounts/home.html', context)


def register_user(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Create the user
            # user = form.save(commit=False)

            username = form.cleaned_data.get('username')
            if not username:
                form.add_error('username', 'Username is required.')
                return render(request, 'register_user.html', {'form': form})

            # user.username = username
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password1')
            # user.save()

            position = form.cleaned_data.get('position')
            
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    position=position
                )
            
            except IntegrityError:
                form.add_error('username', 'This username is already taken.')
                return render(request, 'accounts/register_user.html', {'form': form})
            
            # position = form.cleaned_data.get('position')

            # CustomUser.objects.create(
            #     user=user,
            #     # email=user.email,
            #     # first_name=user.first_name,
            #     # last_name=user.last_name,
            #     position=position
            # )

            # Authenticate and log in the user
            login(request, user)

            # Redirect based on user_type
            if position == 'reader':
                messages.success(request, 'You have been successfully registered and logged in as a reader.')
                return redirect('reader_dashboard')
            
            elif position == 'editor':
                messages.success(request, 'You have been successfully registered and logged in as an editor.')
                return redirect('dashboard_editor')
            
            elif position == 'journalist':
                messages.success(request, 'You have been successfully registered and logged in as a journalist.')
                return redirect('journalist_dashboard')
            
            elif position == 'publisher':
                messages.success(request, 'You have been successfully registered and logged in as a publisher.')
                return redirect('publisher_home')

        else:
            messages.error(request, "The registration was unsuccessful. Please try again.")
            return render(request, 'accounts/register_user.html', {'form': form})
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register_user.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        user = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=user, password=password)
        
        position = request.POST.get('position')
        
        if user is not None:
            login(request, user)
            try:
                profile = user
                
                position = profile.position
                if position == 'reader':
                    return redirect('reader_dashboard')
                elif position == 'editor':
                    return redirect('dashboard_editor')
                elif position == 'journalist':
                    return redirect('journalist_dashboard')
                # elif position == 'publisher':
                #     return redirect('publisher_home')
            
            except CustomUser.DoesNotExist:
                messages.error(request, "User profile not found. Please register first.")
                return redirect('register_user')

            # messages.success(request, 'You have been successfully logged in. Welcome user!')
            # return redirect('home_view')
        
        else:
            messages.error(request, ('Login was unsuccessful please try again'))
            return HttpResponseRedirect(reverse('login_user'))
            # return redirect('home_view')
        
    else:
        return render(request, 'accounts/login_user.html')
    
    
def logout_user(request):
    logout(request)
    messages.success(request, ('You have been successfully logged out '))
    return redirect('home_view')


def reset_password(request):
    # Placeholder for password reset functionality
    messages.info(request, "Password reset functionality is not implemented yet.")
    return redirect('home_view')


def build_email(user, reset_url):
    subject = "Password Reset"
    user_email = user.email
    domain_email = "example@domain.com"
    body = f"Hi {user.username},\nHere is your link to reset your password: {reset_url}"
    email = EmailMessage(subject, body, domain_email, [user_email])
    return email


def generate_reset_url(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, "No user with that email was found.")
        else:
            for user in users:
                domain = "http://127.0.0.1:8000/"
                token = secrets.token_urlsafe(16)
                expiry_date = timezone.now() + timedelta(minutes=5)
                hashed_token = sha1(token.encode()).hexdigest()

                
                ResetToken.objects.create(user=user, token=hashed_token, expiry_date=expiry_date)

                reset_link = f"{domain}takealot/password_reset_user/{user.id}/{token}/"


            messages.success(request, "A password reset link has been sent to your email.")

        return redirect('login_user')

    return render(request, 'accounts/password_reset.html')


def reset_user_password(request):

    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.filter(email=email)
            url = generate_reset_url(request)
            email = EmailMessage("Reset Your Password", f"Click the link to reset your password: {url}")
            email.send()

            messages.success(request, "A password reset link has been sent to your email.")
        except User.DoesNotExist:
            messages.error(request, "No user with that email was found.")
        return redirect('login_user')
    return render(request, 'accounts/password_reset.html')


def password_confirmation(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        reset_token = ResetToken.objects.get(user=user)

        if not reset_token.is_valid(token):
            messages.error(request, "Reset link is invalid or has expired.")
            return redirect('login_buyer')

        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                reset_token.delete()
                messages.success(request, "Password reset successful.")
                return redirect('login_buyer')
        else:
            form = SetPasswordForm(user)
    except (User.DoesNotExist, ResetToken.DoesNotExist):
        messages.error(request, "Invalid reset request.")
        return redirect('login_buyer')

    return render(request, 'accounts/password_reset_confirm.html', {'form': form})

