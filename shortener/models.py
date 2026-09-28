from django.db import models
from django.utils.crypto import get_random_string

def generate_short_code():
    return get_random_string(length=6)

class URLMapping(models.Model):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(max_length=15, unique=True, default=generate_short_code)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

class ClickAnalytics(models.Model):
    url_mapping = models.ForeignKey(URLMapping, on_delete=models.CASCADE, related_name='clicks')
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Click for {self.url_mapping.short_code} at {self.clicked_at}"
