from django.db import models
from accounts.models import User


class Subscription(models.Model):
    BASIC = 'Basic'
    PREMIUM = 'Premium'
    VIP = 'VIP'

    SUBSCRIPTION_CHOICES = [
        (BASIC, 'Basic'),
        (PREMIUM, 'Premium'),
        (VIP, 'VIP'),
    ]

    SUBSCRIPTION_PRICES = {
        BASIC: 10,
        PREMIUM: 25,
        VIP: 50,
    }

    type = models.CharField(max_length=50, choices=SUBSCRIPTION_CHOICES, default=BASIC)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscriptions')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type} Subscription for {self.user.username} ({'Active' if self.is_active else 'Inactive'})"

    def get_price(self):
        return self.SUBSCRIPTION_PRICES.get(self.type, 0)

    class Meta:
        ordering = ['-start_date']