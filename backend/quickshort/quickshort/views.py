# Create your views here.
import json
import logging
import random
import string

from bakery.views import BuildableTemplateView
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.db import IntegrityError
from django.db.models.functions import TruncMonth, TruncHour
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework import viewsets

from quickshort.quickshort.models import ShortenedUrl, Click
from quickshort.quickshort.serializers import UserSerializer, GroupSerializer, ShortenedUrlSerializer, ClickSerializer


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


logger = logging.getLogger(__name__)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class UrlRedirectView(View):
    def get(self, request, *args, **kwargs):
        short_code = kwargs['slug']

        try:
            entry = ShortenedUrl.objects.get(shortened_url=short_code)
        except ShortenedUrl.DoesNotExist:
            return HttpResponse("does not exist")

        previous_url = self.request.META.get('HTTP_REFERER')

        original_url = entry.original_url
        source_ip = get_client_ip(request)
        c = Click(url=entry, source_ip=source_ip, referrer_url=previous_url)
        c.save()

        logger.info(
            f"Redirecting short={request.get_full_path()} to {original_url} c={c.url} ip={source_ip} previous_url={previous_url}")
        return HttpResponseRedirect(original_url)


def random_string(N=10):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


class CreateShortUrl(View):
    def post(self, request, *args, **kwargs):
        logger.info(f"{request} {args} {kwargs} {request.body}")

        try:
            data = json.loads(request.body)
        except IndexError:
            return HttpResponseBadRequest('invalid-json')

        url = data['url']

        try:
            validate = URLValidator(schemes=('http', 'https', 'ftp', 'ftps', 'rtsp', 'rtmp'))
            validate(url)
        except ValidationError:
            return HttpResponseBadRequest('invalid-url')

        has_code = data.get('code')

        logger.info(f"has_code={has_code} {kwargs}")

        for short_value in [has_code] if has_code else (random_string(6) for x in range(10)):
            stats_key = random_string(6)

            try:
                print(f"saving model {stats_key} {short_value}")
                su = ShortenedUrl(shortened_url=short_value, stats_key=stats_key, original_url=url)
                su.save()
                return JsonResponse({'short_url': short_value, "stats_key": stats_key})
            except IntegrityError as e:
                logging.error(f"Unable to create for {stats_key} {short_value} {e}")

        return HttpResponseBadRequest('invalid-code')


# def index(request):
#     # View code here...
#     return render(request, 'quickshort/index.html', {})


class IndexView(BuildableTemplateView):
    build_path = 'index.html'
    template_name = 'quickshort/index.html'


from django.db.models import Count

def get_click_set(request, kwargs):
    #logger.info(f"{request} {kwargs} {request.body}")
    stats_key = kwargs['slug']
    url = ShortenedUrl.objects.get(stats_key=stats_key)
    return url, url.click_set

class UrlStatsView(View):
    def get(self, request, *args, **kwargs):

        try:
            url, clicks = get_click_set(request, kwargs)
        except ShortenedUrl.DoesNotExist:
            return HttpResponse("does not exist")

        max_values = 25

        # grouped =

        def get_grouping(x):
            return clicks.values(x).annotate(count=Count(x)).order_by('-count').filter(count__gt=0)[:max_values]

        return render(request, 'quickshort/stats.html', {
            "long_url":url.original_url,
            "short_url": url.shortened_url,
            "number_of_clicks": clicks.count(),
            "grouped_urls": get_grouping('referrer_url'),
            "grouped_ips": get_grouping('source_ip'),
        })

from django.core import serializers


class UrlStatsTVView(View):
    def get(self, request, *args, **kwargs):
        try:
            url, clicks = get_click_set(request, kwargs)
        except ShortenedUrl.DoesNotExist:
            return HttpResponse("does not exist")

        ts = clicks.annotate(t=TruncHour('timestamp')).values('t').annotate(y=Count('id'))
        # data = serializers.serialize("json", ts)
        data = []
        for x in ts:
            data.append({"t":x["t"].isoformat(), "y":x["y"]})

        logger.info(f"ts={ts} {data}")
        return JsonResponse(data, safe=False)
