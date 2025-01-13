from django.db import models
from payment.cc import sweep_wallet
from payment.models import Intent
from payment.tasks import check_intent_update_order_email_user

# Create your models here.
class Extract(models.Model):

    target_address = models.TextField()
    was_executed_before = models.BooleanField(default=False)
    source_address_count =  models.IntegerField(default=0)
    transaction = models.CharField(blank=True, max_length=84)

    BTC_amount = models.DecimalField(default=0.0, max_digits=8, decimal_places=5)
    executed_on = models.DateTimeField(auto_now_add=True)

    # row-level level operation 
    def extract(self):

        # perform db updates and email updates for paid orders 
        intents = Intent.objects.filter(paid=False, expired=False)
        for intent in intents:
            check_intent_update_order_email_user(intent.order_key)

        # start extraction 
        BTC_amount, no_keys, tx_str = sweep_wallet(self.target_address)
        self.src_address_count = no_keys
        self.BTC_amount = BTC_amount
        if len(tx_str) == 0: 
            # no transactions override blank string  
            tx_str = "NotAvailable"

        self.transaction = tx_str

    def __str__(self) -> str:
        return f'{self.executed_on: %B %d, %Y %H:%M:%S}'
    
    def save(self, **kwargs):
        self.was_executed_before = True
        self.extract()
        super().save(**kwargs)
  

    