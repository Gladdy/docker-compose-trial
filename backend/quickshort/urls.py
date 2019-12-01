"""quickshort URL Configuration

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
from django.urls import include, path
from rest_framework import routers
from quickshort.quickshort import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'urls', views.UrlViewSet)
router.register(r'clicks', views.ClickViewSet)


from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import render



from django.conf import settings


debug_patterns = [
    path('', views.IndexView.as_view()),
    path('rest', include(router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
] if settings.DEBUG else []

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = debug_patterns + [
    path('create', csrf_exempt(views.CreateShortUrl.as_view())),
    path('stats/<slug:slug>', views.UrlStatsView.as_view()),
    path('stats/<slug:slug>/ts', views.UrlStatsTVView.as_view()),
    path('<slug:slug>', views.UrlRedirectView.as_view())
]