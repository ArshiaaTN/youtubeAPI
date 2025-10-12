from django.urls import path
from .views import WatchHistoryView, PaymentHistoryView, CombinedHistoryView

urlpatterns = [
    path('watch/', WatchHistoryView.as_view(), name='watch-history'),
    path('payment/', PaymentHistoryView.as_view(), name='payment-history'),
    path('all/', CombinedHistoryView.as_view(), name='combined-history'),
]