from rest_framework import serializers
from .models import Trip, TripDay, FuelStop

class TripDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = TripDay
        fields = '__all__'

class FuelStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelStop
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    days = TripDaySerializer(many=True, read_only=True)
    fuel_stops = FuelStopSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = '__all__'

class TripPlanRequestSerializer(serializers.Serializer):
    current_location = serializers.CharField(max_length=200)
    pickup_location = serializers.CharField(max_length=200)
    dropoff_location = serializers.CharField(max_length=200)
    cycle_used = serializers.FloatField()

class TripPlanResponseSerializer(serializers.Serializer):
    trip_id = serializers.IntegerField()
    total_miles = serializers.FloatField()
    total_driving_hours = serializers.FloatField()
    total_on_duty_hours = serializers.FloatField()
    total_days = serializers.IntegerField()
    fuel_stops = FuelStopSerializer(many=True)
    days = TripDaySerializer(many=True)
    cycle_tracking = serializers.DictField()
    route_geometry = serializers.ListField(child=serializers.ListField(), required=False)