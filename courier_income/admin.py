from django.contrib import admin

from .models import Courier, Trip, TripPenaltyAward, DailyIncome


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    pass

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    pass

@admin.register(TripPenaltyAward)
class TripPenaltyAwardAdmin(admin.ModelAdmin):
    pass

@admin.register(DailyIncome)
class DailyIncomeAdmin(admin.ModelAdmin):
    pass

