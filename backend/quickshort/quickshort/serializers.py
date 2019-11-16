from django.contrib.auth.models import User, Group
from rest_framework import serializers

from quickshort.quickshort.models import ShortenedUrl, Click

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ShortenedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedUrl
        fields = [ 'timestamp', 'original_url', 'shortened_url']

class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = [ 'id', 'timestamp', 'url']