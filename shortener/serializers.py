from rest_framework import serializers
from .models import URLMapping, ClickAnalytics

class URLMappingSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = URLMapping
        fields = ['original_url', 'short_code', 'short_url', 'created_at', 'click_count']
        read_only_fields = ['short_code', 'created_at', 'click_count', 'short_url']

    def get_short_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f'/{obj.short_code}')
        return f'/{obj.short_code}'

class ClickAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClickAnalytics
        fields = ['clicked_at', 'ip_address']
