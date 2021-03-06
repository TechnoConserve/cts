from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from accounts import views as account_views

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    # Django-Registration
    url(r'^accounts/', include('accounts.urls')),

    # Plant database
    path('plant-database/', include('plant_database.urls')),

    # User stats
    url(r'^~(?P<username>[\w.@+-]+)/$', account_views.user_profile, name='user_profile'),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^members/', include('members.urls')),
    url(r'^fundraising/', include('fundraising.urls')),
    url(r'', include('home.urls')),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
