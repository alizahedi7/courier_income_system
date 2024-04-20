from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import WeeklyIncome
from .serializers import WeeklyIncomeSerializer

class WeeklyIncomeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WeeklyIncome.objects.all()
    serializer_class = WeeklyIncomeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['week_start_date']
