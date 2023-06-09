import json
import pytest
import datetime
import time
import random

from rest_framework import status

from api.tests.factories import CustomerFactory, SpotFactory
from api.services.date_handlers import date_to_unix
from api.serializers.spots import DURATION_VALUES


@pytest.mark.django_db
class TestSpot:
    endpoint = '/api/spots/'

    def test_create_valid_data(self, admin_client):
        # setup customer
        customer = CustomerFactory.create()
        # get tomorrow date as unix timestamp
        tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow_timestamp = date_to_unix(tomorrow_date)

        data = {
            "customer_id": customer.id,
            "date": tomorrow_timestamp,
            "time": "12:00",
            "duration": random.choice(DURATION_VALUES)
        }

        expected_response = {
            "success": True,
        }

        response = admin_client.post(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert response_json == expected_response

