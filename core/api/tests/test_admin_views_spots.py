import json
import pytest
import datetime
import time
import random

from rest_framework import status

from api.tests.factories import SpotFactory
from api.services.date_handlers import date_to_unix
from api.serializers.spots import DURATION_VALUES


@pytest.mark.django_db
class TestSpot:
    endpoint = '/api/spots/'

    def test_create_valid_data(self, admin_client, customer):
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

    def test_create_existed_spot(self, admin_client, customer):
        ...

    def test_create_existed_spot_another_duration(self, admin_client, customer):
        ...

    def test_create_invalid_date(self, admin_client, customer):
        ...

    def test_create_invalid_time(self, admin_client, customer):
        ...

    def test_create_invalid_duration(self, admin_client, customer):
        ...

    def test_delete_valid_one_spot(self, admin_client, customer):
        ...

    def test_delete_valid_all_for_the_day(self, admin_client, customer):
        ...

    def test_delete_invalid(self, admin_client, customer):
        # come up with a few tests here
        ...

