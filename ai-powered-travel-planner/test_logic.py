from travel_planner import TravelPlanner
import pandas as pd

def test_logic():
    planner = TravelPlanner()
    print("Unique Cities:", planner.get_unique_cities()[:5])
    
    # Test 1: Strict Filter (Assuming 'Delhi' and 'Temple' exist and are cheap)
    print("\n--- Test 1: Strict Filter ---")
    res1 = planner.filter_places('Delhi', 'Temple', 0)
    print(f"Found {len(res1)} results for Delhi, Temple, Budget 0")
    if not res1.empty:
        print(res1[['place', 'Entrance Fee in INR']].head())

    # Test 2: Plan-B (Try a very low budget for a place that definitely costs money)
    print("\n--- Test 2: Plan-B ---")
    # Using a city and type but with 0 budget where places might cost money, 
    # OR requesting a type that doesn't exist to trigger relaxation.
    # Let's try 'Mumbai' 'Amusement Park' with 10 rupees. Essel World is 1149.
    res2, msg = planner.plan_b_search('Mumbai', 'Amusement Park', 10)
    print(f"Plan-B Message: {msg}")
    print(f"Found {len(res2)} results.")
    if not res2.empty:
        print(res2[['place', 'type', 'Entrance Fee in INR']].head())

    # Test 3: XAI
    print("\n--- Test 3: XAI ---")
    if not res1.empty:
        row = res1.iloc[0]
        explanation = planner.generate_explanation(row, 100)
        print(f"Explanation for {row['place']}: {explanation}")

    # Test 4: Logistics
    print("\n--- Test 4: Logistics ---")
    mode, cost = planner.suggest_travel_mode(5, 2)
    print(f"5km, 2 pax -> {mode} ({cost})")

if __name__ == "__main__":
    test_logic()
