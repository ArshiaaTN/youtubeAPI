from rest_framework import serializers
from .models import History
from payments.models import Payment


class WatchHistorySerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source='video.title', read_only=True)
    video_id = serializers.IntegerField(source='video.id', read_only=True)

    class Meta:
        model = History
        fields = ['id', 'video_id', 'video_title', 'watch_date', 'duration']
        read_only_fields = ['id', 'watch_date']


class PaymentHistorySerializer(serializers.ModelSerializer):
    subscription_type = serializers.CharField(source='subscription.type', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'subscription_type']
        read_only_fields = ['id', 'payment_date']