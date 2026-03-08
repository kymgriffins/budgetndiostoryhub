from django.shortcuts import render
from django.conf import settings


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
