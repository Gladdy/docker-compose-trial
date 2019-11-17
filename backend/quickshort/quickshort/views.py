from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import IntegrityError
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from quickshort.quickshort.serializers import UserSerializer, GroupSerializer, ShortenedUrlSerializer, ClickSerializer

from quickshort.quickshort.models import ShortenedUrl, Click
import logging

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
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



import logging

logger = logging.getLogger(__name__)


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


from django.http import JsonResponse

import random
import string
import json


def random_string(N=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


class CreateShortUrl(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'foo': 'bar'})

    def post(self, request, *args, **kwargs):
        logger.info(f"{request} {args} {kwargs} {request.body}")

        try:
            data = json.loads(request.body)
        except IndexError:
            return HttpResponseBadRequest('Invalid json')

        url = data['url']

        try:
            validate = URLValidator(schemes=('http', 'https', 'ftp', 'ftps', 'rtsp', 'rtmp'))
            validate(url)
        except ValidationError:
            return HttpResponseBadRequest('Not a valid URL')

        for x in range(10):
            stats_key = random_string(6)
            short_value = random_string(6)

            try:
                print(f"saving model {stats_key} {short_value}")
                su = ShortenedUrl(shortened_url = short_value, stats_key=stats_key, original_url=url)
                su.save()
                return JsonResponse({'short_url': short_value, "stats_key": stats_key})
            except IntegrityError as e:
                logging.error(f"Unable to create for {stats_key} {short_value} {e}")

        return HttpResponseBadRequest('Unknown error')
