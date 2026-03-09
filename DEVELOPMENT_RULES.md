# Django App Development Rules

## Overview
This document outlines the development rules and best practices for the Budget Ndio Story Django application.

## Development Environment Setup

### Virtual Environment
```bash
# Activate virtual environment
cd /home/gunzo/Downloads/django
source .venv/bin/activate  # or: . .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Development Server
```bash
# Standard run
python manage.py runserver

# With specific port
python manage.py runserver 8000

# Production-like testing
python manage.py runserver 0.0.0.0:8000
```

## Code Quality Checks

### Before Committing
Always run these checks:
```bash
# Check for Django errors
python manage.py check

# Verify URL configuration
python manage.py show_urls  # if django-extensions installed

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

## URL Configuration Rules

### URL Pattern Order (Critical)
URL patterns must be ordered from most specific to least specific:

1. **Admin URLs** - `admin/` (first)
2. **Core App URLs** - `apps.core.urls` (serves pages)
3. **Next.js Static Files** - `_next/`
4. **Next.js Pages** - `apps.nextjs.urls`
5. **Static Assets** - favicon, images, videos
6. **API Dashboard** - `/api/docs/`, `/api/`, `/api/browser/`
7. **Specific API Endpoints** - `/api/v1/accounts/`, `/api/v1/content/`, etc.
8. **Catch-all API Proxy** - `/api/v1/<str:app_name>/` (LAST)

### Correct URL Order Example
```python
urlpatterns = [
    # 1. Admin
    path('admin/', admin.site.urls),
    
    # 2. Core app - pages and CRUD
    path('', include('apps.core.urls')),
    
    # 3. Next.js static files
    re_path(r'^_next/(?P<path_info>.*)$', serve_next_static),
    
    # 4. Next.js pages
    path('', include('apps.nextjs.urls')),
    
    # 5. Static assets
    re_path(r'^(?P<filename>favicon\.ico)$', serve_public_file),
    
    # 6. API Dashboard
    path('api/docs/', api_docs),
    path('api/', views_api.APIDashboardView.as_view()),
    
    # 7. Specific API endpoints (MUST come before catch-all)
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/content/', include('apps.content.urls')),
    path('api/v1/newsletter/', include('apps.newsletter.urls')),
    
    # 8. Catch-all (LAST)
    path('api/v1/<str:app_name>/', views_api.APIEndpointProxyView.as_view()),
]
```

## API Endpoints Reference

### Authentication (`/api/auth/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/csrf/` | Get CSRF token |
| POST | `/api/auth/login/` | User login |
| POST | `/api/auth/logout/` | User logout |
| GET | `/api/auth/user/` | Get current user |

### Content API (`/api/v1/content/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/content/posts/` | Blog posts list/create |
| GET/PUT/DELETE | `/api/v1/content/posts/{id}/` | Blog post detail |
| GET/POST | `/api/v1/content/videos/` | Videos list/create |
| GET/PUT/DELETE | `/api/v1/content/videos/{id}/` | Video detail |
| GET/POST | `/api/v1/content/categories/` | Categories list/create |
| GET/POST | `/api/v1/content/news/` | News items list/create |

### Accounts API (`/api/v1/accounts/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/accounts/users/` | Users list/create |
| GET/PUT/DELETE | `/api/v1/accounts/users/{id}/` | User detail |
| GET/POST | `/api/v1/accounts/donors/` | Donors list/create |
| GET/POST | `/api/v1/accounts/sponsors/` | Sponsors list/create |
| GET/POST | `/api/v1/accounts/partners/` | Partners list/create |

### Newsletter API (`/api/v1/newsletter/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/newsletter/subscribers/` | Subscribers list/create |
| GET/POST | `/api/v1/newsletter/campaigns/` | Campaigns list/create |

### Sponsors API (`/api/v1/sponsors/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/v1/sponsors/donations/` | Donations list/create |
| GET/POST | `/api/v1/sponsors/deliverables/` | Deliverables list/create |
| GET/POST | `/api/v1/sponsors/assets/` | Assets list/create |

## Frontend Integration

### Next.js to Django URL Mapping
The Next.js frontend uses JavaScript API client (`static/js/api-client.js`) which points to:

- **Base URL**: `/api/v1`
- **Auth URL**: `/api/auth`

### Next.js Page Routes
| Page | Django Backend |
|------|----------------|
| `/` | Next.js index |
| `/blog/` | Next.js blog page → API: `/api/v1/content/posts/` |
| `/auth/` | Next.js auth page → API: `/api/auth/` |
| `/dashboard/` | Next.js dashboard → Django: `/dashboard/` |
| `/videos/` | Next.js videos → API: `/api/v1/content/videos/` |

## Git Workflow

### Commit Rules
1. Always test locally before committing
2. Run `python manage.py check` - must pass
3. Write meaningful commit messages
4. Commit related changes together

### Deployment Commands
```bash
# Check git status
git status

# Add changes
git add -A

# Commit with message
git commit -m "Description of changes"

# Push to remote
git push origin main
```

### CPanel Deployment (if applicable)
```bash
# Ensure all changes are committed
git push origin main

# On server, pull changes
git pull origin main

# Restart application (via Passenger or supervisor)
```

## Common Issues & Solutions

### URL Conflicts
If API endpoints return 404:
1. Check URL pattern order in `api/urls.py`
2. Ensure specific routes come before catch-all
3. Run `python manage.py check` to verify

### CSRF Token Issues
If CSRF errors occur:
1. Ensure `/api/csrf/` is accessible
2. Frontend must include `X-CSRFToken` header
3. Check cookie is set correctly

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_ROOT in settings.py
```

## File Structure
```
django/
├── api/                    # Django project settings
│   ├── settings.py
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py
├── apps/                  # Django applications
│   ├── accounts/         # User management
│   ├── analytics/        # Analytics
│   ├── cms/              # Content management
│   ├── content/          # Blog, videos, news
│   ├── core/             # Core views and URLs
│   ├── nextjs/           # Next.js integration
│   ├── newsletter/      # Newsletter management
│   └── sponsors/         # Sponsorships
├── public/               # Next.js build output
├── static/               # Static files (CSS, JS)
├── templates/            # Django templates
│   ├── frontend/        # Frontend templates
│   └── admin/           # Admin templates
├── manage.py
└── requirements.txt
```

## Testing Checklist
- [ ] `python manage.py check` passes
- [ ] All URLs resolve correctly
- [ ] API endpoints return expected responses
- [ ] Auth login/logout works
- [ ] Static files load properly
- [ ] No console errors in browser

---
Last Updated: 2026-03-09
