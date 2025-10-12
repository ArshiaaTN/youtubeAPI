from rest_framework import serializers
from .models import Subscription
from payments.models import Payment


class SubscriptionSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['id', 'type', 'start_date', 'end_date', 'user', 'price', 'is_active']
        read_only_fields = ['id', 'user', 'price', 'is_active']

    def get_price(self, obj):
        return obj.get_price()


class SubscriptionPurchaseSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=Subscription.SUBSCRIPTION_CHOICES)

    def create(self, validated_data):
        from datetime import datetime, timedelta

        user = self.context['request'].user
        subscription_type = validated_data['type']

        active_subscription = Subscription.objects.filter(user=user, is_active=True).first()
        if active_subscription:
            raise serializers.ValidationError(
                "You already have an active subscription. Please cancel it first or wait for it to expire.")

        price = Subscription.SUBSCRIPTION_PRICES.get(subscription_type)

        if user.wallet_balance < price:
            raise serializers.ValidationError(
                f"Insufficient balance. Required: {price}, Available: {user.wallet_balance}"
            )
        user.wallet_balance -= price
        user.save()

        subscription = Subscription.objects.create(
            user=user,
            type=subscription_type,
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=30),
            is_active=True
        )

        Payment.objects.create(
            user=user,
            amount=price,
            payment_date=datetime.now().date(),
            subscription=subscription
        )

        return subscription


class SubscriptionRenewSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=Subscription.SUBSCRIPTION_CHOICES)

    def create(self, validated_data):
        from datetime import datetime, timedelta
        from payments.models import Payment

        user = self.context['request'].user
        new_subscription_type = validated_data['type']

        old_subscription = Subscription.objects.filter(user=user, is_active=True).first()

        if not old_subscription:
            raise serializers.ValidationError("You don't have any active subscription to renew")
        price = Subscription.SUBSCRIPTION_PRICES.get(new_subscription_type)

        if user.wallet_balance < price:
            raise serializers.ValidationError(
                f"Insufficient balance. Required: {price}, Available: {user.wallet_balance}"
            )

        user.wallet_balance -= price
        user.save()
        old_subscription.is_active = False
        old_subscription.save()

        new_subscription = Subscription.objects.create(
            user=user,
            type=new_subscription_type,
            start_date=datetime.now().date(),
            end_date=datetime.now().date() + timedelta(days=30),
            is_active=True
        )

        Payment.objects.create(
            user=user,
            amount=price,
            payment_date=datetime.now().date(),
            subscription=new_subscription
        )

        return new_subscription