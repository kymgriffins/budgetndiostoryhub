from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm


def api_docs(request):
    """Serve API documentation page."""
    return render(request, 'api_docs.html')


def home(request):
    """Home page - serves the Next.js build output."""
    return render(request, 'out/home/index.html')


def index(request):
    """Main index page - serves the main app."""
    return render(request, 'out/home/index.html')


def config_page(request):
    """Serve UI configuration page."""
    return render(request, 'config.html')


def v2_page(request):
    """V2 landing page - serves the new Budget Ndio Story landing page."""
    return render(request, 'v2.html')


def manuals_page(request):
    """Serve the manuals and documentation hub page."""
    return render(request, 'frontend/manuals.html')


def manual_page(request):
    """Serve the user manual page."""
    return render(request, 'frontend/manual.html')


def settings_page(request):
    """Serve the settings page."""
    return render(request, 'frontend/settings.html')


def profile_page(request):
    """Serve the profile page."""
    return render(request, 'frontend/profile.html')


def content_page(request):
    """Serve the content list page."""
    return render(request, 'frontend/content-list.html')


def register_page(request):
    """Serve the registration page."""
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth import login
    from django.shortcuts import redirect
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login_page(request):
    """Serve the login page with both login and signup options."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login-new.html', {'form': form})
