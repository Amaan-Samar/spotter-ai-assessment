import logging
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def interpolate_position(route_geometry, fraction):
    """Interpolate position along route based on fraction (0-1)"""
    if not route_geometry or len(route_geometry) < 2:
        return [39.8283, -98.5795]  # Center of US
    
    # Simple interpolation between start and end
    start_lat, start_lon = route_geometry[0][0], route_geometry[0][1]
    end_lat, end_lon = route_geometry[-1][0], route_geometry[-1][1]
    
    lat = start_lat + (end_lat - start_lat) * fraction
    lon = start_lon + (end_lon - start_lon) * fraction
    
    return [lat, lon]


def generate_log_entries_for_day(day_num, drive_today, is_first_day, is_last_day, has_fuel_stop):
    """Generate 24-hour log entries for a single day based on HOS rules"""
    entries = []
    
    # Off-duty from midnight to 6am (at least 8-10 consecutive hours)
    entries.append({'start': '00:00', 'end': '06:00', 'status': 'off_duty'})
    
    current_time = 6.0  # Start at 6am
    
    # Add 30-minute pre-trip inspection (on-duty, not driving)
    entries.append({
        'start': format_hour(current_time),
        'end': format_hour(current_time + 0.5),
        'status': 'on_duty'
    })
    current_time += 0.5
    
    # First driving segment (up to 8 hours)
    first_segment = min(8, drive_today)
    if first_segment > 0:
        entries.append({
            'start': format_hour(current_time),
            'end': format_hour(current_time + first_segment),
            'status': 'driving'
        })
        current_time += first_segment
    
    # Add 30-minute rest break if driving more than 8 hours
    if drive_today > 8:
        entries.append({
            'start': format_hour(current_time),
            'end': format_hour(current_time + 0.5),
            'status': 'off_duty'  # Break can be off-duty
        })
        current_time += 0.5
        
        # Second driving segment (remaining hours)
        second_segment = drive_today - 8
        if second_segment > 0:
            entries.append({
                'start': format_hour(current_time),
                'end': format_hour(current_time + second_segment),
                'status': 'driving'
            })
            current_time += second_segment
    
    # Add fuel stop (30 minutes on-duty)
    if has_fuel_stop and drive_today > 0:
        entries.append({
            'start': format_hour(current_time),
            'end': format_hour(current_time + 0.5),
            'status': 'on_duty'
        })
        current_time += 0.5
    
    # Add pickup on first day (1 hour on-duty)
    if is_first_day:
        entries.append({
            'start': format_hour(current_time),
            'end': format_hour(current_time + 1.0),
            'status': 'on_duty'
        })
        current_time += 1.0
    
    # Add dropoff on last day (1 hour on-duty)
    if is_last_day:
        entries.append({
            'start': format_hour(current_time),
            'end': format_hour(current_time + 1.0),
            'status': 'on_duty'
        })
        current_time += 1.0
    
    # Remaining time off-duty or sleeper berth
    if current_time < 24:
        # If driving a lot, use sleeper berth, otherwise off-duty
        remaining_status = 'sleeper_berth' if drive_today > 8 else 'off_duty'
        entries.append({
            'start': format_hour(current_time),
            'end': '24:00',
            'status': remaining_status
        })
    
    return entries


def calculate_on_duty_from_entries(log_entries):
    """Calculate total on-duty hours from log entries"""
    on_duty_statuses = ['driving', 'on_duty']
    total = 0.0
    
    for entry in log_entries:
        if entry['status'] in on_duty_statuses:
            # Calculate hours between start and end
            start_parts = entry['start'].split(':')
            end_parts = entry['end'].split(':')
            
            start_hour = int(start_parts[0]) + int(start_parts[1]) / 60
            end_hour = int(end_parts[0]) + int(end_parts[1]) / 60
            
            if end_hour == 0:
                end_hour = 24
            
            total += (end_hour - start_hour)
    
    return total


def format_hour(hour):
    """Convert decimal hour to HH:MM format (e.g., 6.5 -> '06:30')"""
    h = int(hour)
    m = int((hour - h) * 60)
    return f"{h:02d}:{m:02d}"


