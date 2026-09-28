from django.urls import path
from .views import CreateShortURLView, RedirectView, AnalyticsView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/urls/', CreateShortURLView.as_view(), name='create-url'),
    path('api/analytics/<str:short_code>/', AnalyticsView.as_view(), name='url-analytics'),
    path('<str:short_code>/', RedirectView.as_view(), name='redirect'),
]
