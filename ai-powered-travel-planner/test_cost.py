import urllib.request
import urllib.parse

def test_cost_logic():
    base_url = "http://127.0.0.1:5000/recommend"
    
    # Test Case: Chennai, Beach, Budget 5000, 2 Pax, 2 Days
    # Avg Budget Chennai = 1200
    # Base Cost = 1200 * 2 * 2 = 4800
    # Entry Fees ~ 0
    # Result should be feasible.
    
    data = urllib.parse.urlencode({
        'city': 'Chennai',
        'type': 'Beach',
        'budget': '5000',
        'travelers': '2',
        'days': '2'
    }).encode()
    
    try:
        req = urllib.request.Request(base_url, data=data)
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            
            # Checks
            if "Stay + Food + Travel" in html and "4800" in html:
                print("SUCCESS: Base Cost Calculation Correct (4800).")
            else:
                print("FAILURE: Base Cost Calculation Incorrect or Missing.")
                
            if "Day-wise Itinerary" in html:
                 print("SUCCESS: Itinerary Generated.")
            else:
                 print("FAILURE: Itinerary Missing.")

    except Exception as e:
        print(f"FAILURE: Request failed. {e}")

if __name__ == "__main__":
    test_cost_logic()
