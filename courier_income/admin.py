from django.contrib import admin

from .models import Courier, Trip, TripPenaltyAward, DailyIncome, WeeklyIncome


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    pass

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('courier', 'income', 'date')
    list_filter = ('courier', 'date')
    search_fields = ('courier', 'date')

@admin.register(TripPenaltyAward)
class TripPenaltyAwardAdmin(admin.ModelAdmin):
    list_display = ('trip', 'amount', 'type')
    list_filter = ('trip', 'type')

@admin.register(DailyIncome)
class DailyIncomeAdmin(admin.ModelAdmin):
    list_display = ('courier', 'date', 'total_income')
    list_filter = ('courier', 'date')

@admin.register(WeeklyIncome)
class WeeklyIncomeAdmin(admin.ModelAdmin):
    list_display = ('courier', 'week_start_date', 'total_income')
    list_filter = ('courier', 'week_start_date')