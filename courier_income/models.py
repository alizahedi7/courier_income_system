from django.db import models

class Courier(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    