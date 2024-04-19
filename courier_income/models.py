from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


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

    def __str__(self):
        return f"Trip for {self.courier.name} - Income: {self.income}"