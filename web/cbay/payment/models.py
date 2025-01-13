from django.db import models
from orders.models import Order


class Intent(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="intent_user"
    )
    order_key = models.CharField(default="", max_length=200)

    email = models.CharField(max_length=100, default="")
    payment_address = models.CharField(max_length=100, default="")

    paid_amount = models.DecimalField(max_digits=8, decimal_places=5)
    total_amount = models.DecimalField(max_digits=8, decimal_places=5)

    paid = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    # def payment_confirmation_email(self, subject, message):
    #     send_mail(
    #         subject,
    #         message,
    #         settings.EMAIL_HOST_USER,
    #         [self.email],
    #         fail_silently=False,
    #     )

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Intents"
        verbose_name_plural = "Intents"