def get_date_for_day(day_num):
    """Generate a date string based on day number"""
    base_date = datetime.now().date()
    target_date = base_date + timedelta(days=day_num - 1)
    return target_date.strftime('%Y-%m-%d')


@api_view(['GET'])
def test(request):
    """Test endpoint to verify API is working"""
    logger.info("✅ Test endpoint called")
    return Response({
        'message': 'Backend is working!',
        'status': 'ok',
        'debug': True
    })


@api_view(['POST'])
def plan_trip(request):
    """Plan a trip and generate HOS-compliant logs based on FMCSA 70hr/8day rule"""
    logger.info("=" * 60)
    logger.info("🚚 PLAN TRIP ENDPOINT CALLED")
    logger.info(f"📥 Request data: {request.data}")
    
    try:
        # Extract input data
        current = request.data.get('current_location', '').strip()
        pickup = request.data.get('pickup_location', '').strip()
        dropoff = request.data.get('dropoff_location', '').strip()
        cycle_used = float(request.data.get('cycle_used', 35))
        
        # Validate inputs
        if not current or not pickup or not dropoff:
            return Response({
                'error': 'All location fields are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if cycle_used < 0 or cycle_used > 70:
            return Response({
                'error': 'Cycle used must be between 0 and 70 hours'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        logger.info(f"📍 Current: {current}")
        logger.info(f"📦 Pickup: {pickup}")
        logger.info(f"🏁 Dropoff: {dropoff}")
        logger.info(f"⏱️ Cycle used: {cycle_used} hours")
        
        # ============================================
        # STEP 1: Calculate route distance and geometry
        # ============================================
        logger.info("📡 Calculating route distance...")
        
        # For now, use mock data based on city names
        # In production, you would call OSRM API here
        route_distances = {
            ('Chicago', 'Indianapolis'): 180,
            ('Indianapolis', 'Atlanta'): 540,
            ('Chicago', 'Atlanta'): 720,
            ('New York', 'Chicago'): 790,
            ('Chicago', 'Los Angeles'): 2015,
            ('New York', 'Los Angeles'): 2800,
            ('Seattle', 'Denver'): 1300,
            ('Denver', 'Miami'): 2050,
            ('Chicago', 'Dallas'): 920,
            ('Dallas', 'Los Angeles'): 1450,
        }
        
        # Calculate distances
        dist1 = route_distances.get((current, pickup), 500)
        dist2 = route_distances.get((pickup, dropoff), 500)
        total_miles = dist1 + dist2
        
        # Route geometry (latitude, longitude)
        route_geometry = {
            ('Chicago', 'Indianapolis', 'Atlanta'): [
                [41.8781, -87.6298],  # Chicago
                [39.7684, -86.1581],  # Indianapolis
                [33.7490, -84.3880],  # Atlanta
            ],
            ('New York', 'Chicago', 'Los Angeles'): [
                [40.7128, -74.0060],  # New York
                [41.8781, -87.6298],  # Chicago
                [34.0522, -118.2437],  # Los Angeles
            ],
            ('Seattle', 'Denver', 'Miami'): [
                [47.6062, -122.3321],  # Seattle
                [39.7392, -104.9903],  # Denver
                [25.7617, -80.1918],   # Miami
            ],
            ('Chicago', 'Dallas', 'Los Angeles'): [
                [41.8781, -87.6298],  # Chicago
                [32.7767, -96.7970],  # Dallas
                [34.0522, -118.2437],  # Los Angeles
            ],
        }
        
        # Default route geometry
        geometry_key = (current, pickup, dropoff)
        if geometry_key not in route_geometry:
            geometry_key = ('Chicago', 'Indianapolis', 'Atlanta')
        
        route_geometry_points = route_geometry.get(geometry_key, [
            [41.8781, -87.6298],
            [39.7684, -86.1581],
            [33.7490, -84.3880],
        ])
        
        logger.info(f"📏 Total distance: {total_miles:.1f} miles")
        logger.info(f"🗺️ Route geometry points: {len(route_geometry_points)}")
        
        # ============================================
        # STEP 2: Calculate basic trip metrics
        # ============================================
        AVG_SPEED_MPH = 55
        FUEL_INTERVAL_MILES = 1000
        PICKUP_DROPOFF_HOURS = 1.0
        MAX_DRIVING_PER_DAY = 11.0
        CYCLE_LIMIT = 70.0
        
        # Calculate driving hours
        driving_hours = total_miles / AVG_SPEED_MPH
        logger.info(f"🚗 Total driving hours: {driving_hours:.1f}")
        
        # Calculate fuel stops
        num_fuel_stops = int(total_miles // FUEL_INTERVAL_MILES)
        fuel_stop_hours = num_fuel_stops * 0.5  # 30 minutes per stop
        logger.info(f"⛽ Fuel stops: {num_fuel_stops} (total {fuel_stop_hours:.1f} hours)")
        
        # Calculate total on-duty time
        total_on_duty = driving_hours + PICKUP_DROPOFF_HOURS + fuel_stop_hours
        logger.info(f"💼 Total on-duty hours: {total_on_duty:.1f}")
        
        # Calculate cycle tracking
        after_trip = cycle_used + total_on_duty
        remaining = CYCLE_LIMIT - after_trip
        
        # Check if trip exceeds cycle limit
        if remaining < 0:
            logger.warning(f"⚠️ Trip exceeds cycle limit by {abs(remaining):.1f} hours")
        
        # Calculate number of days needed
        total_days = max(1, int((driving_hours + 0.99) // MAX_DRIVING_PER_DAY))
        logger.info(f"📅 Total days needed: {total_days}")
        
        # ============================================
        # STEP 3: Generate fuel stops with coordinates
        # ============================================
        fuel_stops = []
        for i in range(1, num_fuel_stops + 1):
            fraction = (i * FUEL_INTERVAL_MILES) / total_miles
            lat, lon = interpolate_position(route_geometry_points, fraction)
            
            fuel_stops.append({
                'miles': i * FUEL_INTERVAL_MILES,
                'location': f'Fuel stop at {i * FUEL_INTERVAL_MILES} miles',
                'latitude': lat,
                'longitude': lon,
                'estimated_arrival': f'Day {i}'
            })
        
        # ============================================
        # STEP 4: Generate daily breakdown
        # ============================================
        days = []
        remaining_drive = driving_hours
        miles_per_hour = total_miles / driving_hours if driving_hours > 0 else 55
        
        for day_num in range(1, total_days + 1):
            # Calculate driving for this day
            drive_today = min(MAX_DRIVING_PER_DAY, remaining_drive)
            remaining_drive -= drive_today
            
            # Calculate miles for this day
            miles_today = drive_today * miles_per_hour
            
            # Determine start and end locations for this day
            start_location = current if day_num == 1 else ''
            end_location = dropoff if remaining_drive <= 0 else ''
            
            # Check if this day has a fuel stop
            has_fuel = False
            for stop in fuel_stops:
                stop_day = int(stop.get('estimated_arrival', 'Day 1').split(' ')[1]) if 'Day' in stop.get('estimated_arrival', '') else 0
                if stop_day == day_num:
                    has_fuel = True
                    break
            
            # Generate log entries for this day
            log_entries = generate_log_entries_for_day(
                day_num=day_num,
                drive_today=drive_today,
                is_first_day=(day_num == 1),
                is_last_day=(remaining_drive <= 0),
                has_fuel_stop=has_fuel
            )
            
            # Calculate on-duty hours for this day from log entries
            on_duty_today = calculate_on_duty_from_entries(log_entries)
            
            days.append({
                'day_number': day_num,
                'date': get_date_for_day(day_num),
                'driving_hours': round(drive_today, 1),
                'on_duty_hours': round(on_duty_today, 1),
                'total_miles': round(miles_today, 0),
                'start_location': start_location,
                'end_location': end_location,
                'log_entries': log_entries
            })
        
        # ============================================
        # STEP 5: Save trip to database (if models exist)
        # ============================================
        trip_id = None
        try:
            from .models import Trip, TripDay
            
            trip = Trip.objects.create(
                current_location=current,
                pickup_location=pickup,
                dropoff_location=dropoff,
                cycle_used_start=cycle_used,
                total_miles=round(total_miles, 1),
                total_driving_hours=round(driving_hours, 1),
                total_on_duty_hours=round(total_on_duty, 1),
                cycle_used_end=round(after_trip, 1),
                cycle_remaining=max(0, round(remaining, 1))
            )
            
            # Save each day to database
            for day in days:
                TripDay.objects.create(
                    trip=trip,
                    day_number=day['day_number'],
                    date=day['date'],
                    driving_hours=day['driving_hours'],
                    on_duty_hours=day['on_duty_hours'],
                    total_miles=day['total_miles'],
                    start_location=day.get('start_location', ''),
                    end_location=day.get('end_location', ''),
                    log_entries=day['log_entries']
                )
            
            logger.info(f"💾 Saved trip to database with ID: {trip.id}")
            trip_id = trip.id
            
        except Exception as e:
            logger.warning(f"Database save skipped (models may not exist): {e}")
            trip_id = None
        
        # ============================================
        # STEP 6: Prepare response
        # ============================================
        response_data = {
            'trip_id': trip_id,
            'total_miles': round(total_miles, 1),
            'total_driving_hours': round(driving_hours, 1),
            'total_on_duty_hours': round(total_on_duty, 1),
            'total_days': total_days,
            'fuel_stops': fuel_stops,
            'days': days,
            'cycle_tracking': {
                'started_with': cycle_used,
                'trip_added': round(total_on_duty, 1),
                'remaining': max(0, round(remaining, 1)),
                'after_trip': round(after_trip, 1),
                'is_violation': remaining < 0
            },
            'route_geometry': route_geometry_points
        }
        
        # Add warning if exceeding cycle limit
        if remaining < 0:
            response_data['warning'] = f'⚠️ This trip exceeds the 70-hour cycle limit by {abs(remaining):.1f} hours!'
        
        logger.info(f"✅ Response prepared: {total_days} days, {total_miles:.1f} miles")
        logger.info(f"📊 Cycle: {cycle_used} → {after_trip:.1f} (remaining: {max(0, remaining):.1f})")
        logger.info("=" * 60)
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"❌ Error in plan_trip: {str(e)}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': f'Failed to plan trip: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def list_trips(request):
    """List all saved trips"""
    logger.info("📋 List trips endpoint called")
    try:
        from .models import Trip
        trips = Trip.objects.all().order_by('-created_at')
        history = []
        for trip in trips:
            history.append({
                'id': trip.id,
                'date': trip.created_at.strftime('%Y-%m-%d'),
                'from': trip.current_location,
                'to': trip.dropoff_location,
                'miles': trip.total_miles,
                'days': trip.days.count(),
                'cycle_used': trip.cycle_used_end
            })
        return Response({'trips': history})
    except Exception as e:
        logger.warning(f"Could not fetch trips: {e}")
        return Response({'trips': [], 'message': 'No trips saved yet'})


@api_view(['GET'])
def get_trip(request, trip_id):
    """Get a specific trip"""
    logger.info(f"🔍 Get trip {trip_id} called")
    try:
        from .models import Trip
        from .serializers import TripSerializer
        
        trip = Trip.objects.get(id=trip_id)
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    except Exception as e:
        logger.warning(f"Trip {trip_id} not found: {e}")
        return Response({'error': f'Trip {trip_id} not found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def get_trip_history(request):
    """Get all historical trips for a driver"""
    logger.info("📜 Get trip history called")
    try:
        from .models import Trip
        
        trips = Trip.objects.all().order_by('-created_at')
        
        history = []
        for trip in trips:
            history.append({
                'id': trip.id,
                'date': trip.created_at.strftime('%Y-%m-%d'),
                'from': trip.current_location,
                'to': trip.dropoff_location,
                'miles': trip.total_miles,
                'days': trip.days.count(),
                'cycle_used': trip.cycle_used_end
            })
        
        return Response({'trips': history}, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Error fetching trip history: {e}")
        return Response({'trips': [], 'error': str(e)}, status=status.HTTP_200_OK)