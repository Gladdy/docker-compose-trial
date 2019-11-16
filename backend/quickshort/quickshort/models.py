from django.db import models


# Create your models here.
class ShortenedUrl(models.Model):
    indexes = [
        models.Index(fields=['shortened_url']),
        models.Index(fields=['stats_key']),
    ]

    timestamp = models.DateTimeField(auto_now_add=True, null=False)
    shortened_url = models.TextField(max_length=10, primary_key=True, null=False)
    stats_key = models.TextField(max_length=10, unique=True, null=False)
    original_url = models.URLField(null=False)

class Click(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.ForeignKey(ShortenedUrl, on_delete=models.CASCADE, null=False)