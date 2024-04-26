import decimal

from django.db import models, transaction
from django.db.models import F


# Create your models here.


class Wallet(models.Model):
    label = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=32, decimal_places=18, default=0)

    class Meta:
        ordering = ('id',)

    @transaction.atomic()
    def transact(self, amount: decimal.Decimal, txid: str) -> None:
        self.balance = F("balance") + amount
        self.save(update_fields=["balance"])
        return Transaction.objects.create(wallet_id=self.pk, txid=txid, amount=amount)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    txid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=32, decimal_places=18)

    class Meta:
        ordering = ('id',)
