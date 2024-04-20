from rest_framework.routers import DefaultRouter
from .views import WeeklyIncomeViewSet

router = DefaultRouter()
router.register(r'weekly_incomes', WeeklyIncomeViewSet)

urlpatterns = router.urls
