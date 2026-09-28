from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import URLMapping, ClickAnalytics
import time

@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class URLShortenerTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = reverse('create-url')
        
    def test_create_short_url(self):
        data = {'original_url': 'https://www.google.com'}
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('short_code' in response.data)
        self.assertEqual(URLMapping.objects.count(), 1)
        
    def test_redirect_and_analytics(self):
        mapping = URLMapping.objects.create(original_url='https://www.example.com')
        redirect_url = reverse('redirect', kwargs={'short_code': mapping.short_code})
        
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, 'https://www.example.com')
        
        # Check analytics
        mapping.refresh_from_db()
        self.assertEqual(mapping.click_count, 1)
        self.assertEqual(ClickAnalytics.objects.count(), 1)
        
        # Check cache hit (by making another request)
        response = self.client.get(redirect_url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        mapping.refresh_from_db()
        self.assertEqual(mapping.click_count, 2)
        
    def test_analytics_endpoint(self):
        mapping = URLMapping.objects.create(original_url='https://www.example.com')
        redirect_url = reverse('redirect', kwargs={'short_code': mapping.short_code})
        self.client.get(redirect_url)
        
        analytics_url = reverse('url-analytics', kwargs={'short_code': mapping.short_code})
        response = self.client.get(analytics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['click_count'], 1)
        self.assertEqual(len(response.data['recent_clicks']), 1)
