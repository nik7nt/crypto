from django.urls import include, path

from webhooks.views import TradingView

urlpatterns = [
    path('trading/', TradingView.as_view(), name='main-view'),
]