from rest_framework.filters import SearchFilter
from rest_framework_json_api import filters, django_filters
from rest_framework_json_api.views import ModelViewSet

from apps.accounting.api.v1.serializers import WalletSerializer, TransactionSerializer
from apps.accounting.models import Wallet, Transaction


class WalletViewSet(ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    filter_backends = (
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend, SearchFilter
    )

    filterset_fields = {
        'label': ('exact', 'iexact', 'contains', 'icontains'),
        'balance': ('exact', 'lt', 'gt', 'gte', 'lte'),
    }
    search_fields = ('id', 'label', 'balance')


class TransactionViewSet(ModelViewSet):
    http_method_names = ["get", "post", "head", "options"]
    serializer_class = TransactionSerializer

    filter_backends = (
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend, SearchFilter
    )

    filterset_fields = {
        'txid': ('exact',),
        'amount': ('exact', 'lt', 'gt', 'gte', 'lte'),
    }
    search_fields = ('id', 'label', 'balance')

    def get_queryset(self):
        return Transaction.objects.filter(wallet=self.kwargs['wallet_pk'])
