from django.db import models
from django.apps import apps

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.CASCADE, related_name='payments')

    def __str__(self):
        return f"Payment of {self.amount} by {self.user.username} for {self.subscription.type} Subscription"
