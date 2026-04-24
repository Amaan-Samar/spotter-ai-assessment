from django.db import models

class Trip(models.Model):
    current_location = models.CharField(max_length=200)
    pickup_location = models.CharField(max_length=200)
    dropoff_location = models.CharField(max_length=200)
    cycle_used_start = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Calculated fields
    total_miles = models.FloatField(null=True, blank=True)
    total_driving_hours = models.FloatField(null=True, blank=True)
    total_on_duty_hours = models.FloatField(null=True, blank=True)
    cycle_used_end = models.FloatField(null=True, blank=True)
    cycle_remaining = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        return f"Trip {self.id}: {self.current_location} → {self.dropoff_location}"

class TripDay(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField()
    date = models.DateField()
    driving_hours = models.FloatField()
    on_duty_hours = models.FloatField()
    total_miles = models.FloatField()
    start_location = models.CharField(max_length=200, blank=True)
    end_location = models.CharField(max_length=200, blank=True)
    log_entries = models.JSONField(default=list)
    
    def __str__(self):
        return f"Trip {self.trip.id} - Day {self.day_number}"