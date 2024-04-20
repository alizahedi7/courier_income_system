from django.test import TestCase
from .models import Courier, Trip, TripPenaltyAward, DailyIncome
from decimal import Decimal
from django.core.exceptions import ValidationError

class CourierModelTest(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(name='Test Courier')

    def test_trip_income_calculation(self):
        trip1 = Trip.objects.create(courier=self.courier, income=Decimal('10.00'))
        trip2 = Trip.objects.create(courier=self.courier, income=Decimal('20.00'))
        TripPenaltyAward.objects.create(trip=trip1, amount=Decimal('5.00'), type='AWARD')
        TripPenaltyAward.objects.create(trip=trip2, amount=Decimal('3.00'), type='PENALTY')

        daily_income = DailyIncome.objects.get(courier=self.courier)
        self.assertEqual(daily_income.total_income, Decimal('32.00'))

    def test_trip_income_validation(self):
        with self.assertRaises(ValidationError):
            Trip.objects.create(courier=self.courier, income=Decimal('-10.00'))