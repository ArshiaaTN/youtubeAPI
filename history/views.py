from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import History
from .serializers import WatchHistorySerializer, PaymentHistorySerializer
from payments.models import Payment


class WatchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = History.objects.filter(user=request.user).order_by('-watch_date')
        serializer = WatchHistorySerializer(history, many=True)

        return Response({
            "total_watches": history.count(),
            "watch_history": serializer.data
        }, status=status.HTTP_200_OK)


class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-payment_date')
        serializer = PaymentHistorySerializer(payments, many=True)

        total_amount = sum(payment.amount for payment in payments)

        return Response({
            "total_payments": payments.count(),
            "total_amount": str(total_amount),
            "payment_history": serializer.data
        }, status=status.HTTP_200_OK)


class CombinedHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        watch_history = History.objects.filter(user=request.user).order_by('-watch_date')
        watch_serializer = WatchHistorySerializer(watch_history, many=True)
        payment_history = Payment.objects.filter(user=request.user).order_by('-payment_date')
        payment_serializer = PaymentHistorySerializer(payment_history, many=True)

        total_amount = sum(payment.amount for payment in payment_history)

        return Response({
            "watch_history": {
                "total_watches": watch_history.count(),
                "history": watch_serializer.data
            },
            "payment_history": {
                "total_payments": payment_history.count(),
                "total_amount": str(total_amount),
                "history": payment_serializer.data
            }
        }, status=status.HTTP_200_OK)