BLOGS-

TemplateDoesNotExist at /blog/

public/blog.html


http://localhost:8000/blogs/ - 404 


ABOUT 
TemplateDoesNotExist at /about/

public/about.html

Inconsistency in UI (ensure we are using one harmonized base.html for /dashboards, these inconsistency is a rookies mistake ) :http://localhost:8000/dashboard/   AND http://localhost:8000/dashboard/posts/create/, http://localhost:8000/dashboard/campaigns/create/, http://localhost:8000/dashboard/donations/create/, http://localhost:8000/dashboard/news/, http://localhost:8000/dashboard/categories/

ImproperlyConfigured at /dashboard/users/

AccountsListView is missing a QuerySet. Define AccountsListView.model, AccountsListView.queryset, or override AccountsListView.get_queryset().

Request Method: 	GET
Request URL: 	http://localhost:8000/dashboard/users/

ImproperlyConfigured at /dashboard/donors/

AccountsListView is missing a QuerySet. Define AccountsListView.model, AccountsListView.queryset, or override AccountsListView.get_queryset().

ReverseMatch at /dashboard/posts/

Reverse for 'blogpost-update' with arguments '(UUID('4c9d3611-22ed-42f7-879e-1858997e7d40'),)' not found. 1 pattern(s) tried: ['dashboard/posts/(?P<pk>[0-9]+)/edit/\\Z']


TemplateSyntaxError at /dashboard/analytics/

Invalid filter: 'multiply'

Request Method: 	