from rest_framework import serializers
from .models import WeeklyIncome

class WeeklyIncomeSerializer(serializers.ModelSerializer):
    courier = serializers.StringRelatedField()

    class Meta:
        model = WeeklyIncome
        fields = ['courier', 'week_start_date', 'total_income']
