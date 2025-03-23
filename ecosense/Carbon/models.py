from django.db import models

class CarbonFootprintRecord(models.Model):
    num_people = models.IntegerField()
    monthly_kwh = models.IntegerField()
    num_ac = models.IntegerField()
    ac_hours = models.IntegerField()
    num_fridge = models.IntegerField()
    num_fans = models.IntegerField()
    fan_hours = models.IntegerField()
    num_tv = models.IntegerField()
    tv_hours = models.IntegerField()
    daily_car_km = models.IntegerField()
    daily_bus_km = models.IntegerField()
    daily_bike_km = models.IntegerField()
    diet_type = models.CharField(max_length=10)
    waste_type = models.CharField(max_length=10)
    total_footprint = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carbon Footprint Record - {self.created_at}"

