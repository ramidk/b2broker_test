from django.urls import path, include
from rest_framework_nested import routers

from apps.accounting.api.v1 import views

wallets_router = routers.SimpleRouter()
wallets_router.register('wallets', views.WalletViewSet, basename='wallet')

wallet_transactions_router = routers.NestedSimpleRouter(
    wallets_router, 'wallets', lookup='wallet'
)
wallet_transactions_router.register(
    'transactions', views.TransactionViewSet, basename='wallet-transaction'
)

urlpatterns = [
    path(r'', include(wallets_router.urls)),
    path(r'', include(wallet_transactions_router.urls)),
]
