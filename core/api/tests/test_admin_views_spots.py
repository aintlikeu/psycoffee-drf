import json
import pytest
import datetime
import random

from rest_framework import status

from api.models import Spot
from api.tests.factories import SpotFactory
from api.services.date_handlers import date_to_unix
from api.serializers.spots import DURATION_VALUES


@pytest.mark.django_db
class TestSpot:
    endpoint = '/api/spots/'

    @classmethod
    def _get_date_timestamp(self, shift_days: int) -> int:
        # get date in unix timestamp (example: tomorrow -> shift_days=1)
        tomorrow_date = datetime.datetime.now() + datetime.timedelta(days=shift_days)
        return date_to_unix(tomorrow_date)

    @classmethod
    def _get_random_time_string(self) -> str:
        # get random time formatted as string (like "11:00")
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        return f"{hour:02d}:{minute:02d}"

    @classmethod
    def _convert_time_to_string(self, time: datetime.time) -> str:
        # convert time from django TimeField to string
        return time.strftime("%H:%M")

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

    def test_create_existed_spot(self, admin_client, customer, spot):
        data = {
            "customer_id": customer.id,
            "date": spot.date,
            "time": spot.time,
            "duration": spot.duration
        }

        expected_response = {
            "success": False,
            "error": "Такое окно уже существует"
        }

        response = admin_client.post(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == expected_response

    def test_create_existed_spot_another_duration(self, admin_client, customer, spot):
        new_duration = random.choice([d for d in DURATION_VALUES if d != spot.duration])

        data = {
            "customer_id": customer.id,
            "date": spot.date,
            "time": spot.time,
            "duration": new_duration
        }

        expected_response = {
            "success": True,
        }

        response = admin_client.post(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response.status_code == status.HTTP_201_CREATED
        assert response_json == expected_response

    def test_create_invalid_date_format(self, admin_client, customer):
        data = {
            "customer_id": customer.id,
            "date": "12.06.2023",                # error here
            "time": self._get_random_time_string(),
            "duration": random.choice(DURATION_VALUES)
        }

        expected_response = {
            "success": False,
            "date": "Некорректный формат даты"
        }

        response = admin_client.post(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == expected_response

    def test_create_invalid_date_in_the_past(self, admin_client, customer):
        data = {
            "customer_id": customer.id,
            "date": self._get_date_timestamp(shift_days=-1),  # yesterday
            "time": self._get_random_time_string(),
            "duration": random.choice(DURATION_VALUES)
        }

        expected_response = {
            "success": False,
            "date": "Создаваемые окна не могут быть в прошлом"
        }

        response = admin_client.post(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == expected_response

    def test_create_invalid_time_format(self, admin_client, customer):
        data = {
            "customer_id": customer.id,
            "date": self._get_date_timestamp(shift_days=1),
            "time": "25:00",        # error here
            "duration": random.choice(DURATION_VALUES)
        }

        expected_response = {
            "success": False,
            "date": "Некорректное время сессии"
        }

        response = admin_client.post(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == expected_response

    def test_create_invalid_duration(self, admin_client, customer):
        data = {
            "customer_id": customer.id,
            "date": self._get_date_timestamp(shift_days=1),
            "time": self._get_random_time_string(),
            "duration": 900,    # error here
        }

        expected_response = {
            "success": False,
            "duration": "Возможные интервалы сессии - 60, 90 и 120 минут"
        }

        response = admin_client.post(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_json == expected_response

    def test_delete_valid_one_spot(self, admin_client, customer, spot):
        data = {
            "customer_id": customer.id,
            "date": spot.date,
            "time": spot.time
        }

        expected_response = {
            "success": True
        }

        response = admin_client.delete(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response_json == expected_response
        assert len(SpotFactory.objects.all()) == 0
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_valid_all_for_the_day(self, admin_client, customer):
        # size of batch, value > 1 and <= max spots per day
        size = 4
        # date in the future, here is tomorrow
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        spots = SpotFactory.create_batch(size=size,
                                         customer=customer,
                                         date=date)

        before_spots_on_date = Spot.objects.filter(date=date)

        data = {
            "customer_id": customer.id,
            "date": date_to_unix(date)
        }

        expected_response ={
            "success": True
        }

        after_spots_on_date = Spot.objects.filter(date=date)

        response = admin_client.delete(self.endpoint, data=data)
        response_json = json.loads(response.content)

        assert response_json == expected_response
        assert after_spots_on_date == before_spots_on_date - 1
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_invalid(self, admin_client, customer):
        # come up with a few tests here
        ...

