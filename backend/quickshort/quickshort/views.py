from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickshort.quickshort.serializers import UserSerializer, GroupSerializer, ShortenedUrlSerializer, ClickSerializer

from quickshort.quickshort.models import ShortenedUrl, Click
import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UrlViewSet(viewsets.ModelViewSet):
    queryset = ShortenedUrl.objects.all()
    serializer_class = ShortenedUrlSerializer


class ClickViewSet(viewsets.ModelViewSet):
    queryset = Click.objects.all()
    serializer_class = ClickSerializer


# class UrlRedirectSet(viewsets.ModelViewSet):
#     queryset = ShortenedUrl.objects.all()
#     serializer_class = ShortenedUrlSerializer



import logging

logger = logging.getLogger(__name__)


# log = logging.getLogger(__name__)

class UrlRedirectView(View):

    def get(self, request, *args, **kwargs):
        short_code = kwargs['slug']

        try:
            entry = ShortenedUrl.objects.get(shortened_url=short_code)
        except ShortenedUrl.DoesNotExist:
            return HttpResponse("does not exist")

        original_url = entry.original_url

        c = Click(url=entry)
        c.save()

        logger.info(f"Redirecting short={request.get_full_path()} to {original_url} c={c.url}")
        return HttpResponseRedirect(original_url)


