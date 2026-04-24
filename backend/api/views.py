# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Trip, TripDay, FuelStop
# from .serializers import TripSerializer, TripPlanRequestSerializer
# from .services.routing import get_route_distance, geocode_address, get_full_route
# from .services.hos_engine import calculate_trip_plan

# @api_view(['POST'])
# def plan_trip(request):
#     """Main endpoint: Plan a trip and generate HOS-compliant logs"""
#     serializer = TripPlanRequestSerializer(data=request.data)
    
#     if not serializer.is_valid():
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     data = serializer.validated_data
#     current = data['current_location']
#     pickup = data['pickup_location']
#     dropoff = data['dropoff_location']
#     cycle_used = data['cycle_used']
    
#     # Calculate total distance
#     total_miles, route_geometry = get_full_route(current, pickup, dropoff)
    
#     if total_miles == 0:
#         return Response({'error': 'Could not calculate route distance'}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Calculate HOS plan
#     try:
#         days = calculate_trip_plan(current, pickup, dropoff, cycle_used, total_miles)
#     except ValueError as e:
#         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
#     # Save trip to database
#     trip = Trip.objects.create(
#         current_location=current,
#         pickup_location=pickup,
#         dropoff_location=dropoff,
#         cycle_used_start=cycle_used,
#         total_miles=total_miles,
#         total_driving_hours=sum(d['driving_hours'] for d in days),
#         total_on_duty_hours=sum(d['driving_hours'] + d['on_duty_not_driving_hours'] for d in days),
#         cycle_used_end=cycle_used + sum(d['driving_hours'] + d['on_duty_not_driving_hours'] for d in days),
#         cycle_remaining=70 - (cycle_used + sum(d['driving_hours'] + d['on_duty_not_driving_hours'] for d in days))
#     )
    
#     # Save trip days
#     for day in days:
#         TripDay.objects.create(
#             trip=trip,
#             day_number=day['day_number'],
#             date=day['date'].date(),
#             driving_hours=day['driving_hours'],
#             on_duty_not_driving_hours=day['on_duty_not_driving_hours'],
#             off_duty_hours=day['off_duty_hours'],
#             sleeper_hours=day['sleeper_hours'],
#             total_miles=day['total_miles'],
#             start_location=current if day['day_number'] == 1 else '',
#             end_location=dropoff if day['day_number'] == len(days) else '',
#             log_entries=day['log_entries']
#         )
    
#     # Prepare response
#     response_data = {
#         'trip_id': trip.id,
#         'total_miles': total_miles,
#         'total_driving_hours': trip.total_driving_hours,
#         'total_on_duty_hours': trip.total_on_duty_hours,
#         'total_days': len(days),
#         'fuel_stops': [],  # Add fuel stop logic later
#         'days': [{
#             'day_number': d['day_number'],
#             'date': d['date'].isoformat(),
#             'driving_hours': d['driving_hours'],
#             'on_duty_hours': d['on_duty_not_driving_hours'],
#             'log_entries': d['log_entries'],
#             'total_miles': d['total_miles']
#         } for d in days],
#         'cycle_tracking': {
#             'started_with': cycle_used,
#             'trip_added': round(trip.total_on_duty_hours, 1),
#             'remaining': round(trip.cycle_remaining, 1),
#             'after_trip': round(trip.cycle_used_start + trip.total_on_duty_hours, 1)
#         },
#         'route_geometry': route_geometry
#     }
    
#     return Response(response_data, status=status.HTTP_201_CREATED)

# @api_view(['GET'])
# def get_trip(request, trip_id):
#     """Retrieve a saved trip by ID"""
#     try:
#         trip = Trip.objects.get(id=trip_id)
#     except Trip.DoesNotExist:
#         return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)
    
#     serializer = TripSerializer(trip)
#     return Response(serializer.data)

# @api_view(['GET'])
# def list_trips(request):
#     """List all trips for history"""
#     trips = Trip.objects.all().order_by('-created_at')
#     serializer = TripSerializer(trips, many=True)
#     return Response(serializer.data)



# @api_view(['GET'])
# def test(request):
#     return Response({'message': 'Backend is working!', 'status': 'ok'})



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def test(request):
    """Test endpoint to verify API is working"""
    return Response({
        'message': 'Backend is working!',
        'status': 'ok',
        'debug': True
    })

@api_view(['POST'])
def plan_trip(request):
    """Plan a trip and generate HOS-compliant logs"""
    # For now, return a mock response
    return Response({
        'trip_id': 1,
        'total_miles': 720,
        'total_driving_hours': 13.1,
        'total_on_duty_hours': 15.1,
        'total_days': 2,
        'fuel_stops': [],
        'days': [
            {
                'day_number': 1,
                'date': '2026-04-23',
                'driving_hours': 11.0,
                'on_duty_hours': 13.0,
                'total_miles': 550,
                'log_entries': [
                    {'start': '00:00', 'end': '06:00', 'status': 'off_duty'},
                    {'start': '06:00', 'end': '11:00', 'status': 'driving'},
                    {'start': '11:00', 'end': '11:30', 'status': 'on_duty'},
                    {'start': '11:30', 'end': '12:00', 'status': 'driving'},
                    {'start': '12:00', 'end': '12:30', 'status': 'off_duty'},
                    {'start': '12:30', 'end': '16:00', 'status': 'driving'},
                    {'start': '16:00', 'end': '17:00', 'status': 'on_duty'},
                    {'start': '17:00', 'end': '18:00', 'status': 'driving'},
                    {'start': '18:00', 'end': '24:00', 'status': 'sleeper_berth'},
                ]
            },
            {
                'day_number': 2,
                'date': '2026-04-24',
                'driving_hours': 2.1,
                'on_duty_hours': 3.1,
                'total_miles': 170,
                'log_entries': [
                    {'start': '00:00', 'end': '06:00', 'status': 'sleeper_berth'},
                    {'start': '06:00', 'end': '08:06', 'status': 'driving'},
                    {'start': '08:06', 'end': '09:06', 'status': 'on_duty'},
                    {'start': '09:06', 'end': '24:00', 'status': 'off_duty'},
                ]
            }
        ],
        'cycle_tracking': {
            'started_with': 35,
            'trip_added': 15.1,
            'remaining': 19.9,
            'after_trip': 50.1
        },
        'route_geometry': [
            [-87.6298, 41.8781],
            [-86.1581, 39.7684],
            [-84.3880, 33.7490],
        ]
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def list_trips(request):
    """List all saved trips"""
    return Response({'trips': [], 'message': 'No trips saved yet'})

@api_view(['GET'])
def get_trip(request, trip_id):
    """Get a specific trip"""
    return Response({'message': f'Trip {trip_id} not found'}, status=status.HTTP_404_NOT_FOUND)