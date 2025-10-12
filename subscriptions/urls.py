from django.urls import path
from .views import SubscriptionView, SubscriptionRenewView, SubscriptionHistoryView

urlpatterns = [
    path('', SubscriptionView.as_view(), name='subscription'),
    path('renew/', SubscriptionRenewView.as_view(), name='subscription-renew'),
    path('history/', SubscriptionHistoryView.as_view(), name='subscription-history'),
]