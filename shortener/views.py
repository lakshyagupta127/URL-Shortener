from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.cache import cache
from django.db.models import F
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .models import URLMapping, ClickAnalytics
from .serializers import URLMappingSerializer, ClickAnalyticsSerializer

class IndexView(TemplateView):
    template_name = 'shortener/index.html'

class CreateShortURLView(generics.CreateAPIView):
    serializer_class = URLMappingSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

import threading

class RedirectView(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, short_code, *args, **kwargs):
        cache_key = f"url_{short_code}"
        cached_data = cache.get(cache_key)

        if not cached_data:
            url_mapping = get_object_or_404(URLMapping, short_code=short_code)
            original_url = url_mapping.original_url
            mapping_id = url_mapping.id
            cache.set(cache_key, (original_url, mapping_id), timeout=60*60*24)
        else:
            original_url, mapping_id = cached_data
        
        ip_address = request.META.get('REMOTE_ADDR')
        
        def record_analytics(m_id, ip):
            URLMapping.objects.filter(id=m_id).update(click_count=F('click_count') + 1)
            ClickAnalytics.objects.create(url_mapping_id=m_id, ip_address=ip)
            
        threading.Thread(target=record_analytics, args=(mapping_id, ip_address)).start()
        
        return HttpResponseRedirect(redirect_to=original_url)

class AnalyticsView(generics.RetrieveAPIView):
    queryset = URLMapping.objects.all()
    serializer_class = URLMappingSerializer
    lookup_field = 'short_code'
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        clicks = instance.clicks.order_by('-clicked_at')[:10]
        clicks_serializer = ClickAnalyticsSerializer(clicks, many=True)
        
        data = serializer.data
        data['recent_clicks'] = clicks_serializer.data
        return Response(data)
