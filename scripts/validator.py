from geopy.distance import geodesic
import datetime

def check_distance_accuracy(start_coords, end_coords, reported_km):
    """Checks if the reported map distance matches the mathematical ground truth."""
    actual_km = geodesic(start_coords, end_coords).kilometers
    accuracy_gap = abs(actual_km - reported_km)
    
    return round(actual_km, 2), round(accuracy_gap, 2)

def is_business_open(current_time, opening_hours):
    """
    Simulates checking if a business in Kolkata is open.
    Example opening_hours: {"start": 9, "end": 21} (9 AM to 9 PM)
    """
    hour = current_time.hour
    if opening_hours["start"] <= hour < opening_hours["end"]:
        return "Open"
    return "Closed"

# --- TEST CASE: HOWRAH BRIDGE TO VICTORIA MEMORIAL ---
howrah = (22.5851, 88.3468)
victoria = (22.5448, 88.3426)
reported_app_dist = 5.2  # Let's say a map app reported 5.2km

real_dist, gap = check_distance_accuracy(howrah, victoria, reported_app_dist)

print(f"--- Kolkata Map Validation Report ---")
print(f"Ground Truth Distance: {real_dist} km")
print(f"Accuracy Gap: {gap} km")

if gap > 1.0:
    print("ALERT: Flagging this route for manual review (High Inaccuracy).")
else:
    print("STATUS: Route distance within acceptable parameters.")