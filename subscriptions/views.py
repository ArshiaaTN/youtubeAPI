from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Subscription
from .serializers import SubscriptionSerializer, SubscriptionPurchaseSerializer, SubscriptionRenewSerializer


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = Subscription.objects.filter(user=request.user, is_active=True).first()

        if not subscription:
            return Response({"message": "You don't have any active subscription"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubscriptionPurchaseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            subscription = serializer.save()
            return Response({
                "message": "Subscription purchased successfully",
                "subscription": SubscriptionSerializer(subscription).data,
                "remaining_balance": str(request.user.wallet_balance)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        subscription = Subscription.objects.filter(user=request.user, is_active=True).first()

        if not subscription:
            return Response({"error": "You don't have any active subscription to cancel"},
                            status=status.HTTP_404_NOT_FOUND)

        subscription.is_active = False
        subscription.save()

        return Response({
            "message": "Subscription cancelled successfully",
            "cancelled_subscription": SubscriptionSerializer(subscription).data
        }, status=status.HTTP_200_OK)


class SubscriptionRenewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscriptionRenewSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            new_subscription = serializer.save()
            return Response({
                "message": "Subscription renewed successfully. Old subscription deactivated.",
                "new_subscription": SubscriptionSerializer(new_subscription).data,
                "remaining_balance": str(request.user.wallet_balance)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscriptions = Subscription.objects.filter(user=request.user)
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response({
            "total_subscriptions": subscriptions.count(),
            "subscriptions": serializer.data
        }, status=status.HTTP_200_OK)