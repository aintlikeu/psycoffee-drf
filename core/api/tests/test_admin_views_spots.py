import json
import pytest
import datetime
import random

from rest_framework import status

from api.tests.factories import SpotFactory
from api.services.date_handlers import date_to_unix
from api.serializers.spots import DURATION_VALUES


@pytest.mark.django_db
class TestSpot:
    endpoint = '/api/spots/'

    @classmethod
    def _get_date_timestamp(self, shift_days: int) -> int:
        # get date in unixtimestamp
        tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=shift_days)
        return date_to_unix(tomorrow_date)

    @classmethod
    def _get_random_time_string(self) -> str:
        # get random time formatted as string
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"

    def test_create_valid_data(self, admin_client, customer):

        data = {
            "customer_id": customer.id,
            "date": self._get_date_timestamp(shift_days=1),
            "time": self._get_random_time_string(),
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

    def test_create_invalid_date_format(self, admin_client, customer):
        ...

    def test_create_invalid_date_in_the_past(self, admin_client, customer):
        ...

    def test_create_invalid_time_format(self, admin_client, customer):
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

