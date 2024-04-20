from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Courier(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name


class Trip(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        if self.income < 0:
            raise ValidationError("Income cannot be negative")
        super().save(*args, **kwargs)
        self.update_daily_income()

    def update_daily_income(self):
        daily_income, created = DailyIncome.objects.get_or_create(
            courier=self.courier,
            date=self.date,
            defaults={'total_income': 0}
        )
        total_income = Trip.objects.filter(courier=self.courier, date=self.date).aggregate(models.Sum('income'))['income__sum'] or 0
        total_award = TripPenaltyAward.objects.filter(trip__courier=self.courier, trip__date=self.date, type='AWARD').aggregate(models.Sum('amount'))['amount__sum'] or 0
        total_penalty = TripPenaltyAward.objects.filter(trip__courier=self.courier, trip__date=self.date, type='PENALTY').aggregate(models.Sum('amount'))['amount__sum'] or 0
        daily_income.total_income = total_income + total_award - total_penalty
        daily_income.save()

    def __str__(self):
        return f"Trip for {self.courier.name} - Income: {self.income}"


class TripPenaltyAward(models.Model):
    TRIP_CHOICES = (
        ('PENALTY', 'Penalty'),
        ('AWARD', 'Award'),
    )

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRIP_CHOICES)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.trip.update_daily_income()

    def __str__(self):
        return f"{self.get_type_display()} for trip {self.trip.id}: {self.amount}"
    

class DailyIncome(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    total_income = models.DecimalField(max_digits=10, decimal_places=2)

    class meta:
        unique_together = ('courier', 'date')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_weekly_income()

    def update_weekly_income(self):
        # Adjusted calculation for Saturday as the first day of the week
        week_start_date = self.date - timedelta(days=(self.date.weekday() + 2) % 7)
        weekly_income, created = WeeklyIncome.objects.get_or_create(
            courier=self.courier,
            week_start_date=week_start_date,
            defaults={'total_income': 0}
        )
        total_income = DailyIncome.objects.filter(courier=self.courier, date__gte=week_start_date, date__lt=week_start_date + timedelta(days=7)).aggregate(models.Sum('total_income'))['total_income__sum'] or 0
        weekly_income.total_income = total_income
        weekly_income.save()

    def __str__(self):
        return f"Daily Income for {self.courier.name} on {self.date}: {self.total_income}"


class WeeklyIncome(models.Model):
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    week_start_date = models.DateField()
    total_income = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('courier', 'week_start_date')

    def __str__(self):
        return f"Weekly Income for {self.courier.name} starting {self.week_start_date}: {self.total_income}"
