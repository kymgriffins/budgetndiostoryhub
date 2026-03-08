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
