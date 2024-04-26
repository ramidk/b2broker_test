from decimal import Decimal

import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from apps.accounting.models import Wallet

pytestmark = pytest.mark.django_db


class TestWallet:
    WALLET_LABEL = 'wallet_label'
    WALLET_BALANCE = "0.000000000000000000"

    TRANSACTION_1_TXID = "111"
    TRANSACTION_1_AMOUNT = "10.000000000000000000"

    TRANSACTION_2_TXID = "222"
    TRANSACTION_2_AMOUNT = "20.000000000000000000"

    def test_wallet_ok(self, api_client: APIClient):
        # test empty list
        result = api_client.get(reverse("accounting:wallet-list"))

        assert result.status_code == 200
        assert len(result.json()['data']) == 0

        # test create wallet
        payload = {
            "data": {
                "type": "Wallet",
                "attributes": {
                    "label": self.WALLET_LABEL
                }
            }
        }
        result = api_client.post(reverse("accounting:wallet-list"), data=payload)

        assert result.status_code == 201
        data = result.json()['data']
        assert data['attributes']['label'] == self.WALLET_LABEL
        assert data['attributes']['balance'] == self.WALLET_BALANCE

        # test get by id
        result = api_client.get(reverse("accounting:wallet-detail", kwargs={"pk": data['id']}))
        data = result.json()['data']
        assert data['attributes']['label'] == self.WALLET_LABEL
        assert data['attributes']['balance'] == self.WALLET_BALANCE

        # test non-empty wallet list
        result = api_client.get(reverse("accounting:wallet-list"))

        assert result.status_code == 200
        assert len(result.json()['data']) == 1

    @pytest.fixture
    def wallet(self):
        return Wallet.objects.create(label=self.WALLET_LABEL)

    def test_transactions_ok(self, wallet: Wallet, api_client: APIClient):
        result = api_client.get(
            reverse("accounting:wallet-transaction-list", kwargs={"wallet_pk": wallet.pk}))

        assert result.status_code == 200
        assert len(result.json()['data']) == 0

        payload = {
            "data": {
                "type": "Transaction",
                "attributes": {
                    "txid": self.TRANSACTION_1_TXID,
                    "amount": self.TRANSACTION_1_AMOUNT,
                }
            }
        }
        result = api_client.post(
            reverse("accounting:wallet-transaction-list", kwargs={"wallet_pk": wallet.pk}),
            data=payload)

        assert result.status_code == 201
        data = result.json()['data']
        assert data['attributes']['txid'] == self.TRANSACTION_1_TXID
        assert data['attributes']['amount'] == self.TRANSACTION_1_AMOUNT

        result = api_client.get(reverse("accounting:wallet-transaction-detail",
                                        kwargs={"wallet_pk": wallet.pk, "pk": data['id']}))
        data = result.json()['data']
        assert data['attributes']['txid'] == self.TRANSACTION_1_TXID
        assert data['attributes']['amount'] == self.TRANSACTION_1_AMOUNT

        result = api_client.get(
            reverse("accounting:wallet-transaction-list", kwargs={"wallet_pk": wallet.pk}))

        assert result.status_code == 200
        assert len(result.json()['data']) == 1

        wallet.refresh_from_db()
        assert wallet.balance == 10

        # create second transaction and verify wallet balance

        payload = {
            "data": {
                "type": "Transaction",
                "attributes": {
                    "txid": self.TRANSACTION_2_TXID,
                    "amount": self.TRANSACTION_2_AMOUNT,
                }
            }
        }
        api_client.post(
            reverse("accounting:wallet-transaction-list", kwargs={"wallet_pk": wallet.pk}),
            data=payload)

        wallet.refresh_from_db()
        assert wallet.balance == 30

        result = api_client.get(reverse("accounting:wallet-detail", kwargs={"pk": data['id']}))
        data = result.json()['data']
        assert Decimal(data['attributes']['balance']) == wallet.balance

    def test_transactions_wrong_wallet_id(self, api_client: APIClient):
        payload = {
            "data": {
                "type": "Transaction",
                "attributes": {
                    "txid": self.TRANSACTION_1_TXID,
                    "amount": self.TRANSACTION_1_AMOUNT,
                }
            }
        }
        result = api_client.post(
            reverse("accounting:wallet-transaction-list", kwargs={"wallet_pk": 999}),
            data=payload)

        assert result.status_code == 404
