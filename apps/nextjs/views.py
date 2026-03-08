"""
Django views for serving Next.js static export pages.
"""
from django.http import Http404, FileResponse, HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
from pathlib import Path
import mimetypes
import os


# Base directory for Next.js export
NEXT_EXPORT_DIR = Path(__file__).resolve().parent.parent.parent / 'templates' / 'out'


def get_next_js_file_path(relative_path: str) -> Path:
    """
    Get the full path to a Next.js export file.
    
    Args:
        relative_path: The relative path from the export root
        
    Returns:
        Path object pointing to the file
    """
    # Remove leading slash if present
    if relative_path.startswith('/'):
        relative_path = relative_path[1:]
    
    return NEXT_EXPORT_DIR / relative_path


def serve_next_static(request, path_info):
    """
    Serve Next.js static files from the _next folder.
    
    Args:
        request: The HTTP request
        path_info: The path to the static file
        
    Returns:
        FileResponse or 404 response
    """
    # Try the templates/out/_next path first
    file_path = NEXT_EXPORT_DIR / '_next' / path_info
    
    if not file_path.exists() or not file_path.is_file():
        # Fall back to public/_next path
        file_path = Path(__file__).resolve().parent.parent.parent / 'public' / '_next' / path_info
    
    if file_path.exists() and file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            # Default to octet-stream for unknown types
            content_type = 'application/octet-stream'
        
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        # Cache static files for 1 year (production)
        response['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response
    
    return HttpResponse('Not Found', status=404)


def serve_next_asset(request, filename):
    """
    Serve Next.js assets like favicon, images from the export root.
    
    Args:
        request: The HTTP request
        filename: The name of the asset file
        
    Returns:
        FileResponse or 404 response
    """
    # First check in templates/out
    file_path = NEXT_EXPORT_DIR / filename
    
    if not file_path.exists() or not file_path.is_file():
        # Fall back to public folder
        file_path = Path(__file__).resolve().parent.parent.parent / 'public' / filename
    
    if file_path.exists() and file_path.is_file():
        content_type, _ = mimetypes.guess_type(str(file_path))
        if content_type is None:
            content_type = 'application/octet-stream'
        
        response = FileResponse(open(file_path, 'rb'), content_type=content_type)
        response['Cache-Control'] = 'public, max-age=31536000, immutable'
        return response
    
    return HttpResponse('Not Found', status=404)


class NextJSPageView(TemplateView):
    """
    Generic view to serve Next.js static export pages.
    """
    template_name = None  # Will be set dynamically
    content_type = 'text/html'
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET requests for Next.js pages.
        """
        # Get the path from kwargs
        path = kwargs.get('path', '')
        
        # Determine the template path - only use .html files
        if path == '' or path == '/':
            # Root index
            template_path = 'index.html'
        elif path.endswith('/'):
            # Directory index (e.g., 'about/' -> 'about/index.html')
            template_path = f'{path}index.html'
        else:
            # Direct file - always use .html extension
            template_path = f'{path}.html'
        
        # Check if template exists - only look for .html files
        template_file = NEXT_EXPORT_DIR / template_path
        
        # If not found, try the directory/index.html pattern
        if not template_file.exists() or not str(template_file).endswith('.html'):
            template_file = NEXT_EXPORT_DIR / path / 'index.html'
            
        # If still not found, try the 404 page
        if not template_file.exists() or not str(template_file).endswith('.html'):
            template_404 = NEXT_EXPORT_DIR / '404.html'
            if template_404.exists():
                template_file = template_404
            else:
                raise Http404("Page not found")
        
        # Render the template manually to avoid Django template loader issues
        try:
            with open(template_file, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            return HttpResponse(content, content_type=self.content_type)
        except Exception as e:
            raise Http404(f"Page not found: {e}")
    
    def render_to_response(self, context, **response_kwargs):
        """
        Render the response with proper content type.
        """
        response = super().render_to_response(context, **response_kwargs)
        # Set cache headers for production
        response['Cache-Control'] = 'public, max-age=3600'
        return response


def nextjs_spa_fallback(request):
    """
    SPA fallback view for Next.js client-side routing.
    Serves the index.html for any unmatched routes that might be handled by Next.js client-side.
    """
    # Get the requested path
    path = request.path
    
    # List of known Next.js routes that should return index.html for client-side routing
    # These are routes that exist in the Next.js build but might not have corresponding HTML files
    nextjs_routes = [
        '/home',
        '/about',
        '/blog',
        '/contact',
        '/videos',
        '/donate',
        '/newsletter',
        '/subscribe',
        '/take-action',
        '/learn',
        '/insights',
        '/reports',
        '/tracker',
        '/media-hub',
        '/organization',
        '/partners',
        '/services',
        '/advertisements',
    ]
    
    # Check if this is a known Next.js route
    for route in nextjs_routes:
        if path.startswith(route):
            # Serve the index.html for client-side routing
            index_path = NEXT_EXPORT_DIR / 'index.html'
            if index_path.exists():
                return FileResponse(open(index_path, 'rb'), content_type='text/html')
    
    # Not a known Next.js route, return 404
    raise Http404("Page not found")
