import math
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

AVG_SPEED_MPH = 55
FUEL_INTERVAL_MILES = 1000
BREAK_30_MINUTES = 0.5  # hours
PICKUP_DROPOFF_HOURS = 1.0
MAX_DRIVING_PER_DAY = 11.0
MAX_DUTY_WINDOW = 14.0
CYCLE_LIMIT = 70.0

def calculate_trip_plan(current: str, pickup: str, dropoff: str, cycle_used: float, total_miles: float):
    """
    Main HOS calculation engine
    Returns: trip_days list with log entries, fuel stops, etc.
    """
    driving_hours = total_miles / AVG_SPEED_MPH
    num_fuel_stops = math.floor(total_miles / FUEL_INTERVAL_MILES)
    fuel_stop_hours = num_fuel_stops * 0.5  # 30 min each
    
    total_on_duty = driving_hours + PICKUP_DROPOFF_HOURS + fuel_stop_hours
    
    # Check if trip exceeds cycle limit
    if cycle_used + total_on_duty > CYCLE_LIMIT:
        raise ValueError(f"Trip exceeds 70-hour cycle limit. Available: {CYCLE_LIMIT - cycle_used}hrs, Needed: {total_on_duty}hrs")
    
    # Split driving into days
    days = split_into_days(driving_hours, PICKUP_DROPOFF_HOURS, fuel_stop_hours, num_fuel_stops, total_miles)
    
    # Generate log entries for each day
    for i, day in enumerate(days):
        day['log_entries'] = generate_log_entries(day, i == 0)  # first day has pickup
    
    return days

def split_into_days(driving_hours: float, pickup_dropoff_hours: float, fuel_stop_hours: float, num_fuel_stops: int, total_miles: float) -> List[Dict]:
    """Split total driving into HOS-compliant days"""
    days = []
    remaining_drive = driving_hours
    day_num = 1
    miles_covered = 0
    miles_per_drive_hour = total_miles / driving_hours if driving_hours > 0 else 55
    
    while remaining_drive > 0:
        drive_today = min(MAX_DRIVING_PER_DAY, remaining_drive)
        
        # Calculate fuel stops for this day
        fuel_stops_today = 0
        if num_fuel_stops > 0:
            # Simplified: fuel stops happen at specific mile intervals
            pass
        
        # Calculate on-duty time for day
        on_duty_today = drive_today
        
        # Add 30-min break if driving > 8 hours
        if drive_today > 8:
            on_duty_today += BREAK_30_MINUTES
        
        # Add pickup on day 1 only
        if day_num == 1:
            on_duty_today += PICKUP_DROPOFF_HOURS
        
        # Add dropoff on last day only
        if remaining_drive - drive_today <= 0:
            on_duty_today += PICKUP_DROPOFF_HOURS
        
        miles_today = drive_today * miles_per_drive_hour
        
        day_data = {
            'day_number': day_num,
            'date': datetime.now() + timedelta(days=day_num - 1),
            'driving_hours': drive_today,
            'on_duty_not_driving_hours': on_duty_today - drive_today,
            'off_duty_hours': 24 - on_duty_today,  # Simplified
            'sleeper_hours': 0,
            'total_miles': miles_today,
            'start_location': '',  # Will be filled with route data
            'end_location': ''
        }
        days.append(day_data)
        
        remaining_drive -= drive_today
        day_num += 1
    
    return days

def generate_log_entries(day: Dict, is_first_day: bool) -> List[Dict]:
    """Generate 24-hour log entries for a single day"""
    entries = []
    
    # Start off-duty from midnight
    current_hour = 0.0
    
    # Assuming driver starts at 6:00 AM (6.0 hours after midnight)
    start_hour = 6.0
    
    # Off-duty before start
    if start_hour > 0:
        entries.append({
            'start': format_hour(0),
            'end': format_hour(start_hour),
            'status': 'off_duty'
        })
    
    # Driving and on-duty logic
    remaining_drive = day['driving_hours']
    current_drive_hour = start_hour
    
    # First segment: Drive up to 8 hours or remaining
    first_segment = min(8, remaining_drive)
    if first_segment > 0:
        entries.append({
            'start': format_hour(current_drive_hour),
            'end': format_hour(current_drive_hour + first_segment),
            'status': 'driving'
        })
        current_drive_hour += first_segment
        remaining_drive -= first_segment
    
    # 30-min break if needed
    if day['driving_hours'] > 8:
        entries.append({
            'start': format_hour(current_drive_hour),
            'end': format_hour(current_drive_hour + 0.5),
            'status': 'off_duty'  # Break can be off-duty or on-duty
        })
        current_drive_hour += 0.5
    
    # Second driving segment
    if remaining_drive > 0:
        entries.append({
            'start': format_hour(current_drive_hour),
            'end': format_hour(current_drive_hour + remaining_drive),
            'status': 'driving'
        })
        current_drive_hour += remaining_drive
    
    # Pickup on first day (1 hour on-duty)
    if is_first_day:
        entries.append({
            'start': format_hour(current_drive_hour),
            'end': format_hour(current_drive_hour + 1.0),
            'status': 'on_duty'
        })
        current_drive_hour += 1.0
    
    # Off-duty rest of day
    if current_drive_hour < 24:
        entries.append({
            'start': format_hour(current_drive_hour),
            'end': '24:00',
            'status': 'off_duty'
        })
    
    return entries

def format_hour(hour: float) -> str:
    """Convert 6.5 to '06:30'"""
    h = int(hour)
    m = int((hour - h) * 60)
    return f"{h:02d}:{m:02d}"