from travel_planner import TravelPlanner

def test_distance():
    planner = TravelPlanner()
    
    # Test 1: Chennai -> Bangalore (Approx 290-300km straight line, 350km road)
    # Haversine calculates straight line (Great Circle)
    details = planner.calculate_journey_details("Chennai", "Bangalore", 1)
    dist = details['distance']
    print(f"Chennai -> Bangalore: {dist} km")
    
    if 280 <= dist <= 310:
        print("PASS: Distance is within valid Haversine range.")
    else:
        print(f"WARNING: Distance {dist} seems off (Expected ~290km).")

    # Test 2: Delhi -> Mumbai (Approx 1150km straight line)
    details_long = planner.calculate_journey_details("Delhi", "Mumbai", 1)
    dist_long = details_long['distance']
    print(f"Delhi -> Mumbai: {dist_long} km")
    
    if 1100 <= dist_long <= 1200:
        print("PASS: Long distance valid.")
    else:
        print(f"WARNING: Distance {dist_long} seems off.")

    # Test 3: Same City
    details_same = planner.calculate_journey_details("Chennai", "Chennai", 1)
    print(f"Chennai -> Chennai: {details_same['distance']} km (Mock Local)")

if __name__ == "__main__":
    test_distance()
