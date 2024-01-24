"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

# from home.plots import dashboard
from django.conf import settings
from django.conf.urls.static import static

admin.sites.AdminSite.site_header = 'My site admin header'
admin.sites.AdminSite.site_title = 'My site admin title'
admin.sites.AdminSite.index_title = 'My site admin index'

urlpatterns = [
    path('', include('home.urls')),
    path("admin/", admin.site.urls),
    path("", include("authentication.urls")), # Auth routes - login / register
#     path('django_plotly_dash/', include('django_plotly_dash.urls')),
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # path("", include('admin_adminlte.urls'))
]
