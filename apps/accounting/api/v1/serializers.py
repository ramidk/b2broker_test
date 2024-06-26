from rest_framework.generics import get_object_or_404
from rest_framework_json_api import serializers

from apps.accounting.models import Wallet, Transaction


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('label', 'balance')
        read_only_fields = ('balance',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('txid', 'amount')
        read_only_fields = ('wallet',)

    def create(self, validated_data):
        wallet = get_object_or_404(
            Wallet, **dict(pk=self.context['view'].kwargs['wallet_pk'])
        )
        transaction = wallet.transact(amount=validated_data['amount'],
                                      txid=validated_data['txid'])
        return transaction
