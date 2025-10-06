from django.db import models
from accounts.models import User
from payments.models import Payment


class Subscription(models.Model):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    VIP = 'VIP'

    SUBSCRIPTION_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (VIP, 'VIP'),
    ]

    type = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, default=BASIC)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions')

    def __str__(self):
        return f"{self.type} Subscription for {self.user.username}"
