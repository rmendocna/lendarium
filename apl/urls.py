"""apl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, re_path, include

from content.views import index

urlpatterns = i18n_patterns(
    # re_path(r'^select2/', include('django_select2.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^$', index, name="index"),
    re_path('^apl/', include('legends.urls')),
    re_path(r'^rosetta/', include('rosetta.urls')),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
    path('aplng/', include('legends.langurls')),
    path('places/', include('portugal.urls')),
    path('biblio/', include('biblio.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns