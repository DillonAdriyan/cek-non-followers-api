from django.db import models

# Create your models here.

class UserLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"
