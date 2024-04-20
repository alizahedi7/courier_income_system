from django.test import TestCase
from .models import Courier, Trip, TripPenaltyAward, DailyIncome, WeeklyIncome
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, date

class CourierModelTest(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(name='Test Courier')

    # Test multiple trips without award and penalty
    def test_multiple_trips_without_award_penalty(self):
        trip1 = Trip.objects.create(courier=self.courier, income=Decimal('10.00'))
        trip2 = Trip.objects.create(courier=self.courier, income=Decimal('20.00'))
        trip3 = Trip.objects.create(courier=self.courier, income=Decimal('30.00'))

        daily_income = DailyIncome.objects.get(courier=self.courier)
        self.assertEqual(daily_income.total_income, Decimal('60.00'))
    
    # Test trip income with award and penalty
    def test_trip_income_with_award_penalty(self):
        trip1 = Trip.objects.create(courier=self.courier, income=Decimal('10.00'))
        trip2 = Trip.objects.create(courier=self.courier, income=Decimal('20.00'))
        TripPenaltyAward.objects.create(trip=trip1, amount=Decimal('5.00'), type='AWARD')
        TripPenaltyAward.objects.create(trip=trip2, amount=Decimal('3.00'), type='PENALTY')

        daily_income = DailyIncome.objects.get(courier=self.courier)
        self.assertEqual(daily_income.total_income, Decimal('32.00'))

    # Test validation for trip income
    def test_trip_income_validation(self):
        with self.assertRaises(ValidationError):
            Trip.objects.create(courier=self.courier, income=Decimal('-10.00'))


class WeeklyIncomeModelTest(TestCase):
    def setUp(self):
        self.courier = Courier.objects.create(name='Test Courier')

    def test_weekly_income_calculation(self):
        # Use a fixed start date
        start_date = date(2024, 1, 1)  # This is a Monday

        for i in range(7):
            # Create trips for each day from Saturday to Friday
            trip_date = start_date + timedelta(days=i+5)  # Add 5 to make the first day a Saturday
            Trip.objects.create(courier=self.courier, income=Decimal('10.00'), date=trip_date)
        
        # Calculate the start date of the current week (Saturday)
        week_start_date = start_date + timedelta(days=5)  # This is the Saturday of the week
        
        weekly_income = WeeklyIncome.objects.get(courier=self.courier, week_start_date=week_start_date)
        self.assertEqual(weekly_income.total_income, Decimal('70.00'))
